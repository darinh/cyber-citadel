# 11 — Player & Verify → `verify_episode` + `package.py` + local play

QA the **delivered mp4** (not upstream clips), then package the interactive player and watch the course
locally. No cloud, no publishing.

---

## Goal
Confirm every rendered episode contains all scripted narration, build the local player + manifest +
posters, and play the course in a browser with the interactive quiz working.

---

## 1. Verify the final mp4 (audio QA)

```powershell
$env:PYTHONUTF8 = "1"
python engine/gates/verify_episode.py ep01
```

- Takes episode id(s); with no id it verifies every rendered episode. Run it in the TTS environment
  (faster-whisper + torch; e.g. `.venv_tts`).
- It transcribes the mp4 and aligns it to the script; it must read `OK` — e.g.
  `ep01: recall=0.98  confirmed_missing_run=0  OK`. It flags only contiguous **dropped** runs of scripted
  words (the two-pass mux exists to prevent these).
- **Before treating a flag as real:** the gate already re-transcribes just the flagged region to kill
  false positives from Whisper's long-form short-line omissions. If it STILL fails, the drop is real —
  re-render that episode (phase 10) and re-verify. Do not ship a FAIL.

---

## 2. Package for local playback

```powershell
python engine/package.py
```

This scans `course/episodes/*.cues.json` (+ each mp4 + its source spec) and writes:

- `course/episodes/manifest.json` = `{ brand, theme{palette,world}, episodes[] }`,
- a bright **poster** jpg per episode, `.srt` → `.vtt` captions, `course/quizzes.json` (a quiz bank), and
  `course/transcripts/*.md`,
- and copies `watch.html`, `index.html`, `serve.py`, `play.cmd`, `play.sh` to the project root.

The **link-check must be clean** — the tail must read `link check: all local references resolve` with no
`WARNING missing assets`. It does NOT publish anything.

---

## 3. Play it locally

```powershell
python serve.py
```

…or double-click **`play.cmd`** (Windows) / run **`./play.sh`** (mac/Linux). `watch.html` plays each
episode and lays **transparent clickable hotspots EXACTLY over the video's own option boxes**: the video
pauses at each quiz, you click an answer, and it scores and resumes (score saved in the browser).

`file://` will NOT work — browsers block `fetch()` of the manifest/cues, and stock servers don't do HTTP
Range (so seeking / quiz-skip break). Always use `serve.py` / `play.cmd` / `play.sh`.

---

## Self-review
- Does `verify_episode` read `OK` for every rendered episode?
- Did `package.py` finish with a clean link-check, and are `watch.html` / `index.html` / `serve.py` /
  `play.cmd` / `play.sh` present at the project root?
- Does each episode have mp4 + srt/vtt + cues + poster?
- In the browser: do quiz hotspots align with the boxes, and do pause-on-quiz, click-to-answer, score,
  resume, and chapter jumps all work?
- Are there zero references to any existing franchise on screen or in audio (`lint_prompts` still PASSED)?

Then route to `system-prompts/12_reference_materials.md` (optional) — or you are done.
