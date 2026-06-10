# CONCEPT PROPOSAL FOR COUNCIL REVIEW
## "CYBER CITADEL: The 20 Guardians" — a video training series for NIST SP 800-53 Rev 5

### The ask
Make a 492-page federal security-controls catalog **fun, memorable, and
genuinely educational** as a **binge-watchable video series** with strong
visuals + multi-voice narration (also enjoyable audio-only). Must be accurate,
not dumbed-down-wrong. Learner prefers video/visuals.

### Creative framing
The information system + its organization is dramatized as **AEGIS CITADEL**, a
fortified digital city-state guarding the **Crown Data**. It is under siege by
**THE NULL**, an adversary collective embodying every threat 800-53 defends
against (external attackers, malicious insiders, accidents, environmental
hazards, supply-chain saboteurs). The 20 control families are the **20 districts
/ guardians** of the city. Spatial memory (a city map of 20 districts) anchors
recall of the 20 families.

### Recurring cast (voices = piper neural voices)
- **VEGA** — veteran SOC analyst / castellan's advisor. The expert. (ryan-high)
- **NOVA** — newly-appointed apprentice CISO; the learner's avatar; asks the
  questions a learner would. (amy / jenny)
- **THE ARCHIVIST** — dry keeper of the catalog who reads short *authentic* NIST
  control text aloud → keeps the series truthful. (lessac / hfc_male)
- **THE NULL** — antagonist narrating each attack. (processed hfc_male / libritts)

### Episode lineup (Season 1 — 22 episodes)
- **EP00 "The Citadel Awakens"** — what 800-53 is; FISMA/why it exists; the
  consolidated security+privacy catalog; control structure (ID, control,
  discussion, enhancements, related); baselines moved to 800-53B; where it sits
  in the RMF (800-37); meet the cast + The Null; reveal the 20-district map.
- **EP01–EP20 — one family per episode**, in catalog order: AC, AT, AU, CA, CM,
  CP, IA, IR, MA, MP, PE, PL, PM, PS, PT, RA, SA, SC, SI, SR. Each ~6–9 min:
  1. Cold open: "Breach of the Week" — The Null attempts an attack this family
     defends against.
  2. Meet the Guardian: the family personified + its purpose (what it protects).
  3. The real controls: 3–5 flagship controls with accurate IDs/titles + plain
     meaning; Archivist reads one short authentic snippet.
  4. Connections: related families / defense-in-depth placement.
  5. Mnemonic + on-screen cheat card for retention.
  6. Cliffhanger tying to the season arc.
- **EP21 "Siege Night" (finale)** — The Null launches a coordinated multi-vector
  assault; the 20 guardians interlock (defense in depth); the RMF lifecycle
  (categorize→select→implement→assess→authorize→monitor) is shown operationally;
  wrap-up on how to actually use 800-53 + 800-53B in real life.

### Visual style (built with Pillow + ffmpeg, fully local)
Neon-on-dark "cyber-castle" motion-graphics explainer. Per episode: animated
title card, district highlight on the city map, character cards, control cards
showing real IDs, simple animated diagrams (access gates, data flows, audit
trails), kinetic captions synced to narration, closing cheat-sheet card.
Motion via ken-burns/zoom/slide + crossfades; burned-in captions + sidecar SRT.
Locally-synthesized ambient music bed (no copyrighted audio). Optional stretch:
local Stable Diffusion hero art (fallback = designed graphics).

### Why this should work pedagogically
- Spatial + narrative memory (districts, guardians, recurring villain).
- "Breach of the Week" makes each family's *purpose* concrete and memorable.
- Archivist's authentic snippets keep accuracy; mnemonics + cheat cards aid recall.
- Multimodal: video + audio + captions; the audio track stands alone as a podcast.

### Deliverables (in this folder)
- `course/episodes/epNN_*.mp4` (the series) + `.srt`
- `course/scripts/epNN_*.md` (full transcripts/scripts)
- `course/art/` + `course/cheatsheets/` (map, character cards, per-family one-pagers, master cheat sheet)
- `index.html` course player; `README.md`; `.github/copilot-instructions.md`

### Open questions for the council
1. Scope/feasibility: 22 episodes is large. Approve a "build a templated pipeline,
   polish EP00 + 2 pilot family eps, then batch-produce the rest" approach?
2. Is the Citadel framing the strongest choice, or is a different metaphor
   (heist serial / late-night "Control Room" talk show / academy) more memorable?
3. Accuracy guardrails: is "Archivist reads authentic snippets + on-screen real
   control IDs" sufficient to keep it trustworthy while staying fun?
4. Biggest risks to call out now (technical or pedagogical)?
5. TTS: piper local multi-voice (chosen for offline/local) vs. higher-quality
   edge-tts (online) — acceptable to stay fully local with piper?

### Verdict requested
Reply with: APPROVE / APPROVE-WITH-CHANGES / REJECT, your top 3–5 highest-signal
improvements, and the single biggest risk. Be specific and critical; do not
rubber-stamp. Do NOT modify any files — this is a review only.
