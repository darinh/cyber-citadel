---
name: course-production
description: >-
  Orchestrate an accurate, effective narrated video course from authoritative truth through
  objective-first learning design, purposeful visuals, practice, text-first review, narration,
  assembly, final verification, and local packaging. Use for the existing course or a new topic.
---

# Course production orchestrator

Build for learner performance, not a predetermined story format. Review plans and artifacts with a
multi-model council before expensive rendering or scaling.

## Choose the correct path

- Maintaining the existing NIST course: follow `course/PRODUCTION_BIBLE.md` and its established
  cast/story conventions.
- Creating any new course: use `prompt-system/AGENTS.md` and a dedicated
  `prompt-system/projects/<slug>/`. Do **not** copy the original course's world, cast, palette, or
  episode recipe.

Read `course/GENERATION_PLAYBOOK.md`, `course/AUTHORING_NEW_COURSE.md`, and the prompt-system
pedagogy/visual-language references.

## New-course pipeline

1. **Truth** — authoritative `truth.json`; every factual claim and visual value traces to it.
2. **Learning blueprint** — audience/use context, terminal performance, prerequisites, source
   coverage, aligned evidence, practice, feedback, transfer, retention, and representations.
3. **Delivery/media plan** — direct narrator-only by default. Image, screenshot, source video,
   chart, diagram, comparison, worked example, scenario, story, cast, avatar, and music are selected
   only when they serve an objective. Register provenance and alt text.
4. **Storyboard/script** — declarative v2 beats with objective/fact/purpose traceability.
5. **Text-first review** — multi-model screenplay + instructional review before TTS.
6. **Accuracy and design gates** — `lint_instruction.py`, deterministic fact check, hostile claim
   audit, IP lint, and craft lint.
7. **Optional production branches** — avatars only if opted in; sourced music only if opted in;
   high-quality Chatterbox narration on GPU or CPU.
8. **Assemble one pilot** — incremental rendering, normalized source clips, two-phase practice,
   captions, interactive quiz cues, and two-pass mux.
9. **Verify/package** — final-mp4 audio QA, visual/player checks, credits, and local range server.
10. **Scale only after the pilot passes.**

## Non-negotiables

- Observable objectives and aligned higher-order evidence; recognition is not a proxy for transfer.
- Model complex work, fade support, require learner commitment, and give explanatory feedback.
- Use complementary visuals; remove decorative motion and narrated text walls.
- Story, characters, avatars, music, and progress/stakes chrome are optional—not quality proxies.
- Hardware changes speed, not default model quality. A downgrade requires explicit user approval.
- Read every quiz question and option, then the correct answer text and why.
- Verify the delivered mp4, not intermediate audio; preserve the two-pass mux.
- Structural gates do not prove learning. Record SME/learner performance evidence when available.
- Update the playbook/changelog and relevant skill whenever the pipeline learns something durable.

## Council

Use varied hosted models plus local models. Review the blueprint and complete script end-to-end.
Merge corroborated findings, validate each against truth/contracts, fix P1s and accepted P2s, rerun
gates, then render. Review agents use isolated worktrees.
