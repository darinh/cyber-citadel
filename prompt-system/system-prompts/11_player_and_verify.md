# 11 — Verify final artifacts and local player

Run final-artifact verification for every episode:

```powershell
python engine/gates/verify_episode.py ep01
python engine/package.py
python player/serve.py
```

`verify_episode.py` checks the **delivered mp4** for stream integrity, duration, captions, audio
presence, clipped/repeated/truncated narration, and expected cue alignment. Do not infer success from
upstream WAV files or intermediate clips.

Test the player over its range-capable HTTP server, never `file://` or a basic server without Range
support. At each interactive cue verify:

- buttons are clickable from the first visible frame;
- only the visible option buttons are clickable;
- hover outline and pointer cursor work;
- hit regions remain aligned after resizing;
- answer selection pauses/resumes correctly and provides full explanatory feedback;
- keyboard focus and captions remain usable.

Also check package links, transcript visual descriptions, media credits, alt text, optional job aids,
and responsive layout. Record learner or SME pilot feedback separately from structural gate results.
Structural conformance is necessary but does not prove transfer or retention.

Continue to `12_reference_materials.md` if reinforcement materials are enabled.
