# Render-contract test (optional)

Proves the signature feature survives any theme: the interactive quiz **click-hotspots land
exactly over the video's own rendered option boxes**, the overlay is transparent (no blur over
the captions), the quiz plays in the background, and the theme palette/brand are applied — with
no console errors.

It drives the **example** course (`examples/kitchen-academy`) through a real headless browser
against the local range server.

## Run it
```bash
# 1) render + package the example once (from the prompt-system root):
CC_PROJECT=examples/kitchen-academy CC_THEME=examples/kitchen-academy/theme.json \
  python engine/build_episode.py examples/kitchen-academy/course/scripts/ep01.json
python engine/package.py --project examples/kitchen-academy

# 2) run the contract test:
cd engine/webtest
npm install            # installs Playwright (downloads a browser the first time)
npx playwright install chromium
node contract-check.js
```
Expected: `PASS ✓ render contract holds on a custom theme` (maxAlignErr < 0.02).

This is a developer check, not required to build a course. `node_modules/` is gitignored.
