# 06 — Narration and optional character voices

Read `project.json`, the learning blueprint, `theme.json`, `capabilities.json`, and
`reference/AUDIO_RULES.md`.

## Default

Use one natural, conversational narrator. Additional speakers are optional instructional devices,
not a production-quality requirement. Add a second speaker only when contrast, interview, coached
practice, or perspective genuinely improves the objective.

Do not assign learner exposition to a fictional novice merely to create dialogue. Do not make
characters recite source material that direct narration could teach more clearly.

## Quality contract

- Chatterbox is the default on GPU **and CPU**.
- Use license-clean local reference recordings.
- A CPU may be slower; speed does not justify silent replacement with a weaker model.
- Piper or another downgrade requires explicit user approval.
- Apply project pronunciation rules before synthesis.
- Synthesize short beat-level clips so defects can be retried without rebuilding an episode.
- Run the self-correcting synth gate and verify narration again in the final mp4.

Create or curate references under `assets/voices/`, configure the actual files in `theme.json`, and
render representative lines containing acronyms, numbers, technical terms, and expressive changes.
Listen for truncation, repetition, hallucinated words, wrong speaker, clipping, and unnatural stress.

```powershell
$env:CC_VERIFY = "1"
python engine/tts.py "Representative narration line." "NARRATOR" "_voice_check.wav"
```

Record approved references and stable voice knobs in project notes. Continue to
`07_music_and_sfx.md`.
