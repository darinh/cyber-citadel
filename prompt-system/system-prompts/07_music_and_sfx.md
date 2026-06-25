# 07 — Music & SFX → `assets/music/*` (SOURCED beds; SFX bundled)

Add a license-clean orchestral/underscore bed that sits UNDER the narration. The engine loops, masters,
and ducks it automatically — you only **source** the file, **attribute** it, and **point** the
theme/spec at it. SFX are already bundled; nothing to source there.

Music is **opt-in**. With no track configured the render still succeeds with a silent bed — a valid,
shippable outcome. Never block a course on music.

---

## Goal
For each episode, give the engine a real, license-clean source track in `assets/music/` and wire it via
`theme.json` or the episode spec. CC-BY tracks get an attribution line in `THIRD_PARTY_NOTICES.md`.

---

## Golden rule
Music is **SOURCED**, never generated. Use only **CC0 / public-domain / CC-BY** (CC-BY requires
attribution). Generated/AI music is forbidden — low quality and license-murky. SFX are bundled,
license-clean engine assets.

---

## Find license-clean tracks
Pick an instrumental mood per episode (calm, tense, triumphant…) — no vocals to fight the narration.
Confirm the license on the track's OWN page. Good sources:

- `incompetech.com` — Kevin MacLeod, mostly **CC-BY** (attribution required).
- `musopen.org` — **public-domain** classical recordings/scores.
- `freemusicarchive.org` — filter to **CC** licenses.
- `ccmixter.org` — **CC** tracks.

Avoid vague "royalty-free" downloads, streaming rips, and any film/game/TV/brand music
(`reference/ATTRIBUTION_AND_LICENSING.md` → "Do not use").

---

## Download into `assets/music/`
This folder is the project root. Keep a clear filename:

```powershell
New-Item -ItemType Directory -Force assets\music | Out-Null
curl.exe -L -o assets\music\calm_underscore.mp3 "<TRACK_DOWNLOAD_URL>"
```

mp3 / ogg / wav / flac all work (ffmpeg reads them).

---

## Wire the track
Map moods in `theme.json` (preferred for a course) OR set one per spec:

```json
{ "music": { "tracks": { "ep01": "calm_underscore.mp3" }, "default": "calm_underscore.mp3" } }
```

```json
{ "id": "ep01", "music": "calm_underscore.mp3", "beats": [] }
```

Selection order (`engine/music.py`): spec `music` → theme `music.tracks[epid]` → theme `music.default`
→ **silent bed**. Filenames resolve inside `assets/music/`; an absolute path also works. Optional
`"music_offset": <seconds>` on the spec skips an intro.

---

## Mastering is automatic — do NOT pre-process
On render the engine loop-extends the track (seamless crossfade), high-passes it, dips ~3 kHz to carve
room for the voice, compresses, loudness-normalizes, fades, and **ducks it under narration** via
sidechain compression. Your job is only to source + attribute.

---

## Attribute CC-BY (REQUIRED)
Public-domain / CC0 need no credit; **CC-BY MUST be credited** or you cannot ship. Append one line per
track to `THIRD_PARTY_NOTICES.md` at the project root:

```markdown
- "Track Title" by Artist Name, <source URL>, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes: looped, EQ/compression/loudness normalization, ducked, fades.
```

Use the exact license version + the track's source URL. Record title/creator/license/URL even for CC0
(see the "Music intake checklist" in `reference/ATTRIBUTION_AND_LICENSING.md`).

---

## SFX — nothing to source
Transition/scene SFX (whoosh, boom, sting, chime, riser, rumble, click, sparkle) are bundled in
`engine/assets/sfx/` and applied automatically per scene type, ducked under narration. Do not add,
source, or wire SFX, and do not replace them with unlicensed sound libraries.

---

## Self-review
- Is every wired track verifiably CC0 / public-domain / CC-BY?
- Does each referenced filename actually exist in `assets/music/`? (A missing file silently falls back to silence.)
- Does `python engine/music.py 20 ep01` print the source you intended (or `NONE -> silent`)?
- Does every CC-BY track have a `THIRD_PARTY_NOTICES.md` line with license version + source URL?
- Does `python engine/gates/lint_prompts.py` still PASS?

Then route to `system-prompts/08_script.md`.
