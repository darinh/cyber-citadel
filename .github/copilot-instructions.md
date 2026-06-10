# Copilot instructions — NIST 800-53 "Cyber Citadel" course

This repo builds a **video training series** teaching NIST SP 800-53 Rev 5 in a fun,
memorable, accurate way. The learner (@darinh) **prefers video/visuals**. Work
autonomously; review plans + artifacts with a **council of multiple agents and LLMs**
(adversarial review → consensus) before proceeding.

## Read first
- `course/PRODUCTION_BIBLE.md` — the authoritative creative + technical spec (concept,
  cast, 8-episode map, accuracy rules, pipeline). Follow it.
- Session plan: `~/.copilot/session-state/<id>/plan.md`.

## Golden rules
1. **Accuracy is non-negotiable.** All control IDs/titles/text come from
   `course/data/truth.json` (built from the official OSCAL catalog by `tools/build_truth.py`),
   NOT from LLM memory or loose PDF text. Archivist quotes are verbatim + cited on screen.
   Baselines live in **SP 800-53B**, not 800-53. Run `tools/verify_script.py` (hostile
   auditor) on every script before rendering.
2. **Fully local pipeline.** ollama (LLM drafting/review), piper (TTS), Pillow (scenes),
   ffmpeg (motion/assembly). No copyrighted audio; synthesize music locally.
3. **Templated production.** Scenes are declarative types rendered by `tools/scene.py`;
   episodes are JSON specs assembled by `tools/build_episode.py`. Don't hand-render frames.
4. **Retention-first.** Quizzes per episode + final Guardian Roll Call; RMF mapping every
   episode; translate the Citadel metaphor back to real-world meaning.

## Key tools
- `tools/build_truth.py` → `course/data/truth.json` (authoritative content).
- `tools/llm.py` → ollama helper (`ask(model, prompt, system=...)`).
- `tools/tts.py` → piper narration + SRT (acronym pronunciation preprocessor).
- `tools/scene.py` → Pillow scene renderer (1920x1080).
- `tools/build_episode.py` → spec JSON → mp4 + srt.

## Environment (Windows)
- Use Windows paths (backslashes). piper voices in `tools/voices/`.
- ollama models: gpt-oss:120b (heavy/may OOM — prefer 20b/gemma3:27b for reliability),
  gpt-oss:20b, gemma3:27b, qwen3:8b.
- ffmpeg/ffprobe 8.0, python 3.11. `$env:PYTHONUTF8=1` for scripts.

## Council
Use the `task` tool with varied `model` (gpt-5.5, gemini-3.1-pro-preview, claude-sonnet-4.5)
+ ollama (`tools/council_ollama.py`) for local-LLM diversity. Reach consensus before scaling.
