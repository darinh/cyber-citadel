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

**Better-engine evaluation (3-LLM council, 2026-06: gpt-5.5 + gemini-3.1-pro + claude-sonnet-4.6,
primary-source-verified).** The learner asked repeatedly for a more reliable voice. Findings:
- **The recurring "fucked up audio" was primarily the MUX BUG (§11.D), not Chatterbox** — fixing
  the mux removed most of the pain. An engine swap is OPTIONAL future work, not required.
- **Architecture is what kills word-drops:** autoregressive engines (Chatterbox, XTTS, Fish,
  Orpheus, Zonos, Dia, Llasa, Higgs) sample tokens and can drop/repeat/garble; **non-autoregressive
  / flow-matching** engines generate the whole utterance at once and structurally do not.
- **#1 for reliability — F5-TTS** (NAR flow-matching; MIT *code*; zero-shot clone from a 3–10 s ref;
  ~2–4 GB VRAM; ~7× realtime on a 4090; native Windows pip; deterministic per seed). **Caveat
  (verified at source — 2 of 3 LLMs got this WRONG): the pretrained WEIGHTS are CC-BY-NC-4.0**
  (Emilia dataset) → fine for this personal/non-commercial course, NOT clean if it ever goes commercial.
- **#1 license-clean — CosyVoice2/3** (Apache-2.0 code+weights; zero-shot clone; strong published
  WER; repetition-aware sampling + built-in number/symbol normalization). Partly AR, so less
  bulletproof than F5 but still strong; the production-clean pick if commercial use is possible.
- **Not viable as cloners:** Kokoro / MeloTTS / Parler (no zero-shot ref-WAV cloning).
  **Non-commercial weights:** XTTS-v2 (CPML), Fish-Speech, Higgs, Llasa.
- **Migration cost:** any swap re-clones all 6 voices, re-tunes expressiveness, invalidates the
  voicecache, and forces a full re-render. The STT-verify gate is engine-agnostic — keep it regardless.
- **Decision (2026-06):** stay on Chatterbox (mux bug fixed; quality is good). For max reliability
  later, prototype **F5-TTS** and A/B the historically-hard lines via `verify_episode.py` before migrating.

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
# Deterministic CRAFT gate (must PASS before render): word echoes, duplicate headings,
# quiz double-pause, title/variable-text overflow (measured with real fonts), incomplete quotes
.\.venv_tts\Scripts\python.exe tools\lint_script.py            # all eps; --warn shows P2
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
> **Full step-by-step + the episode-spec/scene-type field contract: `course/AUTHORING_NEW_COURSE.md`.**
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
re-run gates → only then render/scale. Record material outcomes in the Changelog (§14).

> **Why concrete seeds/knobs live in THIS file (not only the Bible):** the user's standing
> directive is "remember the seed and inputs." The playbook is the human-readable record of
> record; `course/seed_registry.yaml` is the machine-readable mirror. The Bible holds the
> *creative* spec (world, cast, episode map); this file holds the *reproducible how*.

---

## 10. Known gaps / backlog
See `VNEXT.md` and the detailed, council-prioritized backlog in **§13**. Headline aspiration:
true **character animation** (lip-sync / motion) instead of static avatars + motion graphics.

---

## 11. PRODUCTION RULES (council-ratified — do not repeat these mistakes)
*Ratified by a 5-LLM council (gpt-5.5, gemini-3.1-pro, claude-opus-4.6, gemma3:27b, gpt-oss:20b)
reviewing the shipped v3.1 series. Each rule exists because we got it wrong at least once.
Treat as a script-review + render checklist. "Mistakes are okay; repeating them is not."*

### A. Character & dialogue
- **NULL is never neutral.** Every NULL line drips contempt, menace, disdain, or tactical
  threat. **Test: could Vega or the Narrator say this line? If yes, it fails.** (Killed lines:
  EP08 "Good. Because I never stop, either." / EP7B "Good. Because neither do I." — villain
  agreeing with the hero.)
- **NULL never sounds defeated, bewildered, or helpful.** A repelled attack = fury or tactical
  regrouping, never confusion ("one of these should have worked…") or self-narrated defeat
  ("every move I make, another tower turns my way"). **NULL never teaches** — he covets,
  threatens, mocks; explaining *why* something matters is Vega's job.
- **NULL is present in EVERY episode (≥2 active-threat lines)** — including Act II. An episode
  with 0 NULL lines (EP09) is a bug; the villain looming keeps stakes alive.
- **The NULL cold-open catchphrase escalates/varies each episode** and previews that episode's
  threat vector; never repeat it verbatim across episodes (it was identical 4× in EP01–04).
- **NULL reacts to each flagship control** with a 1-line contemptuous/frustrated cutaway, so
  controls visibly *hurt* him.
- **NOVA never uses a term before it's defined** on-screen, and **never names a guardian persona
  before Vega introduces it** (she may say the family code). Her growth is **shown** (she
  decides; Vega coaches), not just declared in the finale.
- **VEGA stays mentor** (calm authority; never panics/fights/asks novice questions) and should
  hold **≤55% of lines per episode** (redistribute exposition to Narrator/Nova).
- **THE ARCHIVIST speaks ONLY verbatim catalog text + an on-screen citation.** Never paraphrase,
  list section headings, give opinions, or converse. (Killed: EP00 "Identifier. Control.
  Discussion…" — that's paraphrase, not a quote.)

### B. Story & structure
- **Every episode opens with a real-incident cold open** (year + headline + MITRE technique) —
  Act II included (EP08–11 currently have none).
- **Every episode closes on a NULL escalation cliffhanger** that names/implies the next topic.
- **Act II uses the same dramatic engine as Act I:** NULL is actively probing a new target;
  frame each RMF step as a race against NULL (the siege is *coming*, not past).
- **A Citadel "integrity meter" is visible every episode** — drops on NULL beats, rises on
  control beats — so the learner always sees the stakes.
- **Nova's Notebook closes every episode** with consistent styling + a callback to a prior entry
  (spaced repetition).

### C. Pedagogy & quizzes
- **Quiz THINK phase:** narration reads the **full question AND all option texts aloud** (today
  it only says a vague "pause and answer" — fails audio-only/visually-impaired learners).
- **Quiz REVEAL:** read the **full correct ANSWER TEXT (not just the letter) + a one-sentence
  "why"** (incl. why the distractor is wrong). e.g. "The answer is B — SP 800-53B; baselines
  moved out of the main catalog in Rev 5."
- **Frame ≥1 quiz/episode as a NULL challenge** ("I just did X — what stops me?").
- **Never call enhancements "optional"** without the caveat *"unless selected by your baseline or
  tailoring."* **Name ≥1 notable enhancement by official ID** per control beat that references
  enhancements (e.g., IA-2(1), AC-6(1)).
- **Tailoring decisions require Authorizing Official (AO) approval** — say so whenever tailoring
  is mentioned.
- **Never describe the Discussion section as a requirement** (it's informative, not normative).
- Reaffirmed: **baselines live in SP 800-53B** (say it every time); **RMF mapped every episode**;
  always **translate the metaphor back to real-world meaning**; **controls ≥50% of runtime**.

### D. Audio (see §12 for the architecture that enforces these)
- **⭐ VERIFY THE FINAL MP4, NOT JUST UPSTREAM CLIPS.** The most expensive mistake this project
  made: QA'ing per-line clips / beat WAVs / `narr.wav` (ALL clean) while the SHIPPED mp4 dropped
  ~2–3 s of speech. **Run `tools/verify_episode.py [ep...]` on the delivered mp4** (.venv_tts) — it
  transcribes the encoded video (large-v3) and sequence-aligns it to the script, failing on any
  contiguous missing run of *content* words. It is **self-confirming**: number/acronym/letter
  readback is filtered ("800-53"→"853", spelled numbers, control IDs never false-fail), AND every
  candidate missing-run is **re-confirmed by re-transcribing just that region** (via the render
  manifest's per-line start+duration) before it is allowed to fail — because faster-whisper's
  long-form pass omits short isolated lines that ARE present (confirmed: ep04 "Who sets the
  strategy…" / ep06 "What is the edge…" flagged by the full pass, both verbatim-present locally).
  Pass thresholds: `confirmed_missing_run < 4` and `recall ≥ 0.85`. This gate is the LAST line of
  defense before deploy; all 13 episodes must read `OK`.
- **⭐ ROOT CAUSE of the recurring "fucked up audio" = a MUX BUG, not the TTS.** Combining the
  audio mix (`amix` + `sidechaincompress`) and the heavy video graph (`subtitles` + avatar
  overlays + libx264) in ONE ffmpeg `-filter_complex` made ffmpeg **non-deterministically DROP
  audio samples at scene boundaries** (a different amount each run; upstream artifacts stayed
  clean, which is why it hid for so long). FIX (shipped in `build_episode2.py`): **render the
  mixed audio in its OWN ffmpeg pass → `mix.wav`, then mux the video and map that audio RAW
  (`-map 1:a`, no audio filter in the video graph).** Rule: never put a non-trivial audio
  filtergraph and a heavy video filtergraph in the same `-filter_complex`.
- **STT hallucinates repetition loops.** faster-whisper can emit "a threat is a threat is a
  threat…" for perfectly clean audio (a decoding-loop artifact). Re-check a suspected loop by
  **freshly re-extracting just that region** before treating it as a defect. These are EXTRA
  words, never a drop, so `verify_episode.py` is immune (it only fails on MISSING content).
- **Why TTS errors happen:** Chatterbox is an **autoregressive, stochastic** neural TTS — it
  samples audio tokens with temperature, so any take can drop/repeat/garble words (like an LLM).
  It destabilizes most on **ALL-CAPS words** (spells them: "HIGH"→"H-I-G-H"), numbers, IDs, and
  **ultra-short fragments**. Mitigations, in order: harden input (preprocessor), gate output
  (STT verify), reword the unfixable.
- **Self-correcting synth gate (`tts3.synth_line`, `CC_VERIFY=1`):** every freshly synthesized
  clip is transcribed (faster-whisper) and **auto re-rolled up to 4×** if a content word is
  dropped/repeated/garbled/truncated; the best take is kept and anything still failing is logged
  to `tools/_tmp/synth_verify_fails.log` for a reword. This makes bad takes never ship.
- **Preprocessor hardening (`tts.py`):** ALL-CAPS emphasis words are lowercased so they're spoken
  not spelled (acronyms/codes protected); acronyms/IDs/numbers expanded. Keep emphasis in the
  on-screen text, not the spoken text.
- **Audio defects are ACOUSTIC too — STT word-recall alone is NOT enough.** Also verify with
  acoustic metrics: echo autocorrelation (slap-back > ~0.28 = garbled) + spectral rolloff (low =
  muddy). Scan: `tools/audio_scan.py` (acoustic) + `tools/audio_qa.py` (per-clip STT). Example:
  NULL's "Crown Data" passed STT recall but had echo@95ms=0.37 + rolloff 2517 Hz.
- **STT vs audio:** flags on numbers/IDs/compounds/quotes ("800-53"→"853", "oathkeeper"→"Oath
  Keeper", "'log'"→"log") are FALSE positives — the audio is correct. Distinguish with an LLM/human
  pass (the gate ignores number-words + <3-content-word lines to avoid looping).
- **TTS effect chains must not garble speech.** No slap-back echo; don't over-lowpass.
- **Ultra-short fragments**: reword/lengthen (re-rolling won't fix them).
- **Fix one bad clip surgically:** `tools/regen_line.py <ep> <clip>...` re-rolls listed clips +
  re-muxes the episode. The beat cache key includes a **voice fingerprint** so voice/FX changes
  re-synth the affected beats instead of reusing old audio.
- **Never ship unaudited audio.** Every line passes `audio_qa.py` (STT recall) AND `audio_scan.py`
  (acoustic); review flags, regen real defects. Approved audio persists under `course/render/<ep>/lines/`.
- **Final mix passes integrated-loudness + true-peak checks** (loudnorm −16 + limiter).
- **Caption timing** ideally derives from real clip timing (prefer word-level ASR alignment).
- **Pronunciation fixes go in `preprocess()`/the map**, never ad-hoc misspelling in scripts.

### E. Engagement devices (feasible with Pillow + ffmpeg + TTS + SFX)
NULL reaction cutaways · Citadel integrity meter · per-family guardian sigils/icons ·
NULL-challenge quiz framing · split-screen "debate" 2-shots (Vega vs NULL) · escalating
catchphrase · cross-episode callbacks · richer avatar micro-expressions · kinetic emphasis on
key terms. Prioritized in §13.

### F. Encoding / file-size (deployability)
- **NO temporal film grain** (`noise=...:allf=t`). Per-frame noise destroys H.264 inter-frame
  prediction and bloated episodes ~9x (ep00 25MB → 226MB), blowing past **GitHub's 100MB
  per-file limit**. A clean grade (eq + vignette + light unsharp) keeps files deployable
  (~30–45MB for a 7-min 1080p). If you want texture, use a *static* overlay, not temporal noise.
- **Verify file sizes before deploy** (no file > ~95MB for GitHub); episodes are committed for
  Pages, so size is a hard constraint, not a nicety.

---

## 12. INCREMENTAL RENDER ARCHITECTURE (IMPLEMENTED v3.2 — "fix one part, reassemble")
**What shipped:** `build_episode2.py` now persists every beat's artifacts under
`course/render/<epid>/` (gitignored) and rebuilds only what changed:
```
course/render/<epid>/
  manifest.json                 # {version, beats:{idx:{key,dur,starts,ldurs,video,audio}}}
  lines/  b000_l00_NULL.wav  b000_l01_VEGA.wav  ...   # PERSISTENT per-line narration clips
  b000.wav  b000.png  b000.mp4   # per-beat stitched audio, scene still, silent video clip
  b010.wav  b010.mp4 ...
```
- Each beat has a **content hash** (`RENDER_VER` + visual fields + lines + timing/motion params).
  On re-render, if the hash matches and artifacts exist, the beat is **reused** (no TTS, no scene
  render, no encode). Verified: a no-op re-render skips all TTS (2nd EP00 render 9.8 s vs 21.5 s).
- **Editing one line/slide ⇒ only that beat's files rebuild**, then the cheap final mux re-runs.
  Per-line WAVs persist under `lines/` for inspection. Bump `RENDER_VER` to force a full rebuild
  when render *logic* changes.
- Final mux (concat + music duck + SFX + avatars + burned captions + **cinematic grade** +
  **audio master**) always runs; it's fast relative to synth/scene render. **It is TWO ffmpeg
  passes:** (A) audio-only filtergraph → `mix.wav`; (B) video-only filtergraph + audio mapped RAW.
  This decoupling is mandatory — see §11.D (one combined `-filter_complex` drops audio samples).
  Always run `tools/verify_episode.py` on the result before packaging/deploy.

**Future enhancement (not yet built):** promote the per-line clips to a richer manifest
(`text_hash`, `stt_recall`, `loudness`, `approved`, `locked`) with a `--regen-line` candidate→
promote workflow + an STT gate, so individual lines can be approved/locked and auto-audited.

---

## 13. Council review findings + prioritized backlog (2025 v3.1 review)
**Council verdicts:** Audio (gpt-5.5) = *BLOCK for scaling*; Pedagogy (gemini) =
*APPROVE-WITH-CHANGES*; Story/Engagement (opus) = *Narrative B-, Character B, Engagement C+*.
Act I (EP00–07) is genuinely engaging; **Act II (EP08–11) is the weak spot** (NULL absent, no
cold opens, Nova's leadership told-not-shown). STT audit: word-dropping mostly fixed (good); the
residual audio risk is pronunciation/prosody/sync + the *cost of fixing one mistake*.

**Confirmed character violations to fix (verified vs scripts):** EP02 "every move I make…another
tower" (NULL helpless); EP07 "one of these should have worked…" (bewildered); EP00 map "no
second copy of trust" (teaching); EP05 MA-4 "was going to be my way in" (defeated); EP08/EP7B
"Good. Because…" (agreeable); EP00 anatomy Archivist line (non-verbatim); EP01–06 Nova names
personas before intro; EP09 zero NULL lines.

**Prioritized backlog — status after the v3.2 implementation pass:**
1. **Quiz read-aloud** — ✅ DONE. Think phase reads full Q + all options; reveal reads the
   correct answer TEXT + a one-line `why` (added to all 30 quizzes).
2. **NULL character-line fixes** — ✅ DONE. All flagged violations rewritten to drip contempt;
   escalating per-episode catchphrase (EP02–04).
3. **Pedagogy accuracy patches** — ✅ DONE. Enhancement "optional" bullet caveated (EP00),
   AO-approval added to tailoring (EP10), MFA cited as IA-2(1)/(2) (EP01), Archivist
   non-verbatim heading-list removed (EP00).
4. **Act II revival** — ◐ PARTIAL. EP09 now has NULL presence (was zero); full Act II cold-open
   beats + Nova on-screen decision moments still TODO.
5. **Incremental render architecture** — ✅ DONE (§12): persistent per-beat/per-line artifacts
   under `course/render/<ep>/` + content-hash rebuild. (STT gate + per-line approve/lock = future.)
6. **Engagement: NULL cutaways + Citadel integrity meter + guardian sigils** — ☐ TODO (deferred:
   `scene.py` work; higher risk; do as a focused next pass).
7. **Cinematic + audio polish** — ◐ PARTIAL. ✅ cinematic color grade (contrast/saturation/
   vignette/fine grain/light sharpen) + ✅ audio master (loudnorm −16 + true-peak limiter).
   Still TODO: `xfade` crossfades (kept hard cuts for A/V-sync safety), per-seam microfades,
   word-level caption alignment.

> Re-rendering is cheaper now (§12 incremental), but still batch big content changes into ONE
> pass after the gates + a council spot-check, per §8.

### Cinematic ceiling — PROVEN finding (don't re-attempt blindly)
**True "Hollywood" = animated, lip-synced characters in dynamic scenes. This pipeline's format
(designed slides + Ken-Burns + a ~150px corner character portrait + TTS) has a hard ceiling
well below that, and color grading / HUD / audio mastering raise polish but NOT the format.**
- **Tested locally:** 2D viseme lip-flap on the avatars via IP-Adapter (matched closed/open mouth
  frames, same seed, scale 0.8). Result: identity holds, but (a) the corner avatar is too small
  for lip motion to read, and (b) frame-to-frame head/hair/eye drift causes a visible *wobble*.
  **Verdict: not worth it in the corner-portrait format.** Clean lip-sync models (Wav2Lip/
  SadTalker) are trained on real faces and tend to fail/look uncanny on anime art.
- **The real path to cinematic** (a different, larger project — needs the user's go-ahead):
  1. **Redesign to large character "stage" scenes** (visual-novel close-ups), not corner avatars,
     so character motion can actually be seen.
  2. **Clean animation**, one of: SDXL **mouth-inpainting** visemes (mask the mouth so only it
     changes → no wobble) driven by an audio phoneme/amplitude envelope; a rigged 2D puppet; or a
     dedicated talking-head model that handles stylized faces.
  3. **Living backgrounds** via image-to-video (SVD/AnimateDiff on the 4090) behind transparent
     UI — reliable cinematic motion, but requires separating the UI layer from the background in
     `scene.py`.
  4. **Editing grammar:** shot variety, push-ins, match cuts, crossfades (xfade was dropped for
     A/V-sync safety; revisit now that beat durations are known via the §12 manifest).
- **Honest status:** what ships is a **premium animated explainer**, not a cinematic animated
  series. Calling it "Hollywood" would be inaccurate.

---

## 14. Changelog of learnings
- **2026-06 — quiz UX: transparent click-hotspots laid EXACTLY over the video's own option
  boxes (no blur over the burned-in subtitles).** The user wanted the interactive answers to be
  *just the buttons* — clickable regions sitting precisely on the boxes the video already renders,
  with a hover outline + pointer cursor — instead of a full-screen translucent/blurred panel that
  covered the captions. Implementation: `scene.quiz_layout(beat)` is now the **single source of
  truth** for option-box geometry (kicker@175, question wrapped from y=250 FB58/1.2/max1500, +30,
  then 96px boxes every 120px, 1240px wide, centered); `s_quiz` draws from it (pixel-identical, so
  **no re-render needed**) and `build_episode2` emits **normalized `opt_rects`** (`[x,y,w,h]` as
  fractions of 1920x1080) into each `cues.json` quiz cue. `watch.html` replaced `#ov` (the blur
  panel) with `#qhot`, a transparent layer of `.hot` buttons positioned by `opt_rects` as
  percentages of the 16:9 stage (the video fills the stage with no letterbox, so % maps 1:1 to the
  frame). Hover/focus draws a cyan outline + glow; a per-view answer tints the picked box mint/red
  and highlights the correct one; the lock-in pause now pulses the hotspots and shows a status line
  **below** the stage (never over the captions). Hotspots are live from `t_question` (the moment the
  boxes appear), not just at lock-in. The hotspot corner radius is driven by a `--qhotr` CSS var
  (a `ResizeObserver` sets it to `stageWidth/120` = the video's 16px-in-1920-frame box radius), so
  the corners keep matching the video's when the window/video is resized — a fixed `px` radius drifts.
  The 30 existing cues were back-filled by recomputing
  `opt_rects` from each cue's own `q`+`options` (same `quiz_layout`), so the feature shipped without
  re-rendering any mp4. Added Playwright tests: hotspots **align within 1.5%** of the rendered boxes,
  the layer is **transparent with no backdrop blur**, options are **clickable the moment they
  appear**, and the **corner radius rescales** with the stage. 54/54 across Chromium/Firefox/WebKit.
  Lesson: to overlay interactive UI on rendered video, export the renderer's geometry into the cue
  file (never re-derive font metrics in JS) and scale fixed-px chrome like the radius to the display.
- **2026-06 — interactive quiz never showed for returning viewers (root cause) + a regression
  gate + a WebKit test-harness nudge.** The user reported repeatedly that "the interactive test is
  never displayed." Root cause in `watch.html`: the `timeupdate` open loop gated on
  `if(!answered.has(q.n))`, and `answered` is hydrated from `localStorage.cc_ans`, so **anyone who
  had ever answered a quiz (i.e. the returning user) had it permanently suppressed.** My Playwright
  tests missed it because they used fresh browser contexts with empty storage. FIX: **decouple
  DISPLAY from SCORE.** The quiz now always opens at `t_question` (regardless of past answers);
  a per-view `responded` flag (reset in `openQuiz`/`closeQuiz`) gates the pause-at-lock-in and
  the one-time scoring (`ansStore[ep][n]` still counts a question only once). Added a **regression
  test** that presets `localStorage.cc_ans` via `page.addInitScript` before load and asserts the
  overlay still opens with all options — it FAILS on the old code, PASSES now. Lesson:
  **persistent-state features need a "returning user" (seeded-storage) test, not just fresh-context
  tests.** Separately hardened `ready()` in the harness: WebKit defers `preload="metadata"` under
  range-server contention (readyState stuck at 0 → 30 s timeouts), so `ready()` now waits for app
  init (speed buttons) first, then **nudges a muted `v.load()`** before waiting on `readyState>=1`.
  Suite is deterministic again: **45/45 across Chromium/Firefox/WebKit in ~17 s** (was flaky 36 s+).
  watch.html is a static asset — no re-render needed; returning users may need a hard-refresh or the
  "↺ reset" link to clear stale storage, but the new code shows quizzes regardless of prior answers.
- **2026-06 — viewer-reported polish pass + deterministic craft gate + provenance.** Ran a 3-LLM
  screenplay-review council over all 13 transcripts and applied consensus fixes: NOVA kept in the
  learner role (she no longer recites control IDs/history before they're taught — the systemic
  "preview/summary line" slip), NULL kept menacing (no coaching/conceding), word echoes removed
  (incl. the EP00 "exist/exist"). Built **`tools/lint_script.py`** — a deterministic CRAFT gate
  (run before every render) for whole CLASSES of defect: duplicate section/map headings
  (EP01-07 each repeated the layer title -> map beats renamed "THE CITADEL MAP"), the
  double-spoken quiz "Pause and answer" (assembler appends one, so scenario lines must not),
  title/variable-text **overflow measured with the real fonts** (IA-2's 56-char official name
  overflowed), and **incomplete Archivist quotes** truncated mid-list at a colon (PE-3/AU-2/AT-2/
  PS-4/PL-2/PM-9/SA-8 — replaced with complete verbatim lead-in + first sub-requirement, still
  passing verify_script). Fixed `scene.py` to **auto-shrink/fit every variable single-line text**
  (titles, guardian name/persona, quiz options, mnemonics, term, cites) via `fit_font`/`draw_fit`.
  Added **source provenance**: control cards show "NIST SP 800-53r5 · §3.N" (family->section map).
  Rebuilt the **interactive quiz** (watch.html) to play-in-background: the quiz shows while the
  video keeps reading, pauses only at the lock-in point if unanswered, skips to the reveal once
  answered. All web behavior verified by the Playwright harness (42/42 across Chromium/Firefox/
  WebKit). Lesson (user, emphatic): **when you own a mistake, build a GATE for the whole class —
  don't just fix the one example.** Bumped RENDER_VER v3.3 -> v3.4 (scene.py changed).
- **2026-06 — reusable SKILLS library + work-item backlog + web-player upgrades.** Captured the
  pipeline as discoverable **skills** in `.copilot/skills/` (screenplay-review, accuracy-verification,
  base-avatar-creation, avatar-expression-variants, tts-narration, music-bed, video-assembly,
  quiz-and-reference, course-production orchestrator), junctioned into `~/.copilot/skills/` for
  local discovery and committed so they travel with the repo (instructions point agents there).
  Durable backlog now lives in **GitHub issues** (labels skill/pipeline/content/web); agents run
  `gh issue list` for work. Web player (`watch.html`): added **playback-speed** control
  (persisted, pitch-preserved, keyboard, re-applied per source load), **sidebar chapter list**
  with `m:ss` markers under the active episode, and **poster thumbnails** (`tools/make_posters.py`,
  no more black screens). Established a reusable **Playwright cross-browser test harness**
  (`tools/webtest`, Chromium/Firefox/WebKit, range-capable static server) — chose Playwright over
  Puppeteer specifically for real WebKit (pitch-preservation is engine-dependent); 30/30 green.
  Also kicked off a 3-LLM **screenplay-review council** over all 13 transcripts — confirmed the
  EP00 "exist" echo and found a systematic NOVA-as-learner slip (she drops control IDs/history
  before they're taught) to fix in the scripts.
- **2026-06 — THE mux bug (root cause of the "still fucked up audio") + final-mp4 verification.**
  Despite all upstream audio being clean (per-line clips, beat WAVs, `narr.wav`, and even an
  isolated audio-only mix ALL transcribed perfectly), the SHIPPED mp4 dropped ~2.8 s of speech at
  a scene boundary (VEGA's "Picture an organization's information as a walled…"). Bisected it to a
  **ffmpeg filtergraph bug**: putting the audio mix (`amix`+`sidechaincompress`) and the heavy
  video graph (`subtitles`+avatar overlays+libx264) in ONE `-filter_complex` **non-deterministically
  drops audio samples**. FIX: **two-pass mux** — audio-only graph → `mix.wav`, then video graph with
  audio mapped RAW (`-map 1:a`). Added `tools/verify_episode.py` (transcribe the FINAL mp4, align to
  script, fail on contiguous missing *content* runs; number/acronym/letter readback filtered). Also
  learned: **faster-whisper hallucinates repetition loops** ("a threat is a threat is a threat…") on
  clean audio — re-extract the region to confirm before chasing it. Re-rendered all 13 with the
  two-pass mux; every episode passes `verify_episode.py`. Lesson: **QA the delivered artifact, not
  upstream intermediates.** Also ran a **3-LLM council on better TTS engines** (§5): F5-TTS is the
  most reliable architecture (NAR) but its weights are CC-BY-NC; CosyVoice2/3 is the Apache-clean
  pick; the recurring pain was the mux, not Chatterbox, so no engine swap was needed.
- **2025 — full audio QA + self-correcting gate.** Root cause of recurring audio errors: Chatterbox
  is autoregressive/stochastic and garbles ALL-CAPS/numbers/short fragments. Transcribed all 642
  line clips (large-v3) and compared each to the script with **3 LLM agents + a deterministic
  check**; fixed every real defect (~38 re-rolled, 16 reworded for systematic failures). Permanent
  fix: ALL-CAPS preprocessor hardening + a **synth-time STT-verify-and-retry gate** (tts3) so bad
  takes never ship, + multi-clip `regen_line.py`. Lesson: gate audio AT SYNTH, and distinguish
  real garbles from STT number/acronym/compound/quote artifacts (see §11.D).
- **2025 — audio QA + repair pass.** Found the reported garble: NULL's FX chain had a 95 ms
  slap-back echo + lowpass 4600 that smeared speech (objective: echo 0.37, rolloff 2517 Hz) —
  STT word-recall had passed it. Fixed the FX (subtle echo, lowpass 7200), re-rendered (echo gone
  on all 45 NULL clips). Built permanent QA tools: `tools/audio_scan.py` (acoustic echo/clip/
  muddiness) + `tools/audio_qa.py` (per-clip STT) + `tools/regen_line.py` (surgical one-clip
  re-roll + re-mux); added a **voice fingerprint** to the beat cache key so voice/FX changes
  re-synth. Full per-clip pass caught 6 word-level defects (garbled/dropped/repeated); fixed by
  re-roll, and reworded 2 ultra-short fragments Chatterbox can't synth. Rules in §11.D.
- **2025 — v3.3 engagement + cinematic pass.** Added the **Citadel integrity-meter HUD**
  (running stakes; dips on attacks, rises on controls) and honest **"FROM THE FIELD" Act II cold
  opens** (EP08–11, no fabricated breaches) with NULL menace. **Proved** (PoC) that corner-avatar
  lip-sync isn't viable locally (too small to read + frame wobble) — documented the real path to
  cinema in §13. **Caught at verify-before-deploy:** temporal film grain bloated episodes ~9x
  (ep00 25→226MB, over GitHub's 100MB limit) → removed grain, kept the clean grade (§11.F);
  ep00 back to ~41MB. Honest framing: premium animated explainer, not "Hollywood."
- **2025 — v3.2 production upgrade (implementation).** Built the **incremental render
  architecture** (§12): per-beat + per-line artifacts persist under `course/render/<ep>/`,
  content-hash keyed, so editing one part rebuilds a few files (verified: no-op re-render does
  zero TTS). Added a **cinematic color grade** + **audio master** (loudnorm −16 / true-peak
  limiter) to the final mux, and **quiz read-aloud** (full Q+options, then correct-answer text +
  a `why`). Script fixes: NULL character violations rewritten + escalating catchphrase; EP09
  NULL presence; pedagogy patches (enhancement caveat, AO approval, IA-2(1)/(2), Archivist
  verbatim). Deferred to a focused next pass: integrity-meter HUD, guardian sigils, NULL cutaway
  scenes, full Act II cold opens, xfade crossfades, word-level caption alignment. Lesson:
  **visual-QA a rendered frame before a full batch** — it caught the on-screen "optional
  enhancements" bullet that a `say`-only check missed.
- **2025 — full-series council review (5 LLMs).** Reviewed shipped v3.1 across audio, pedagogy,
  story, character, quizzes, and regeneration. Recorded §11 Production Rules, §12 audio
  regeneration architecture, and §13 findings/backlog. Headline mistakes captured: NULL breaks
  character (agreeable/defeated/teaching lines) + vanishes in Act II; quizzes don't read the
  question/options/answer aloud; enhancements wrongly called "optional"; audio has no STT gate
  and clips aren't persistent/approvable.
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
