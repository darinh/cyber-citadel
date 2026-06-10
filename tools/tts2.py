"""v2 voice engine: Kokoro-82M (Apache-2.0) + per-character audio mastering.

Council insight: the lever isn't just the model, it's prosody, pacing, breath,
room tone, and per-character processing. So: sentence-level synthesis with
inter-sentence pauses, per-character voice + speed, and a mastering chain
(HPF -> EQ/de-ess -> compressor -> per-character reverb -> -16 LUFS loudnorm).
THE NULL uses rubberband pitch-down (not the cheesy asetrate trick) + sub boost.
"""
from __future__ import annotations
import hashlib
import shutil
import subprocess
import sys
import wave
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tts import preprocess  # reuse acronym/ID pronunciation pre-processor

import warnings
warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
SR = 24000
CACHE = ROOT / "tools" / "_tmp" / "voicecache"
CACHE.mkdir(parents=True, exist_ok=True)

# character -> (lang_code, kokoro voice, speed, inter-sentence pause seconds)
CAST = {
    "NARRATOR":  ("b", "bm_george", 0.92, 0.22),
    "VEGA":      ("a", "am_michael", 1.0, 0.16),
    "NOVA":      ("a", "af_heart",  1.0, 0.16),
    "ARCHIVIST": ("b", "bf_emma",   0.90, 0.30),
    "NULL":      ("a", "am_onyx",   0.92, 0.34),
    "HERALD":    ("a", "af_bella",  0.98, 0.18),
}

_BASE_EQ = "firequalizer=gain_entry='entry(120,0);entry(320,-3);entry(3000,2);entry(6800,-4);entry(9500,-5)'"
_COMP = "acompressor=threshold=-18dB:ratio=2:attack=12:release=120"
_NORM = "loudnorm=I=-16:TP=-1.5:LRA=11"

EFFECTS = {
    "NARRATOR":  f"highpass=f=80,{_BASE_EQ},{_COMP},aecho=0.85:0.9:28:0.14,{_NORM}",
    "VEGA":      f"highpass=f=85,{_BASE_EQ},{_COMP},aecho=0.85:0.9:42:0.20,{_NORM}",
    "NOVA":      f"highpass=f=95,firequalizer=gain_entry='entry(320,-2);entry(3000,2);entry(6200,1.5);entry(9500,-4)',{_COMP},aecho=0.85:0.88:24:0.14,{_NORM}",
    "ARCHIVIST": f"highpass=f=80,firequalizer=gain_entry='entry(250,-2);entry(2500,1.5);entry(7000,-5)',{_COMP},lowpass=f=11000,aecho=0.8:0.85:18:0.10,{_NORM}",
    "NULL":      f"rubberband=pitch=0.82,asubboost,highpass=f=60,firequalizer=gain_entry='entry(400,-2);entry(1500,1);entry(4000,-3)',acompressor=threshold=-20dB:ratio=3:attack=8:release=150,aecho=0.8:0.85:90:0.40,lowpass=f=3800,{_NORM}",
    "HERALD":    f"highpass=f=82,{_BASE_EQ},{_COMP},aecho=0.85:0.9:55:0.25,{_NORM}",
}

_PIPES: dict = {}


def _pipe(lang):
    if lang not in _PIPES:
        from kokoro import KPipeline
        _PIPES[lang] = KPipeline(lang_code=lang)
    return _PIPES[lang]


def _write_wav(path, audio, sr=SR):
    a = np.clip(np.asarray(audio, dtype=np.float32), -1, 1)
    data = (a * 32767).astype(np.int16)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(data.tobytes())


def _synth_raw(speaker, text):
    lang, voice, speed, pause = CAST.get(speaker, CAST["NARRATOR"])
    pipe = _pipe(lang)
    segs = []
    gap = np.zeros(int(pause * SR), dtype=np.float32)
    for r in pipe(preprocess(text), voice=voice, speed=speed):
        a = r.audio
        a = a.detach().cpu().numpy() if hasattr(a, "detach") else np.asarray(a)
        segs.append(a.astype(np.float32))
        segs.append(gap)
    if not segs:
        return np.zeros(int(0.2 * SR), dtype=np.float32)
    return np.concatenate(segs)


def synth_line(speaker, text, out_wav) -> float:
    out_wav = Path(out_wav)
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    key = hashlib.md5(
        f"{speaker}|{CAST.get(speaker)}|{EFFECTS.get(speaker)}|{preprocess(text)}".encode("utf-8")
    ).hexdigest()
    cached = CACHE / f"{key}.wav"
    if cached.exists():
        shutil.copyfile(cached, out_wav)
    else:
        raw = out_wav.with_suffix(".raw.wav")
        _write_wav(raw, _synth_raw(speaker, text))
        af = EFFECTS.get(speaker, EFFECTS["NARRATOR"])
        subprocess.run(["ffmpeg", "-y", "-i", str(raw), "-ar", str(SR), "-ac", "1",
                        "-af", af, str(out_wav)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        raw.unlink(missing_ok=True)
        shutil.copyfile(out_wav, cached)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(out_wav)], capture_output=True, text=True).stdout.strip()
    return float(dur)


if __name__ == "__main__":
    tmp = ROOT / "tools" / "_tmp" / "v2voices"
    lines = [
        ("NARRATOR", "In a world run on data, every system is a city. Protect it, and you thrive."),
        ("VEGA", "I'm Vega. Twenty guardians defend this citadel. First, AC-6, Least Privilege."),
        ("NOVA", "So that's giving people only the access they actually need? Nothing more?"),
        ("ARCHIVIST", "Employ the principle of least privilege, allowing only authorized accesses."),
        ("NULL", "Your walls will fall. Every gap, every shortcut. I am the Null."),
    ]
    for i, (sp, tx) in enumerate(lines):
        d = synth_line(sp, tx, tmp / f"{i}_{sp}.wav")
        print(f"{sp:9s} {d:5.2f}s -> {tmp / f'{i}_{sp}.wav'}")
