// Cross-browser UI tests for watch.html (playback speed + sidebar chapters).
// Runs on Chromium, Firefox and WebKit because the speed feature is pitch-/media-
// sensitive and those behaviours differ per engine. Static server is the repo root.
const { defineConfig, devices } = require('@playwright/test');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const PORT = 8731;

module.exports = defineConfig({
  testDir: __dirname,
  timeout: 60000,
  expect: { timeout: 10000 },
  reporter: [['list']],
  use: { baseURL: `http://127.0.0.1:${PORT}` },
  webServer: {
    command: `node server.js`,
    cwd: __dirname,
    env: { PORT: String(PORT) },
    url: `http://127.0.0.1:${PORT}/watch.html`,
    reuseExistingServer: false,
    timeout: 30000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'],
        launchOptions: { firefoxUserPrefs: {           // stop the _maybeDontRestoreTabs teardown crash
          'browser.sessionstore.resume_from_crash': false,
          'browser.sessionstore.max_resumed_crashes': 0,
          'toolkit.startup.max_resumed_crashes': -1,
        } } } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
