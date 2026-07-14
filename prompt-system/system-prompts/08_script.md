# 08 — Storyboard and script from the learning blueprint

Read the truth layer, learning blueprint, media manifest, theme, `reference/PEDAGOGY_RULES.md`,
`reference/VISUAL_LANGUAGE.md`, and `reference/SCENE_CONTRACT.md`. Author
`course/scripts/epNN.json` as an aligned **instructional storyboard**, not a transcript pasted onto
slides.

## 1. Trace every episode and beat

Each episode declares `objective_ids`. Each beat declares:

- `objective_ids` it advances;
- `fact_ids` for every factual claim;
- `purpose` such as activate, explain, model, non-example, guided practice,
  independent practice, feedback, retrieve, transfer, or assess;
- `visual_purpose`: what the learner should notice or do with the visual;
- `alt` for explanatory visuals;
- `practice_id` or `evidence_id` where applicable;
- `narrative_function` only if narrative is enabled.

Do not write ornamental filler. If a beat has no objective or instructional function, remove it.

## 2. Use complementary channels

Narration carries explanation and reasoning. On-screen text labels, signals, and summarizes; it does
not reproduce paragraphs of narration. Show the referent while naming it. Point to the exact chart
feature, UI control, process step, or contrast at the moment it is discussed.

Use treatments from the blueprint:

- `image` for relevant appearance/context;
- `screenshot` plus callouts for interfaces/documents;
- `video` for source demonstrations;
- `comparison` for alternatives and non-examples;
- `timeline` for temporal order/change;
- `process` for stages and relationships;
- `chart` for quantities/patterns;
- `diagram` for structure;
- `worked_example` for expert reasoning;
- `practice` for pause-and-do performance;
- `quiz` for aligned retrieval or decisions;
- `quote` only when exact language matters.

The engine owns layout. Scripts provide semantic content and normalized callout rectangles, never
raw pixel coordinates.

## 3. Build learning, not just coverage

For complex performance, model the reasoning, then use guided/completion practice and fade toward
independence. Put feedback after commitment: state the correct answer/action, why it is correct, why
the likely alternative fails, and what cue to use next time. Include a novel surface context for
apply-level or higher objectives.

Use retrieval across episodes, not only same-scene repetition. If discrimination matters, mix
problem types rather than blocking one category at a time. Keep pacing segmented: one conceptual
move per beat, with natural pauses at boundaries.

## 4. Quiz and practice contracts

The interactive player preserves answer geometry from the rendered quiz scene. Keep exactly four
options for interactive MCQ beats; state the full answer text and one-line explanation in narration.
Do not use MCQ for a performance objective when a scenario, artifact, explanation, or pause-and-do
task is the aligned evidence.

`practice` beats are two-phase: first show the task and a visible work interval, then resume with the
reveal, model answer, and explanatory feedback.

## 5. Review before audio

Run a multi-model table read and an adversarial instructional review. Reviewers ask:

- Does each objective receive explanation, aligned practice, and feedback?
- Does higher-order evidence require higher-order performance?
- Is coverage complete without becoming source recitation?
- Are visual choices causally useful rather than decorative?
- Does narration duplicate dense screen text?
- Does story, if any, consume time without teaching?
- Can a learner apply the skill to a new example?

Fix text now. Then continue to `09_gates.md`.
