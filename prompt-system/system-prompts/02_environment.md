# 02 — Environment → `capabilities.json`

Set up the local environment for the detected hardware tier **before** any live/demo run. Avoid surprise first-run downloads in front of an audience.

Run commands from the project root: the folder with `AGENTS.md`, `engine/`, and `system-prompts/`.

---

## Goal
Write `capabilities.json`, create a Python venv, install tier-appropriate dependencies, fetch voice models, and run preflight.

Quality is identical across tiers. Only voice timbre, avatar fidelity, and speed vary.

---

## Environment variables
Windows PowerShell:

```powershell
$env:PYTHONUTF8 = "1"
$env:CC_PROJECT = (Get-Location).Path
$env:CC_VERIFY = "1"
```

macOS/Linux:

```bash
export PYTHONUTF8=1
export CC_PROJECT="$PWD"
export CC_VERIFY=1
```

`CC_THEME` normally stays unset; `engine/theme.py` auto-discovers `theme.json` or `course/theme.json`.

---

## 1 — Probe the machine

```powershell
python engine/probe.py
```

This writes `capabilities.json`; read `overall` and `tiers` (`tts`, `avatars`, `stt`, `stt_compute`).

Tier rules from `engine/probe.py`: TTS is `chatterbox` at CUDA + 6GB VRAM, else `piper`; avatars are `sdxl_ipa` at CUDA + 10GB, `sd_turbo` at CUDA + 4GB, else `illustrated`; STT is `large-v3`, `small`, or `base`.

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
python -m pip install Pillow numpy faster-whisper
ffmpeg -version
ffprobe -version
```

> Windows + `faster-whisper`: if the audio gate later fails with `DLL load failed`, install the
> Microsoft Visual C++ Redistributable (x64): https://aka.ms/vs/17/release/vc_redist.x64.exe
> Node.js is NOT required — only the optional developer contract test uses it, so ignore
> `node: false` in the probe report.

---

## 4 — Install TTS for the tier
GPU / `tiers.tts = chatterbox`:

```powershell
python -m pip install chatterbox-tts
python -m pip install torch --index-url https://download.pytorch.org/whl/cu124
$env:CC_TTS = "chatterbox"
```

CPU / `tiers.tts = piper`:

```powershell
python -m pip install piper-tts
New-Item -ItemType Directory -Force assets\voices | Out-Null
curl.exe -L -o assets\voices\en_US-lessac-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
curl.exe -L -o assets\voices\en_US-lessac-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
$env:CC_TTS = "piper"
```

macOS/Linux: use `mkdir -p assets/voices`, `curl -L`, and `export CC_TTS=...`.

---

## 5 — Install avatar deps only if needed
If avatars are opted in and `tiers.avatars` is `sdxl_ipa` or `sd_turbo`:

```powershell
python -m pip install diffusers transformers accelerate safetensors
```

If `tiers.avatars = illustrated`, install no diffusion packages.

---

## 6 — Pre-download before demo/live use

```powershell
python engine/probe.py preflight
```

Read the printed plan, then **trigger the first-run model downloads NOW** (never mid-demo):

```powershell
# voice model + the audio-gate STT model (synthesize one throwaway line; the FIRST line is slow
# because it also loads the verify model — this is normal):
python engine/tts.py
# avatars, only if opted in (downloads SDXL/Turbo on a GPU tier; instant on the illustrated tier):
python engine/gen_avatars.py
```
macOS/Linux: same commands with `python3`.

---

## Self-review
- Does `capabilities.json` exist?
- Are deps matched to the detected tier and selected options?
- Are `ffmpeg` and `ffprobe` on PATH?
- Is `CC_VERIFY=1` set?
- Did `python engine/probe.py preflight` run before live/demo use?

Then route to `system-prompts/03_truth_layer.md`.



