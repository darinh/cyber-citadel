# Third-Party Notices

Cyber Citadel is produced with open, locally-run tools. Generated media in this
repo (videos, background images, music, SFX) are produced by these tools; the
creative script and designed UI are original to this project.

## Source material
- **NIST SP 800-53 Rev 5, SP 800-53B, FIPS 199/200, SP 800-37/53A/60/137** — U.S.
  Government works (generally public domain in the U.S.). Control text shown on
  screen is drawn from NIST's official **OSCAL** content
  (https://github.com/usnistgov/oscal-content). This project is an independent
  educational aid and is **not** affiliated with or endorsed by NIST.

## Models & libraries
- **Kokoro-82M** (text-to-speech) — Apache-2.0 (hexgrad/Kokoro-82M).
- **Stable Diffusion XL base 1.0** (background images) — CreativeML Open RAIL++-M
  license (stabilityai/stable-diffusion-xl-base-1.0). Backgrounds are abstract,
  text-free, and character-free.
- **piper-tts** (legacy v1 voices) — MIT.
- **ffmpeg** — LGPL/GPL; **Pillow** — HPND/MIT-style; **diffusers/transformers** —
  Apache-2.0; **PyTorch** — BSD-3-Clause.
- **Music & SFX** — Sound effects and the fallback ambient bed are synthesized
  procedurally in this repo (`tools/sfx.py`, `tools/music.py`). The orchestral
  underscore beds are by **Kevin MacLeod (incompetech.com)**, licensed
  **Creative Commons Attribution 4.0** (https://creativecommons.org/licenses/by/4.0/).
  Tracks used (mixed/mastered and ducked under narration): *Long Note Four*,
  *Ossuary 1 - A Beginning*, *Ossuary 6 - Air*, *Bittersweet*, *Dark Times*,
  *Midnight Tale*, *Strength of the Titans*. Raw tracks are not committed; they
  are baked into the rendered videos.
- **Fonts** — Segoe UI / Consolas (Microsoft), used at build time from the local
  Windows installation.

This material is provided for education. Always consult the official NIST
publications for authoritative requirements.
