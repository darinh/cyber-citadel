---
name: music-bed
description: >-
  Add high-quality, license-clean orchestral underscore that sits UNDER narration without
  distracting, with proper attribution. Use when scoring episodes, adding/swapping music, or
  setting per-episode mood. Covers licensing rules, mastering to duck under voice, and the
  synthesized fallback so renders never break.
---

# Music Bed (license-clean orchestral underscore)

Scores each episode with professional-sounding orchestral music **mastered to sit under
narration**. Read `course/GENERATION_PLAYBOOK.md` §6 and `THIRD_PARTY_NOTICES.md`.

## Licensing (non-negotiable)
- Permitted: **CC0 / public-domain / royalty-free / CC-BY (with attribution)**, plus locally
  generated music. **No copyrighted tracks.** Must be **high-quality orchestral and
  non-distracting** (the user's explicit bar).
- Current source: **Kevin MacLeod (incompetech.com), CC-BY 4.0** — attributed in
  `THIRD_PARTY_NOTICES.md`. Any new track must be added there with its license + author.

## Tooling & commands
- `tools/music2.py` builds the bed: `ensure_assets()` fetches the raw CC-BY tracks (into
  `tools/music_assets/`, gitignored), and `make_bed(total_seconds, out_wav, epid=...)` produces a
  per-episode bed. Per-episode mood mapping lives in `music2.py` `TRACKS`.
- It is **mastered to sit under voice**: high-pass to clear rumble, a ~3 kHz presence dip to carve
  room for narration, gentle compression so swells don't poke through, single-pass loudnorm,
  seamless crossfade-loop for short tracks, long fades in/out.
- **Ducking** happens in `build_episode2.py` (sidechain compress against narration) — the bed is
  pulled down whenever someone speaks. Music volume + duck live in the assembler's audio pass.
- **Fallback:** if a source asset is missing, it falls back to the synthesized
  `music.make_bed` so renders never break.

## Rules
- Keep the bed quiet enough that captions/narration are always clearly intelligible; verify in the
  FINAL mp4 (the bed is part of the mux the `verify_episode.py` gate transcribes).
- New track ⇒ add to `TRACKS` (mood/episode), download via `ensure_assets`, and record
  license+author in `THIRD_PARTY_NOTICES.md`. Mirror notable choices to GENERATION_PLAYBOOK.

## Definition of done
- Each episode has a mood-appropriate, ducked, loudness-matched bed; narration stays clearly
  audible in the final mp4; all sources attributed in THIRD_PARTY_NOTICES.md.
