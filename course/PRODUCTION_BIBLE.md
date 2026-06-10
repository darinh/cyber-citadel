# CYBER CITADEL — Production Bible
*The single source of truth for the NIST SP 800-53r5 video training series.*
*Concept approved (APPROVE-WITH-CHANGES) by a 5-LLM council: GPT-5.5, Gemini 3.1 Pro,*
*Claude Sonnet 4.5, ollama gpt-oss:20b, gemma3:27b. All changes below are adopted.*

---

## 1. What we are making
A binge-watchable, ~8-episode animated **video** training series (also a standalone
audio track) that teaches NIST SP 800-53 Rev 5 in a fun, memorable, and **accurate**
way. Learner prefers video/visuals. Fully local production (ollama, piper, Pillow, ffmpeg).

## 2. The world & cast
- **AEGIS CITADEL** — a fortified digital city = an information system + its organization,
  guarding the **Crown Data**. 20 control families = **20 districts/guardians** on a map
  (method-of-loci spatial memory).
- **THE NULL** — adversary collective. Threat **varies per family** and is tied to a real
  threat profile + MITRE ATT&CK technique (e.g., AU = stealthy log-wiper / T1070; PS =
  malicious insider; CP = ransomware/disaster).
- Recurring guides (piper voices):
  - **VEGA** — veteran analyst, the expert (ryan-high).
  - **NOVA** — apprentice CISO = learner's avatar; asks the learner's questions (amy).
  - **THE ARCHIVIST** — reads **verbatim** NIST text; accuracy anchor (lessac).
  - **THE NULL** — antagonist narration (hfc_male, pitched/processed).

## 3. Episode map (thematic clustering — endorsed over catalog order for retention)
| EP | Title | Families | Threat spine |
|----|-------|----------|--------------|
| 00 | The Citadel Awakens | (orientation) | The siege begins |
| 01 | The Outer Walls | AC, IA, PE | Forged identity / tailgating / break-in |
| 02 | The Watchtowers | AU, SI, IR | Stealthy intruder erasing logs; malware; breach |
| 03 | The Keepers of the Pact | AT, PS, PT | Insider, social engineering, privacy abuse |
| 04 | The High Council | RA, PL, PM, CA | Unmanaged risk / failed authorization |
| 05 | The Forge | SA, CM, MA, SR | Supply-chain implant; misconfig; rogue maintenance |
| 06 | The Vaults & Lifelines | SC, MP, CP | Interception; lost media; disaster/ransomware |
| 07 | Siege Night (finale) | all + RMF | Coordinated multi-vector assault |

All 20 families get a distinct district segment + control card + cheat sheet.
EP00 covers: FISMA/why; consolidated **security+privacy** catalog; the 20-family map;
control anatomy (ID • Control • Discussion • Enhancements • Related); **baselines live in
SP 800-53B (not here)**; tailoring/overlays; where 800-53 sits in the **RMF (SP 800-37)**;
disclaimer.

## 4. Per-episode segment budget (~8-10 min) — *controls get ≥50% of runtime*
1. Cold open / threat hook — **≤60s**
2. Layer intro + map highlight — ~30s
3. Per family: district+guardian (~20s) → purpose-translated-to-reality (~20s) →
   **2-3 flagship controls** (real ID + plain meaning + one Archivist verbatim quote
   shown on-screen) (~80-100s)
4. RMF tie-in for the layer — ~30s  *(every episode, not just finale)*
5. **Active-recall quiz** (2-3 Qs, pause-and-answer) — ~45s
6. Recap cheat card + cliffhanger — ~30s

## 5. ACCURACY RULES (unanimous #1 council priority — non-negotiable)
- **Truth layer**: all IDs/titles/statements/discussion come from `course/data/truth.json`
  (parsed from the official **OSCAL** catalog), never from loose PDF text or LLM memory.
- **On-screen real ID + title** for every control mentioned; Archivist quotes are
  **verbatim** and shown on screen in quotes with a citation (`NIST SP 800-53r5 · AC-6`).
- **Separate story from fact**: narrative is "interpretation"; on-screen text is authoritative.
  Always translate the metaphor back to real-world org meaning.
- **Baselines** = SP **800-53B** (tailoring start points), not 800-53. Say so.
- **Enhancements** exist and matter; name notable ones; cheat sheets list them.
- Use the **Discussion** section for context; don't treat it as optional.
- **Disclaimer** in EP00 + README: educational aid, not a substitute for the standard.
- **Hostile-auditor gate**: every script passes `tools/verify_script.py` (LLM checks each
  claim vs truth.json/full_text) before TTS/render; flagged items fixed.

## 6. Pedagogy (retention-first)
- Two layers: **video** = mental model + headline controls; **cheat sheets** = full flagship
  set + notable enhancements + RMF mapping + assessment questions (depth/coverage).
- **Quizzes** per episode + a final **"Guardian Roll Call"** 20-question quiz.
- RMF mapping in every episode; "why these controls"; brief implementation pitfalls.

## 7. Production pipeline (local)
- **Scene engine** (`tools/scene.py`, Pillow): a small set of declarative **scene types**
  (title, map, character-dialog, control-card, archivist-quote, diagram, quiz, cheat-card,
  lower-third). Pre-render crisp 1920x1080 stills.
- **Motion** via ffmpeg `zoompan`/`fade`/`xfade`/`overlay` (Ken Burns), not bespoke frames.
- **TTS** (`tools/tts.py`, piper): pronunciation pre-processor for acronyms/IDs
  (NIST→"nisst", CISO→"sisso", AC→"A C", 800-53→"eight hundred dash fifty-three"),
  per-line WAV, loudness-normalized, silence padding, timings → **SRT captions**.
- **Music**: locally synthesized ambient bed (no copyrighted audio).
- **Assembler** (`tools/build_episode.py`): episode spec (JSON) → scenes + narration →
  timed mp4 with burned captions + music + sidecar .srt.
- **Episode spec**: `course/scripts/epNN.json` (lines, speaker, scene directions, on-screen text).

## 8. Deliverables
`course/episodes/epNN_*.mp4` + `.srt`; `course/scripts/epNN_*.{json,md}`;
`course/cheatsheets/*.png|pdf` (20 families + master); `course/art/` (map, characters);
`course/quizzes/`; `index.html` player; `README.md`; `.github/copilot-instructions.md`.

## 9. Council protocol & gates
- [x] R1 PLAN — 5 LLMs, consensus APPROVE-WITH-CHANGES (this bible adopts all changes).
- [ ] R2 SCRIPTS — pilot scripts pass hostile-auditor + multi-LLM review.
- [ ] R3 PILOT — EP00 rendered; storyboard/transcript/frames reviewed.
- [ ] R4 FINAL — full package reviewed.
Adversarial review with multiple agents + LLMs; proceed only on consensus.
