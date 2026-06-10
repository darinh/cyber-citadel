"""Procedural sound-design library (numpy) - license-safe (self-generated).

Subtle, tasteful cues per the council: one whoosh per transition, a deep boom on
section/title beats, a chime on quiz reveal, a low rumble when THE NULL speaks, a
sting on guardian intros, a soft click on cards/bullets. Renders to tools/sfx/*.wav
and a manifest the assembler overlays (ducked) onto the timeline.
"""
from __future__ import annotations
import json
import wave
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "sfx"
OUT.mkdir(parents=True, exist_ok=True)
SR = 48000


def _env(n, attack, decay, hold=0.0):
    a = int(attack * SR); h = int(hold * SR); d = int(decay * SR)
    parts = [np.linspace(0, 1, max(1, a)), np.ones(max(0, h)),
             np.exp(-np.linspace(0, 6, max(1, d)))]
    e = np.concatenate(parts)
    if len(e) < n:
        e = np.concatenate([e, np.zeros(n - len(e))])
    return e[:n]


def _stereo(mono, pan=0.0):
    l = mono * (1 - max(0, pan)); r = mono * (1 + min(0, pan))
    return np.stack([l, r], axis=1)


def _noise(n, lp=0.0):
    x = np.random.default_rng(1).standard_normal(n)
    if lp:
        k = max(1, int(lp)); x = np.convolve(x, np.ones(k) / k, mode="same")
    return x


def whoosh(dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    x = _noise(n, lp=40) * _env(n, 0.12, 0.35)
    sweep = np.sin(2 * np.pi * (t * 0) )  # placeholder
    pan = np.linspace(-0.6, 0.6, n)
    st = np.stack([x * (1 - np.clip(pan, 0, 1)), x * (1 + np.clip(pan, -1, 0))], axis=1)
    return st * 0.5


def boom(dur=1.1):
    n = int(dur * SR); t = np.arange(n) / SR
    f = np.linspace(85, 45, n)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.005, 1.0)
    sub = np.sin(2 * np.pi * 33 * t) * _env(n, 0.01, 1.0) * 0.7
    click = _noise(n, lp=6) * _env(n, 0.001, 0.04) * 0.4
    m = tone + sub + click
    return _stereo(m / (np.max(np.abs(m)) + 1e-9) * 0.85)


def sting(dur=0.7):
    n = int(dur * SR); t = np.arange(n) / SR
    chord = sum(np.sin(2 * np.pi * f * t) for f in (220, 330, 440)) / 3
    m = chord * _env(n, 0.01, 0.6, hold=0.05)
    shimmer = np.sin(2 * np.pi * 880 * t) * _env(n, 0.02, 0.5) * 0.2
    return _stereo((m + shimmer) * 0.5)


def chime(dur=0.8):
    n = int(dur * SR); t = np.arange(n) / SR
    notes = [(523, 0.0), (659, 0.06), (784, 0.12)]
    m = np.zeros(n)
    for f, off in notes:
        o = int(off * SR)
        e = np.zeros(n); seg = _env(n - o, 0.005, 0.6); e[o:] = seg
        m += np.sin(2 * np.pi * f * t) * e
    return _stereo(m / (np.max(np.abs(m)) + 1e-9) * 0.7)


def rumble(dur=1.4):
    n = int(dur * SR); t = np.arange(n) / SR
    low = np.sin(2 * np.pi * 42 * t) * _env(n, 0.25, 1.0)
    nz = _noise(n, lp=80) * _env(n, 0.3, 1.0) * 0.5
    m = low + nz
    return _stereo(m / (np.max(np.abs(m)) + 1e-9) * 0.6)


def click(dur=0.09):
    n = int(dur * SR); t = np.arange(n) / SR
    m = np.sin(2 * np.pi * 1400 * t) * _env(n, 0.002, 0.05)
    return _stereo(m * 0.4)


def riser(dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR
    f = np.linspace(200, 900, n)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    nz = _noise(n, lp=30)
    env = np.linspace(0, 1, n) ** 2
    m = (tone * 0.5 + nz * 0.5) * env
    return _stereo(m * 0.4)


def sparkle(dur=0.7):
    n = int(dur * SR); t = np.arange(n) / SR
    m = np.zeros(n)
    rng = np.random.default_rng(3)
    for _ in range(7):
        f = rng.uniform(1500, 4000); off = rng.uniform(0, 0.4); o = int(off * SR)
        e = np.zeros(n); e[o:] = _env(n - o, 0.005, 0.3)
        m += np.sin(2 * np.pi * f * t) * e * rng.uniform(0.3, 1)
    return _stereo(m / (np.max(np.abs(m)) + 1e-9) * 0.4)


GENS = {"whoosh": whoosh, "boom": boom, "sting": sting, "chime": chime,
        "rumble": rumble, "click": click, "riser": riser, "sparkle": sparkle}


def save(name, arr):
    a = np.clip(arr, -1, 1); data = (a * 32767).astype(np.int16)
    with wave.open(str(OUT / f"{name}.wav"), "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(data.tobytes())


# scene-type -> (sfx, gain dB) cue at beat start
SCENE_SFX = {
    "title": ("boom", -8), "section": ("boom", -9), "map": ("whoosh", -14),
    "guardian": ("sting", -13), "control": ("click", -16), "quote": ("sparkle", -16),
    "diagram": ("whoosh", -16), "points": ("whoosh", -17), "cheatcard": ("sparkle", -14),
    "quiz": ("riser", -16),
    "coldopen": ("sting", -10), "define": ("sparkle", -17),
    "oath": ("boom", -12), "notebook": ("click", -18),
}


if __name__ == "__main__":
    for name, fn in GENS.items():
        save(name, fn())
        print("sfx:", name)
    (OUT / "manifest.json").write_text(json.dumps(SCENE_SFX, indent=1), encoding="utf-8")
    print("wrote", len(GENS), "sfx +", "manifest")
