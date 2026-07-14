# Production rules

These rules preserve instructional and technical quality across subjects and delivery styles.

## Before scripting

1. Keep the course under `projects/<slug>/`.
2. Build and cite `truth.json`.
3. Define audience, terminal performance, prerequisites, conditions, and success criteria.
4. Complete `learning-blueprint.json`: scope decisions, aligned evidence, practice, feedback,
   representations, episode order, retention, and delivery rationale.
5. Register every image/clip in `assets/media.json`.
6. Review the blueprint adversarially before spending time on polished script or media.

## Authoring

- Default to one direct narrator; story, cast, avatars, and music are opt-in.
- Trace each beat to objectives and facts.
- Choose scene treatment by cognitive purpose, not visual habit.
- Use complementary narration and visuals, signaling, segmenting, and restrained motion.
- Model complex reasoning; fade practice; require independent/transfer performance.
- Give explanatory feedback after learner commitment.
- Read interactive quiz questions, every option, full correct answer text, and one-line why.
- Keep all layouts semantic and engine-owned; scripts do not hand-pack pixels.

## Asset and IP safety

- Use original or explicitly licensed media, voices, music, fonts, and SFX.
- Music is sourced, never generated.
- Record media provenance and accessibility metadata.
- Do not reference protected franchises, named characters/places, celebrity likenesses, studio
  branding, trade dress, or “in the style of” living artists.
- Aesthetic inspiration is translated into generic design attributes, not imitation.

## Quality and hardware

- Hardware changes speed, not the default model quality.
- Use Chatterbox, SDXL when generation is needed, and large-v3 final audio verification on GPU or CPU.
- Fail loudly when high-quality dependencies are unavailable.
- A downgrade requires explicit user approval and a recorded reason.

## Render and verification

1. Run instructional, fact, IP, and craft gates before rendering.
2. Render and inspect one representative pilot before any batch.
3. Use incremental beat caches; media fingerprints invalidate affected beats.
4. Normalize source clips separately and strip their audio by default.
5. Use the two-pass final mux.
6. Verify the delivered mp4, captions, cues, media credits, and interactive player.
7. Test hotspot geometry and accessibility after player resize.

Structural gates establish conformance, not learning efficacy. Add SME approval and learner
performance/transfer evidence when available.
