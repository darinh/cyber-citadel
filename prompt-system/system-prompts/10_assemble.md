# 10 — Assemble one representative pilot

Render exactly one representative episode before any batch. It should exercise the project’s
highest-risk feature: technical pronunciation, source video, callouts, chart animation, practice,
or interactive quiz.

```powershell
$env:CC_PROJECT = "projects\<slug>"
$env:PYTHONUTF8 = "1"
$env:CC_VERIFY = "1"
Remove-Item Env:CC_TTS -ErrorAction SilentlyContinue
python engine/build_episode.py course/scripts/ep01.json
```

## Assembly contracts

- Images and clips resolve through `assets/media.json`; changing an asset invalidates affected beat caches.
- Source clips are normalized separately to 1920x1080, 30 fps, H.264, and muted before narration.
- When narration is longer than a source excerpt, hold its final frame; never loop a procedure invisibly.
- Practice beats render the task/work interval and reveal/feedback as separate phases.
- Captions stay below instructional content and never cover quiz options.
- Interactive quiz option rectangles come from the frozen rendered scene and remain normalized.
- Music/SFX follow project settings; minimal means no habitual sound on every beat.
- Final A/V uses the proven two-pass mux. Verify the delivered mp4, not intermediate clips.

Watch the entire pilot at normal size and resized. Check visual legibility, callout alignment,
caption overlap, pacing, learner work time, narration completeness, music ducking, scene variety,
and whether every visual clarifies the narration. Fix and rerender the pilot until it passes before
rendering the rest of a course. Then continue to `11_player_and_verify.md`.
