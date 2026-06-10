# Cyber Citadel — VNEXT backlog

Most of the review feedback is now DONE (see bottom). Remaining ideas for a
future pass:

## 1. Cartoon / character animation (aspirational)
- Dream goal: animated-film / cartoon-style **character animation** (lip-sync,
  motion) rather than static avatars + motion graphics. Hard to generate locally;
  revisit with dedicated animation/video models.

## 2. Fuller animated cast introduction
- A dedicated "meet the cast" sequence in EP00 with the large character portraits
  and a beat each, to establish personas even more strongly.

## 3. Optional polish
- Crossfade (xfade) transitions between beats (kept hard cuts + transition SFX for
  audio-sync safety).
- Staggered bullet reveals on dense `points` slides (currently they just hold longer).

---

## Done (review feedback addressed)
- **Pronunciation** — IDs and doc numbers now speak correctly: "AC-6" → "ay see
  six", "800-53B" → "eight hundred fifty three B" (dropped the literal "dash",
  phonetic family codes, number hyphens → spaces). `tools/tts.py`.
- **Character avatars** — anime-style portrait of the current speaker (VEGA, NOVA,
  ARCHIVIST, NULL, NARRATOR) now appears beside their subtitle (visual-novel style).
  Generated locally with SDXL (`tools/gen_avatars.py` + `make_avatars.py`),
  overlaid in `build_episode2.py`.
- **Slide pacing + depth** — dense `points`/`cheatcard` slides now hold longer
  (min time scales with bullet count) and the "Anatomy of a control" beat has
  deeper, step-by-step narration.
- **Animated** map (sequential district reveal) + diagrams (boxes pop, arrows draw)
  + kinetic title/section fade-ins.
- Fixed the "Your guides" count (three guides + the Null) and a temp-cleanup crash.

