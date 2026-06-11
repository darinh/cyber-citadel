---
name: tts-narration
description: >-
  Generate reliable, persona-matched narration for the Cyber Citadel course with local neural
  TTS (Chatterbox) including the self-correcting synth gate, the shared pronunciation
  pre-processor, and the MANDATORY final-mp4 verification. Use when synthesizing or
  regenerating spoken lines, fixing a bad audio clip, changing a voice, or before shipping any
  narrated render. Encodes why audio defects happen and how to prevent shipping them.
---

# TTS Narration (Chatterbox + verify gate)

Local, license-clean neural narration with **persona-matched voices** and a **self-correcting
gate** so bad takes never ship. Read `course/GENERATION_PLAYBOOK.md` §5 (voice) and §11.D
(audio rules) — this skill is the operational checklist.

## Environment
- venv: **`.venv_tts`** (Chatterbox + faster-whisper + torch cu124). `$env:PYTHONUTF8=1`.
- Engine switch: `$env:CC_TTS='chatterbox'` (current). Kokoro `tts2.py` / piper `tts.py` are
  fallbacks; all share the `tts.py` pronunciation pre-processor.
- Self-correcting gate on by default: `$env:CC_VERIFY='1'`.

## Interface (any engine must match)
`tts3.synth_line(speaker, text, out_wav) -> duration_seconds`. Voices are **zero-shot clones**
of license-clean reference clips in `tools/voices_ref/<SPEAKER>.wav`. Per-character knobs live
in `tools/tts3.py` `CAST` and effects in `EFFECTS`; the authoritative mirror is
`course/seed_registry.yaml` (`voice.cast`). Cast: VEGA (younger male), NOVA (young, eager),
ARCHIVIST (young British female), NULL (deep/menacing, pitch 0.84), NARRATOR, HERALD.

## Why TTS errors happen (must understand)
Chatterbox is **autoregressive/stochastic** — it samples tokens, so a take can drop/repeat/garble
words. Worst on **ALL-CAPS** (spells them), **numbers/IDs** ("800-53"), and **ultra-short
fragments** (≤3-4 words). Mitigations in order: harden input (pre-processor) → gate output
(STT verify + re-roll) → reword the unfixable.

## Pre-processor (`tools/tts.py preprocess`, shared)
Runs on **spoken text only**, never on-screen text. Lowercases ALL-CAPS emphasis (acronyms/codes
protected), expands acronyms/IDs/numbers (NIST→"nisst", AC-6→"ay see six", "800-53r5"→"eight
hundred fifty three, revision five"). **Extend the map whenever a new acronym/ID appears.**
Pronunciation fixes go HERE, never as misspellings in scripts. If you change the pre-processor
but the output string is unchanged, the voice cache key won't change — delete
`tools/_tmp/voicecache_cbx/` to force re-synth.

## Self-correcting synth gate (`tts3.synth_line`, `CC_VERIFY=1`)
Every freshly synthesized clip is transcribed (faster-whisper) and **auto re-rolled up to 4×**
if a content word is dropped/repeated/garbled/truncated; the best take is kept; anything still
failing is logged to `tools/_tmp/synth_verify_fails.log` for a reword.

## ⭐ Verify the FINAL mp4 — not just clips
The most expensive mistake this project made was QA-ing per-line clips / beat WAVs / `narr.wav`
(all clean) while the SHIPPED mp4 dropped ~2-3 s of speech. **Always run
`python tools/verify_episode.py [ep...]`** (in `.venv_tts`) on the delivered mp4 — it transcribes
the encoded video, aligns to the script, filters number/acronym/letter readback, and
**re-confirms any flagged region locally** before failing (faster-whisper omits short isolated
lines in long-form). Pass = `confirmed_missing_run < 4` and `recall ≥ 0.85`. All episodes must
read `OK` before deploy.

### STT artifacts that are NOT defects (don't chase)
- **Repetition hallucination** ("a threat is a threat is a threat…") — re-extract that region to
  confirm; it's a Whisper decoding loop, not bad audio.
- **Long-form omission** — short lines (a 4-6 word question) dropped by the full-episode pass but
  present when you transcribe just that region.
- Number/ID/compound/quote readback ("800-53"→"853", "oathkeeper"→"Oath Keeper").

## Fixing one bad clip (surgical)
`python tools/regen_line.py <ep> <clip>...` re-rolls listed line clips (busts their cache) and
re-muxes only that episode (beats are content-hashed; the key includes a **voice fingerprint** so
voice/FX changes re-synth the affected beats). Acoustic QA: `tools/audio_scan.py` (echo/clip/
muddiness) + `tools/audio_qa.py` (per-clip STT). TTS effect chains must not garble speech (no
slap-back echo; don't over-lowpass).

## A better engine? (evaluated 2026)
The recurring word-drop pain was largely the **mux bug** (see video-assembly), not Chatterbox.
If migrating for max reliability: **F5-TTS** (non-autoregressive flow-matching, MIT code) is the
strongest, but its **weights are CC-BY-NC** (non-commercial). **CosyVoice2/3** is the Apache-clean
pick. Any swap re-clones all voices, invalidates the voicecache, and forces a full re-render; keep
the verify gate regardless. See GENERATION_PLAYBOOK §5.

## Definition of done
- Lines synthesized with `CC_VERIFY=1`; `synth_verify_fails.log` reviewed (real fails reworded).
- Episode rendered, then `verify_episode.py` reports `OK` on the final mp4.
- New acronyms/IDs added to the pre-processor; voice knob/FX changes mirrored to seed_registry.
