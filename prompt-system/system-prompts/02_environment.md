# 02 — Environment → `capabilities.json`

Install the **high-quality** models (chatterbox voice, SDXL avatars, large-v3 audio-QA) **before** any
live/demo run. These run on **GPU or CPU** — hardware only affects SPEED, not quality. Avoid surprise
first-run downloads in front of an audience.

Run commands with `CC_PROJECT` set to your project folder (`projects/<slug>`); the engine writes there.

---

## Goal
Write `capabilities.json`, create a Python venv, install the high-quality dependencies, fetch the
voice reference clips, and run preflight so the first render is fast.

**Quality is fixed HIGH on every machine.** A missing GPU makes rendering slower, not worse — you
still install and use the same high-quality models. Only apply a downgrade (piper/illustrated/small
STT) if the user explicitly asks to trade quality for speed.

---

## Environment variables
Windows PowerShell:

```powershell
$env:PYTHONUTF8 = "1"
$env:CC_PROJECT = "projects\<slug>"   # your course folder (create it if new)
$env:CC_VERIFY = "1"
```

macOS/Linux:

```bash
export PYTHONUTF8=1
export CC_PROJECT="projects/<slug>"
export CC_VERIFY=1
```

`CC_THEME` normally stays unset; `engine/theme.py` auto-discovers the project's `theme.json`. Do NOT
set `CC_TTS`/`CC_AVATARS`/`CC_STT_MODEL` here — they default to the high-quality models.

---

## 1 — Probe the machine

```powershell
python engine/probe.py
```

This writes `capabilities.json`. Read `speed` (`fast`/`ok`/`slow`) and `recommended` (always the
high-quality models: `chatterbox`, `sdxl`, `large-v3`). If `speed` is `slow` (CPU-only), tell the user
rendering will take longer but stays full quality; only downgrade with their approval
(`downgrades_opt_in` lists the switches).

---

## 2 — Create and activate a venv
Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

macOS/Linux: `python3 -m venv .venv`, then `. .venv/bin/activate`, then `python -m pip install --upgrade pip`.

If PowerShell blocks activation: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again.

---

## 3 — Install required tooling
**ffmpeg** (with ffprobe) must be on PATH — install it first:
- Windows: `winget install Gyan.FFmpeg`  (or `choco install ffmpeg`)
- macOS: `brew install ffmpeg`  ·  Linux: `sudo apt install ffmpeg`

```powershell
python -m pip install Pillow numpy jsonschema faster-whisper
ffmpeg -version
ffprobe -version
```

> Windows + `faster-whisper`: if the audio gate later fails with `DLL load failed`, install the
> Microsoft Visual C++ Redistributable (x64): https://aka.ms/vs/17/release/vc_redist.x64.exe
> Node.js is NOT required — only the optional developer contract test uses it, so ignore
> `node: false` in the probe report.

---

## 4 — Install the HIGH-QUALITY voice engine (chatterbox — GPU or CPU)
This is the default on every machine. On a CUDA GPU, install the GPU torch build; on CPU, the plain
build (same quality, slower):

```powershell
python -m pip install chatterbox-tts
# GPU (CUDA):
python -m pip install torch --index-url https://download.pytorch.org/whl/cu124
# CPU only (no CUDA): just `python -m pip install torch`
```

Leave `CC_TTS` unset (chatterbox is automatic). **Only** install Piper if the user has approved the
fast/robotic downgrade — see `06_voices.md` (then `pip install piper-tts` + fetch an `.onnx` voice and
set `CC_TTS=piper`).

---

## 5 — Install avatar deps (SDXL — GPU or CPU), only if avatars are opted in
SDXL is the default high-quality avatar path and runs on CPU too (slower, one-time):

```powershell
python -m pip install diffusers transformers accelerate safetensors
```

If the user approved the instant illustrated downgrade (`CC_AVATARS=illustrated`), no diffusion
packages are needed. If avatars are skipped entirely, install nothing here.

---

## 6 — Pre-download before demo/live use

```powershell
python engine/probe.py preflight
```

Read the printed plan, then **trigger the first-run model downloads NOW** (never mid-demo):

```powershell
# high-quality voice weights + the audio-gate STT model (synthesize one throwaway line; the FIRST
# line is slow because it also loads the verify model — this is normal, especially on CPU):
python engine/tts.py
# avatars, only if opted in (downloads SDXL ~6GB on first run; GPU or CPU):
python engine/gen_avatars.py
```
macOS/Linux: same commands with `python3`.

---

## Self-review
- Does `capabilities.json` exist, and did you note the `speed` (warn the user if `slow`)?
- Is the **high-quality** chatterbox voice installed (not a silent piper fallback)?
- Are `ffmpeg` and `ffprobe` on PATH?
- Is `CC_VERIFY=1` set, and are `CC_TTS`/`CC_AVATARS` unset (unless the user approved a downgrade)?
- Did `python engine/probe.py preflight` + the trigger commands run before live/demo use?

Then route to `system-prompts/03_truth_layer.md`.


