# Cyber Citadel — a fun, interactive video course on NIST SP 800-53 & the RMF

**Cyber Citadel** turns NIST Special Publication 800-53 Revision 5 — and the wider
**Risk Management Framework** ecosystem — into a binge-watchable, **12-episode
interactive video course** with multi-voice narration, on-screen control cards,
diagrams, **pause-and-answer quizzes**, and printable cheat sheets.

It dramatizes an information system as a fortified digital city, **Aegis Citadel**,
guarding the *Crown Data* against an adversary collective, **The Null**. The 20
control families become 20 districts / guardians (Act I); Act II — "The Campaign" —
shows how you actually stand a system up under the RMF.

> **Start here:** open **`watch.html`** for the **interactive player** (it pauses at
> each quiz so you can answer and tracks your score), or **`index.html`** for the
> course home with the cheat-sheet gallery.

## Watch order
### Act I — The Twenty Guardians (the 800-53 catalog)
| EP | Title | Covers | What you'll learn |
|----|-------|--------|-------------------|
| 00 | The Citadel Awakens | orientation | What 800-53 is, FISMA, how to read a control, baselines → 800-53B, the RMF |
| 01 | The Outer Walls | AC · IA · PE | Access, identity, and physical security |
| 02 | The Watchtowers | AU · SI · IR | Audit, system integrity, incident response |
| 03 | The Keepers of the Pact | AT · PS · PT | Training, personnel security, privacy/PII |
| 04 | The High Council | RA · PL · PM · CA | Risk, planning, program mgmt, assessment & authorization |
| 05 | The Forge | SA · CM · MA · SR | Acquisition, configuration, maintenance, supply chain |
| 06 | The Vaults & Lifelines | SC · MP · CP | Comms protection, media protection, contingency |
| 07 | Siege Night | all 20 + RMF | Act I finale: defense in depth, the RMF at a glance |
### Act II — The Campaign (the RMF ecosystem)
| EP | Title | Covers | What you'll learn |
|----|-------|--------|-------------------|
| 08 | The Campaign: the RMF | SP 800-37r2 | The 7-step Risk Management Framework + the NIST document family |
| 09 | Know Your Realm | FIPS 199/200 · 800-60 | Security categorization, the C-I-A high-water mark, minimum requirements |
| 10 | The Armory: Baselines | SP 800-53B | Low/Moderate/High/Privacy baselines and how to tailor them |
| 11 | The Reckoning | SP 800-53A · 800-137 | Assessment methods, the SAR & POA&M, authorization (ATO), continuous monitoring |

Family episodes follow the same rhythm: a cold-open threat → meet the guardian →
2–3 real flagship controls (with a **verbatim** quote read by *The Archivist*) →
how it fits the RMF → a **pause-and-answer** quiz → a cheat card.

## What's in this folder
- `watch.html` — the **interactive course player** (pauses at quizzes, tracks score).
- `index.html` — the course home (videos + cheat-sheet gallery + quiz bank).
- `course/episodes/` — the rendered `.mp4` episodes + `.srt`/`.vtt` captions + `*.cues.json` (interactive markers).
- `course/cheatsheets/` — one printable PNG per family (+ a master map).
- `course/transcripts/` — full transcripts per episode.
- `course/scripts/` — the episode specs (JSON) the renderer builds from.
- `course/quizzes.json` — every quiz question + answer.
- `course/data/` — the OSCAL catalog + 800-53B baseline profiles and the derived **truth layers**.
- `tools/` — the local production pipeline (see below).
- `course/PRODUCTION_BIBLE.md` — the full creative + technical spec.

## Accuracy
This is an **educational aid, not a substitute for the standard.** To keep it honest:
- Every on-screen control **ID, title, and Archivist quote** is pulled from NIST's
  official **OSCAL** catalog (`course/data/truth.json`) and checked by a deterministic
  gate (`tools/verify_script.py`) — quotes are verified **verbatim**.
- Narration was adversarially fact-checked by multiple LLMs.
- The story is fictional; the control text on screen is real. Baselines (Low/Moderate/
  High) live in **SP 800-53B**, not 800-53. Always consult the source for real decisions.

## How it was made (fully local pipeline)
- **Content:** parsed the official OSCAL 800-53r5 catalog → `truth.json`, and the
  official 800-53B baseline profiles → `baselines.json` (real Low/Mod/High/Privacy counts).
- **Voices:** [Kokoro-82M](https://github.com/hexgrad/kokoro) neural TTS (Apache-2.0) —
  5 distinct character voices with per-character mastering (EQ, de-ess, compression,
  reverb, −16 LUFS loudness); *The Null* uses rubberband pitch-shifting. An acronym/ID
  pronunciation pre-processor keeps "AC-6" and "800-53" speakable.
- **Sound design:** procedural SFX (`tools/sfx.py`) + a locally-synthesized music bed
  that **ducks under speech**.
- **Visuals:** a Pillow scene engine (`tools/scene.py`) → ffmpeg Ken-Burns motion,
  per-speaker-colored burned captions; quizzes have a **countdown** then a delayed reveal.
- **Interactivity:** each render emits `epNN.cues.json`; `watch.html` uses it to pause
  at quizzes and let you answer.
- **Review:** plan + pilot + every script reviewed by a council of multiple agents and
  LLMs (GPT-5.5, Gemini 3.1 Pro, Claude Sonnet/Opus, local gpt-oss / gemma3).

### Regenerate
```powershell
$env:PYTHONIOENCODING='utf-8'   # so the checkmark/quotes print on Windows consoles
# 1. (once) install deps, place the OSCAL catalog, then build the truth layer
python -m pip install piper-tts Pillow numpy pypdf
#    download course/data/oscal_catalog.json from usnistgov/oscal-content, then:
python tools/build_truth.py
# 2. author/verify a spec  (specs live in tools/episodes_src/*.py)
python tools/episodes_src/ep01.py ; python tools/verify_script.py course/scripts/ep01.json
# 3. render an episode (or tools/render_all.py for all)
python tools/build_episode.py course/scripts/ep01.json
# 4. rebuild cheat sheets + the player (package.py runs a link check)
python tools/cheatsheets.py ; python tools/package.py
```
Requires Python 3.11+, `piper-tts`, `Pillow`, `numpy`, and `ffmpeg` on PATH, plus the
piper voices in `tools/voices/` (`python -m piper.download_voices <voice> --data-dir tools/voices`).

---
*NIST publications are U.S. Government works. This fan-made course is an independent
educational aid and is not affiliated with or endorsed by NIST.*
