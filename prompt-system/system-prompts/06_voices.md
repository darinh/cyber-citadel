# 06 — Voices → `assets/voices/*` + `theme.json cast[].voice`

Give each character a license-clean voice. Use Chatterbox zero-shot cloning on GPU, Piper ONNX voices on CPU.

---

## Goal
For every speaking character in `theme.json.cast[]`, configure `cast[].voice` so `engine/tts.py` can synthesize dialogue.

`engine/tts.py` consumes:

```json
{"ref":"<reference wav>","exaggeration":0.5,"cfg_weight":0.5,"temperature":0.8,"piper":"<onnx voice name>","effects":"<optional ffmpeg filters>","length":1.0}
```

Use only fields needed by the selected backend.

---

## Environment
Windows PowerShell:

```powershell
$env:PYTHONUTF8 = "1"
$env:CC_PROJECT = (Get-Location).Path
$env:CC_VERIFY = "1"
python engine/probe.py
```

`CC_VERIFY=1` keeps the self-correcting audio gate on. Chatterbox re-rolls lines that Faster-Whisper hears as garbled, repeated, or truncated.

---

## GPU tier: Chatterbox
If `capabilities.json.tiers.tts` is `chatterbox`, use license-clean reference clips:

```text
assets/voices/<ref>.wav
```

Do not use copyrighted voices, celebrity clips, game/movie audio, or impersonations.

Theme example:

```json
{
  "name": "MENTOR",
  "role": "mentor",
  "caption_color": "gold",
  "voice": {"ref": "mentor.wav", "exaggeration": 0.6, "cfg_weight": 0.45, "temperature": 0.8}
}
```

Knobs: higher `exaggeration` is more expressive; lower `cfg_weight` can be looser; higher `temperature` adds variation. Use `effects` sparingly; defaults already master audio, and antagonist-like roles get a built-in effect.

Set `$env:CC_TTS = "chatterbox"`.

---

## CPU tier: Piper
If `capabilities.json.tiers.tts` is `piper`, place `.onnx` voices in:

```text
assets/voices/
```

`cast[].voice.piper` is the `.onnx` filename without extension.

Theme example:

```json
{
  "name": "MENTOR",
  "role": "mentor",
  "caption_color": "gold",
  "voice": {"piper": "en_US-lessac-medium", "length": 1.0}
}
```

Set `$env:CC_TTS = "piper"`.

If needed, fetch Piper model + config:

```powershell
New-Item -ItemType Directory -Force assets\voices | Out-Null
curl.exe -L -o assets\voices\en_US-lessac-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
curl.exe -L -o assets\voices\en_US-lessac-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

---

## Pronunciations
Add domain pronunciations to `theme.json`:

```json
{"pronunciations":{"OSCAL":"oss cal"},"spell_acronyms":["API","RMF"]}
```

`engine/tts.py` applies these to spoken narration only and speaks IDs like `KN-1` as letters plus numbers.

---

## Smoke test
Run after `theme.json` is valid:

```powershell
python engine/theme.py
python engine/tts.py
```

Expected output includes selected engine, cast voice names, and `.cache\tts_smoke\*.wav` files.

---

## Self-review
- Are reference clips and Piper models license-clean?
- Does each speaking cast member have a usable `voice` config?
- Is `CC_VERIFY=1` set?
- Did `python engine/tts.py` synthesize smoke-test wavs?
- Are domain terms handled in `pronunciations` or `spell_acronyms`?

Then route to `system-prompts/07_music_and_sfx.md`.



