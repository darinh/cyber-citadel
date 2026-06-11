---
name: video-assembly
description: >-
  Assemble a narrated episode from a declarative JSON spec into a captioned, graded, music-bedded
  mp4 using the incremental render pipeline, then package and deploy. Encodes the TWO-PASS A/V
  mux (the fix for non-deterministic audio drops), the content-hash incremental cache, the
  file-size limit, and the verify-before-deploy gate. Use when rendering/re-rendering episodes,
  changing the assembler, or publishing the site.
---

# Video Assembly (spec → mp4 → deploy)

Turns `course/scripts/epNN.json` (declarative `beats`) into a 1920×1080 captioned mp4 with
avatars, music bed, cinematic grade, and read-aloud quizzes. Read `course/GENERATION_PLAYBOOK.md`
§6, §11.F, §12. This skill is the operational checklist.

## Environment & commands
- `$env:PYTHONUTF8=1`; for Chatterbox narration `$env:CC_TTS='chatterbox'; $env:CC_VERIFY='1'`.
- Render ONE: `.\.venv_tts\Scripts\python.exe tools\build_episode2.py course\scripts\ep00.json`
  (or `tools\render_all.py ep00`; `render_all.py` takes episode stems, `build_episode2.py` a spec
  path). **Always render one episode and spot-check before any bulk re-render** — full re-renders
  are expensive.
- Package the site: `python tools\package.py` (transcripts, quizzes.json, manifest, index.html,
  SRT→VTT, posters wiring, link check).
- Posters: `python tools\make_posters.py` (bright representative frame per episode).

## Incremental render architecture (don't hand-render frames)
`build_episode2.py` persists per-beat + per-line artifacts under `course/render/<epid>/`
(gitignored): `lines/bNNN_lKK_SPEAKER.wav`, `bNNN.wav/.png/.mp4`, `manifest.json`. Each beat has a
**content hash** (`RENDER_VER` + visual fields + lines + timing + a **voice fingerprint**); on
re-render, unchanged beats are reused (no TTS, no scene render, no encode). Editing one
line/slide rebuilds only that beat, then the cheap final mux re-runs. **Bump `RENDER_VER`** to
force a full rebuild when render *logic* changes.

## ⭐ The TWO-PASS A/V mux (critical — never regress)
Combining the audio mix (`amix`+`sidechaincompress`) and the heavy video graph
(`subtitles`+avatar overlays+`libx264`) in ONE ffmpeg `-filter_complex` **non-deterministically
drops ~2-3 s of speech at scene boundaries** (upstream clips stay clean, so it hides). The
assembler therefore does TWO passes: (A) audio-only graph → `mix.wav`; (B) video-only graph with
audio mapped **raw** (`-map 1:a`). Rule: **never put a non-trivial audio filtergraph and a heavy
video filtergraph in the same `-filter_complex`.**

## Grade & file size (deployability)
Cinematic grade = `eq` + `vignette` + light `unsharp` (applied before burning captions). **NO
temporal film grain** (`noise=...:allf=t`) — per-frame noise destroys H.264 inter-frame prediction
and bloated episodes ~9× (ep00 25→226 MB), past **GitHub's 100 MB/file limit**. Keep episodes
~15-46 MB. **Verify every file < ~95 MB before deploy.**

## Gates before deploy (in order)
1. **accuracy-verification** skill: `verify_script.py` + `audit_narration.py` must pass.
2. **Deterministic craft gate:** `tools/lint_script.py` must be **0 P1** (duplicate headings,
   quiz double-pause, title/variable-text overflow measured with real fonts, incomplete quotes).
3. (For dialogue changes) **screenplay-review** skill first — cheaper in text.
4. Render, then **`python tools/verify_episode.py`** — every episode must read `OK` (see
   tts-narration). QA the FINAL mp4, not upstream clips.
5. `python tools\package.py` (link check must say all references resolve).
6. Sizes < 95 MB each.

## Deploy (GitHub Pages from `main` root)
The site is `index.html` + `watch.html` + `course/episodes/*.mp4|.jpg|.vtt` + `course/*.json`,
served from `main`. Commit + `git push origin main`; reference issue numbers; then verify the
**live** artifact byte-matches (`gh api repos/<o>/<r>/pages/builds/latest` → `built`, then
download the live mp4 and compare sha/size, and transcribe a known region to confirm the fix is
live). The web player (`watch.html`) is covered by the Playwright harness in `tools/webtest`
(`npm test`).

## Definition of done
- One episode spot-checked before bulk render; only changed beats rebuilt.
- accuracy gate green; verify_episode `OK` on all changed mp4s; all files < 95 MB.
- Packaged (link check clean), pushed, Pages `built`, live artifact verified.
- Any assembler/grade/mux change recorded in GENERATION_PLAYBOOK changelog (+ RENDER_VER bump if
  render logic changed).
