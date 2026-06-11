# Copilot instructions — NIST 800-53 "Cyber Citadel" course

This repo builds a **video training series** teaching NIST SP 800-53 Rev 5 in a fun,
memorable, accurate way. The learner (@darinh) **prefers video/visuals**. Work
autonomously; review plans + artifacts with a **council of multiple agents and LLMs**
(adversarial review → consensus) before proceeding.

## Read first
- `course/PRODUCTION_BIBLE.md` — the authoritative creative + technical spec (concept,
  cast, 8-episode map, accuracy rules, pipeline). Follow it.
- `course/GENERATION_PLAYBOOK.md` — **hard-won learnings**: reusable recipes, exact prompts,
  seeds, voice knobs, pitfalls, the review process, **§11 Production Rules**, **§12 incremental
  render architecture**. Read before producing/regenerating anything.
- `course/AUTHORING_NEW_COURSE.md` — operator's manual for reusing this engine on a **different
  topic** (pipeline, step-by-step, and the episode-spec/scene-type field contract).
- Session plan: `~/.copilot/session-state/<id>/plan.md`.

## Keep the playbook current (do not skip)
Whenever you discover a non-obvious technique, fix a painful bug, settle a creative/voice/
visual decision, or change a seed/prompt/knob, **update `course/GENERATION_PLAYBOOK.md` in the
same change** (and its Changelog). Knowledge that lives only in chat context is lost at the
next compaction. This is the user's explicit, standing priority.

## Golden rules
1. **Accuracy is non-negotiable.** All control IDs/titles/text come from
   `course/data/truth.json` (built from the official OSCAL catalog by `tools/build_truth.py`),
   NOT from LLM memory or loose PDF text. Archivist quotes are verbatim + cited on screen.
   Baselines live in **SP 800-53B**, not 800-53. Before rendering, run BOTH gates:
   `tools/verify_script.py` (deterministic — on-screen control facts vs catalog) and
   `tools/audit_narration.py` (local-LLM hostile-auditor — narrative claims).
2. **Fully local pipeline.** ollama (LLM drafting/review), local TTS (**Chatterbox** current
   via `tts3.py`; Kokoro/piper = fallback), Pillow (scenes), ffmpeg (motion/assembly). No
   copyrighted audio/art; synthesize/curate music locally (CC-BY, attributed).
3. **Templated production.** Scenes are declarative types rendered by `tools/scene.py`;
   episodes are JSON specs assembled by `tools/build_episode2.py` (v2; `build_episode.py` is
   the older path). Don't hand-render frames.
4. **Retention-first.** Quizzes per episode + final Guardian Roll Call; RMF mapping every
   episode; translate the Citadel metaphor back to real-world meaning.

## Definition of done (every session)
Before concluding ANY session, ask: did I change pipeline code, prompts, seeds, voice knobs,
or settle a creative/visual/voice decision? If **yes**, you MUST append a Changelog entry to
`course/GENERATION_PLAYBOOK.md` (and update `course/seed_registry.yaml` if a seed/prompt/knob
changed) **before exiting**. Render ONE episode and spot-check before any bulk re-render.

## Key tools
- `tools/build_truth.py` → `course/data/truth.json` (authoritative content).
- `tools/verify_script.py` → **deterministic** accuracy gate (on-screen control facts vs
  `truth.json`); `tools/audit_narration.py` → local-LLM hostile-auditor of narrative claims.
  Run both on every script before render.
- `tools/llm.py` / `tools/council_ollama.py` → ollama helpers (drafting + local-LLM review).
- `tools/tts3.py` → **current** voice engine (Chatterbox, MIT; zero-shot clones of
  license-clean refs in `tools/voices_ref/`). `tts2.py` (Kokoro) / `tts.py` (piper) = fallback;
  all share the `tts.py` pronunciation pre-processor. `CC_TTS` env switches engine.
- `tools/gen_avatars.py` (fixed-seed base portraits) + `tools/gen_avatar_ipa.py` (IP-Adapter
  expression variants, image-conditioned on the base for **same-character** consistency) +
  `tools/make_avatars.py` (frame into cards).
- `tools/scene.py` → Pillow scene renderer (1920x1080, declarative scene types).
- `tools/build_episode2.py` → spec JSON → mp4 + srt (avatars, music, captions). `build_episode.py` = older path.

## Environment (Windows)
- Use Windows paths (backslashes). `$env:PYTHONUTF8=1` for scripts.
- Two venvs: `.venv_img` (SDXL/diffusers/IP-Adapter, image gen) and `.venv_tts`
  (Chatterbox/torch cu124, voice). piper voices in `tools/voices/`; clone refs in `tools/voices_ref/`.
- ollama models: gpt-oss:120b (heavy/may OOM — prefer 20b/gemma3:27b for reliability),
  gpt-oss:20b, gemma3:27b, qwen3:8b.
- ffmpeg/ffprobe 8.0, python 3.11.
- **Render ONE episode and spot-check before bulk re-rendering** (full re-renders are expensive).

## Council
Use the `task` tool with varied `model` (gpt-5.5, gemini-3.1-pro-preview, claude-sonnet-4.5)
+ ollama (`tools/council_ollama.py`) for local-LLM diversity. Reach consensus before scaling.
