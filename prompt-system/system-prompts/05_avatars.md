# 05 — Avatars → `assets/avatars/<NAME>.png`

Create optional cast portraits, tier-aware. If avatars are not opted in, skip this phase; the renderer can omit the corner portrait and the course still works.

---

## Goal
For each character in `theme.json.cast[]`, produce a framed, roughly square bust portrait:

```text
assets/avatars/<NAME>.png
```

Use names that match `cast[].name` where practical.

---

## 1 — Read the tier

```powershell
python engine/probe.py
```

Read `capabilities.json`:

- `sdxl_ipa` — CUDA + 10GB VRAM: SDXL fixed-seed bases + IP-Adapter expression variants.
- `sd_turbo` — CUDA + 4GB VRAM: few-step static portraits; no IP-Adapter.
- `illustrated` — CPU-only/no diffusion: deterministic illustrated/geometric fallback or BYO images.

GPU is optional. Degrade gracefully; do not block the course on portraits.

---

## Original IP prompt rules
Build character descriptions from primitives:

- silhouette,
- palette,
- 2–3 motifs,
- expression/pose,
- material/lighting,
- strong negative prompt.

Required negative prompt concept:

```text
trademark, logo, copyrighted character, mascot, franchise, recognizable celebrity, brand, named studio, named artist style
```

Never use franchise names, character names, studio names, celebrity likenesses, mascots, logos, or “in the style of <artist>”. Run:

```powershell
python engine/gates/lint_prompts.py
```

---

## GPU tier: `sdxl_ipa`
Use SDXL for fixed-seed base portraits. Create expression variants with IP-Adapter image conditioning so identity stays anchored to the base portrait.

Process:

1. Write one base prompt per character from original primitives.
2. Choose and record a fixed seed for each base portrait.
3. Generate the base bust portrait.
4. Generate expression variants from the base image via IP-Adapter, not text-only re-roll.
5. Frame/export the default portrait as `assets/avatars/<NAME>.png`.

If `engine/gen_avatars.py` or related avatar tools are present, prefer them over hand scripts.

Record seeds/prompts in the project’s seed registry if one exists, for example:

```json
{"avatars":{"MENTOR":{"tier":"sdxl_ipa","seed":123456,"prompt":"<original primitive prompt>","negative":"<negative prompt>"}}}
```

Do not invent engine fields.

---

## Low-VRAM tier: `sd_turbo`
Use SD-Turbo or SD1.5 few-step static portraits.

Rules:

- Static portraits are fine.
- Do not attempt IP-Adapter identity variants.
- Use fixed seeds when possible.
- Export `assets/avatars/<NAME>.png`.

---

## CPU-only tier: `illustrated`
Use either:

1. Deterministic illustrated/geometric portraits using `theme.json` colors and motifs.
2. Bring-your-own license-clean images supplied by the user.

For BYO images, copy/resize/frame them into `assets/avatars/<NAME>.png`. Do not use copyrighted character art.

---

## Quality bar
- Square or near-square bust portrait.
- Clear silhouette at small size.
- Matches the original world palette.
- No logos, text, watermarks, franchise cues, or celebrity likenesses.
- Character identities are distinct.
- File names match cast names.

---

## Self-review
- Were avatars opted in?
- Did you use the correct tier from `capabilities.json`?
- Did `python engine/gates/lint_prompts.py` pass?
- Are exports under `assets/avatars/`?
- If diffusion was used, are fixed seeds/prompts recorded durably?

Then route to `system-prompts/06_voices.md`.
