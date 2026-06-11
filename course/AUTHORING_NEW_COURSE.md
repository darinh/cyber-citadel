# Authoring a NEW course with the Cyber Citadel engine

*This is the operator's manual for reusing this fully-local pipeline to build a **different**
training course (any standard, framework, or body of knowledge). It assumes the tooling in
`tools/` and the conventions in `GENERATION_PLAYBOOK.md`. Read the playbook's **§11 Production
Rules** and **§12 Incremental Render Architecture** first; this guide ties them into a workflow.*

The engine is topic-agnostic: a **truth layer** (authoritative facts) + **declarative JSON
episode specs** (beats made of typed scenes + character dialogue) → **local TTS** + **Pillow
scenes** + **ffmpeg** → mp4s + captions + an interactive web player. Nothing here is specific to
NIST except the content you put in the truth layer and the specs.

---

## 0. One-time environment (per machine)
- **Two Python venvs** (heavy deps don't co-exist): `.venv_img` (SDXL + diffusers + IP-Adapter,
  image gen) and `.venv_tts` (Chatterbox + torch cu124, voice). `ffmpeg/ffprobe 8.0`, `python 3.11`.
- **ollama** for drafting/review councils (gpt-oss:20b, gemma3:27b, …).
- **IP-Adapter weights** under `tools/_ipa/` (see playbook §4a). `$env:PYTHONUTF8=1` for scripts.
- Set `$env:CC_TTS='chatterbox'` to use the current voice engine.

## 1. Pipeline at a glance
```
authoritative source ──build_truth──▶ course/data/truth.json   (facts: id/title/text)
                                          │
world+cast (PRODUCTION_BIBLE) ────────────┤
                                          ▼
        episode specs  course/scripts/epNN.json   (beats = scenes + dialogue)
                                          │  verify_script.py (deterministic gate)
                                          │  audit_narration.py (local-LLM fact-check)
                                          ▼
   build_episode2.py  ──▶ course/render/<ep>/ (persistent per-beat/per-line artifacts)
        scene.py (Pillow stills) + tts3.py (voice) + music2/sfx + ffmpeg
                                          ▼
            course/episodes/epNN_*.mp4 + .srt/.vtt + .cues.json
                                          │  package.py
                                          ▼
            transcripts + quizzes.json + manifest.json + index.html / watch.html → GitHub Pages
```

## 2. Step-by-step for a new course

### Step 1 — Build the truth layer
Point `tools/build_truth.py` at your authoritative source and emit `course/data/truth.json` in
the shape the gates expect: `TRUTH[group].controls[ID] = {title, statement, discussion,
related, enhancements:[{id,title}]}`. You need, per unit: a stable **ID**, an exact **title**,
and a **verbatim quotable statement**. Keep the shape so `verify_script.py` / `audit_narration.py`
work unchanged. *All on-screen IDs/titles/quotes must come from here — never from LLM memory.*

### Step 2 — Design the world + cast (creative spec)
Write a Production-Bible analog: a **method-of-loci** map for your taxonomy and the four
archetypes — **expert** (mentor), **learner-avatar** (asks novice questions, grows), **verbatim
source** (reads the real text; never opines), **antagonist** (embodies the threat/failure mode).
Define tone per character. (See `PRODUCTION_BIBLE.md` for the NIST instantiation.)

### Step 3 — Generate the cast art (see playbook §4 + §4c, `seed_registry.yaml`)
Base portrait per character at a **fixed seed** (`gen_avatars.py`), then expression variants via
**IP-Adapter image-conditioning** on that base (`gen_avatar_ipa.py`, identity scale ~0.72). Frame
into cards (`make_avatars.py`). **Record every seed + prompt in `seed_registry.yaml` before
deriving variants.** Optionally regenerate backgrounds (`gen_backgrounds.py`, hybrid rule §4b).

### Step 4 — Clone the voices (see playbook §5)
Put a license-clean reference clip per character in `tools/voices_ref/<SPEAKER>.wav`; set
per-character Chatterbox knobs (`exaggeration/cfg_weight/temperature`, plus any pitch/EQ) in
`tts3.py CAST`/`EFFECTS`. Extend the pronunciation map in `tts.py preprocess()` for your domain's
acronyms/IDs (spoken text only). Smoke-test with `python tools\tts3.py`.

### Step 5 — Author episode specs (`course/scripts/epNN.json`)
Each spec = `{"id","tag","slug","beats":[ ... ]}`. A beat is `{"scene": <type>, ...fields,
"say": [["SPEAKER","line"], ...], "min_seconds": <float>}`. Follow the **§11 Production Rules**
(antagonist always in character + present every episode; quizzes read Q+options+answer+why;
every episode opens on a hook and closes on an antagonist escalation; verbatim source only
quotes; translate the metaphor back to reality). See the **scene-type contract** in §3 below.

### Step 6 — Gate every script (before rendering)
```powershell
python tools\verify_script.py course\scripts\epNN.json      # deterministic: facts vs truth.json
python tools\audit_narration.py course\scripts\epNN.json    # local-LLM narrative fact-check
```
Fix all hard errors. Then run a **multi-LLM council** (playbook §7) on the scripts.

### Step 7 — Render (incremental; see §12)
```powershell
$env:CC_TTS='chatterbox'; python tools\render_all.py epNN     # ONE episode first (spot-check)
$env:CC_TTS='chatterbox'; python tools\render_all.py          # all, once spot-check passes
```
Artifacts persist under `course/render/<ep>/` keyed by a content hash, so **editing one
line/slide rebuilds only that beat**. Bump `RENDER_VER` in `build_episode2.py` when you change
**render logic** (scene drawing, grade, etc.) to force a rebuild. **Always spot-check one
episode (extract a frame, listen) before a full batch.**

### Step 8 — Package + deploy
```powershell
python tools\package.py        # transcripts (incl. on-screen text), quizzes.json, manifest, index.html, VTT
```
Commit `course/episodes/*.mp4|srt|vtt|cues.json`, `manifest.json`, `index.html`; push to the
Pages branch. (`course/render/` and the venvs/model weights stay gitignored.)

---

## 3. Episode-spec scene-type contract (authoritative field reference)
Every beat: `scene` (required) + optional `say` `[["SPEAKER","text"], ...]` + `min_seconds`.
Speakers: the cast names (e.g. `NARRATOR, VEGA, NOVA, ARCHIVIST, NULL, HERALD`) — each needs a
voice in `tts3.py` and a framed avatar `course/art/avatars/<SPEAKER>.png`. Fields per scene:

| scene | fields (besides `say`/`min_seconds`) | notes |
|-------|--------------------------------------|-------|
| `title` | `badge`, `title`, `subtitle`, `kicker` | episode/series title card; fades in |
| `section` | `num`, `title`, `subtitle` | layer/act divider |
| `map` | `title`, `highlight:[GROUP codes]`, `deps:[[A,B]]` | method-of-loci map; **animated** (sequential reveal) |
| `guardian` | `family`, `family_name`, `persona`, `protects`, `reality` | introduce a group + its real-world meaning |
| `control` | `id`, `title`, `plain`, `why` | **`id`+`title` must match truth.json**; `plain`=meaning, `why`=stakes |
| `quote` | `quote` (VERBATIM), `cite` (must contain the ID) | the verbatim source on screen; `verify_script` checks it's a real substring |
| `diagram` | `title`, `nodes`, `arrows` | **animated** (boxes pop, arrows draw) |
| `points` | `kicker`, `title`, `bullets:[...]`, `note` | dense slide; on-screen time scales with bullet count |
| `cheatcard` | `family`, `title`, `bullets:[...]`, `mnemonic` | recap card |
| `define` | `kicker`, `term`, `expand`, `plain`, `example`, `cite` | plain-English jargon card (beginner-first) |
| `coldopen` | `label` (default "BREACH OF THE WEEK"), `year`, `headline`, `body`, `mitre`, `teaches` | the hook; use a real incident (year+MITRE) OR `label:"FROM THE FIELD"` + headline/body for an honest illustrative scenario (no fabricated dated breach) |
| `quiz` | `q`, `options:[...]`, `answer` (index), `why` | engine auto-reads Q+options in think phase and the correct answer TEXT + `why` at reveal; exports cues for the player |
| `oath` | `family`, `oath`, `controls` | guardian oath/sigil beat |
| `notebook` | `title`, `lines:[...]`, `mnemonic` | learner's recap (callbacks) |

Reserved/auto fields (do **not** set by hand): `_integrity` (running stakes meter, injected by
`build_episode2`), `_t` (animation progress), `tag` (episode tag), `reveal` (quiz phase).

Add a **new** scene type by writing a renderer in `scene.py` and registering it in the
`RENDERERS` dict — never hand-render frames.

---

## 4. Guardrails (don't repeat known mistakes)
- **Accuracy**: on-screen IDs/titles/quotes from `truth.json` only; verbatim quotes are exact
  substrings; run both gates + the council before rendering. Don't fabricate incidents.
- **Audio**: STT-spot-check rendered lines; approved audio lives under `course/render/` (never
  ship from `_tmp`); the final mix is loudnorm'd + limited.
- **Reproducibility**: every seed/prompt/voice-knob is recorded in `seed_registry.yaml`; treat
  approved base portraits as frozen assets.
- **Pacing/pedagogy**: dense slides get reading time; define jargon before use; quizzes read the
  answer + a "why"; map the metaphor back to reality.
- See `GENERATION_PLAYBOOK.md` §11 for the full, council-ratified rule set, and §13 for the
  open backlog.
