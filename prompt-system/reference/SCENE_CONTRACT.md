# Episode and scene contract

`engine/build_episode.py` renders declarative JSON. Layout is engine-owned; authors provide semantic
content and normalized coordinates only. Validate against `schemas/episode-spec.schema.json`.

## Episode fields

```json
{
  "schema_version": "2.0",
  "id": "ep01",
  "slug": "read-the-pattern",
  "title": "Read the Pattern",
  "objective_ids": ["OBJ-1"],
  "sound_design": "minimal",
  "progress_meter": false,
  "beats": []
}
```

`music` is an optional sourced track key/path. `sound_design` is `none`, `minimal`, or `cinematic`;
use `minimal` by default. Progress meters are opt-in and should represent a real instructional state,
not inherited story chrome.

## Common v2 beat fields

```json
{
  "scene": "chart",
  "objective_ids": ["OBJ-1"],
  "fact_ids": ["F-1"],
  "purpose": "model",
  "visual_purpose": "visualize_quantity",
  "alt": "A line chart whose final point reverses the earlier decline.",
  "say": [["NARRATOR", "First identify the overall direction, then inspect exceptions."]],
  "min_seconds": 5
}
```

- `objective_ids` trace instruction.
- `fact_ids` trace claims.
- `purpose` is one of `orient`, `activate`, `define`, `explain`, `model`, `example`,
  `non_example`, `guided_practice`, `independent_practice`, `feedback`, `retrieve`, `synthesize`,
  `transfer`, or `assess`.
- `visual_purpose` states what the representation does.
- `practice_id`/`evidence_id` link activities.
- `narrative` and `narrative_function` are required only for an enabled narrative beat.
- `say` is an array of `[speaker,text]`; narrator-only is valid.
- `alt` is required for explanatory visual treatments.

## Visual treatments

### Title

```json
{"scene":"title","badge":"5-MINUTE SKILL","title":"Read the Pattern",
 "subtitle":"Classify evidence without overclaiming"}
```

`badge` is an optional short label displayed in a fitted pill above the heading. The craft gate
measures the themed badge font and letter spacing before render.

### Image

```json
{"scene":"image","asset":"factory-floor","fit":"cover","focus":[0.62,0.45],
 "caption":"Inspect the work where it happens.","alt":"An operator checking a gauge."}
```

`asset` is a key in `assets/media.json`. `fit` is `cover` or `contain`; `focus` is normalized.
If the image itself contains factual values or labels, its manifest entry declares `fact_ids` and
the beat includes the same IDs.

### Screenshot with callouts

```json
{"scene":"screenshot","asset":"dashboard","title":"Locate the warning",
 "callouts":[{"rect":[0.64,0.18,0.22,0.12],"label":"1","text":"Status and threshold"}],
 "alt":"A dashboard with the status panel highlighted."}
```

Callout `rect` values are normalized `[x,y,w,h]`; `label` is the visible explanation.

### Source video

```json
{"scene":"video","asset":"procedure-demo","start":4.2,"end":12.8,"fit":"contain",
 "alt":"A cursor opens the filter and selects the previous week."}
```

Source audio is stripped. The selected excerpt is normalized; its final frame holds if narration is
longer.

### Comparison

```json
{"scene":"comparison","title":"Trend or anomaly?",
 "left":{"asset":"trend-chart","fit":"contain","label":"Trend",
         "title":"Sustained direction","body":"Several consecutive periods"},
 "right":{"asset":"anomaly-chart","fit":"contain","label":"Anomaly",
          "title":"Isolated departure","body":"One point breaks the pattern"},
 "alt":"Two cases contrasted by persistence over time."}
```

Each side may omit `asset` for a text-only comparison or name a manifested image asset. Nested
assets receive the same existence, provenance, traceability, cache, and credit checks as top-level
media.

### Timeline

```json
{"scene":"timeline","title":"What changed first?",
 "events":[{"when":"09:00","label":"Deploy","note":"Version 4.2 starts"},
           {"when":"09:08","label":"Errors rise","note":"Investigate; timing alone is not cause"}],
 "alt":"Deployment precedes an increase in errors by eight minutes."}
```

### Process

```json
{"scene":"process","title":"Evidence before conclusion","layout":"linear",
 "steps":[{"title":"Observe","detail":"Read the axes"},{"title":"Compare","detail":"Find the baseline"},
          {"title":"Conclude","detail":"Name the supported pattern"}],
 "alt":"Observe, compare, then conclude."}
```

Use `layout:"cycle"` only for a genuine repeating loop.

### Chart

```json
{"scene":"chart","title":"One spike is not a trend","chart_type":"line","unit":"%",
 "data":[{"label":"W1","value":2},{"label":"W2","value":2.2},{"label":"W3","value":7.1}],
 "insight":"The final point is isolated; persistence has not been established.",
 "alt":"Two values near two percent followed by one isolated value above seven percent."}
```

Data and insight must trace to truth facts. The deterministic fact gate checks authored numeric
values against the statements named by `fact_ids`.

### Worked example

```json
{"scene":"worked_example","title":"Model the decision","problem":"Classify the pattern.",
 "steps":[{"title":"Direction","detail":"Mostly flat"},{"title":"Exception","detail":"One spike"}],
 "model_answer":"Anomaly, pending more observations.",
 "alt":"A two-step classification followed by a qualified conclusion."}
```

### Practice

```json
{"scene":"practice","practice_id":"P-1","evidence_id":"E-1",
 "practice_type":"classification","prompt":"Classify this unfamiliar chart.",
 "instructions":"State the pattern and cite one visible cue.","think_seconds":8,
 "model_answer":"A sustained upward trend; four consecutive points rise.",
 "feedback":"The repeated direction, not the final value alone, supports the classification.",
 "alt":"An unlabeled practice chart with four rising points."}
```

The assembler creates prompt/work and reveal/feedback phases and records them in `activities`.

### Quiz

`quiz` requires `q`, exactly four `options`, zero-based `answer`, and explanatory `why`. The engine
renders question/countdown and reveal phases, reads all options aloud, emits frozen normalized
`opt_rects`, and writes interactive cues. The craft gate blocks a question whose wrapping would
push the fourth option into the burned-caption region.

## Legacy treatments

`title`, `section`, `concept`, `control`, `quote`, `diagram`, `points`, `cheatcard`, `define`,
`coldopen`, `notebook`, `map`, `persona`, `guardian`, `pledge`, and `oath` remain render-compatible.
For schema v2, use them only when their instructional purpose is explicit. Persona/guardian/pledge/
oath treatments are blocked when narrative is disabled.

## Reserved fields

Never hand-set `_integrity`, `_t`, `tag`, `reveal`, or quiz option rectangles. The engine owns them.
