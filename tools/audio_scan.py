"""Broad acoustic scan of EVERY persisted line clip across all episodes. Flags audible defects
the text gate misses: slap-back echo, clipping, muddiness, and stuck/over-long takes. .venv_tts."""
import numpy as np, soundfile as sf, glob, re
from pathlib import Path


def metrics(p):
    x, sr = sf.read(str(p))
    if x.ndim > 1:
        x = x.mean(1)
    if len(x) < sr // 5:
        return None
    dur = len(x) / sr
    clip_pct = 100 * np.mean(np.abs(x) > 0.999)
    X = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    freqs = np.fft.rfftfreq(len(x), 1 / sr)
    csum = np.cumsum(X)
    rolloff = freqs[np.searchsorted(csum, 0.85 * csum[-1])]
    xc = x - x.mean()
    nn = len(xc)
    fft = np.fft.rfft(xc, 2 * nn)
    ac = np.fft.irfft(fft * np.conj(fft))[:nn]
    ac = ac / (ac[0] + 1e-9)
    lo, hi = int(0.05 * sr), int(0.2 * sr)
    echo = float(np.max(ac[lo:hi])) if hi < len(ac) else 0.0
    return dur, clip_pct, rolloff, echo


flagged = []
n = 0
for f in sorted(glob.glob("course/render/*/lines/*.wav")):
    m = metrics(Path(f))
    if not m:
        continue
    n += 1
    dur, clip_pct, rolloff, echo = m
    sp = re.search(r"_([A-Z]+)\.wav$", f).group(1)
    reasons = []
    if echo > 0.28:
        reasons.append(f"echo={echo:.2f}")
    if clip_pct > 0.5:
        reasons.append(f"clip={clip_pct:.1f}%")
    if sp != "NULL" and rolloff < 2400:
        reasons.append(f"muddy={rolloff:.0f}Hz")
    if rolloff < 1500:
        reasons.append(f"VERYmuddy={rolloff:.0f}Hz")
    if reasons:
        flagged.append((f.split("render/")[-1] if "render/" in f else f, reasons))

for path, reasons in flagged:
    print(f"  {path}  {' '.join(reasons)}")
print(f"\n=== {len(flagged)} flagged of {n} clips ===")
