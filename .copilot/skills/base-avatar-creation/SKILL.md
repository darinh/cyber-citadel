---
name: base-avatar-creation
description: >-
  Create the canonical fixed-seed base character portraits for a narrated course with SDXL, so
  every episode shows the SAME character beside their dialogue. Use when establishing a cast,
  adding a new character, or regenerating base portraits. Identity is anchored by fixed seeds +
  a shared style; do not re-roll established characters.
---

# Base Avatar Creation (fixed-seed SDXL portraits)

Establishes each persona's canonical look as a **fixed-seed** SDXL bust portrait. These base
images are the identity anchor that `avatar-expression-variants` conditions on, so the character
stays the SAME across expressions and episodes. Read `course/GENERATION_PLAYBOOK.md` §4 and
`course/seed_registry.yaml` (`image_base`) for the authoritative seeds/prompts.

## Environment
- venv: **`.venv_img`** (SDXL / diffusers). 4090 GPU. `$env:PYTHONUTF8=1`.
- Run: `.\.venv_img\Scripts\python.exe tools\gen_avatars.py`
- Output: `course/art/avatars/raw/<NAME>.png` → framed into cards by
  `python tools\make_avatars.py` → `course/art/avatars/<SPEAKER>.png` (RGBA, used as the overlay
  beside the speaker's subtitle).

## Identity = fixed seed + shared style (do not drift)
`tools/gen_avatars.py` `CHARS` holds one **fixed seed + description** per persona, plus a shared
`STYLE` (anime bust, clean cel shading, dramatic rim lighting, dark-teal studio bg, single
character, looking at viewer) and `NEG`. Authoritative seeds (mirror in seed_registry):
- VEGA 1101 · NOVA 1102 · ARCHIVIST 1103 · NULL 1104 · NARRATOR 1105 (a NULL "bruiser" seed 1144
  was tried and **rejected** — keep the seed-1104 hooded design).
Casting facts that must hold: ARCHIVIST is a **young British female**; NOVA is **young/new**;
NULL is the hooded antagonist.

## Rules (hard-won)
- **Keep seeds fixed.** Re-rolling text/seeds yields "different people in the same clothes." The
  user explicitly wants the **exact same character** every time.
- **Don't restyle established characters** without sign-off; casting is a user decision.
- Change a seed/prompt/STYLE/NEG ⇒ update `gen_avatars.py` AND `seed_registry.yaml` AND the
  GENERATION_PLAYBOOK changelog in the same change.
- For a NEW character: add a `CHARS` entry with a new fixed seed + description in the shared STYLE,
  generate, frame, and record the seed. Then create expressions via `avatar-expression-variants`.

## Definition of done
- `course/art/avatars/raw/<NAME>.png` generated at the recorded seed; framed card in
  `course/art/avatars/<SPEAKER>.png`; seeds/prompts mirrored to seed_registry; spot-checked that
  the character matches prior episodes.
