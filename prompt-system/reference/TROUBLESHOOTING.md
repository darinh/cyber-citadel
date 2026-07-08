# Troubleshooting

Run preflight from `prompt-system/` before a live build:

```bash
python engine/probe.py preflight
```

## Quality is fixed HIGH; hardware only changes SPEED
`engine/probe.py` writes `capabilities.json` with the **recommended HIGH-QUALITY models** (always the
same) plus a `speed` estimate. It never auto-downgrades — the same models run on GPU **or** CPU:

| Subsystem | Model (DEFAULT, GPU or CPU) | First-run download | Opt-in downgrade (user approval only) |
| --- | --- | --- | --- |
| TTS | `chatterbox` (expressive neural) | ~3GB | `CC_TTS=piper` (fast, robotic) + `.onnx` voices ~60MB each |
| Avatars | `sdxl` original portraits | ~6GB | `CC_AVATARS=turbo` (few-step) or `=illustrated` (instant, no download) |
| STT gate | `large-v3` | ~3GB | `CC_STT_MODEL=small` (~0.5GB) or `base` (~0.15GB) |

CPU-only builds produce the **same high quality** — they just render slower. Do NOT downgrade to save
time unless the user explicitly approves it.

## Common failures
- **No CUDA**: nothing to change — chatterbox + SDXL + large-v3 run on CPU (slower). Do NOT switch to
  piper/illustrated unless the user approves the speed-for-quality trade.
- **`chatterbox is not installed` error**: install it (`pip install chatterbox-tts torch`) — it runs on
  CPU too. The engine fails loud rather than silently shipping low-quality piper voices.
- **Low VRAM / OOM on GPU**: the high-quality model may spill to RAM/CPU and run slowly; quality stays
  high. Reduce concurrent GPU use or, with user approval, apply a downgrade.
- **ffmpeg/ffprobe not found**: install ffmpeg 6+ and put both commands on PATH. They are required.
- **First run stalls**: model downloads may be in progress. Use `python engine/probe.py preflight` (and
  the trigger commands in `02_environment.md`) to fetch weights before starting.
- **Fonts look wrong or missing**: the engine uses vendored Noto Sans by default. Keep theme font names
  mapped to files in `engine/assets/fonts/` unless using valid absolute paths.
- **`file://` playback fails or quizzes do not click**: use the range server with `python serve.py`, or
  double-click `play.cmd` / run `./play.sh`.
- **CPU render is slow**: expected — quality and interactivity are unchanged, only speed. Warn the user;
  downgrade only with their approval.
- **Suspicious transcript failure**: faster-whisper can hallucinate repetition or miss short lines;
  check the flagged final-MP4 region before re-rendering everything.
## Command reminders
Run from `prompt-system/`; the engine treats the current working directory as the project root.

```bash
python engine/probe.py
python engine/scene.py demo
python engine/build_episode.py course/scripts/ep01.json
python engine/gates/verify_episode.py ep01
```

## Cache and rerender notes
- The assembler uses an incremental cache, so changed beats rebuild without rerendering everything.
- Voice, cast, effect, and narration text changes invalidate affected audio lines.
- Scene image changes invalidate affected beat video.
- If output seems stale, rerun the exact episode build once before deleting caches.
- Render one episode and spot-check before starting a bulk render.
