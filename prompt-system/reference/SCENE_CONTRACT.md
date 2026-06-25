# Scene Contract

Author beats in `course/scripts/epNN.json`; the engine renders frames from `engine/scene.py`. Never hand-render frames. The theme may change colors, fonts, and words only; geometry, caption placement, timing, quiz boxes, and quality stay frozen in `engine/`.

Every beat may include:
- `say`: optional dialogue lines as `["SPEAKER", "line"]`; used for narration/captions/avatars.
- `min_seconds`: optional minimum on-screen duration; dense slides should set it generously.
- Do **not** hand-set reserved auto fields: `_integrity`, `_t`, `tag`, `reveal`.
- To add a visual pattern, add a renderer in `engine/scene.py` and register it in `RENDERERS`.

| Scene | Purpose | Fields | Example |
| --- | --- | --- | --- |
| `title` | Episode title card. | Optional: `kicker`, `badge`, `title`, `subtitle`. | `{ "scene":"title", "kicker":"AN INTERACTIVE COOKING SERIES", "badge":"LESSON 01", "title":"KNIFE SKILLS", "subtitle":"Cut safely" }` |
| `section` | Act/section divider. | Optional: `num`, `title`, `subtitle`. | `{ "scene":"section", "num":"02", "title":"Control", "subtitle":"Hands, board, blade" }` |
| `map` | Course/group map with optional highlights and dependencies. | Optional: `title`, `order`, `highlight`, `deps`. `order` defaults to theme group order. | `{ "scene":"map", "title":"Stations", "order":["KN","HEAT"], "highlight":["KN"], "deps":[["KN","HEAT"]] }` |
| `persona` (`guardian`) | Group/persona card connecting metaphor to real practice. | Optional: `group`/`family`, `group_name`/`family_name`, `persona`, `summary`/`protects`, `meaning`/`reality`. | `{ "scene":"persona", "group":"KN", "group_name":"Knife Station", "persona":"The steady prep lead", "summary":"Safe cutting basics", "meaning":"Stable setup and controlled motion" }` |
| `concept` (`control`) | Fact/concept card with source line. | Optional: `id`, `title`, `plain`, `why`, `source`, `section`. On-screen factual `id`/`title` must match truth. | `{ "scene":"concept", "id":"KN-1", "title":"Pinch Grip", "plain":"Pinch the blade near the handle.", "why":"It improves control.", "source":"Kitchen Academy Handbook", "section":"2.1" }` |
| `quote` | Verbatim source excerpt with citation. | Required for fact gate: `quote` as a verbatim substring, `cite` naming the source/fact. Spoken quote must equal on-screen quote. | `{ "scene":"quote", "quote":"Curl the fingertips of your guiding hand under.", "cite":"Kitchen Academy Handbook · KN-2" }` |
| `diagram` | Boxes and arrows. | Optional: `title`. Required for useful diagram: `nodes` with `{label,x,y,w?,h?,color?}`, `arrows` as `[fromIndex,toIndex,label?]`. | `{ "scene":"diagram", "title":"Prep flow", "nodes":[{"label":"Set board","x":300,"y":360}], "arrows":[] }` |
| `points` | Bullet teaching slide. | Optional: `kicker`, `title`, `bullets`, `note`. | `{ "scene":"points", "kicker":"REMEMBER", "title":"Three checks", "bullets":["Board steady","Blade sharp"], "note":"Set up once." }` |
| `cheatcard` | Recap card for a group/topic. | Optional: `group`/`family`, `title`, `bullets`, `mnemonic`. | `{ "scene":"cheatcard", "group":"KN", "title":"Knife Skills", "bullets":["Pinch grip","The claw"], "mnemonic":"Sharp blade, safe claw." }` |
| `define` | Plain-language definition card. | Optional: `kicker`, `term`, `expand`, `plain`, `example`, `cite`. | `{ "scene":"define", "kicker":"PLAIN LANGUAGE", "term":"Mise en place", "plain":"Everything in its place.", "example":"Put a damp towel under the board." }` |
| `coldopen` | Hook/tension card tied to the lesson. | Optional: `label`, `year`, `headline`, `body`, `mitre`, `teaches`. | `{ "scene":"coldopen", "label":"CASE STUDY", "year":"2024", "headline":"Dinner rush slows prep", "body":"A loose board causes mistakes.", "teaches":"Knife setup" }` |
| `quiz` | Interactive question; engine reads it aloud and exports `opt_rects` for clickable hotspots. | Required: `q`, `options`, `answer` (0-based index), `why`. Optional: `kicker`, `min_seconds`. | `{ "scene":"quiz", "q":"Where should fingertips be?", "options":["Flat","Curled under","Over blade"], "answer":1, "why":"The claw keeps tips behind knuckles." }` |
| `pledge` (`oath`) | Spoken mnemonic pledge for a group. | Optional: `group`/`family`, `oath`, `controls`. | `{ "scene":"pledge", "group":"KN", "oath":"I set the board before I cut.", "controls":"KN-1 · KN-2" }` |
| `notebook` | Recap page with ruled notes. | Optional: `title`, `lines`, `mnemonic`. | `{ "scene":"notebook", "title":"Today’s notes", "lines":["Stable board first","Guide with knuckles"], "mnemonic":"Steady, sharp, tucked." }` |

Quiz geometry is frozen in `quiz_layout()`: question at the top, 96px option boxes stacked below, and the same rectangles exported as normalized `opt_rects`. Do not alter player hotspots separately.
## Field notes
- `title`: `badge` and `kicker` are optional labels; `subtitle` should fit on one line.
- `section`: use `num` for act numbering; keep `title` unique inside an episode.
- `map`: `deps` is a list of two-item group-key pairs; `highlight` reveals selected groups.
- `persona`/`guardian`: `group` is the short key; `group_name` is the human-readable name.
- `concept`/`control`: `id` drives group color by prefix and is checked by the fact gate.
- `quote`: keep `say` exactly equal to `quote` if the quote is narrated.
- `diagram`: node `x`/`y` are pixel positions in the frozen 1920x1080 frame.
- `points` and `cheatcard`: each `bullets` item is a string; use `note` or `mnemonic` for the final takeaway.
- `define`: `expand` is for acronyms; `plain` is the learner-facing definition.
- `coldopen`: use sourced, non-fabricated cases; `teaches` is the lesson target.
- `quiz`: `answer` is zero-based; the engine draws A/B/C letters and reveal checkmark.
- `pledge`/`oath`: `controls` is rendered as a single mono line.
- `notebook`: `lines` are rendered as ruled handwritten-style notes.

## Rendering rule
The `RENDERERS` keys are the authoritative scene names. If a key is absent there, the engine cannot render that scene.
