# 05 — Avatars → `assets/avatars/<NAME>.png`

Create optional cast portraits, **high quality by default (SDXL, GPU or CPU)**. If avatars are not opted in, skip this phase; the renderer omits the corner portrait and the course still works.

---

## Goal
For each character in `theme.json.cast[]`, produce a framed, roughly square bust portrait:

```text
assets/avatars/<NAME>.png
```

Use names that match `cast[].name` where practical.

---

## 1 — Avatar quality (SDXL by default, on GPU or CPU)
The default is **SDXL** original portraits — highest quality — and SDXL **runs on CPU too** (slower,
one-time). Read `capabilities.json.speed`: if `slow` (CPU), warn the user that portrait generation
will take a few minutes but stays full quality.

`engine/gen_avatars.py` defaults to SDXL and does NOT auto-downgrade. Downgrades are opt-in **only with
the user's approval**:
- `CC_AVATARS=turbo` — SD-Turbo few-step portraits (faster, lower fidelity).
- `CC_AVATARS=illustrated` — instant geometric Pillow portraits (no model download).

If the SDXL dependencies aren't installed, `gen_avatars.py` **fails loud** with install guidance — do
not silently switch to illustrated; install the deps (they run on CPU) or get the user's OK for a
downgrade. Avatars are optional — you may also skip them entirely (the renderer omits the portrait).

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

## Default: SDXL (high quality, GPU or CPU)
`engine/gen_avatars.py` reads your theme cast and produces one **fixed-seed base portrait** per
character from original primitives + a strong negative prompt. This is the default on every machine.

Process:

1. Add an `art` block per character in `theme.json`: `{ "seed": <int>, "description": "<original primitives: silhouette, palette, 2-3 motifs>" }`, plus an optional theme-level `"art_style"`.
2. Run `python engine/gen_avatars.py` — it writes `assets/avatars/<NAME>.png` for each character. Record the seeds you keep. (On CPU this is slow but full quality; warn the user.)
3. (Optional, advanced) For per-dialogue expression variants, image-condition on the fixed base portrait with IP-Adapter so identity stays anchored — a manual enhancement, not produced automatically by `gen_avatars.py`.

Record seeds/prompts durably (e.g. a project seed registry):

```json
{"avatars":{"MENTOR":{"seed":123456,"prompt":"<original primitive prompt>","negative":"<negative prompt>"}}}
```

Do not invent engine fields.

---

## Approved downgrades only (never automatic)
Apply these **only if the user asks to trade quality/speed** — set the env var, then rerun `gen_avatars.py`:
- **`CC_AVATARS=turbo`** — SD-Turbo/SD1.5 few-step static portraits (faster, lower fidelity). Use fixed seeds; export `assets/avatars/<NAME>.png`.
- **`CC_AVATARS=illustrated`** — instant deterministic geometric portraits from `theme.json` colors/motifs (no model). Also the path for **bring-your-own** license-clean images: copy/resize/frame them into `assets/avatars/<NAME>.png` (never copyrighted character art).

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
- Did you use the default high-quality SDXL path (or a user-approved `CC_AVATARS` downgrade)?
- Did `python engine/gates/lint_prompts.py` pass?
- Are exports under `assets/avatars/`?
- If diffusion was used, are fixed seeds/prompts recorded durably?

Then route to `system-prompts/06_voices.md`.
