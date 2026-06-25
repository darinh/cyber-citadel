// Render-contract test: proves the interactive player keeps its guarantees on ANY theme.
// Self-contained: starts the example's range server, drives a headless browser, checks that
//   (1) the theme palette + brand are applied, (2) the quiz click-hotspots land EXACTLY over
//   the video's rendered option boxes, (3) the layer is transparent (no blur over captions),
//   (4) the quiz plays in the background, (5) no console/page errors.
//
// Prereq: render + package the example once, then:  npm install  &&  node contract-check.js
//   (renders:  CC_PROJECT=<example> python ../../engine/build_episode.py <example>/course/scripts/ep01.json
//    package:  python ../../engine/package.py --project <example>)
const { chromium } = require('@playwright/test');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const EX = path.resolve(__dirname, '..', '..', 'examples', 'kitchen-academy');
const PORT = process.env.CC_PORT || 8211;
const BASE = `http://127.0.0.1:${PORT}`;
const PY = process.env.CC_PY || 'python';

function fail(msg) { console.error('FAIL ✗ ' + msg); proc && proc.kill(); process.exit(1); }
let proc;

(async () => {
  if (!fs.existsSync(path.join(EX, 'course', 'episodes', 'ep01.cues.json'))) {
    fail('example not rendered/packaged yet — render + package examples/kitchen-academy first');
  }
  proc = spawn(PY, [path.join(EX, 'serve.py'), String(PORT)], { stdio: 'ignore' });
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

  const q = JSON.parse(fs.readFileSync(path.join(EX, 'course', 'episodes', 'ep01.cues.json'), 'utf8')).quizzes[0];
  await page.evaluate((t) => { const v = document.querySelector('#vid'); v.currentTime = t; v.play(); }, q.t_question + 0.4);
  await page.waitForSelector('#qhot.show', { timeout: 12000 });

  const r = await page.evaluate(() => {
    const s = document.querySelector('.stage').getBoundingClientRect();
    const h = document.querySelector('#qhot'); const cs = getComputedStyle(h);
    const hots = [...document.querySelectorAll('#qhot .hot')].map(e => {
      const b = e.getBoundingClientRect();
      return [(b.left - s.left) / s.width, (b.top - s.top) / s.height, b.width / s.width, b.height / s.height];
    });
    return { hots, bg: cs.backgroundColor, bd: cs.backdropFilter || 'none', paused: document.querySelector('#vid').paused };
  });
  let maxErr = 0;
  r.hots.forEach((h, i) => h.forEach((v, k) => { maxErr = Math.max(maxErr, Math.abs(v - q.opt_rects[i][k])); }));
  await browser.close();
  proc.kill();

  console.log(`brand=${brand} accent=${accent} hotspots=${r.hots.length}/${q.options.length} ` +
    `maxAlignErr=${maxErr.toFixed(4)} transparent=${['rgba(0, 0, 0, 0)', 'transparent'].includes(r.bg)} ` +
    `noBlur=${r.bd === 'none'} playingBehind=${!r.paused} errors=${errs.length}`);
  const ok = brand === 'KITCHEN ACADEMY' && r.hots.length === q.options.length && maxErr < 0.02 &&
    ['rgba(0, 0, 0, 0)', 'transparent'].includes(r.bg) && r.bd === 'none' && !r.paused && errs.length === 0;
  console.log(ok ? 'PASS ✓ render contract holds on a custom theme' : 'FAIL ✗ contract broken');
  process.exit(ok ? 0 : 1);
})().catch(e => fail(String(e)));
