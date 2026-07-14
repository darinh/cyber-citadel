# Attribution and Licensing

The engine is portable because course assets stay license-clean.

## Music
Music is **never generated**. Use only:
- CC0 music.
- Public-domain music.
- CC-BY music with attribution.

Good sourcing starting points:
- Kevin MacLeod / Incompetech (`incompetech.com`) for CC-BY tracks.
- Free Music Archive for license-filtered tracks.
- Musopen for public-domain classical recordings and scores.
- ccMixter for Creative Commons tracks.

Place approved source tracks in `assets/music/`. If no track is configured, the engine renders a silent bed.

## CC-BY attribution
CC-BY requires attribution in `THIRD_PARTY_NOTICES.md`. Template:

```markdown
- "Track Title" by Artist Name, source URL, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes: looped, EQ/compression/loudness normalization, fades.
```

Include the exact license version and source URL. If the license requires additional wording, include it.

## Fonts, SFX, images, and source video
- Vendored Noto Sans fonts are licensed under the SIL Open Font License.
- SFX are self-contained engine assets; do not replace them with unlicensed sound libraries.
- Images, avatars, logos, screenshots, and video clips must be original or explicitly licensed for reuse.
- Register every image/clip in `assets/media.json` with origin, license, creator, source URL where
  applicable, credit, alt text, and represented truth `fact_ids`.
- Generated-original visuals record tool, model, prompt, and seed.
- Do not use protected characters, trademarks, celebrity likenesses, named fictional places, studio marks, or “in the style of” a living artist.
## Music intake checklist
- Save the original source URL.
- Save the title, creator, license name, and license URL.
- Confirm commercial reuse and derivative processing are allowed.
- Record any changes such as looping, fades, EQ, compression, or loudness normalization.
- Keep a copy of the license text or source page when practical.

## Do not use
- Unclear “royalty free” downloads without a license.
- Streaming-platform rips.
- Game, film, television, or brand soundtrack material.
- Sound-alike prompts or generated songs.
- Images that imitate protected characters, logos, trade dress, or celebrity likenesses.
