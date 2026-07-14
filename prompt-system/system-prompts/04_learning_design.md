# 04 — Learning design: objective -> evidence -> practice -> instruction

Write `course/design/learning-blueprint.json` before choosing a visual style, story, or cast. Read
`reference/PEDAGOGY_RULES.md` and `schemas/learning-blueprint.schema.json`.

## 1. Scope the source deliberately

List every `truth.json` fact under either:

- `required_fact_ids`: necessary for the requested performance; or
- `excluded_fact_ids`: intentionally outside scope, each with a concrete reason.

No source fact may disappear accidentally. “Comprehensive” means all in-scope knowledge is taught
and used, not that every source sentence is dumped into narration.

## 2. Write observable objectives

Begin with one terminal performance, then decompose it into prerequisite objectives. Each objective
needs:

- an observable `action_verb` and full `performance`;
- condition and measurable success criteria;
- cognitive level (`remember` through `create`);
- prerequisite and truth fact IDs;
- known misconceptions;
- acceptable evidence that matches the cognitive level;
- planned practice with scaffolding and explanatory feedback;
- a novel transfer context for `apply` and above;
- one or more necessary representations, each with an instructional rationale.

Reject “understand,” “learn,” “know,” “appreciate,” and “be familiar with.” Ask what a learner who
truly understood would **do differently**.

## 3. Align evidence and practice

Choose evidence before content. Recognition MCQ is suitable mainly for remember/understand. For
higher-order objectives prefer scenario decisions, classification, ordering, prediction, error
detection, worked-example completion, explanation, performance, product, or application to a novel
case.

Plan a learning cycle appropriate to the objective:

1. Activate only relevant prior knowledge.
2. Explain and show the concept.
3. Model expert reasoning or performance for complex skills.
4. Give guided or completion practice.
5. Fade support toward independent practice.
6. Give specific corrective, elaborative, process, or comparative feedback.
7. Retrieve later and transfer to a different surface context.

Do not force every technique onto every objective. Interleave when learners must discriminate
between problem types; use examples/non-examples when category boundaries matter.

## 4. Plan episodes and retention

Sequence prerequisites before dependent performance. `episodes[].retrieves` names prior objectives
that will be actively recalled in a later episode. For a single video, add delayed follow-up
activities under `retention.follow_up` (for example, one day and one week later).

## 5. Select delivery mode last

Default:

```json
{"mode":"direct","cast":"narrator-only","narrative":{"enabled":false}}
```

Enable documentary, demonstration, case, scenario, or story only when it improves the objective.
If narrative is enabled, state a concrete `instructional_function`; “engagement” alone is not enough.

## Gate now

Create the blueprint using `schemas/learning-blueprint.schema.json`, then run:

```powershell
python engine/gates/lint_instruction.py
```

At this phase scripts do not yet exist, so the gate will report missing implementation. Review the
blueprint-specific findings now; script traceability findings are resolved in phase 08. Then continue
to `05_visual_language.md`.
