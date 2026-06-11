---
name: avatar-expression-variants
description: >-
  Generate multiple expressions (asking, inquisitive, explaining, worried, smug, etc.) for an
  EXISTING character while keeping the exact same identity, using IP-Adapter image-conditioning on
  the character's fixed-seed base portrait. Use when a character needs expression variants for
  dialogue states. Text re-rolls do NOT hold identity — condition on the one base image.
---

# Avatar Expression Variants (IP-Adapter, same character)

Produces expression variants of an established persona that remain unmistakably the **same
character**, by conditioning on the character's base portrait (CLIP image features) and varying
only the expression in the prompt. Read `course/GENERATION_PLAYBOOK.md` §4/§4a and
`course/seed_registry.yaml` (`image_expressions`).

## Why image-conditioning (the key learning)
Re-rolling text prompts/seeds produces "different people in the same clothes." To hold identity,
derive every variant from **one fixed-seed base portrait** via **IP-Adapter** image-conditioning:
identity comes from the reference IMAGE, the prompt changes only the expression/pose. This is the
recent character-consistency workflow the user asked for.

## Environment & commands
- venv: **`.venv_img`** (SDXL + diffusers + IP-Adapter). `$env:PYTHONUTF8=1`.
- Expression variants: `.\.venv_img\Scripts\python.exe tools\gen_avatar_ipa.py [NAME ...]`
  (e.g. `NOVA VEGA`). Anchors on `course/art/avatars/raw/<NAME>.png` (from
  `base-avatar-creation`).
- Expression SHEETS (grid): `tools\gen_expression_sheet.py` (seeds VEGA 7101, NOVA 7102).
- Frame results into cards: `python tools\make_avatars.py`.

## Settings (authoritative in the tool + seed_registry)
IP-Adapter **Plus** (tencent, Apache-2.0) + h94 weights (Apache-2.0) on SDXL base (OpenRAIL++-M),
DDIM scheduler, **scale 0.72**, **seed 42**, identity from the reference image. **License-clean,
no InsightFace.** Vary only the expression text (asking a question / inquisitive / explaining /
worried / smug-for-NULL / confident, etc.) keyed to dialogue states.

## Rules (hard-won)
- **Condition on the base image**; never try to re-create identity from text alone.
- Keep scale/seed as recorded so variants are reproducible; changing them ⇒ update the tool +
  seed_registry + GENERATION_PLAYBOOK changelog.
- Stay on the established design (don't change hair/clothes/face) — same character, new expression.

## Definition of done
- Expression variants generated for the requested character(s), visibly the same person as the
  base; framed into cards; settings mirrored to seed_registry; spot-checked against the base.
