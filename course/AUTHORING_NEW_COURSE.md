# Authoring a new course with the portable prompt system

Use `prompt-system/` for a new subject. The original course under `course/` is one creative
instantiation with its own cast and tooling; it is not the template. The portable engine defaults to
direct, narrator-only instruction and chooses media, scenarios, or narrative from the learning task.

Read:

- `prompt-system/AGENTS.md`
- `prompt-system/reference/PEDAGOGY_RULES.md`
- `prompt-system/reference/VISUAL_LANGUAGE.md`
- `prompt-system/reference/SCENE_CONTRACT.md`
- `prompt-system/reference/PRODUCTION_RULES.md`

## 1. Project isolation

Every new course lives under `prompt-system/projects/<slug>/`:

```text
project.json
capabilities.json
theme.json
course/data/truth.json
course/design/learning-blueprint.json
course/scripts/epNN.json
assets/media.json
assets/{media,voices,avatars,music}/
```

Do not put generated course artifacts in the repository root or copy the original course's names,
world, palette, cast, story structure, or scene sequence.

## 2. Objective-first pipeline

```text
authoritative source
  -> truth.json (stable facts and citations)
  -> desired terminal performance and prerequisite objectives
  -> acceptable evidence, learner practice, feedback, and transfer
  -> purposeful representations and optional delivery concept
  -> episode storyboard/script
  -> instructional + fact + IP + craft gates
  -> one pilot render and final-mp4/player verification
  -> remaining episodes and optional reinforcement
```

### Intake

Collect the audience, prior knowledge, use context, source, scope, and an observable completion:

> After this course, the learner can ___ under ___ conditions to ___ criteria.

Ask about delivery preferences, but do not require an aesthetic, world, cast, avatars, music, or
story. When the user delegates those decisions, default to direct narrator-only instruction,
practice enabled, and restrained subject-derived visuals.

### Truth layer

Parse or curate the authoritative source into `course/data/truth.json`. Each fact needs a stable ID,
title, statement, and citation/section where available. Source every factual visual claim too. Never
use model memory as authority.

### Learning blueprint

Write `course/design/learning-blueprint.json` using
`prompt-system/schemas/learning-blueprint.schema.json`. Explicitly:

- require or exclude every truth fact with a reason;
- decompose the terminal performance into measurable prerequisite objectives;
- choose evidence before instruction;
- match evidence/practice to cognitive demand;
- model and fade complex skills toward independent performance;
- provide explanatory feedback;
- include novel transfer for apply-level and higher objectives;
- plan delayed/cumulative retrieval;
- state why each image, screenshot, clip, chart, diagram, comparison, or worked example is needed.

### Visual language and media

Choose treatment by the learner's task:

| Need | Treatment |
|---|---|
| Recognize appearance/context | relevant image |
| Locate a real control or document element | annotated screenshot |
| Observe a procedure | source video or screenshot sequence |
| See change/order | animation, timeline, process, or chart |
| Understand structure | diagram/process |
| Discriminate cases | comparison with examples/non-examples |
| Interpret quantity | sourced chart |
| Follow reasoning | worked example |
| Perform/retrieve | practice or interactive quiz |

Register images and clips in `assets/media.json` with path, origin, license, creator, source URL,
credit, and alt text. Music is optional and sourced only. Story/cast/avatar work occurs only when
`learning-blueprint.delivery.narrative.enabled` is true with a concrete instructional function.

## 3. Episode v2 contract

Each spec is schema version `2.0` and declares the planned objective IDs. Every non-structural beat
traces to:

- `objective_ids`
- `fact_ids`
- `purpose` (`explain`, `model`, `guided_practice`, `transfer`, and so on)
- `visual_purpose`
- `practice_id` / `evidence_id` where relevant
- `alt` for explanatory visuals
- `say` narration/dialogue

Primary treatments:

| Scene | Semantic fields |
|---|---|
| `image` | `asset`, `fit`, `focus`, `title`, `caption` |
| `screenshot` | `asset`, normalized `callouts[].rect`, `label` |
| `video` | `asset`, `start`, `end`, `fit` |
| `comparison` | semantic `left` and `right` cases |
| `timeline` | `events[{when,label,note}]` |
| `process` | `steps[{title,detail}]`, `layout` |
| `chart` | `chart_type`, `data[{label,value}]`, `unit`, `insight` |
| `worked_example` | `problem`, reasoning `steps`, `model_answer` |
| `practice` | `prompt`, `instructions`, `think_seconds`, `model_answer`, `feedback` |
| `quiz` | `q`, four `options`, zero-based `answer`, explanatory `why` |

The engine owns pixels, font measurement, animation, captions, and quiz geometry. See
`prompt-system/reference/SCENE_CONTRACT.md` for exact examples and legacy scene compatibility.

## 4. Gates before rendering

From `prompt-system/`:

```powershell
$env:CC_PROJECT = (Resolve-Path "projects\<slug>").Path
$env:PYTHONUTF8 = "1"
$env:CC_VERIFY = "1"

python engine\gates\lint_instruction.py --warn
python engine\gates\verify_facts.py "$env:CC_PROJECT\course\scripts\ep01.json"
python engine\gates\lint_prompts.py
python engine\gates\lint_script.py ep01 --warn
```

Then run an adversarial source/claim audit and a multi-model screenplay/instructional review.
Reconcile findings against the source and contracts. Automated structure checks do not prove learner
effectiveness.

## 5. Render and verify one pilot

```powershell
Remove-Item Env:CC_TTS -ErrorAction SilentlyContinue
python engine\build_episode.py "$env:CC_PROJECT\course\scripts\ep01.json"
python engine\gates\verify_episode.py ep01
python engine\package.py
python player\serve.py
```

Chatterbox, SDXL when generation is needed, and large-v3 verification are the high-quality defaults
on GPU or CPU. Hardware changes speed, never model quality. Any downgrade requires explicit user
approval.

Watch the pilot completely and resized. Verify source clip timing, callouts, chart labels, learner
work time, explanatory reveals, captions, final audio, and interactive hotspot alignment. Only then
render additional episodes.

## 6. Retention and performance support

Use a job aid for in-workflow decisions, a study guide for explanation and examples, delayed
retrieval for retention, and varied transfer cases for flexible use. Do not generate a decorative
summary that merely repeats headings.

## 7. Legacy compatibility

Schema-v1 projects and narrative scene types remain renderable. They do not receive the v2
instructional gate automatically. New projects should use schema v2; do not backport the original
course's mandatory world/cast/story assumptions into the portable workflow.
