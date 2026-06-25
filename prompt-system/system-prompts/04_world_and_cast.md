# 04 — World + cast → `theme.json`

Design the original course world and cast, then write `theme.json`. The theme controls creative tokens only: colors, fonts, vocabulary, groups, cast metadata, pronunciations, and voice placeholders.

---

## Goal
Turn the user’s aesthetic into an **ORIGINAL** method-of-loci world and 3–4 original characters, then validate the theme with `engine/theme.py`.

Never use franchise names, character likenesses, studios, artists, mascots, brands, or “in the style of …”. `engine/gates/lint_prompts.py` will block them later.

---

## Method-of-loci world design
Use `project.json` + `course/data/truth.json`.

1. Restate the aesthetic as an original place.
2. Map topic groups to parts of that place.
3. Choose world vocabulary labels that fit the metaphor.
4. Keep the mapping useful for memory, not just decorative.

Example: “cozy cooking academy” becomes stations, dishes, kitchen code, taste tests — not a borrowed restaurant or media property.

---

## Cast archetypes
Create 3–4 original characters:

- **Expert / mentor** — teaches confidently.
- **Learner** — asks novice questions; does not lecture.
- **Verbatim-source reader** — reads exact quotes from `truth.json`.
- **Optional antagonist / tension** — represents misconceptions, risk, or pressure.

Describe characters as primitives for later avatar prompts: silhouette, palette, 2–3 motifs, and strong negatives. Do not describe any recognizable character.

---

## `theme.json` shape
Fill these fields exactly as consumed by `engine/theme.py` and `engine/tts.py`:

```json
{
  "brand": "<COURSE BRAND>",
  "series_kicker": "AN INTERACTIVE <TOPIC> SERIES",
  "fonts": {
    "regular": "NotoSans-Regular.ttf",
    "semibold": "NotoSans-SemiBold.ttf",
    "bold": "NotoSans-Bold.ttf",
    "light": "NotoSans-Regular.ttf",
    "mono": "NotoSans-Bold.ttf"
  },
  "palette": {
    "bg_top": [14, 16, 22],
    "bg_bot": [26, 30, 40],
    "panel": [30, 35, 47],
    "panel_hi": [44, 51, 68],
    "ink": [236, 238, 244],
    "muted": [150, 158, 176],
    "accent": [120, 170, 255],
    "accent2": [255, 138, 96],
    "gold": [240, 196, 110],
    "mint": [128, 222, 178],
    "danger": [240, 110, 120],
    "violet": [176, 150, 240]
  },
  "world": {
    "stakes_label": "PROGRESS",
    "center_label": "CORE",
    "group_role_label": "GUIDE",
    "covers_label": "COVERS",
    "meaning_label": "IN PRACTICE",
    "quiz_kicker": "KNOWLEDGE CHECK · PICK YOUR ANSWER",
    "oath_label": "THE PLEDGE",
    "source_label": "<truth source name>"
  },
  "groups": {
    "order": ["<group id>"],
    "clusters": {
      "<cluster name>": {"color": "accent", "members": ["<group id>"]}
    }
  },
  "cast": [
    {"name": "NARRATOR", "role": "narrator", "caption_color": "accent", "voice": {"ref": "narrator.wav", "exaggeration": 0.5, "cfg_weight": 0.5, "temperature": 0.8}},
    {"name": "MENTOR", "role": "mentor", "caption_color": "gold", "voice": {"ref": "mentor.wav", "exaggeration": 0.6, "cfg_weight": 0.45, "temperature": 0.8}}
  ],
  "pronunciations": {},
  "spell_acronyms": []
}
```

Palette must include exactly these 12 tokens. Pick a cohesive, high-contrast scheme fitting the aesthetic; do not default to cyan/magenta unless truly apt. Ensure `ink` contrasts with `panel` and `bg_bot`.

Fonts default to vendored Noto. If using a themed font, drop the font file in `engine/assets/fonts` and reference its filename.

---

## Validate

```powershell
python engine/theme.py
```

It prints brand, accent/ink, font path, and `validation: OK` or a list of contrast/font problems.

Optional visual QA after theme exists:

```powershell
python engine/scene.py demo
```

---

## Self-review before routing
- Is every world/character original IP?
- Does the world map help memory for the actual topic groups?
- Are all 12 palette tokens present as `[r,g,b]` arrays?
- Are `groups.order` and `groups.clusters` useful for map/persona scenes, or empty for a single video?
- Does `python engine/theme.py` report no P1 problems?

Then route to `system-prompts/05_avatars.md`.
