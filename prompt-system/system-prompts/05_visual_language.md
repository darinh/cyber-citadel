# 05 — Visual language, media plan, and optional cast

Create `theme.json` and `assets/media.json` from the learning blueprint. A coherent visual identity
does not mean one repeated slide. The treatment changes with the learning task while typography,
palette, captions, and motion remain consistent.

Read `reference/VISUAL_LANGUAGE.md`, `reference/SCENE_CONTRACT.md`,
`schemas/theme.schema.json`, and `schemas/media-manifest.schema.json`.

## Choose treatment by instructional need

| Learner must perceive or do | Prefer |
|---|---|
| Recognize appearance or context | Relevant sourced/original `image` |
| Operate software or inspect a UI | `screenshot` with normalized callouts |
| Perform a physical/software procedure | Muted narrated `video` demonstration or screenshot sequence |
| See change over time | Animated `timeline`, `process`, chart, or source clip |
| Understand relationships/structure | `diagram` or `process` |
| Compare examples, non-examples, or choices | `comparison` |
| Interpret quantity or trend | `chart` sourced to truth facts |
| Follow expert reasoning | `worked_example`, then a faded/independent `practice` |
| Retrieve or decide | Interactive `quiz` or pause-and-do `practice` |
| Read exact source language | Short `quote`, used sparingly |

Never add a picture merely to break up text. Never put dense prose on screen and narrate the same
prose, except for a deliberately read verbatim quote. Use signaling—callouts, contrast, progressive
reveal—to direct attention to the exact feature being explained.

## `theme.json`

For direct instruction, use one narrator and no fictional world:

```json
{
  "brand": "DATA IN PRACTICE",
  "series_kicker": "A PRACTICAL VIDEO LESSON",
  "fonts": {
    "regular": "NotoSans-Regular.ttf",
    "semibold": "NotoSans-SemiBold.ttf",
    "bold": "NotoSans-Bold.ttf",
    "light": "NotoSans-Regular.ttf",
    "mono": "NotoSans-Bold.ttf"
  },
  "palette": {
    "bg_top": [14,16,22], "bg_bot": [24,28,36], "panel": [34,39,50],
    "panel_hi": [50,57,72], "ink": [240,242,246], "muted": [166,174,190],
    "accent": [112,164,244], "accent2": [239,157,91], "gold": [238,195,104],
    "mint": [126,210,170], "danger": [232,105,119], "violet": [173,149,235]
  },
  "visual": {"background_style":"clean","chrome":"minimal","image_tint":0.18},
  "cast": [
    {"name":"NARRATOR","role":"narrator","caption_color":"accent",
     "voice":{"ref":"narrator.wav","exaggeration":0.5,"cfg_weight":0.5,"temperature":0.8}}
  ],
  "pronunciations": {},
  "spell_acronyms": []
}
```

Only add `world`, groups, fictional cast, or avatars when the blueprint enables narrative. Original-IP
rules still apply.

## `assets/media.json`

Every image or clip gets a stable key and complete provenance:

```json
{
  "schema_version": "2.0",
  "assets": {
    "dashboard-example": {
      "path": "assets/media/dashboard.png",
      "kind": "image",
      "origin": "original",
      "license": "Original course asset",
      "creator": "Course team",
      "source_url": "",
      "credit": "",
      "fact_ids": ["F-CHART-1"],
      "alt": "A weekly line chart with one isolated spike."
    }
  }
}
```

Use `fact_ids` whenever a visual itself contains values, labels, events, or other factual claims.
Use only original, generated-original, public-domain, CC0, CC-BY, or explicitly licensed media.
Record generation tool/model/prompt/seed for generated visuals. Never hallucinate a path: download or
create the asset, open it, and verify the callout coordinates against the real image.

## Optional avatars

If and only if `project.json.options.avatars` is true and a cast serves the learning design, use
`engine/gen_avatars.py`. SDXL remains the high-quality default on GPU or CPU; any downgrade still
requires explicit approval. A direct narrator does not need an avatar.

Run `python engine/theme.py`, `python engine/gates/lint_prompts.py`, and
`python engine/scene.py demo`, then continue to `06_voices.md`.
