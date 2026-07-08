# Audio Rules

The final delivered MP4 is the artifact that matters. Always verify that, not just the source clips.

## Two-pass A/V mux
Never combine a non-trivial audio graph and a heavy video graph in one `ffmpeg -filter_complex`. The engine uses:
1. **Pass A**: mix narration, sourced music, and SFX in an audio-only graph.
2. **Pass B**: run video grading, avatar overlays, and burned subtitles while mapping the premixed audio raw.

This avoids non-deterministic audio drops at scene boundaries.

## Final MP4 QA
Run after rendering:

```bash
python engine/gates/verify_episode.py ep01
```

`verify_episode` checks the final MP4 audio, including quiz question/options/reveal lines. Do not rely on upstream line WAVs or intermediate narration files.

## TTS and verification
- **Default = `chatterbox`** (high-quality neural voice) on GPU **and** CPU — never set `CC_TTS` for the
  normal path. A missing GPU makes it slower, not lower quality.
- `CC_TTS=piper` is a **user-approved downgrade** only (fast, robotic). The engine never falls back to
  it automatically; if chatterbox isn't installed it fails loud with install guidance.
- `CC_VERIFY=1` enables the self-correcting synth gate: garbled, repeated, or truncated takes are re-rolled.
- The shared text preprocessor applies pronunciations and acronym spelling to spoken lines only.

Faster-whisper can sometimes hallucinate repetition loops or omit short lines in long-form transcription. If a verification flag seems suspicious, re-extract and inspect the exact region before treating it as a real audio failure.

## Music and SFX
- Music is sourced, never generated.
- No sourced track means the bed is silent; rendering still succeeds.
- Music is ducked under voice with sidechain compression, then loudnorm and limiter are applied.
- SFX are bundled engine assets and mixed below narration.
## Environment switches
- Set `PYTHONUTF8=1` once per shell.
- Leave `CC_TTS` **unset** for the default high-quality chatterbox voice (GPU or CPU).
- Set `CC_TTS=piper` ONLY as a user-approved fast/lower-quality downgrade.
- Leave `CC_VERIFY=1` enabled for production unless debugging a verifier problem.

## Practical checks
- Listen around scene boundaries, where mux mistakes are most obvious.
- Listen to every quiz reveal: it must include the correct answer text and the why.
- Confirm captions match spoken lines in the final player.
- If a rerender changes voices or effects, the incremental cache should resynthesize affected lines.
- If no music is configured, expect silence rather than a generated substitute.
