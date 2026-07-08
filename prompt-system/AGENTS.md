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
Each course lives in its **own project folder** (`projects/<slug>/`). Look there (not the engine root):
- **No `projects/*/` with a `theme.json`** → **NEW project.** Greet the user, ask their topic + the
  world/aesthetic, then create `projects/<slug>/`, set `CC_PROJECT` to it, and start at
  `system-prompts/01_intake.md`. Go in order. (Never build a course in the engine root.)
- **A project has `theme.json` + `course/data/truth.json` but no `course/episodes/*.mp4`** → content is
  authored but not rendered → resume at `system-prompts/09_gates.md` then `10_assemble.md`.
- **A project has `course/episodes/*.mp4`** → resume at `11_player_and_verify.md` (package/verify) or
  ask the user what to change. Use the incremental render cache — editing one line rebuilds one beat.
Always read the project's `plan.md` (if present) and `capabilities.json` (run `python engine/probe.py`
from the project folder if missing).

## 1. The pipeline (what the prompts walk you through)
```
01 intake        -> project.json         (topic, audience, AESTHETIC, scope, options)
02 environment   -> capabilities.json    (probe hardware for SPEED; install the HIGH-QUALITY models)
03 truth layer   -> course/data/truth.json   (verbatim FACTS with ids/titles/quotes + source/section)
04 world + cast  -> theme.json            (ORIGINAL world metaphor + ORIGINAL characters in the aesthetic)
05 avatars       -> assets/avatars/*.png  (SDXL fixed-seed original portraits — GPU or CPU)
06 voices        -> assets/voices/*       (one voice per character; high-quality neural chatterbox — GPU or CPU)
07 music + sfx   -> assets/music/*        (SOURCED public-domain/CC beds; attributed. SFX are bundled)
08 script        -> course/scripts/epNN.json   (declarative beats: scenes + dialogue)
09 gates         -> (verify_facts, lint_prompts, lint_script) must pass before render
10 assemble      -> course/episodes/epNN_*.mp4 + .srt + .cues.json   (incremental render, two-pass mux)
11 player+verify -> verify_episode + package -> watch.html/index.html + serve.py (LOCAL play)
12 reference     -> OPTIONAL quizzes / study guide / quick reference
```
**Build each course in its OWN project folder — never in this engine folder.** Create
`projects/<slug>/` (e.g. `projects/home-espresso/`), set `CC_PROJECT` to it, and run all commands
against it. That keeps `theme.json`, `project.json`, `course/`, `assets/`, and the copied player out
of the engine root so the system stays clean and you can build several courses side by side.

A single video OR a whole course. **Quizzes are ON by default** (the signature feature); avatars,
music, study guides, and extra episodes are **opt-in** with sane defaults — so a quick demo can
produce ONE interactive video even on a laptop with **no GPU** (same high quality — just slower).

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
4. **Quality is fixed HIGH — never silently downgrade; hardware only affects SPEED.** Always use the
   highest-quality models by DEFAULT: **chatterbox** neural voice, **SDXL** portraits, **large-v3**
   audio-QA. These all run on **CPU too** — a missing GPU makes rendering slower, NOT lower quality,
   so run the same model on CPU. NEVER auto-swap to a lower-quality model/voice (piper, illustrated,
   small STT). If the high-quality path isn't installed, the engine FAILS LOUD with setup guidance —
   do not work around it by degrading. If CPU rendering is too slow, **WARN the user and get their
   EXPLICIT approval before applying any downgrade** (`CC_TTS=piper`, `CC_AVATARS=illustrated`,
   `CC_STT_MODEL=small`). The user MUST approve any quality reduction. Geometry, timing, the two-pass
   A/V mux, caption placement, the quiz hotspot layout, and the gates are also FROZEN in `engine/`;
   the theme changes only colors/fonts/words; never reimplement the quiz hotspots.
5. **Verify the delivered artifact.** QA the final mp4 (`verify_episode`), not upstream clips. Render
   ONE episode and spot-check before any bulk render.
6. **Adversarial review.** For scripts and any significant artifact, review as text with multiple
   models (a council) and reach consensus before rendering — text review is far cheaper than re-renders.

## 3. Folder layout — the engine folder vs. your project folder
The engine folder holds the reusable system; **each course lives in its own `projects/<slug>/`** so it
never pollutes the engine root. All engine commands read `CC_PROJECT` (a project dir) — set it once.
```
prompt-system/                          <- THE ENGINE (don't put course content here)
  AGENTS.md  system-prompts/  engine/  player/  reference/  schemas/  examples/
  projects/<slug>/                      <- YOUR COURSE lives here (CC_PROJECT points at it)
    project.json  theme.json  capabilities.json   <- intake + world/cast + detected hardware
    course/data/truth.json              <- the truth layer (facts)
    course/scripts/epNN.json            <- episode specs you author
    course/episodes/*.mp4 .srt .cues.json   <- rendered output (gitignored)
    assets/{voices,avatars,music,backgrounds}/  <- generated/sourced media
    watch.html index.html serve.py play.cmd play.sh   <- copied here by package.py for local play
```

## 4. Commands (set `CC_PROJECT` to your project folder; the engine writes everything there)
Set once per shell: `CC_PROJECT=projects/<slug>` (the course folder); `PYTHONUTF8=1`; `CC_VERIFY=1`
(self-correcting audio gate). `CC_THEME` auto-discovers the project's `theme.json`. Do NOT set
`CC_TTS`/`CC_AVATARS`/`CC_STT_MODEL` — they default to the HIGH-QUALITY models (GPU or CPU); set them
ONLY to apply a user-approved downgrade.
```
python engine/probe.py                                  # SPEED tier + recommended models -> capabilities.json
python engine/scene.py demo                             # eyeball all scene types in the theme
python engine/build_episode.py course/scripts/ep01.json # render ONE episode (spot-check first!)
python engine/gates/verify_facts.py course/scripts/ep01.json
python engine/gates/lint_prompts.py
python engine/gates/lint_script.py ep01
python engine/gates/verify_episode.py ep01              # final-mp4 audio QA
python engine/package.py                                # manifest + posters + copy player into the project
cd $CC_PROJECT; python serve.py   (or double-click play.cmd / ./play.sh)   # watch it locally
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
