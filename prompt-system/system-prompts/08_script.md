# 08 — Script → `course/scripts/epNN.json`

Author one JSON spec per episode: an ordered list of **beats** (a scene + on-screen fields + spoken
`say` lines) that the engine renders into a captioned, quizzed mp4. You write words and structure only;
geometry, timing, caption placement, and quiz layout are fixed in `engine/`.

Read `reference/SCENE_CONTRACT.md` (every beat field) and `reference/PRODUCTION_RULES.md` (craft) first.
Copy `examples/kitchen-academy/course/scripts/ep01.json` as your template and mirror its beat patterns.

---

## Goal
Produce a valid `course/scripts/epNN.json` whose on-screen facts all trace to `course/data/truth.json`,
that opens on a hook, teaches 2–3 concepts (each anchored by a verbatim quote), recaps, and quizzes.

---

## Spec shape

```json
{
  "id": "ep01",
  "tag": "L01",
  "slug": "knife_skills",
  "beats": []
}
```

Top-level optional fields: `num`, `title`, `subtitle` (or `families`), `synopsis`, `background`
(an `assets/backgrounds/<name>.png`), and `music` (a file in `assets/music/`). See
`schemas/episode-spec.schema.json`.

---

## Beat shape + scene types
Every beat has a `scene` plus its scene-specific fields, optional `say`, and optional `min_seconds`:

```json
{
  "scene": "concept",
  "id": "KN-1",
  "title": "Pinch Grip",
  "plain": "Pinch the blade just ahead of the handle for control.",
  "why": "It turns your wrist into a precise hinge.",
  "source": "Kitchen Academy Handbook",
  "section": "2.1",
  "say": [["APPRENTICE", "Where should my hand be?"], ["CHEF", "Pinch the blade, thumb and finger."]],
  "min_seconds": 6.0
}
```

Scene types (neutral names; legacy aliases in parens): `title`, `section`, `map`, `persona`(`guardian`),
`concept`(`control`), `quote`, `diagram`, `points`, `cheatcard`, `define`, `coldopen`, `quiz`,
`pledge`(`oath`), `notebook`. Per-field details are in `reference/SCENE_CONTRACT.md`. **Never hand-set**
`_integrity`, `_t`, `tag`, or `reveal` — the engine injects them.

---

## Rules to bake in (NON-NEGOTIABLE)
1. **Facts are sourced.** Every on-screen `id`/`title`/`quote` comes from `course/data/truth.json`. A
   `concept`/`control` `id`+`title` must match a fact; a `quote` must be a **verbatim substring** of that
   fact's `statement`, with a `cite` naming the id. `verify_facts` enforces this (phase 09).
2. **Quotes read verbatim.** On a `quote` beat the spoken `say` must equal the on-screen `quote`
   word-for-word — the source-reader never reads a truncated quote. Put the same text in both.
3. **Quizzes are interactive + read aloud.** A `quiz` beat needs `q`, `options` (2–4), `answer` (0-based
   index), and `why`. The engine auto-narrates the question, every option ("A… B… C…"), a "pause and lock
   in" prompt with think-time, then a reveal that reads the **correct answer text + the one-line why** —
   and exports normalized `opt_rects` so the player lays clickable hotspots EXACTLY on the rendered
   boxes. Do NOT write "pause" in a quiz `say` line (lint blocks the double prompt).
4. **Episode arc.** Open on a **hook** (`coldopen`/`title`); `define` jargon before use; teach **2–3
   concepts** (each a `concept` plain + why, anchored by a verbatim `quote`); then **recap**
   (`points`/`cheatcard`/`notebook`); then a **quiz**. End scenes with forward motion.
5. **Characters keep their archetype.** The learner-avatar asks novice questions (never lectures); the
   expert/mentor explains and corrects; the verbatim-source reader only reads source text. Don't have two
   characters deliver the same explanation.

---

## Author the spec
1. Copy `examples/kitchen-academy/course/scripts/ep01.json` into `course/scripts/ep01.json` and adapt it.
2. Pull every `id`/`title`/`quote`/`cite` straight from `course/data/truth.json`.
3. Set `min_seconds` generously on dense slides (`points`, `cheatcard`, `define`, `notebook`).
4. Keep section/map/title headings unique in the episode; keep titles short enough to fit (phase 09
   measures overflow).

---

## Review as TEXT with a council (cheaper than re-rendering)
Before any render, run an **adversarial multi-model council** on the script text:

- Launch several `task` agents with **different `model` values** (e.g. a GPT, a Gemini, a Claude), plus
  the `screenplay-review` skill if available. Ask each to find: factual drift from `truth.json`,
  archetype slips (a learner lecturing), word echoes across adjacent lines, dull pacing,
  weak/ambiguous quiz options, and metaphor that never maps back to reality.
- Reconcile the notes, reach **consensus**, and revise the spec before proceeding.

---

## Self-review
- Does the JSON parse, with every `scene` a valid scene type?
- Does every on-screen `id`/`title`/`quote` trace to `truth.json`, and does each `quote` `say` equal the on-screen quote?
- Are there 2–3 concepts, a hook, a recap, and — if quizzes are enabled — at least one quiz with a single clearly-correct answer?
- Are character voices distinct, with no duplicated explanations?
- Did the council reach consensus and were edits applied?

Then route to `system-prompts/09_gates.md`.
