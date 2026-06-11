const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const fmt = s => { s = Math.max(0, Math.round(s)); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; };

async function ready(page) {
  await page.goto('/watch.html', { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => {
    const v = document.querySelector('#vid');
    return v && v.readyState >= 1 && document.querySelectorAll('#spbtns .spbtn').length > 0;
  }, null, { timeout: 30000 });
}
const rate = page => page.evaluate(() => document.querySelector('#vid').playbackRate);

test.describe('playback speed', () => {
  test('click sets rate + persists + preserves pitch + active button', async ({ page }) => {
    await ready(page);
    await page.click('#spbtns .spbtn[data-s="1.5"]');
    expect(await rate(page)).toBeCloseTo(1.5, 5);
    const st = await page.evaluate(() => {
      const v = document.querySelector('#vid');
      return {
        stored: localStorage.getItem('cc_speed'),
        on: (document.querySelector('#spbtns .spbtn.on') || {}).textContent,
        pitch: v.preservesPitch === true || v.webkitPreservesPitch === true || v.mozPreservesPitch === true,
      };
    });
    expect(st.stored).toBe('1.5');
    expect(st.on).toBe('1.5×');
    expect(st.pitch).toBe(true);
  });

  test('keyboard . faster, , slower, 0 reset', async ({ page }) => {
    await ready(page);
    await page.click('#spbtns .spbtn[data-s="1.5"]');
    await page.keyboard.press('Period');                 // -> 1.75
    expect(await rate(page)).toBeCloseTo(1.75, 5);
    await page.keyboard.press('Comma');                  // -> 1.5
    expect(await rate(page)).toBeCloseTo(1.5, 5);
    await page.keyboard.press('Digit0');                 // -> 1
    expect(await rate(page)).toBeCloseTo(1.0, 5);
  });

  test('rate persists across reload (re-applied on metadata)', async ({ page }) => {
    await ready(page);
    await page.click('#spbtns .spbtn[data-s="1.25"]');
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => {
      const v = document.querySelector('#vid'); return v && v.readyState >= 1;
    }, null, { timeout: 20000 });
    await page.waitForFunction(() => Math.abs(document.querySelector('#vid').playbackRate - 1.25) < 1e-6, null, { timeout: 8000 });
    expect(await rate(page)).toBeCloseTo(1.25, 5);
    expect(await page.evaluate(() => (document.querySelector('#spbtns .spbtn.on') || {}).textContent)).toBe('1.25×');
  });

  test('rate persists across episode switch (src reload)', async ({ page }) => {
    await ready(page);
    await page.click('#spbtns .spbtn[data-s="1.5"]');
    await page.evaluate(() => { const e = document.querySelectorAll('.ep'); (e[2] || e[1]).click(); });
    await page.waitForFunction(() => {
      const v = document.querySelector('#vid'); return v && v.readyState >= 1;
    }, null, { timeout: 20000 });
    await page.waitForFunction(() => Math.abs(document.querySelector('#vid').playbackRate - 1.5) < 1e-6, null, { timeout: 8000 });
    expect(await rate(page)).toBeCloseTo(1.5, 5);
  });
});

test.describe('sidebar chapters', () => {
  test('render under active ep with correct time-markers', async ({ page }) => {
    await ready(page);
    await page.waitForSelector('#navchaps .epchap');
    const cues = JSON.parse(fs.readFileSync(path.join(ROOT, 'course', 'episodes', 'ep00.cues.json'), 'utf8'));
    const rows = await page.$$eval('#navchaps .epchap', els => els.map(e => ({
      t: e.querySelector('.ct').textContent, l: e.querySelector('.cl').textContent,
    })));
    expect(rows.length).toBe(cues.chapters.length);
    expect(rows[0].t).toBe(fmt(cues.chapters[0].t));
    expect(rows[0].l).toBe(cues.chapters[0].title);
    // time markers look like m:ss
    for (const r of rows) expect(r.t).toMatch(/^\d+:\d{2}$/);
  });

  test('clicking a chapter seeks the video', async ({ page }) => {
    await ready(page);
    await page.waitForSelector('#navchaps .epchap');
    const cues = JSON.parse(fs.readFileSync(path.join(ROOT, 'course', 'episodes', 'ep00.cues.json'), 'utf8'));
    const target = cues.chapters[Math.min(2, cues.chapters.length - 1)];
    const ti = Math.min(2, cues.chapters.length - 1);
    await page.evaluate(() => document.querySelector('#vid').pause());
    await page.$$eval('#navchaps .epchap', (els, i) => els[i].click(), ti);
    await page.waitForFunction(t => Math.abs(document.querySelector('#vid').currentTime - t) < 1.2, target.t, { timeout: 8000 });
    const ct = await page.evaluate(() => document.querySelector('#vid').currentTime);
    expect(Math.abs(ct - target.t)).toBeLessThan(1.2);
  });

  test('current chapter is highlighted', async ({ page }) => {
    await ready(page);
    await page.waitForSelector('#navchaps .epchap');
    const cues = JSON.parse(fs.readFileSync(path.join(ROOT, 'course', 'episodes', 'ep00.cues.json'), 'utf8'));
    const ti = Math.min(2, cues.chapters.length - 1);
    // use the real UI path (click the chapter row, which seeks + plays); WebKit defers
    // seeks while paused, so a synthetic paused currentTime set is not representative.
    await page.$$eval('#navchaps .epchap', (els, i) => els[i].click(), ti);
    await page.waitForFunction(i => {
      const rows = document.querySelectorAll('#navchaps .epchap');
      return rows[i] && rows[i].classList.contains('cur');
    }, ti, { timeout: 8000 });
    const cur = await page.$$eval('#navchaps .epchap', els => els.findIndex(e => e.classList.contains('cur')));
    expect(cur).toBe(ti);
  });
});

test.describe('poster thumbnails', () => {
  test('watch.html stage video has a poster (not blank)', async ({ page }) => {
    await ready(page);
    const poster = await page.evaluate(() => document.querySelector('#vid').getAttribute('poster'));
    expect(poster, 'stage <video> poster').toMatch(/course\/episodes\/.+\.jpg$/);
  });

  test('index.html cards all have poster thumbnails', async ({ page }) => {
    await page.goto('/index.html', { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('video');
    const posters = await page.$$eval('video', vs => vs.map(v => v.getAttribute('poster')));
    expect(posters.length).toBeGreaterThan(0);
    for (const p of posters) expect(p).toMatch(/course\/episodes\/.+\.jpg$/);
  });
});

test('no console/page errors on load', async ({ page }) => {
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.goto('/watch.html', { waitUntil: 'domcontentloaded' });
  // app initialised without throwing: speed buttons built AND chapters rendered for the
  // active episode (proves init -> selectEp -> cues fetch -> renderList ran cleanly).
  // Intentionally does NOT require video metadata (decoupled from media-load timing).
  await page.waitForSelector('#spbtns .spbtn', { timeout: 30000 });
  await page.waitForSelector('#navchaps .epchap', { timeout: 30000 });
  await page.waitForTimeout(400);
  expect(errs, errs.join('\n')).toEqual([]);
});
