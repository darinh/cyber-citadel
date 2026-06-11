"""Verify the FINAL rendered episode mp4 actually contains all scripted narration.

WHY THIS EXISTS (hard-won): the per-line clips, the per-beat WAVs and the concatenated
narr.wav can ALL transcribe perfectly clean while the final mp4 still drops speech — a
combined audio+video `-filter_complex` in the mux dropped ~2-3s of words at scene
boundaries. So audio QA MUST run on the DELIVERED mp4, never just on upstream artifacts.

This transcribes the mp4 with faster-whisper (large-v3) and sequence-aligns the transcript
to the script, flagging any contiguous MISSING RUN of scripted words (the drop signature).
It is deliberately tolerant of STT artifacts that are NOT real defects:
  * number/acronym readback ("800-53" -> "853", "eight hundred fifty three")
  * repetition hallucinations ("a threat is a threat is a threat") — these are EXTRA words,
    never missing words, so they cannot create a missing-run.
Only contiguous DROPS of scripted words fail the gate. Run inside .venv_tts.

Usage:
  python tools/verify_episode.py                 # verify every ep*.json
  python tools/verify_episode.py ep00 ep01       # verify specific episodes
Env: VERIFY_MISS_RUN (default 5), VERIFY_MIN_RECALL (default 0.85).
"""
import json
import os
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPDIR = ROOT / "course" / "episodes"
SCRIPTS = ROOT / "course" / "scripts"
MISS_RUN = int(os.environ.get("VERIFY_MISS_RUN", "4"))
MIN_RECALL = float(os.environ.get("VERIFY_MIN_RECALL", "0.85"))

_W = re.compile(r"[a-z0-9']+")

# Tokens that STT renders inconsistently (digits<->number words, letter-spelled acronyms,
# option letters). These are NEVER real content drops, so we strip them from BOTH the script
# and the transcript before aligning — a number/acronym readback mismatch must not fail QA.
_NUMW = set("zero one two three four five six seven eight nine ten eleven twelve thirteen "
            "fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty "
            "sixty seventy eighty ninety hundred thousand million billion oh".split())
_ACR = set("nist sp rmf fisma fips oscal cia mfa ato poa pii pt sr isso ao ac au ca cm cp ia "
           "ir ma mp pe pl pm ps ra sa sc si pl csf omb cui siem dns tls ssh vpn pki s(p) "
           "id ids ips waf".split())
_CONSONANT = re.compile(r"[bcdfghjklmnpqrstvwxz]{2,5}$")   # letter-spelled acronyms: rmf, sp, tls


def _benign(t):
    return (t.isdigit() or re.fullmatch(r"\d+[a-z]?", t) is not None or t in _NUMW
            or len(t) == 1 or t in _ACR or _CONSONANT.fullmatch(t) is not None)


def toks(s):
    return _W.findall(s.lower())


def content(words):
    return [w for w in words if not _benign(w)]


def expected_lines(spec):
    """(speaker, text) for every spoken line in render order — mirrors build_episode2."""
    return [(sp, tx) for sp, tx, _idx, _k in _render_lines(spec)]


def _render_lines(spec):
    """(speaker, text, render_idx, line_k) for every spoken line, in render order."""
    out = []
    for i, beat in enumerate(spec["beats"]):
        say = [(x[0], x[1]) for x in beat.get("say", [])]
        if beat.get("scene") == "quiz":
            opts = beat.get("options", [])
            ans = beat.get("answer", 0)
            letter = chr(65 + ans)
            letters = [chr(65 + j) for j in range(len(opts))]
            read_opts = "   ".join(f"{letters[j]}.  {o}." for j, o in enumerate(opts))
            why = beat.get("why", "")
            qlines = say + [("NARRATOR", beat.get("q", "")),
                            ("NARRATOR", f"Your options.   {read_opts}"),
                            ("NOVA", "Pause here and lock in your answer.")]
            for k, (sp, tx) in enumerate(qlines):
                out.append((sp, tx, i * 10, k))
            correct = opts[ans] if ans < len(opts) else ""
            out.append(("VEGA", f"The answer is {letter}.   {correct}."
                        + (f"   {why}" if why else ""), i * 10 + 1, 0))
        else:
            for k, (sp, tx) in enumerate(say):
                out.append((sp, tx, i * 10, k))
    return out


def line_start_times(ep, spec):
    """Absolute audio (start, dur) per render line, from course/render/<ep>/manifest.json.
    Returns {(render_idx, line_k): (start_s, dur_s)} or {} if no manifest (confirm skipped)."""
    mf_path = ROOT / "course" / "render" / ep / "manifest.json"
    if not mf_path.exists():
        return {}
    beats_mf = json.loads(mf_path.read_text(encoding="utf-8")).get("beats", {})
    times, timeline = {}, 0.0
    for i, beat in enumerate(spec["beats"]):
        sc = beat.get("scene")
        idxs = [i * 10, i * 10 + 1] if sc == "quiz" else [i * 10]
        for idx in idxs:
            ent = beats_mf.get(str(idx))
            if not ent:
                continue
            starts = ent.get("starts", [])
            ldurs = ent.get("ldurs", [])
            for k in range(len(starts)):
                times[(idx, k)] = (timeline + starts[k],
                                   ldurs[k] if k < len(ldurs) else 3.0)
            timeline += ent["dur"]
    return times


_STT = None


def stt():
    global _STT
    if _STT is None:
        import torch
        from faster_whisper import WhisperModel
        _STT = WhisperModel("large-v3", device="cuda" if torch.cuda.is_available() else "cpu",
                            compute_type="float16" if torch.cuda.is_available() else "int8")
    return _STT


def transcribe(mp4):
    wav = ROOT / "tools" / "_tmp" / f"_verify_{mp4.stem}.wav"
    wav.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(mp4), "-ar", "16000", "-ac", "1", str(wav)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    segs, _ = stt().transcribe(str(wav), language="en", beam_size=5,
                               condition_on_previous_text=False)
    heard = _W.findall(" ".join(s.text for s in segs).lower())
    wav.unlink(missing_ok=True)
    return heard


def heard_in_region(mp4, t0, t1):
    """Re-transcribe ONLY [t0,t1] of the mp4 — used to CONFIRM a flagged miss.
    faster-whisper long-form omits short isolated lines that ARE present; a local
    re-transcription of just that region recovers them, killing false 'missing' flags."""
    reg = ROOT / "tools" / "_tmp" / f"_vconf_{mp4.stem}.wav"
    reg.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-ss", f"{max(0, t0):.2f}", "-i", str(mp4),
                    "-t", f"{t1 - t0:.2f}", "-ar", "16000", "-ac", "1", str(reg)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    segs, _ = stt().transcribe(str(reg), language="en", beam_size=5,
                               condition_on_previous_text=False)
    words = set(content(_W.findall(" ".join(s.text for s in segs).lower())))
    reg.unlink(missing_ok=True)
    return words


def verify(ep):
    spec = json.loads((SCRIPTS / f"{ep}.json").read_text(encoding="utf-8"))
    slug = spec.get("slug", ep)
    mp4 = EPDIR / f"{ep}_{slug}.mp4"
    if not mp4.exists():
        print(f"{ep}: FAIL  (mp4 not found: {mp4.name})")
        return ep, False
    times = line_start_times(ep, spec)
    exp, line_at = [], []
    for sp, tx, idx, k in _render_lines(spec):
        for w in toks(tx):
            if _benign(w):
                continue
            exp.append(w)
            line_at.append((sp, tx, idx, k))
    heard = content(transcribe(mp4))
    sm = SequenceMatcher(a=exp, b=heard, autojunk=False)
    matched = sum(b - a for tag, a, b, c, d in sm.get_opcodes() if tag == "equal")
    recall = matched / len(exp) if exp else 1.0
    runs = sorted(((b - a, a, b) for tag, a, b, c, d in sm.get_opcodes()
                   if tag in ("delete", "replace")), reverse=True)

    # CONFIRM each candidate miss by re-transcribing just that region — kills false flags
    # from Whisper long-form short-line omission. Only confirmed-missing runs count.
    confirmed = []
    for n, a, b in runs:
        if n < MISS_RUN:
            break
        sp, tx, idx, k = line_at[a] if a < len(line_at) else ("?", "", None, None)
        t0, dur = times.get((idx, k), (None, None))
        miss_words = exp[a:b]
        if t0 is not None:
            t1 = t0 + max(dur, 0.5 * n) + 1.5     # cover the WHOLE line (long option readouts)
            local = heard_in_region(mp4, t0 - 0.5, t1)
            still = [w for w in miss_words if w not in local]
            if len(still) < MISS_RUN:        # recovered locally -> false positive
                continue
            miss_words = still
        confirmed.append((len(miss_words), sp, tx, miss_words, t0))

    worst = confirmed[0][0] if confirmed else 0
    ok = worst < MISS_RUN and recall >= MIN_RECALL
    print(f"{ep}: recall={recall:.3f}  confirmed_missing_run={worst}  "
          f"{'OK' if ok else 'FAIL'}")
    for n, sp, tx, miss_words, t0 in confirmed[:3]:
        at = f" @{t0:.1f}s" if t0 is not None else ""
        print(f"     -{n}w near [{sp}]{at} \"{tx[:60]}\"  missing: \"{' '.join(miss_words)[:90]}\"")
    return ep, ok


def main():
    eps = sys.argv[1:] or [p.stem for p in sorted(SCRIPTS.glob("ep*.json"))]
    results = [verify(e) for e in eps]
    bad = [e for e, ok in results if not ok]
    print(f"\n=== {len(results) - len(bad)}/{len(results)} episodes clean "
          f"(miss_run>={MISS_RUN} or recall<{MIN_RECALL} fails) ===")
    if bad:
        print("FAILED:", ", ".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
