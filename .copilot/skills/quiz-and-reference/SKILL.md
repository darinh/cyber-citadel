---
name: quiz-and-reference
description: >-
  Author aligned learner practice, read-aloud interactive quizzes, delayed retrieval, transfer
  activities, job aids, study guides, and quiz banks for narrated courses.
---

# Practice, quizzes, and performance support

Watching is not evidence of learning. Start from the objective and acceptable evidence, then choose
the activity form.

## Match activity to performance

- Remember/understand: retrieval, explanation, selected response.
- Apply/analyze: classification, ordering, prediction, error detection, completion problem, scenario.
- Evaluate/create: justification, performance, product, critique, or application to a novel case.

Recognition MCQ does not establish that a learner can perform a procedure or justify a decision.
Use `practice` beats for pause-and-do work and `quiz` only when four-option selection is aligned.

## Interactive quiz contract

`q`, four mutually exclusive `options`, zero-based `answer`, and explanatory `why` are required.

1. Show and read the full question and every option.
2. Make only the visible option buttons clickable from their first frame.
3. Pause for commitment.
4. Reveal and read the letter, full correct answer text, and a one-line explanation—never the
   letter alone.

The engine exports normalized option rectangles from the renderer, so the player must use those
coordinates rather than re-derive layout.

## Pause-and-do practice contract

Provide `practice_type`, `prompt`, concise `instructions`, sufficient `think_seconds`,
`model_answer`, and specific `feedback`. The reveal explains why the response works, why a likely
alternative fails, or which process cue to use next. For complex skills, sequence modeled,
guided/completion, and independent/transfer activities.

## Retention and reference artifacts

- **Delayed retrieval:** recall/use before answer exposure at increasing intervals.
- **Transfer set:** varied surface contexts preserving the underlying principle.
- **Job aid:** decision cues, steps, thresholds, examples, and escalation points used during work.
- **Study guide:** objective-organized explanations, examples/non-examples, misconceptions, sources.
- **Quiz bank:** parallel items mapped to objective/evidence/fact IDs with explanatory feedback.

Do not produce a decorative recap that only repeats headings. Mix prior objectives into later
practice when discrimination and retention matter.

## Gates

Run instructional alignment, screenplay clarity, and fact verification before render. After render,
verify the final mp4 speaks every question/option/answer/why, practice cues contain both phases, and
hotspots remain aligned and accessible after resize.
