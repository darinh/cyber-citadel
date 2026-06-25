"""Voice engine (theme-cast-driven) with two interchangeable backends:

  - chatterbox  : expressive zero-shot voice cloning (best quality; GPU-ideal). Includes
                  the SELF-CORRECTING synth gate (re-rolls a take that an STT pass shows was
                  garbled/dropped). STT model size steps DOWN by tier so it runs on CPU too.
  - piper       : fast deterministic ONNX TTS — the always-works CPU fallback.

Both share one interface — synth_line(speaker, text, out_wav) -> seconds — plus a shared,
generic pronunciation pre-processor. Per-speaker voice config (timbre, knobs, effects) comes
from the THEME cast, never from hardcoded character names, so it is topic/world agnostic.

Engine selection: $CC_TTS ('chatterbox'|'piper'), else chatterbox if importable AND CUDA is
present, else piper. The assembler keys its incremental cache on CAST+EFFECTS so a voice
change re-synthesizes the affected lines.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme as _theme

ENGINE = Path(__file__).resolve().parent
PROJECT = Path(os.environ.get("CC_PROJECT") or Path.cwd())
SR = 24000
CACHE = PROJECT / ".cache" / "voicecache"
CACHE.mkdir(parents=True, exist_ok=True)
_T = _theme.load()

# ---- generic pronunciation pre-processor (spoken text only) --------------
_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
         "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
         "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def _n2w(n: int) -> str:
    n = int(n)
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + _n2w(n % 100))
    return str(n)


# theme may add domain pronunciations: {"pronunciations": {"FOO": "fooh"}, "spell": ["API"]}
_PRON = {k.upper(): v for k, v in (_T.get("pronunciations", {}) or {}).items()}
_SPELL = {s.upper() for s in (_T.get("spell_acronyms", []) or [])}
# A two-letter code + number ("KN-1", "AC-6(2)") -> spelled letters + number.
_ID_RE = re.compile(r"\b([A-Z]{2})-(\d{1,3})(?:\((\d{1,3})\))?")
_SPELLED = {"A": "ay", "B": "bee", "C": "see", "D": "dee", "E": "ee", "F": "eff", "G": "jee",
            "H": "aitch", "I": "eye", "J": "jay", "K": "kay", "L": "el", "M": "em", "N": "en",
            "O": "oh", "P": "pee", "Q": "cue", "R": "are", "S": "ess", "T": "tee", "U": "you",
            "V": "vee", "W": "double-you", "X": "ex", "Y": "why", "Z": "zee"}


def _say_letters(s):
    return " ".join(_SPELLED.get(c, c) for c in s)


def _id_repl(m):
    out = f"{_say_letters(m.group(1))} {_n2w(m.group(2))}"
    if m.group(3):
        out += f", enhancement {_n2w(m.group(3))}"
    return out


def preprocess(text: str) -> str:
    """Make narration text speakable (applied to spoken lines only, never on-screen text)."""
    for k, v in _PRON.items():
        text = re.sub(r"\b" + re.escape(k) + r"\b", v, text)
    text = _ID_RE.sub(_id_repl, text)                       # KN-1 -> "kay en one"
    # spell out acronyms the theme marks, and lowercase OTHER all-caps emphasis words so the
    # model says them instead of spelling them letter by letter.
    def _caps(m):
        w = m.group(0)
        if w in _SPELL:
            return _say_letters(w)
        if w in _PRON:
            return _PRON[w]
        return w.capitalize()
    text = re.sub(r"\b[A-Z][A-Z]+\b", _caps, text)
    text = re.sub(r"\bRev\.?\s*(\d)\b", lambda m: "revision " + _n2w(m.group(1)), text)
    text = text.replace(" — ", ", ").replace("—", ", ").replace(" – ", ", ")
    text = text.replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


# ---- per-speaker voice config from the theme cast ------------------------
_DEF_KNOBS = {"exaggeration": 0.5, "cfg_weight": 0.5, "temperature": 0.8}
_NORM = "loudnorm=I=-16:TP=-1.5:LRA=11"
_DEF_EFFECT = f"highpass=f=75,acompressor=threshold=-18dB:ratio=2:attack=12:release=120,{_NORM}"
_ANTAG_EFFECT = (f"rubberband=pitch=0.86,asubboost,highpass=f=55,"
                 f"acompressor=threshold=-20dB:ratio=3:attack=8:release=160,"
                 f"aecho=0.9:0.9:38:0.12,lowpass=f=7200,{_NORM}")


def _voice(speaker):
    sp = (speaker or "").upper()
    for c in (_T.get("cast", []) or []):
        if (c.get("name") or "").upper() == sp:
            v = dict(c.get("voice", {}) or {})
            v["_role"] = (c.get("role") or "").lower()
            return v
    return {"_role": ""}


def _knobs(speaker):
    v = _voice(speaker)
    return {k: v.get(k, _DEF_KNOBS[k]) for k in _DEF_KNOBS}


def _effect(speaker):
    v = _voice(speaker)
    if v.get("effects"):
        return v["effects"]
    if v.get("_role") in ("antagonist", "villain", "threat"):
        return _ANTAG_EFFECT
    return _DEF_EFFECT


# dicts the assembler hashes for its incremental cache (so a voice edit re-synths the line)
CAST = {(_c.get("name") or "").upper(): _knobs(_c.get("name"))
        for _c in (_T.get("cast", []) or []) if _c.get("name")}
EFFECTS = {(_c.get("name") or "").upper(): _effect(_c.get("name"))
           for _c in (_T.get("cast", []) or []) if _c.get("name")}


def _ref_clip(speaker):
    """Resolve a chatterbox reference clip for a speaker (timbre to clone)."""
    v = _voice(speaker)
    name = v.get("ref")
    for cand in ([Path(name)] if name and Path(name).is_absolute() else []) + (
            [PROJECT / "assets" / "voices" / name, ENGINE / "assets" / "voices_ref" / name]
            if name else []):
        if cand.exists():
            return cand
    # fall back to any available ref so synthesis never hard-fails
    for d in (PROJECT / "assets" / "voices", ENGINE / "assets" / "voices_ref"):
        if d.exists():
            for f in sorted(d.glob("*.wav")):
                return f
    return None


def _piper_voice(speaker):
    v = _voice(speaker)
    return v.get("piper", _theme.load().get("music", {}).get("_", None) or "en_US-lessac-medium")


def _engine_choice():
    e = os.environ.get("CC_TTS", "").lower()
    if e in ("chatterbox", "cbx", "3"):
        return "chatterbox"
    if e in ("piper", "1"):
        return "piper"
    try:
        import importlib.util
        if importlib.util.find_spec("chatterbox") and importlib.util.find_spec("torch"):
            import torch
            if torch.cuda.is_available():
                return "chatterbox"
    except Exception:                                       # noqa: BLE001
        pass
    return "piper"


_ENGINE = _engine_choice()


def _dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip()
    return float(out) if out else 0.0


def _master(raw, out_wav, speaker):
    subprocess.run(["ffmpeg", "-y", "-i", str(raw), "-ar", str(SR), "-ac", "1",
                    "-af", _effect(speaker), str(out_wav)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


# ---- piper backend -------------------------------------------------------
def _piper_voice_dirs():
    return [PROJECT / "assets" / "voices", ENGINE / "assets" / "voices_ref",
            PROJECT / "voices"]


def _piper_model(speaker):
    name = _piper_voice(speaker)
    for d in _piper_voice_dirs():
        cand = d / f"{name}.onnx"
        if cand.exists():
            return cand
    # any onnx we can find
    for d in _piper_voice_dirs():
        if d.exists():
            for f in sorted(d.glob("*.onnx")):
                return f
    raise RuntimeError("no piper .onnx voice found; run the environment setup to fetch voices")


def _piper_synth(speaker, text, out_wav):
    model = _piper_model(speaker)
    ls = _voice(speaker).get("length", 1.0)
    raw = Path(out_wav).with_suffix(".raw.wav")
    p = subprocess.run([sys.executable, "-m", "piper", "-m", str(model), "-f", str(raw),
                        "--length-scale", str(ls)],
                       input=preprocess(text).encode("utf-8"),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if p.returncode != 0 or not raw.exists():
        raise RuntimeError(f"piper failed for {speaker}: {text[:60]}")
    _master(raw, out_wav, speaker)
    raw.unlink(missing_ok=True)
    return _dur(out_wav)


# ---- chatterbox backend (+ self-correcting verify) -----------------------
_MODEL = None
_CONDS: dict = {}
_STT_M = None
VERIFY = os.environ.get("CC_VERIFY", "1") != "0"
VERIFY_TRIES, VERIFY_THRESH = 4, 0.8


def _cbx_model():
    global _MODEL
    if _MODEL is None:
        import torch  # noqa: F401
        from chatterbox.tts import ChatterboxTTS
        dev = "cuda" if __import__("torch").cuda.is_available() else "cpu"
        _MODEL = ChatterboxTTS.from_pretrained(device=dev)
    return _MODEL


def _stt():
    global _STT_M
    if _STT_M is None:
        from faster_whisper import WhisperModel
        try:
            import torch
            cuda = torch.cuda.is_available()
        except Exception:                                   # noqa: BLE001
            cuda = False
        model = os.environ.get("CC_STT_MODEL") or ("large-v3" if cuda else "small")
        _STT_M = WhisperModel(model, device="cuda" if cuda else "cpu",
                              compute_type="float16" if cuda else "int8")
    return _STT_M


_STOPW = set("a an the of to and or is are be it that this with for in on at as you your".split())


def _content(s):
    return [w for w in re.sub(r"[^a-z' ]", " ", s.lower()).split() if w not in _STOPW and len(w) > 2]


def _verify_score(text, wav):
    from collections import Counter
    ew = _content(preprocess(text))
    if len(ew) < 3:
        return True, 1.0, ""
    segs, _ = _stt().transcribe(str(wav), language="en", beam_size=5)
    heard = " ".join(x.text for x in segs).strip()
    hw = _content(heard)
    hc = Counter(hw); hit = 0
    for w in ew:
        if hc.get(w, 0) > 0:
            hit += 1; hc[w] -= 1
    recall = hit / len(ew)
    ec = Counter(ew)
    repeat = any(Counter(hw)[w] - ec.get(w, 0) >= 2 for w in set(hw))
    truncated = len(hw) < 0.4 * len(ew)
    return (recall >= VERIFY_THRESH) and not repeat and not truncated, recall, heard


def _cbx_raw(speaker, text, raw_path):
    m = _cbx_model()
    ref = _ref_clip(speaker)
    s = _knobs(speaker)
    key = (speaker or "").upper()
    if key not in _CONDS:
        m.prepare_conditionals(str(ref) if ref else None, exaggeration=s["exaggeration"])
        _CONDS[key] = m.conds
    m.conds = _CONDS[key]
    wav = m.generate(preprocess(text), exaggeration=s["exaggeration"],
                     cfg_weight=s["cfg_weight"], temperature=s["temperature"],
                     repetition_penalty=1.2, min_p=0.05, top_p=1.0)
    import torchaudio as ta
    ta.save(str(raw_path), wav.detach().cpu(), m.sr)


def _cbx_synth(speaker, text, out_wav):
    raw = Path(out_wav).with_suffix(".raw.wav")
    best, best_recall = None, -1.0
    tries = VERIFY_TRIES if VERIFY else 1
    for _ in range(tries):
        _cbx_raw(speaker, text, raw)
        _master(raw, out_wav, speaker)
        if not VERIFY:
            break
        ok, recall, _heard = _verify_score(text, out_wav)
        if recall > best_recall:
            best_recall, best = recall, Path(out_wav).read_bytes()
        if ok:
            best = None
            break
    if VERIFY and best is not None:
        Path(out_wav).write_bytes(best)
    raw.unlink(missing_ok=True)
    return _dur(out_wav)


# ---- public API ----------------------------------------------------------
def _key(speaker, text):
    import hashlib
    h = hashlib.sha1()
    h.update(repr((_ENGINE, (speaker or "").upper(), _knobs(speaker), _effect(speaker),
                   str(_ref_clip(speaker)), preprocess(text))).encode("utf-8"))
    return h.hexdigest()[:20]


def synth_line(speaker, text, out_wav) -> float:
    out_wav = Path(out_wav)
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    cached = CACHE / f"{_key(speaker, text)}.wav"
    if cached.exists():
        shutil.copyfile(cached, out_wav)
        return _dur(out_wav)
    if _ENGINE == "chatterbox":
        _cbx_synth(speaker, text, out_wav)
    else:
        _piper_synth(speaker, text, out_wav)
    shutil.copyfile(out_wav, cached)
    return _dur(out_wav)


if __name__ == "__main__":
    print("engine:", _ENGINE, "| cast voices:", list(CAST))
    out = PROJECT / ".cache" / "tts_smoke"
    out.mkdir(parents=True, exist_ok=True)
    for i, (sp, tx) in enumerate([("NARRATOR", "Welcome to the lesson."),
                                  (list(CAST)[0] if CAST else "NARRATOR", "Let's begin with the basics.")]):
        d = synth_line(sp, tx, out / f"{i:02d}_{sp}.wav")
        print(f"[{sp}] {d:.2f}s -> {out}")
