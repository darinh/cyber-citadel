"""Locally-synthesized ambient music bed (no copyrighted audio).

A calm-but-tense evolving pad for the "citadel under siege while you learn" mood.
make_bed(duration_seconds, out_path).
"""
from __future__ import annotations
import sys
import wave
from pathlib import Path
import numpy as np

SR = 44100


def _osc(freq, t, kind="sine", detune=0.0):
    f = freq * (1 + detune)
    if kind == "saw":
        return 2 * (t * f - np.floor(0.5 + t * f))
    return np.sin(2 * np.pi * f * t)


def make_bed(duration: float, out_path: str, key_hz: float = 110.0, seed: int = 7):
    rng = np.random.default_rng(seed)
    n = int(duration * SR)
    t = np.arange(n) / SR
    # minor-ish stack: root, minor third-ish (6/5), fifth, octave, high fifth
    partials = [(key_hz, 0.5), (key_hz * 1.2, 0.22), (key_hz * 1.5, 0.32),
                (key_hz * 2.0, 0.18), (key_hz * 3.0, 0.08)]
    left = np.zeros(n)
    right = np.zeros(n)
    for i, (f, amp) in enumerate(partials):
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * (0.03 + 0.017 * i) * t + i)
        det = 0.002 * np.sin(2 * np.pi * 0.07 * t)
        v = amp * lfo * (_osc(f, t, "sine") + 0.3 * _osc(f, t, "saw", det))
        pan = 0.5 + 0.35 * np.sin(0.05 * i + 0.2)
        left += v * (1 - pan)
        right += v * pan
    # airy filtered noise (slow)
    noise = rng.standard_normal(n)
    k = 600
    kernel = np.ones(k) / k
    noise = np.convolve(noise, kernel, mode="same")
    swell = 0.5 + 0.5 * np.sin(2 * np.pi * 0.013 * t)
    left += 0.05 * noise * swell
    right += 0.05 * np.roll(noise, 500) * swell
    # subtle low pulse (heartbeat of the siege)
    pulse_env = (np.sin(2 * np.pi * 0.5 * t) > 0.985).astype(float)
    pulse = np.convolve(pulse_env, np.exp(-np.linspace(0, 6, int(0.25 * SR))), mode="same")
    sub = 0.12 * pulse * _osc(key_hz / 2, t, "sine")
    left += sub
    right += sub

    stereo = np.stack([left, right], axis=1)
    # normalize + gentle soft clip
    stereo /= (np.max(np.abs(stereo)) + 1e-9)
    stereo = np.tanh(stereo * 1.2) * 0.5  # headroom; sits under narration
    # fades
    fade = int(2.5 * SR)
    env = np.ones(n)
    env[:fade] = np.linspace(0, 1, fade)
    env[-fade:] = np.linspace(1, 0, fade)
    stereo *= env[:, None]

    data = (stereo * 32767).astype(np.int16)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    return out_path


if __name__ == "__main__":
    dur = float(sys.argv[1]) if len(sys.argv) > 1 else 20.0
    out = sys.argv[2] if len(sys.argv) > 2 else "tools/_tmp/bed.wav"
    make_bed(dur, out)
    print("wrote", out, dur, "s")
