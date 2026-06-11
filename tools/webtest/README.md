# Web player tests (Playwright, cross-browser)

Cross-browser UI tests for the Cyber Citadel web player. We use **Playwright** (not Puppeteer)
because the playback-speed feature is pitch-/media-sensitive and only Playwright can drive a real
**WebKit** engine alongside Chromium and Firefox.

## Run

```powershell
# from repo root, one-time:
npm install
npm run test:install        # downloads chromium, firefox, webkit

# run the suite (Playwright starts its own range-capable static server):
npm test
```

## What it covers (`speed-chapters.spec.js`)
- **Playback speed**: clicking a speed button sets `playbackRate`, persists to `localStorage`,
  preserves pitch, marks the active button; keyboard `.`/`,`/`0`; persistence across reload and
  episode switch (the rate is re-applied on each source load).
- **Sidebar chapters**: render under the active episode with `m:ss` time-markers; clicking seeks
  the video; the current chapter is highlighted during playback.
- **Posters**: the stage video and every index card expose a `.jpg` poster (no black screens).
- **No console/page errors** on load.

## Notes
- `server.js` is a tiny static server **with HTTP Range support** — required for `<video>`
  seeking (Python's `http.server` lacks ranges and breaks seek tests).
- Firefox uses `firefoxUserPrefs` to disable session-restore (avoids a known Playwright/Firefox
  `_maybeDontRestoreTabs` teardown crash).
- `node_modules/`, `test-results/`, `playwright-report/` are gitignored; the config + spec +
  server are committed as the reusable harness.
