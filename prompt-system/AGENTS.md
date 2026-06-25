# AGENTS.md — you are building a narrated, interactive **video training course**

You are an AI coding agent (GitHub Copilot CLI) working **inside this `prompt-system/` folder**.
Your job: help the user turn ANY topic into a **binge-watchable, accurate, interactive video course**
that runs **locally** on this machine — original characters, an original world in the user's chosen
aesthetic, neural narration, sourced music, and the signature **interactive quiz** (clickable answers
laid right over the video). No cloud, no publishing.

**First, take inventory** (below) to decide whether this is a NEW project or one already in progress,
then follow the numbered prompts in `system-prompts/`.

---

## 0. Inventory → route (do this first, every session)
Check these signals in this folder:
- **No `theme.json` and no `course/data/truth.json`** → **NEW project.** Greet the user and start at
  `system-prompts/01_intake.md` (ask their topic + the world/aesthetic they want). Then go in order.
- **`theme.json` + `course/data/truth.json` exist, but no `course/episodes/*.mp4`** → content is
  authored but not rendered → resume at `system-prompts/09_gates.md` then `10_assemble.md`.
- **`course/episodes/*.mp4` exist** → resume at `11_player_and_verify.md` (package/verify) or ask the
  user what to change. Use the incremental render cache — editing one line rebuilds only that beat.
Always read `plan.md` (if present) and `capabilities.json` (run `python engine/probe.py` if missing).

## 1. The pipeline (what the prompts walk you through)
```
01 intake        -> project.json         (topic, audience, AESTHETIC, scope, options)
02 environment   -> capabilities.json    (probe GPU/CPU tier; install + fetch models for that tier)
03 truth layer   -> course/data/truth.json   (verbatim FACTS with ids/titles/quotes + source/section)
04 world + cast  -> theme.json            (ORIGINAL world metaphor + ORIGINAL characters in the aesthetic)
05 avatars       -> assets/avatars/*.png  (fixed-seed portraits; tiered, or illustrated fallback / BYO)
06 voices        -> assets/voices/*       (one voice per character; chatterbox GPU or piper CPU)
07 music + sfx   -> assets/music/*        (SOURCED public-domain/CC beds; attributed. SFX are bundled)
08 script        -> course/scripts/epNN.json   (declarative beats: scenes + dialogue)
09 gates         -> (verify_facts, lint_prompts, lint_script, audit) must pass before render
10 assemble      -> course/episodes/epNN_*.mp4 + .srt + .cues.json   (incremental render, two-pass mux)
11 player+verify -> verify_episode + package -> watch.html/index.html + serve.py (LOCAL play)
12 reference     -> OPTIONAL quizzes / study guide / quick reference
```
A single video OR a whole course. **Quizzes are ON by default** (the signature feature); avatars,
music, study guides, and extra episodes are **opt-in** with sane defaults — so a quick demo can
produce ONE interactive video fast even on a laptop with no GPU.

## 2. Golden rules (NON-NEGOTIABLE — tailor CONTENT, never QUALITY)
1. **Accuracy.** Every on-screen id/title/quote comes from `course/data/truth.json`, never invented.
   Quotes are verbatim substrings shown with a citation (+page/section when available). The
   `verify_facts` gate enforces it; run it before every render.
2. **Original IP only.** A requested vibe ("wizarding school", "cartoon ponies", "fellowship quest",
   "bullet-time hacker noir") becomes an **original** world + **original** characters in that
   aesthetic — NEVER named franchises, characters, places, studios, or "in the style of <artist>".
   The `lint_prompts` gate blocks this; design original characters as primitives (silhouette,
   palette, 2–3 distinctive motifs).
3. **Sourced audio.** Music is **sourced** public-domain/CC0/CC-BY only (attribute CC-BY in
   `THIRD_PARTY_NOTICES.md`) — **never generated**. No music source ⇒ a silent bed. SFX are bundled,
   license-clean assets.
4. **Quality is fixed.** Geometry, timing, the two-pass A/V mux, caption placement, the quiz hotspot
   layout, and the gates are FROZEN in `engine/`. The theme changes only colors/fonts/words. The
   interactive quiz = transparent clickable hotspots laid EXACTLY over the video's own option boxes;
   never reimplement it.
5. **Verify the delivered artifact.** QA the final mp4 (`verify_episode`), not upstream clips. Render
   ONE episode and spot-check before any bulk render.
6. **Adversarial review.** For scripts and any significant artifact, review as text with multiple
   models (a council) and reach consensus before rendering — text review is far cheaper than re-renders.

## 3. Folder layout (this folder IS the project root / web root)
```
AGENTS.md  system-prompts/  engine/  player/  reference/  schemas/  examples/   <- the engine (don't edit engine for content)
theme.json                              <- your world + cast (creative tokens)
project.json  capabilities.json         <- intake answers + detected hardware tier
course/data/truth.json                  <- the truth layer (facts)
course/scripts/epNN.json                <- episode specs you author
course/episodes/*.mp4 .srt .cues.json   <- rendered output (gitignored)
assets/{voices,avatars,music,backgrounds}/   <- generated/sourced media
watch.html index.html serve.py play.cmd play.sh   <- copied here by package.py for local play
```

## 4. Commands (run from THIS folder; the engine reads the cwd as the project)
Set once per shell: `PYTHONUTF8=1`; pick a voice engine `CC_TTS=chatterbox` (GPU) or `CC_TTS=piper`
(CPU); `CC_VERIFY=1` enables the self-correcting audio gate. `CC_THEME` auto-discovers `theme.json`.
```
python engine/probe.py                                  # hardware tier -> capabilities.json
python engine/scene.py demo                             # eyeball all scene types in the theme
python engine/build_episode.py course/scripts/ep01.json # render ONE episode (spot-check first!)
python engine/gates/verify_facts.py course/scripts/ep01.json
python engine/gates/lint_prompts.py
python engine/gates/lint_script.py ep01
python engine/gates/verify_episode.py ep01              # final-mp4 audio QA
python engine/package.py                                # manifest + posters + copy player locally
python serve.py            (or double-click play.cmd / ./play.sh)   # watch it locally
```
Reference contracts (read before authoring): `reference/SCENE_CONTRACT.md` (every beat field),
`reference/PRODUCTION_RULES.md`, `reference/ACCURACY_RULES.md`, `reference/AUDIO_RULES.md`,
`schemas/` (theme.json / project.json / truth.json / episode-spec). Hardware tiers + model downloads:
`reference/TROUBLESHOOTING.md`. Music licensing/attribution: `reference/ATTRIBUTION_AND_LICENSING.md`.

## 5. Definition of done (before telling the user a course is ready)
`verify_facts` + `lint_prompts` + `lint_script` pass (0 blocking); ONE episode spot-checked; then for
all rendered episodes `verify_episode` reads `OK`; `package.py` link-check is clean; music attributed;
**zero references to any existing franchise**. The user can double-click `play.cmd` and watch with the
interactive quiz working. Keep `plan.md` and `THIRD_PARTY_NOTICES.md` current.
