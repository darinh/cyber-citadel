# AGENTS.md — build an accurate, effective, memorable video course

You are a GitHub Copilot CLI coding agent working inside this reusable `prompt-system/`.
Turn any subject into local video instruction that helps a defined audience perform a real task.
Start with learner outcomes, source coverage, assessment evidence, and practice. Choose direct
explanation, demonstrations, images, diagrams, animation, cases, or story only when that treatment
serves the learning objective. **A fictional world, characters, and slide deck are never defaults.**

## 0. Inventory and route

Every course lives in `projects/<slug>/`; never put course artifacts in the engine root.

- No project with `project.json`: start at `system-prompts/01_intake.md`. Ask for the topic,
  sources, audience, prior knowledge, work context, and what learners must be able to do. An
  aesthetic is optional.
- Truth exists but `course/design/learning-blueprint.json` does not: resume at
  `system-prompts/04_learning_design.md`.
- Blueprint exists but scripts do not: resume at `05_visual_language.md`, then `08_script.md`.
- Scripts exist but no episode: run `09_gates.md`, then render one pilot via `10_assemble.md`.
- Episodes exist: run final verification/package via `11_player_and_verify.md`.

Read the project's `plan.md`, `project.json`, `capabilities.json`, truth layer, and learning
blueprint before editing an in-progress course.

## 1. Objective-first pipeline

```text
01 intake          -> project.json (learner, desired performance, sources, scope)
02 environment     -> capabilities.json (hardware affects speed, never silent quality loss)
03 truth layer     -> course/data/truth.json (authoritative facts and citations)
04 learning design -> course/design/learning-blueprint.json
                      (objective -> evidence -> practice -> instruction -> transfer)
05 visual language -> theme.json + assets/media.json + optional cast/assets
06 narration       -> narrator voice; additional roles only when instruction needs them
07 music + SFX     -> optional sourced music; minimal sound design by default
08 storyboard      -> course/scripts/epNN.json (aligned beats + meaningful media)
09 gates           -> instruction + facts + IP + craft; all P1 findings block render
10 assemble        -> mp4 + captions + cues (one pilot first)
11 verify/player   -> final-mp4 QA + package + local range server
12 reinforcement  -> optional study guide, job aid, delayed retrieval, transfer practice
```

## 2. Non-negotiable rules

1. **Outcomes before aesthetics.** State observable learner performance and success criteria before
   choosing a delivery format. Avoid vague objectives such as “understand” or “be familiar with.”
2. **Alignment and completeness.** Every scoped fact maps to an objective. Every objective maps to
   acceptable evidence, modeled/guided work where needed, learner practice, explanatory feedback,
   and—at apply level or above—a novel transfer task.
3. **Accuracy.** IDs, titles, quotes, and factual visual claims trace to
   `course/data/truth.json`; quotes are verbatim and cited. Run the deterministic fact gate and an
   adversarial claim review before rendering.
4. **Media must earn its place.** Show appearance with an image, action with a demonstration,
   software with a screenshot/callout, change with animation/timeline, relationships with a diagram,
   quantities with a chart, discrimination with comparison, and reasoning with a worked example.
   Do not decorate a narration with irrelevant imagery or duplicate dense prose on screen.
5. **Story is optional.** Default delivery is direct, narrator-only instruction. Enable a world,
   fictional cast, or plot only with a written instructional function. Every narrative beat still
   serves an objective; entertainment never substitutes for explanation, practice, or feedback.
6. **Active learning, not trivia.** Use retrieval and interactive questions, but match assessment to
   the objective: classification, prediction, error detection, ordering, scenario decisions,
   completion problems, performances, and transfer prompts—not only recognition MCQs.
7. **Retention is designed.** Activate relevant prior knowledge, build prerequisites, use examples
   and non-examples where discrimination matters, fade scaffolds, retrieve prior objectives in later
   episodes, and provide delayed follow-up practice.
8. **Accessible, licensed media.** Every image/clip is declared in `assets/media.json` with path,
   provenance, license, credit, and alt text. Music is sourced public-domain/CC only and attributed.
9. **Quality stays high.** Chatterbox, SDXL when images are generated, large-v3 final audio QA,
   two-pass mux, captions, and quiz geometry remain the defaults on GPU or CPU. A speed-for-quality
   downgrade requires explicit user approval.
10. **Review and verify.** A multi-model council reviews learning design and script text. Render one
    pilot, inspect it, then verify the final mp4 and interactive player before scaling.

## 3. Engine folder and project folder

```text
prompt-system/
  AGENTS.md  system-prompts/  engine/  player/  reference/  schemas/  examples/
  projects/<slug>/
    project.json  capabilities.json  theme.json
    course/data/truth.json
    course/design/learning-blueprint.json
    course/scripts/epNN.json
    course/episodes/*.mp4 *.srt *.cues.json
    assets/media.json
    assets/{media,voices,avatars,music,backgrounds}/
    watch.html index.html serve.py play.cmd play.sh
```

## 4. Commands

Set `CC_PROJECT=projects/<slug>`, `PYTHONUTF8=1`, and `CC_VERIFY=1`. Leave quality-downgrade
variables unset.

```text
python engine/probe.py
python engine/theme.py
python engine/scene.py demo
python engine/gates/lint_instruction.py
python engine/gates/verify_facts.py course/scripts/ep01.json
python engine/gates/audit_narration.py course/scripts/ep01.json
python engine/gates/lint_prompts.py
python engine/gates/lint_script.py ep01
python engine/build_episode.py course/scripts/ep01.json
python engine/gates/verify_episode.py ep01
python engine/package.py
```

Read `reference/PEDAGOGY_RULES.md`, `reference/VISUAL_LANGUAGE.md`,
`reference/SCENE_CONTRACT.md`, `reference/AUDIO_RULES.md`, and
`reference/DEFINITION_OF_DONE.md` before authoring.

## 5. Definition of done

The instructional, fact, IP, and craft gates pass; coverage is deliberate; every objective has
aligned practice/feedback and transfer where required; media provenance is complete; one pilot was
rendered and inspected before any batch; every final mp4 passes audio QA; package links resolve; and
the local player works with accessible captions and aligned interactive hotspots. Structural gates
do not prove learning efficacy—record SME review and learner transfer evidence when available.
