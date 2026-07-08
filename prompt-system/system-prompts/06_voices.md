# 06 — Voices → `assets/voices/*` + `theme.json cast[].voice`

Give each character a license-clean, **high-quality** neural voice. **Chatterbox is the default on
GPU AND CPU** — on CPU it is slower, not lower quality. Piper is a robotic downgrade used **only if
the user explicitly approves it**.

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
Windows PowerShell (macOS/Linux: `export VAR=value`, `python3`):

```powershell
$env:PYTHONUTF8 = "1"
$env:CC_PROJECT = (Get-Location).Path   # your projects/<slug> folder
$env:CC_VERIFY = "1"
python engine/probe.py
```

Leave `CC_TTS` **unset** — the engine defaults to high-quality chatterbox. `CC_VERIFY=1` keeps the
self-correcting audio gate on. Chatterbox re-rolls lines that Faster-Whisper hears as garbled,
repeated, or truncated.

---

## Default (high quality, GPU or CPU): Chatterbox
This is the default and what you should use. Provide a **license-clean reference clip** per character:

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

Do **not** set `CC_TTS` — chatterbox is automatic. If it isn't installed, `engine/tts.py` fails with
install guidance (it runs on CPU too); install it rather than downgrading. If chatterbox on CPU is
too **slow** for the user, that is the ONLY reason to consider Piper — and only with their approval.

---

## Optional downgrade (ONLY with explicit user approval): Piper
Piper is fast but **robotic / lower quality**. Use it **only after** telling the user "high-quality
voices on your CPU will render slowly; do you want to switch to faster, lower-quality robotic voices?"
and getting a clear **yes**. Never switch silently. Then place `.onnx` voices in `assets/voices/` and
set `cast[].voice.piper` to the filename (no extension):

```json
{
  "name": "MENTOR",
  "role": "mentor",
  "caption_color": "gold",
  "voice": {"ref": "mentor.wav", "piper": "en_US-lessac-medium", "length": 1.0}
}
```

Keep the `ref` too, so removing `CC_TTS=piper` restores the high-quality voice. Then set
`$env:CC_TTS = "piper"` (the approved-downgrade switch).

Fetch a Piper model + config if needed (macOS/Linux: `mkdir -p`, `curl -L`):

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

Expected output includes the selected engine (`chatterbox on cuda/cpu`), cast voice names, and `.cache\tts_smoke\*.wav` files. If it prints a piper line without the user approving a downgrade, or errors that chatterbox isn't installed, fix the environment (install chatterbox) rather than accepting low-quality voices.

---

## Self-review
- Is the voice **high quality** — chatterbox by default (piper only if the user explicitly approved it)?
- Are reference clips (and any Piper models) license-clean?
- Does each speaking cast member have a usable `voice` config?
- Is `CC_VERIFY=1` set (and `CC_TTS` unset unless a downgrade was approved)?
- Did `python engine/tts.py` synthesize smoke-test wavs (and print `chatterbox on ...`)?
- Are domain terms handled in `pronunciations` or `spell_acronyms`?

Then route to `system-prompts/07_music_and_sfx.md`.



