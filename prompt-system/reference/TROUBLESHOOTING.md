# Troubleshooting

Run preflight from `prompt-system/` before a live build:

```bash
python engine/probe.py preflight
```

## Hardware tiers and downloads
`engine/probe.py` writes `capabilities.json` and chooses safe tiers:

| Subsystem | Higher tier | Lower/fallback tier |
| --- | --- | --- |
| TTS | `chatterbox` if CUDA and VRAM >= 6GB; first run downloads about 3GB. | `piper`; download 2-3 `.onnx` voices into `assets/voices/` at about 60MB each. |
| Avatars | `sdxl_ipa` if CUDA and VRAM >= 10GB; SDXL about 6GB plus IP-Adapter about 1GB. | `sd_turbo` if CUDA and VRAM >= 4GB; otherwise `illustrated` with no model download. |
| STT | `large-v3` if CUDA and VRAM >= 8GB; about 3GB on first verify. | `small` about 0.5GB, or `base` about 0.15GB. |

CPU-only builds still work, but they are slower and use piper voices plus illustrated avatars.

## Common failures
- **No CUDA**: use `CC_TTS=piper`; expect illustrated avatars.
- **Low VRAM or OOM**: rerun `python engine/probe.py`; the probe forces a lower tier to avoid runtime failures.
- **ffmpeg/ffprobe not found**: install ffmpeg 6+ and put both commands on PATH. They are required.
- **First run stalls**: model downloads may be in progress. Use `python engine/probe.py preflight` to see expected downloads before starting.
- **Fonts look wrong or missing**: the engine uses vendored Noto Sans by default. Keep theme font names mapped to files in `engine/assets/fonts/` unless using valid absolute paths.
- **`file://` playback fails or quizzes do not click**: use the range server with `python serve.py`, or double-click `play.cmd` / run `./play.sh`.
- **CPU render is slow**: this is expected; quality and interactivity remain the same, only speed and media fidelity change.
- **Suspicious transcript failure**: faster-whisper can hallucinate repetition or miss short lines; check the flagged final-MP4 region before re-rendering everything.
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
