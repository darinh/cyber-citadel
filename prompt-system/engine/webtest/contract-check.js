// Render-contract test: proves the interactive player keeps its guarantees on ANY theme.
// Self-contained: starts the example's range server, drives a headless browser, checks that
//   (1) the theme palette + brand are applied, (2) the quiz click-hotspots land EXACTLY over
//   the video's rendered option boxes, (3) the layer is transparent (no blur over captions),
//   (4) the quiz plays in the background, (5) no console/page errors.
//
// Prereq: render + package an example once, then:  npm install  &&  node contract-check.js
//   (renders:  CC_PROJECT=<example> python ../../engine/build_episode.py <example>/course/scripts/ep01.json
//    package:  python ../../engine/package.py --project <example>)
const { chromium } = require('@playwright/test');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const EX = process.env.CC_PROJECT
  ? path.resolve(process.env.CC_PROJECT)
  : path.resolve(__dirname, '..', '..', 'examples', 'kitchen-academy');
const PORT = process.env.CC_PORT || 8211;
const BASE = `http://127.0.0.1:${PORT}`;
const PY = process.env.CC_PY || 'python';

function fail(msg) { console.error('FAIL ✗ ' + msg); proc && proc.kill(); process.exit(1); }
let proc;

(async () => {
  const manifestPath = path.join(EX, 'course', 'episodes', 'manifest.json');
  if (!fs.existsSync(manifestPath)) {
    fail(`project not rendered/packaged yet: ${EX}`);
  }
  const manifestData = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const episodes = Array.isArray(manifestData) ? manifestData : (manifestData.episodes || []);
  const episode = episodes[0];
  if (!episode || !episode.cues) fail(`manifest has no playable episode: ${manifestPath}`);
  const expectedBrand = Array.isArray(manifestData) ? '' : (manifestData.brand || '');
  const cuePath = path.join(EX, ...episode.cues.split('/'));
  proc = spawn(PY, [path.join(EX, 'serve.py'), String(PORT)], {
    stdio: 'ignore',
    env: { ...process.env, CC_NO_BROWSER: '1' },
  });
  await new Promise(r => setTimeout(r, 2500));

  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });

  await page.goto(BASE + '/watch.html', { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => document.querySelectorAll('#spbtns .spbtn').length > 0, null, { timeout: 30000 });
  const brand = (await page.textContent('#brand')).trim();
  const accent = await page.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue('--cy').trim());
  await page.evaluate(() => { const v = document.querySelector('#vid'); if (v) { v.muted = true; v.load(); } });
  await page.waitForFunction(() => { const v = document.querySelector('#vid'); return v && v.readyState >= 1; }, null, { timeout: 30000 });

  const q = JSON.parse(fs.readFileSync(cuePath, 'utf8')).quizzes[0];
  if (!q) fail(`episode has no interactive quiz: ${cuePath}`);
  await page.evaluate((t) => { const v = document.querySelector('#vid'); v.currentTime = t; v.play(); }, q.t_question + 0.05);
  await page.waitForSelector('#qhot.show', { timeout: 12000 });

  async function measure(viewport) {
    await page.setViewportSize(viewport);
    await page.waitForTimeout(150);
    return page.evaluate(() => {
      const s = document.querySelector('.stage').getBoundingClientRect();
      const h = document.querySelector('#qhot'); const cs = getComputedStyle(h);
      const hots = [...document.querySelectorAll('#qhot .hot')].map(e => {
        const b = e.getBoundingClientRect();
        return [(b.left - s.left) / s.width, (b.top - s.top) / s.height, b.width / s.width, b.height / s.height];
      });
      return {
        hots, bg: cs.backgroundColor, bd: cs.backdropFilter || 'none',
        paused: document.querySelector('#vid').paused,
        enabled: [...document.querySelectorAll('#qhot .hot')].every(e => !e.disabled),
      };
    });
  }
  const measurements = [
    await measure({ width: 1280, height: 800 }),
    await measure({ width: 760, height: 900 }),
  ];
  let maxErr = 0;
  measurements.forEach(r => r.hots.forEach((h, i) => h.forEach((v, k) => {
    maxErr = Math.max(maxErr, Math.abs(v - q.opt_rects[i][k]));
  })));
  const first = page.locator('#qhot .hot').first();
  await first.hover();
  await page.waitForTimeout(180);
  const hover = await first.evaluate(e => {
    const cs = getComputedStyle(e);
    return { cursor: cs.cursor, border: cs.borderTopColor };
  });
  await browser.close();
  proc.kill();

  const r = measurements[0];
  const allEnabled = measurements.every(m => m.enabled);
  console.log(`brand=${brand} accent=${accent} hotspots=${r.hots.length}/${q.options.length} ` +
    `maxAlignErr=${maxErr.toFixed(4)} transparent=${['rgba(0, 0, 0, 0)', 'transparent'].includes(r.bg)} ` +
    `noBlur=${r.bd === 'none'} playingBehind=${!r.paused} liveImmediately=${allEnabled} ` +
    `hoverCursor=${hover.cursor} hoverBorder=${hover.border} errors=${errs.length}`);
  const ok = (!expectedBrand || brand === expectedBrand) &&
    r.hots.length === q.options.length && maxErr < 0.02 &&
    ['rgba(0, 0, 0, 0)', 'transparent'].includes(r.bg) && r.bd === 'none' && !r.paused &&
    allEnabled && hover.cursor === 'pointer' &&
    !['rgba(0, 0, 0, 0)', 'transparent'].includes(hover.border) && errs.length === 0;
  console.log(ok ? 'PASS ✓ render contract holds on the packaged project' : 'FAIL ✗ contract broken');
  process.exit(ok ? 0 : 1);
})().catch(e => fail(String(e)));
