# Training-Content Generation Playbook (hard-won learnings)

*Living document. The **Production Bible** (`course/PRODUCTION_BIBLE.md`) says **what**
this specific course is. This playbook captures **how** we actually produced it — the
reusable recipes, exact prompts, seeds, voice knobs, pitfalls, and review process — so a
future **system that generates training content** can reproduce and build on it without
re-learning the hard way.*

> **MAINTENANCE RULE (do not skip):** Whenever you discover a non-obvious technique, fix a
> painful bug, settle a creative/voice/visual decision, or change a seed/prompt/knob, **add
> it here in the same change** (and bump the Changelog at the bottom). If it isn't written
> here, it is lost at the next context compaction. Prefer updating this file over leaving
> knowledge in your head, commit messages, or the session plan.

---

## 0. How to use this file
- Read this **plus** the Production Bible before producing or regenerating anything.
- Treat **Sections 3–6** (pedagogy pattern, character consistency, voice, accuracy) as the
  transferable IP. The NIST specifics are just one instantiation.
- Every prompt/seed/knob below is the **source of record**. If you change one in a tool,
  change it here too.

---

## 1. Learner profile (drives every decision)
- **@darinh learns best from video + visuals**, not audio-only. Always ship watchable
  episodes; audio is a bonus track, never the primary deliverable.
- **Beginner-first.** Assume no prior security background. Define every term in plain English
  the first time (the `define` scene type), then use it.
- **Pacing:** information-dense slides need enough on-screen time to *read* + deeper
  narration. Never rush good content. (Min on-screen time scales with bullet/line count.)
- **Personas must be obvious.** Show a character avatar next to the dialogue they speak.
- **Tone of the learner-avatar (NOVA):** young, new, informal — "So who writes all this
  stuff?" not "So who writes all of this?". Questions should sound like a curious novice.

---

## 2. North-star principles (transferable to any course)
1. **Accuracy is non-negotiable and comes from a TRUTH LAYER, never LLM memory.** Build a
   machine-readable source of record from the authoritative artifact (here: the official
   OSCAL catalog → `truth.json`). All IDs/titles/quotes come from it. A verbatim-source
   character quotes it on screen with a citation.
2. **Accuracy gates before any expensive render (two complementary gates).** (a) A
   **deterministic** check (`tools/verify_script.py`) fails the build unless every on-screen
   control fact agrees with `truth.json` — IDs exist, titles match exactly, Archivist quotes
   are verbatim substrings of the real statement, cheat-card "ID Title" prefixes match — and
   it warns on narration IDs. (b) A **local-LLM hostile-auditor** (`tools/audit_narration.py`)
   scrutinizes the *narrative* claims (FISMA framing, baselines-in-800-53B, RMF step order,
   control anatomy, etc.) for factual errors. Both are cheap vs. re-rendering. The multi-LLM
   council (§7) is the broader adversarial layer. *(Note: `verify_script.py` is deterministic,
   not an LLM — don't conflate the two gates.)*
3. **Fully local + license-clean.** ollama (drafting/review), local TTS, Pillow (scenes),
   ffmpeg (motion/assembly). No copyrighted audio/art. Track every model/asset license.
4. **Templated, declarative production.** Scenes are **data** (typed dicts) rendered by one
   engine; episodes are **JSON specs** assembled by one builder. Never hand-render frames.
   This makes regeneration, review, and bulk edits cheap.
5. **Retention-first pedagogy** (see §3).
6. **Council review → consensus before scaling** (see §7). Validate each reviewer finding
   against established project conventions before applying it — a stylistic "fix" can regress
   consistency with already-shipped work.
7. **Persist learnings** (this file). Knowledge that lives only in context is lost.

---

## 3. The pedagogy / narrative pattern (reusable recipe)
A standard, dry standard becomes binge-watchable by wrapping it in a consistent world:

- **Method-of-loci spatial map.** Map the taxonomy onto a memorable place (here: 20 control
  families → 20 districts/guardians of a citadel). Spatial memory aids recall.
- **A small, clearly-typed cast** with one job each:
  - **Expert** (VEGA) — explains, the authority in-world.
  - **Learner-avatar** (NOVA) — asks the audience's questions; informal, curious, growing.
  - **Verbatim source** (THE ARCHIVIST) — reads the *real* standard text on screen; the
    accuracy anchor. Keeps story separate from fact.
  - **Antagonist** (THE NULL) — embodies the threat; tie each threat to a real-world
    incident + a concrete attack technique (MITRE ATT&CK).
- **Per-unit structure** (~8–10 min episode): cold-open real-incident hook → map highlight →
  guardian intro → **real flagship items** (real ID + plain meaning + one verbatim quote) →
  map the metaphor back to real-world meaning → **active-recall quiz** (pause-and-answer) →
  recap card / "notebook" → cliffhanger.
- **One concrete worked example end-to-end.** Reviewers' #1 fix: add a dedicated episode
  that runs a single, named, concrete system through the whole process (here: "Aegis
  Hospital" through the RMF with a named human cast). Abstractions don't stick; one worked
  example does.
- **Always translate the metaphor back to reality.** The story is "interpretation"; the
  on-screen text is authoritative. Say which is which.
- **Retention scaffolding:** define-cards for jargon, quizzes per episode + a final
  roll-call quiz, recap notebook, and a cheat sheet per family.

---

## 4. CHARACTER / AVATAR CONSISTENCY  ⭐ (the most hard-won learning)

**The problem (user feedback, verbatim):**
- "these look too different" / "i dont want the avatars to look like different people with
  the same clothes and same hair color. i want them to look like the exact same character."
- Resolution path the user pushed us toward: "if you have to generate them all in a single
  character / sprite sheet, do that", "remember the seed and inputs", "i like the original
  avatar images. dont change the characters", and "research image generation character
  consistency. there have been recent developments and workflows."

**What did NOT work:** re-running the text-to-image prompt with a new seed for each
expression/pose. Same wardrobe words ≠ same person — you get different faces ("different
people with the same clothes"). Text prompts alone cannot hold identity.

**What WORKS (the workflow we shipped):**
1. **One canonical base portrait per character**, text-to-image (SDXL), at a **fixed seed**,
   with a **shared STYLE string** and **shared NEGATIVE string** so all characters share an
   art style. Record the seed. This base is the character's identity. **Never regenerate the
   base to "improve" it** once approved — the user likes the originals; changing them breaks
   continuity. (`tools/gen_avatars.py`)
2. **Expression / pose variants come from IMAGE conditioning, not text re-rolls.** Use
   **IP-Adapter Plus** (CLIP image conditioning) anchored on the character's **existing base
   portrait**: the reference image supplies identity; the prompt varies **only** the
   expression. This keeps it the *same character* across "asking", "curious", "explaining",
   "aha", etc. (`tools/gen_avatar_ipa.py`)
   - **Identity strength knob:** `scale = 0.72` (lower = more expression freedom, higher =
     more locked to the reference). 0.72 was the sweet spot for "clearly same person, new
     expression."
   - **Fixed `seed = 42`** for variant reproducibility.
   - Put `"different character"` and `"neutral expression"` in the **negative** prompt for
     variants.
3. **Frame** each portrait into a consistent circular avatar card (ring color per character)
   for overlay beside subtitles. (`tools/make_avatars.py`)
4. **Wire avatars into the render**: show the speaker's portrait beside their subtitle
   (visual-novel style). (`tools/build_episode2.py` avatar overlay.)
   > **STATUS — base portraits only; expression-by-intent is NOT wired yet.** The renderer
   > overlays just `{SPEAKER}.png`: `avatar_cues` stores only `(speaker, start, end)` and the
   > overlay loads `AVATAR_DIR/{sp}.png` (`build_episode2.py` ~lines 269–271 and 343–347). The
   > expression variants below exist on disk but are **not** selected per line. To wire them:
   > tag each script line with an intent (e.g. `"expr": "curious"`), carry that intent through
   > `avatar_cues`, and overlay `f"{sp}_{expr}.png"` when present (fall back to the base). This
   > needs a spec-format change + re-render, so it is **backlog** — do not claim it ships until
   > the overlay actually switches files.

**License-clean stack (important):** Tencent **IP-Adapter (Apache-2.0)**, **h94** adapter
weights (Apache-2.0), **SDXL base** (OpenRAIL++-M). **No InsightFace** (its models/data carry
non-commercial terms). CLIP-image conditioning is enough — face-embedding models are not
required and bring licensing baggage.

**Exact inputs — record of record (keep in sync with the tools AND with
`course/seed_registry.yaml`, the machine-readable mirror a future generator can import):**

Shared style/negative (base portraits, `gen_avatars.py`):
```
STYLE = ", anime style character portrait, head and shoulders bust, centered, clean cel
         shading, dramatic rim lighting, dark teal studio background, highly detailed,
         crisp, single character, looking at viewer"
NEG   = "text, words, letters, watermark, signature, logo, multiple people, crowd, extra
         limbs, extra fingers, deformed, mutated, blurry, lowres, photorealistic, 3d render,
         nsfw, full body, weapon"
SDXL base-1.0, 1024x1024, steps=34, guidance=7.0
```

Per-character base seed + identity description:
| Char | Seed | Description (identity prompt) |
|------|------|-------------------------------|
| VEGA | 1101 | confident veteran cyber officer, man ~30s, short silver-blue hair, navy tactical uniform w/ glowing cyan accents, calm determined |
| NOVA | 1102 | young eager apprentice, woman early-20s, short tousled auburn hair, teal jacket w/ gold trim, bright curious hopeful |
| ARCHIVIST | 1103 | wise archivist scholar, woman, round glasses, dark hooded robe w/ glowing golden circuit embroidery, serene knowing |
| NULL | 1104 | shadowy hooded antagonist, face hidden in shadow, glowing magenta eyes, dark cloak w/ red glitch, menacing |
| NARRATOR | 1105 | dignified herald narrator, older man, deep blue cloak, gold circuitry mask on forehead, calm authoritative |

> **NULL — authoritative seed is 1104 (verified).** The shipped/committed `NULL.png` is the
> hooded-antagonist portrait from **seed 1104** above — verified by inspecting the asset and
> git history (no committed generation script or asset encodes "1144"; only these explanatory
> notes mention it). An in-session experiment regenerated NULL as a *broad-shouldered cloaked bruiser* at **seed
> 1144**, but it was **not adopted or committed** (the user asked us not to change the
> established characters), so `gen_avatars.py` (seed 1104) is correct and reproduces the
> shipped look. The NULL **voice** deepening *did* ship (Chatterbox + ffmpeg `rubberband
> pitch=0.84`, §5) — don't confuse the shipped voice change with the rejected avatar change.
>
> **Asset immutability:** treat every approved base portrait as a **frozen asset of record**.
> Diffusers/torch/SDXL version drift can change pixels even at a fixed seed, so don't
> regenerate an approved portrait casually — the committed PNG (+ its seed/prompt) is the
> source of truth, mirrored in `course/seed_registry.yaml`.

Expression variants (`gen_avatar_ipa.py`, IP-Adapter Plus, `scale=0.72`, `seed=42`):
```
VEGA.explain : "a man with a clear warm friendly smile, mouth open speaking, kind eyes, explaining"
VEGA.ask     : "a man with a thoughtful curious look, one eyebrow raised high, head tilted, questioning"
NOVA.curious : "a young woman with a gentle soft smile, bright wide attentive eyes, eager and curious"
NOVA.ask     : "a young woman asking a question, both eyebrows raised high, mouth open mid-question, inquisitive"
NOVA.aha     : "a young woman with a big open joyful grin showing teeth, eyes wide with delight, thrilled aha moment"
```
Shipped variant files: `NOVA_{curious,ask,aha}.png`, `VEGA_{ask,explain}.png` (raw + framed).

**Generalizable rule for any future generator:** *Identity = one fixed-seed reference image
per character; everything else (expression, pose, angle, later even lip-sync frames) is
**image-conditioned** off that reference. Never rely on text prompts alone to hold a face.*
Newer equivalents worth evaluating when revisiting: instant-identity / consistent-character
workflows, reference-only / image-prompt adapters, and character-LoRA training from the
approved base set. The principle (condition on the reference) stays the same.

### 4a. Image-generation environment setup (reproduce on a new machine)
All image gen runs in **`.venv_img`** (kept separate from the TTS venv): `torch` (CUDA build),
`diffusers`, `transformers`, `accelerate`, `safetensors`, `Pillow`. Model: SDXL base-1.0 is
pulled by `diffusers.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", variant="fp16")`
(cached under the HF cache).

**IP-Adapter (for §4 expression variants)** — install once, then it's offline:
- `pip install` the **`ip_adapter`** package (Tencent `tencent-ailab/IP-Adapter`, Apache-2.0) into `.venv_img`.
- Download the weights from HF **`h94/IP-Adapter`** into `tools/_ipa/` (gitignored, multi-GB, re-downloadable). Exact layout the code expects (`gen_avatar_ipa.py` `ENC`/`CKPT`):
  - `tools/_ipa/models/image_encoder/{config.json, model.safetensors}` — ViT-H (1280-dim) image encoder
  - `tools/_ipa/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors` — the Plus adapter (ViT-H variant)
- Plus adapter uses `num_tokens=16`; the `_vit-h` adapter **requires the ViT-H** encoder (don't pair it with the smaller ViT-bigG/`image_encoder` under `sdxl_models/`).

### 4b. Backgrounds (hybrid: AI makes ONLY backgrounds, the UI stays designed)
Council-endorsed rule: **AI generates only dark, text-free, character-free backgrounds**; all UI,
sigils, and text are drawn by the deterministic scene engine on top. This avoids garbled AI text
and keeps the layout crisp. (`tools/gen_backgrounds.py`, SDXL, 1344x768, steps 30, guidance 6.5,
seeds `1000+i`.) Saved to `course/art/backgrounds/<name>.png`.
```
STYLE = ", dark moody concept art, deep navy background, high contrast, volumetric fog, cinematic rim lighting, depth of field, 16:9, no text, no characters"
NEG   = "text, words, letters, numbers, watermark, signature, people, person, face, hands, ui, border, frame, bright, washed out, low quality, jpeg artifacts, busy, cluttered"
citadel : "a colossal dark cyber fortress citadel on a hill at night, glowing cyan circuit ramparts, distant gold lights"   (seed 1000)
walls   : "a fortified digital gate, faint cyan energy barrier, towering dark ramparts, atmospheric haze"                   (seed 1001)
watch   : "tall watchtowers above a dark data-city, faint teal scanning light beams in fog"                                (seed 1002)
people  : "a vast dim archive hall of faintly glowing data shelves, warm gold ambient light"                              (seed 1003)
council : "a dark high council chamber, faint holographic blue maps floating, violet ambient glow"                         (seed 1004)
forge   : "a dark industrial forge with dim server racks and supply conduits, faint orange and cyan embers"               (seed 1005)
vault   : "a deep underground data vault, dark blast doors, faint magenta and cyan glowing cores"                         (seed 1006)
network : "an abstract dark void with a faint constellation of cyan and gold light nodes, depth of field"                 (seed 1007)
```

### 4c. How to create a NEW character / re-cast for a NEW course (step-by-step)
1. Pick a **new fixed seed** (don't reuse 1101–1105) and write an identity description in the
   same slot style as the table above (age, hair, wardrobe, signature color, expression).
2. Add it to `gen_avatars.py CHARS` + a ring color in `make_avatars.py COLOR`; run base gen → frame.
3. **Lock it**: copy the seed + exact prompt into `course/seed_registry.yaml` **before** making
   variants. That registry entry — not your memory — is the reproducibility record.
4. Expression variants: add the character + per-expression prompts to `gen_avatar_ipa.py EXPR`
   and run it; identity comes from the base image (scale 0.72), so vary ONLY the expression text.
5. Eyeball that all variants look like the SAME person; if one drifts, nudge `SCALE` up (toward
   ~0.8) or fix the expression wording — do **not** re-roll the base seed.
6. Record the run (seed, prompts, files) in the registry + a Changelog note. Keep failed/rejected
   attempts as documented lessons (see the NULL seed-1144 note) so they aren't retried blindly.

---

## 5. VOICE / TTS  ⭐ (hard-won)

**Engine evolution (and why):** piper (`tts.py`) → Kokoro (`tts2.py`) → **Chatterbox**
(`tts3.py`, current). Each step bought more natural, expressive prosody. All are
**license-clean** (piper MIT-ish voices, Kokoro Apache-2.0, Chatterbox = Resemble AI **MIT**).
Keep the prior engine as a fallback (`CC_TTS` env switch).

**Casting matters and is a user decision.** THE ARCHIVIST must be a **young British female**
(explicit correction after a male render). VEGA uses a **younger male** timbre. Get casting
signed off before bulk render.

**Chatterbox approach (current):** zero-shot **voice cloning** from a short, **license-clean
reference clip per character** (`tools/voices_ref/<SPEAKER>.wav`, themselves generated by
Kokoro so timbres are persona-matched). Chatterbox then supplies natural prosody + an
`exaggeration` emotion knob. Per-character knobs (`tts3.py CAST`):

| Char | exaggeration | cfg_weight | temperature | notes |
|------|--------------|-----------|-------------|-------|
| NARRATOR | 0.52 | 0.50 | 0.78 | |
| VEGA | 0.62 | 0.46 | 0.80 | younger-male ref |
| NOVA | 0.70 | 0.42 | 0.85 | most expressive (young, eager) |
| ARCHIVIST | 0.38 | 0.58 | 0.72 | calm, measured; British-female ref |
| NULL | 0.82 | 0.28 | 0.70 | + ffmpeg `rubberband pitch=0.84` to deepen/menace |
| HERALD | 0.58 | 0.46 | 0.80 | |

**Pronunciation pre-processor (shared, critical).** Acronyms/IDs/doc-numbers must be spoken
correctly; this runs on **spoken text only**, never on-screen text (`tts.py preprocess`,
imported by every engine). Examples: NIST→"nisst", CISO→"see-so", RMF→"R-M-F", AC-6→"ay see
six", "800-53r5"→"eight hundred fifty three, revision five", "800-53B"→"…B". Drop the literal
"dash"; hyphens in IDs become spaces; spell family codes letter-by-letter. **Extend this map
whenever a new acronym/ID appears** — mispronounced IDs read as errors to a security audience.

**Per-character ffmpeg mastering chain** places every voice in the same ~-16 LUFS soundstage
(highpass + gentle compression + per-character EQ + a touch of echo; NULL adds subboost +
lowpass for a cavernous menace). See `tts3.py EFFECTS`.

**PITFALLS (cost us re-renders):**
- **Dropped words.** Neural TTS sometimes silently omits a word (observed: NOVA asks "So who
  writes all this?" and VEGA's reply dropped "NIST", saying only "does."). **Verify rendered
  narration with speech-to-text** (e.g. local Whisper: `whisper line.wav --model base
  --language en`) and reword phrasing the model swallows. Don't trust the text→audio mapping
  blindly on important lines.
- **Caching.** Line audio is cached by a key over `(speaker, knobs, effects, ref-file mtime,
  preprocessed text)`. If you change a voice knob, effect, or the reference clip, the key
  changes and it re-synthesizes — good. But if you edit the **pre-processor** and the output
  string is unchanged, the key won't change: delete the cache dir
  (`tools/_tmp/voicecache_cbx/`) to force re-synthesis.

---

## 6. Production / assembly pipeline
- **Scene engine** (`tools/scene.py`, Pillow, 1920x1080): a fixed set of **declarative scene
  types** (the `RENDERERS` registry) — `title`, `section`, `map`, `guardian`, `control`,
  `quote` (archivist verbatim), `diagram`, `points`, `cheatcard`, `quiz`, plus beginner
  additions `define` (plain-English term card), `coldopen` (incident + MITRE), `oath`
  (guardian oath/sigil), `notebook` (Nova's recap). Add a scene **type**, not a one-off frame.
- **Episode spec** = JSON (`course/scripts/epNN.json`): beats with `scene`, `say`
  (speaker+line list), on-screen text, quiz fields. Assembled by `tools/build_episode2.py`
  (v2; `build_episode.py` is the older path).
- **Motion** via ffmpeg `zoompan`/`fade`/`overlay` (Ken Burns) + animated scenes (sequential
  map-district reveal, boxes pop / arrows draw, kinetic titles). **Video is hard-cut concat**
  (so video length == narration length, perfect A/V sync) with transition SFX over the cuts;
  `xfade` crossfades were tried but dropped for sync safety (see `VNEXT.md`).
- **Captions:** the styled captions are **burned into the video pixels** (ASS `subtitles`
  filter) and the **baked caption size was increased** per user request. The final mux maps
  **only video + audio — no soft subtitle stream is embedded** — so the `.mp4` shows no
  default-on track in players. A sidecar `.srt` is written next to the mp4 for
  accessibility/search but is **not muxed in** (`build_episode2.py` ~lines 360–368). (The
  earlier complaint was a soft track auto-showing; the fix was to stop embedding it.)
- **Music:** locally synthesized / CC-BY orchestral beds, per-episode mood map, seamless
  crossfade-loop, **sidechain-ducked under VO** (`tools/music2.py`). Attribution in
  `THIRD_PARTY_NOTICES.md`.
- **SFX:** per-scene cues + NULL rumble (`tools/sfx.py`).
- **Transcripts** capture on-screen text (define cards, bullets, quizzes), not just spoken
  lines, for accessibility — generated by `tools/package.py` (`_onscreen()` inside
  `build_transcripts_and_quizzes()`), written to `course/transcripts/epNN.md`.
- **Player/site:** `index.html` + `watch.html` (auto-advance: Up Next + countdown + Play
  now/Stay here + course-complete screen). Deployed via GitHub Pages.

---

## 7. Council / adversarial review (process that catches errors)
- For significant deliverables (plans, scripts, pilots, final package): review **iteratively
  with multiple agents and multiple LLMs**, run **adversarial** critiques, and proceed **only
  after consensus**.
- **Diversity of models matters.** Mix hosted (`task` tool: gpt-5.5, gemini-3.1-pro-preview,
  claude-sonnet) with **local ollama** (`tools/council_ollama.py`: gpt-oss:20b, gemma3:27b)
  for independent failure modes.
- **Review the scripts/tools too, not just the final video** — pipeline code written by a
  single model without review can be subtly wrong.
- **Local LLMs hallucinate facts.** The council caught 2 local-LLM control hallucinations
  (RA-2, SA-22) that were rejected against `truth.json`. This is exactly why the truth layer +
  hostile-auditor gate exist.
- **Validate findings against conventions before applying.** A reviewer's stylistic "fix" can
  regress consistency with already-shipped episodes. Check prior work first.

---

## 8. Environment & exact commands (Windows)
- Use **Windows paths (backslashes)**. Set `$env:PYTHONUTF8=1` for scripts.
- **Two venvs** (heavy deps don't co-exist cleanly):
  - `.venv_img` — SDXL / diffusers / IP-Adapter (image gen). 4090 GPU.
  - `.venv_tts` — Chatterbox / torch cu124 (voice). Kokoro/piper also here/standalone.
- **ollama models:** gpt-oss:120b (heavy, may OOM — prefer 20b/gemma3:27b for reliability),
  gpt-oss:20b, gemma3:27b, qwen3:8b.
- **ffmpeg/ffprobe 8.0, python 3.11, node 20.**

Common runs:
```powershell
# Truth layer (authoritative content) -> course/data/truth.json
python tools\build_truth.py

# Base character portraits (fixed seeds)            [.venv_img]
.\.venv_img\Scripts\python.exe tools\gen_avatars.py
# Expression variants via IP-Adapter (image-conditioned on the base)
.\.venv_img\Scripts\python.exe tools\gen_avatar_ipa.py NOVA VEGA
# Frame into avatar cards
python tools\make_avatars.py

# Voice smoke test (Chatterbox)                     [.venv_tts]
.\.venv_tts\Scripts\python.exe tools\tts3.py

# Deterministic accuracy gate (must PASS before render): on-screen facts vs OSCAL truth
python tools\verify_script.py course\scripts\ep00.json
# Local-LLM hostile-auditor over narrative claims (complements the deterministic gate)
python tools\audit_narration.py course\scripts\ep00.json

# Build ONE episode for spot-check. render_all.py takes stems; build_episode2.py takes a spec
# PATH. Chatterbox is opt-in via CC_TTS (default engine is Kokoro/tts2).
$env:CC_TTS='chatterbox'; python tools\render_all.py ep00
# equivalently: $env:CC_TTS='chatterbox'; python tools\build_episode2.py course\scripts\ep00.json
```
> **Always render ONE episode and spot-check before re-rendering all of them** — full
> re-renders are expensive and the user repeatedly asked for single-episode spot checks
> (e.g., "Just render video 00 and stop so I can spot check").

---

## 9. Reuse for a NEW course/topic (the generalization)
This pipeline is topic-agnostic. To target a different standard / body of knowledge:
1. **Build the truth layer first.** Parse the authoritative source into `truth.json` with a
   stable contract the renderer + gates rely on: `TRUTH[family]` with
   `controls[ID] = {title, statement, discussion, related, enhancements}` (see
   `tools/build_truth.py` + `episode_lib.TRUTH`). Whatever the topic, you need a stable unit
   **ID**, an exact **title**, and a **verbatim authoritative text** to quote. Re-point
   `build_truth.py` at the new source but keep the shape, so `verify_script.py` /
   `audit_narration.py` keep working unchanged.
2. **Re-skin the world + cast** (course-specific; lives in `PRODUCTION_BIBLE.md`): pick a
   method-of-loci map for the taxonomy and cast the four archetypes (expert / learner-avatar /
   verbatim-source / antagonist). Generate base portraits (§4) at NEW fixed seeds and record
   them in `seed_registry.yaml`; clone voices (§5) from license-clean reference clips.
3. **Author scripts** as JSON beat specs using the existing scene types (§6): keep ≥50% of
   runtime on real units, one verbatim quote per unit, always translate metaphor → reality.
4. **Run the gates + council, then spot-render ONE episode** before bulk.

**Consensus loop (how "review with multiple agents/LLMs" actually runs):**
draft → deterministic gate (`verify_script.py`) → local-LLM auditor (`audit_narration.py`) →
multi-LLM council (hosted via the `task` tool with varied `model` + local via
`tools/council_ollama.py`) → harvest findings → **validate each finding against existing
conventions/code before applying** (a reviewer can be wrong; verify against the repo) → fix →
re-run gates → only then render/scale. Record material outcomes in the Changelog (§11).

> **Why concrete seeds/knobs live in THIS file (not only the Bible):** the user's standing
> directive is "remember the seed and inputs." The playbook is the human-readable record of
> record; `course/seed_registry.yaml` is the machine-readable mirror. The Bible holds the
> *creative* spec (world, cast, episode map); this file holds the *reproducible how*.

---

## 10. Known gaps / backlog
See `VNEXT.md`. Headline aspiration: true **character animation** (lip-sync / motion) instead
of static avatars + motion graphics — revisit with dedicated animation/video models, reusing
the §4 fixed-base-reference identity so the animated character stays the same person.
**Also backlog:** wire expression-by-intent avatars into the renderer (§4 STATUS note).

---

## 11. Changelog of learnings
- **2025 — image-gen recording pass.** Recorded the remaining image-generation inputs +
  setup/guidance so the avatar/image work is reproducible on a fresh machine: added §4a
  (`.venv_img` + IP-Adapter install + exact `tools/_ipa/` model layout from `h94/IP-Adapter`),
  §4b (backgrounds — hybrid AI-backgrounds-only rule + all 8 `gen_backgrounds.py` prompts/seeds
  1000–1007 + STYLE/NEG), and §4c (step-by-step "create a NEW character / re-cast for a new
  course"). Mirrored into `seed_registry.yaml` (`image_setup`, `image_backgrounds`).
- **2025 — adversarial council review (5 LLMs: gpt-5.5, gemini-3.1-pro, claude-sonnet-4.5,
  gemma3:27b, gpt-oss:20b).** Consensus SHIP-WITH-CHANGES; applied: corrected the accuracy-gate
  description (`verify_script.py` is **deterministic**; `audit_narration.py` is the LLM
  auditor); flagged expression-by-intent avatars as **backlog, not wired** (renderer overlays
  base `{SPEAKER}.png` only); **resolved the NULL seed question** — shipped `NULL.png` is the
  hooded **seed-1104** asset (the 1144 "bruiser" was rejected, not committed); fixed the build
  command (`CC_TTS=chatterbox`; `render_all.py` stems vs `build_episode2.py` path); made the
  soft-subtitle mechanism precise (no soft track muxed); added the `guardian` scene type, STT /
  cache-clear notes, the §9 new-topic generalization + consensus loop, and
  `course/seed_registry.yaml` (machine-readable mirror). Also fixed two stale golden rules in
  `copilot-instructions.md` and the Archivist casting note in `PRODUCTION_BIBLE.md`.
- **2025 — v3.1 voice/avatar pass:** Documented the character-consistency workflow (fixed-seed
  base + IP-Adapter image conditioning, scale 0.72 / seed 42, license-clean no-InsightFace
  stack) and the Chatterbox voice-clone approach (per-character knobs, NULL pitch 0.84,
  dropped-word/STT pitfall). Recorded base seeds 1101–1105. Captions: no soft track muxed,
  baked captions larger. NOVA voiced young/informal. **This playbook created.**
- *(Add new entries above this line as learnings accrue. Date + one-line summary + which
  tool/section changed.)*
