# 10 — Assemble → `course/episodes/epNN_*.mp4` + `.srt` + `.cues.json`

Render `course/scripts/epNN.json` into a captioned, quizzed mp4 with neural narration, the sourced music
bed, bundled SFX, and the interactive-quiz cues. The gates (phase 09) must be green first.

**Render ONE episode and spot-check before any bulk render** — full renders are slow, especially on CPU.

---

## Goal
Produce `course/episodes/epNN_<slug>.mp4`, `course/episodes/epNN_<slug>.srt`, and
`course/episodes/epNN.cues.json` for one episode, verified by eye and ear, before rendering the rest.

---

## Environment

```powershell
$env:PYTHONUTF8 = "1"
$env:CC_TTS = "chatterbox"   # GPU, expressive zero-shot voices  — OR  "piper" (CPU, always-works)
$env:CC_VERIFY = "1"         # self-correcting audio gate: re-synthesizes a line until STT matches
```

`CC_TTS` selects the voice engine (auto-detects chatterbox+CUDA, else falls back to piper). `CC_VERIFY=1`
(the default) makes each narration line verify against STT and retry up to 4× — keep it on. `CC_THEME`
auto-discovers `theme.json`; `CC_PROJECT` overrides the project dir (defaults to the cwd).

---

## Render ONE, then spot-check

```powershell
python engine/build_episode.py course/scripts/ep01.json
```

The CLI takes the **spec path**; add `--beats N` to render only the first N beats for a fast framing
check. Output lands in `course/episodes/`. Spot-check before doing anything else:

```powershell
ffmpeg -y -ss 12 -i course/episodes/ep01_knife_skills.mp4 -frames:v 1 course/episodes/_spot.jpg
# open _spot.jpg (framing + captions), and listen to the first ~30s (narration clear? music ducked? quiz reads?)
```

---

## How the render works
- **Incremental cache.** Per-beat audio/stills/clips are cached under `course/render/<epid>/`, keyed on
  the engine's render version + a content hash of each beat (visual fields, lines, **voice settings**,
  `min_seconds`…). Edit one line → only that beat (and the final mux) rebuild; everything else is reused.
  **Don't bump anything** — the engine owns its render version and bumps it only when render logic changes.
- **Two-pass mux.** Audio is mixed in an audio-only pass, then mapped RAW into a video-only pass. This is
  deliberate: combining both filtergraphs non-deterministically dropped ~2–3s of speech at scene
  boundaries. Never collapse it — and always QA the FINAL mp4 (phase 11), not upstream clips.
- **Quiz beats are automatic.** From `q`/`options`/`answer`/`why` the engine produces the read-aloud
  (question + every option + "pause and lock in" + reveal with answer text + why) and writes normalized
  `opt_rects` into `epNN.cues.json` for the player's clickable hotspots. Chapters come from
  `title`/`section`/`map` and quiz beats.
- Music is loop-mastered + ducked from your sourced track (or silent if none); SFX are bundled and
  applied per scene type.

---

## Render the rest (only after the spot-check)

```powershell
python engine/build_episode.py course/scripts/ep02.json
```

Re-rendering an edited episode is fast (incremental). Full renders are **slow on CPU** (piper + ffmpeg);
on a no-GPU laptop expect long times, so validate ONE episode first and lean on the cache for edits.

---

## Self-review
- Do `course/episodes/epNN_<slug>.mp4`, `.srt`, and `epNN.cues.json` all exist?
- Does the spot frame look right (captions placed, nothing overflowing)?
- Do the first ~30s sound clean, with music sitting under the voice?
- Did re-running an edited beat rebuild ONLY that beat?
- Did the console print `EPISODE: …  (N min, B beats, Q quizzes)` with the expected counts?

Then route to `system-prompts/11_player_and_verify.md`.
