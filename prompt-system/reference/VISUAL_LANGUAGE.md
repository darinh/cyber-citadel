# Visual-language rules

Visual variety is a consequence of **different instructional jobs**, not a quota of layout changes.
Keep identity coherent—type, palette, captions, line weight, animation timing—while selecting the
representation that makes each concept easiest to perceive, reason about, or perform.

## 1. The visual must answer a question

For every explanatory beat, complete:

> After seeing this visual, the learner should notice/do ___ that narration alone would not make as
> clear.

If there is no good answer, use restrained direct narration rather than decorative imagery.

## 2. Treatment selector

| Instructional question | Primary treatment | Typical signaling |
|---|---|---|
| What does it look like? | Full-bleed/contained `image` | Crop, focus point, one label |
| Where is it in a real interface/document? | `screenshot` | Numbered callout or highlight box |
| How is a real action performed? | Muted `video` demo | Cursor/region highlight, narrated step |
| How does it change over time? | `timeline`, animated `chart`, or source clip | Progressive reveal |
| How do parts relate? | `diagram` or `process` | Highlight current node/arrow |
| Which case fits, and why? | `comparison` | Shared criterion and contrasting feature |
| What pattern do the quantities show? | `chart` | Direct labels and highlighted evidence |
| How does an expert reason? | `worked_example` | Step highlight and visible decision cue |
| Can the learner do it? | `practice` or `quiz` | Clear task, work time, then reveal |
| Does exact wording matter? | Short `quote` | Source and relevant phrase emphasis |

Use a sequence when one treatment is insufficient: for example, establish context with a photograph,
locate controls in a screenshot, show the procedure in a clip, then use a practice simulation.

## 3. Complement narration; do not mirror it

- Narrate reasoning, causality, caveats, and transitions.
- Put names, short criteria, values, and structural cues on screen.
- Avoid paragraphs of on-screen prose that substantially repeat narration.
- Display a verbatim quote only when exact language is itself the object of learning.
- Align words and visuals in time; do not describe a feature before it appears or after it disappears.

## 4. Signal attention

Use contrast, callout boxes, arrows, progressive reveal, dimming, or camera focus to direct attention
to the current element. One active signal is usually stronger than five competing decorations.
Signaling must not rely on color alone; pair color with shape, label, position, line style, or icon.

## 5. Scene-specific rules

### Images

- Prefer real, original, or licensed subject-relevant imagery over generic stock symbolism.
- Use `cover` for context and `contain` when the whole artifact matters.
- Set a focus point so crops preserve the instructional subject.
- Keep labels outside the important image region where possible.

### Screenshots

- Capture a clean, legible state at target resolution.
- Callouts use normalized `[x,y,w,h]` coordinates so they survive resize.
- Hide or anonymize credentials, personal data, and irrelevant UI.
- Use successive screenshots or a clip for procedures; do not crowd one screenshot with every step.

### Source video and demonstrations

- Show action, not a talking head repeating narration.
- Select the exact excerpt, strip source audio unless it is instructionally essential and licensed,
  and narrate the visible action.
- Never speed a safety-critical or precision procedure beyond intelligibility.
- If narration outlasts the excerpt, hold the final frame rather than silently looping an action.

### Charts

- Chart data and claimed insight must trace to truth facts.
- Use a zero baseline when magnitude comparison requires it; disclose truncation when justified.
- Label values/series directly when possible; avoid forcing legend lookups.
- Highlight the evidence for the spoken conclusion.
- Do not add 3-D perspective, decorative gradients, or animation unrelated to reading the pattern.

### Processes and timelines

- Use semantic steps/events, not manually packed pixels.
- Show direction and order unambiguously.
- For cycles, explain what returns and under what condition; do not use a circle merely for style.
- Reveal in narrated order and keep previously needed context visible.

### Comparisons

- Compare cases under the same criteria and visual scale.
- Use a meaningful example/non-example or decision boundary.
- Label the discriminating feature; do not rely only on “good/bad” color.

### Worked examples and practice

- Separate problem, steps, answer, and feedback.
- Highlight one reasoning step at a time.
- Completion practice should visibly remove support rather than show another full solution.
- Give enough quiet work time; do not reveal while the prompt is still being read.

## 6. Motion rules

Animate to show change, order, causality, or attention. Entrance motion should complete quickly and
settle so the learner can inspect the final state. Avoid constant pans across diagrams, ornamental
particle fields, temporal noise, or moving backgrounds behind dense content. Static is a valid
choice when motion adds no information.

## 7. Accessibility and provenance

Every explanatory image or clip has concise alt text in both the beat and `assets/media.json`.
Media that embeds data, labels, events, or factual examples also declares `fact_ids`; the consuming
beat repeats those IDs. Captions never cover the primary evidence or interactive controls. Maintain readable type,
contrast, safe margins, and non-color cues. Media entries include origin, license, creator, source
URL where applicable, credit, and generation metadata for generated-original assets.

## 8. Review visual quality by dependency, not quotas

Do not require “one image every N scenes” or “at least five layouts.” Instead ask:

- Was each planned representation implemented?
- Does every representation perform its stated purpose?
- Did a passive text/card streak emerge where showing, modeling, or practice was required?
- Is any media decorative, redundant, misleading, inaccessible, or unsupported?
- Does the sequence move from perception/explanation to learner performance?

The instructional gate reports passive streaks and repeated treatments for review; it should not
force visual churn where a stable representation is pedagogically useful.

## Research basis

The multimedia rules apply signaling, segmenting, weeding, matching modality, and active learning as
synthesized in Brame (2016):
https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380/

The IES practice guide also recommends combining graphics with verbal descriptions and integrating
abstract and concrete representations while highlighting corresponding features:
https://ies.ed.gov/ncee/wwc/PracticeGuide/20072004
