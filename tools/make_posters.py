"""Generate poster thumbnails for each episode mp4 so the web player shows a frame, not black.

Picks a bright, representative frame: prefers the start of early non-quiz chapters (designed
title/section/guardian cards), skips dark cold-opens, and guards against near-black frames by
sampling luma. Dependency-free (ffmpeg only). Writes course/episodes/<epid>_<slug>.jpg.

Usage:  python tools/make_posters.py            # all episodes
        python tools/make_posters.py ep00 ep04  # specific
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPID = ROOT / "course" / "episodes"
W, H = 1280, 720
MIN_LUMA = 55          # 0..255; below this a frame is too dark to be a good poster


def dur(mp4):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def mean_luma(mp4, t):
    """Average luma (0..255) of a small grayscale sample of the frame at time t."""
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(mp4),
                        "-frames:v", "1", "-vf", "scale=80:45,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True)
    b = p.stdout
    return (sum(b) / len(b)) if b else 0.0


def candidates(epid, total):
    """Times to try, best-first: early non-quiz chapter cards, then spread fallbacks."""
    ts = []
    cf = EPID / f"{epid}.cues.json"
    if cf.exists():
        try:
            chaps = json.loads(cf.read_text(encoding="utf-8")).get("chapters", [])
            for ch in chaps:
                t = float(ch.get("t", 0))
                if t >= 8 and t <= total * 0.6 and not str(ch.get("title", "")).lower().startswith("quiz"):
                    ts.append(t + 2.5)        # land mid-card, past the fade-in
        except Exception:
            pass
    ts += [max(8.0, total * 0.12), total * 0.22, total * 0.33, total * 0.45, 10.0]
    # de-dupe (within 1s), keep order
    out = []
    for t in ts:
        if all(abs(t - u) > 1.0 for u in out) and 0 < t < max(1, total - 3):
            out.append(t)
    return out


def make(mp4):
    epid = mp4.stem.split("_")[0]
    total = dur(mp4)
    if total <= 0:
        print(f"  {mp4.name}: no duration, skip"); return None
    best_t, best_l = None, -1.0
    for t in candidates(epid, total):
        l = mean_luma(mp4, t)
        if l > best_l:
            best_l, best_t = l, t
        if l >= MIN_LUMA:                     # first sufficiently-bright frame wins
            best_t = t; break
    out = mp4.with_suffix(".jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{best_t:.2f}", "-i", str(mp4),
                    "-frames:v", "1",
                    "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                    "-q:v", "3", str(out)], check=True)
    print(f"  {out.name}  @ {best_t:.1f}s  luma={best_l:.0f}")
    return out


def main():
    eps = sys.argv[1:]
    mp4s = sorted(EPID.glob("*.mp4"))
    if eps:
        mp4s = [m for m in mp4s if m.stem.split("_")[0] in eps]
    print(f"posters for {len(mp4s)} episode(s):")
    for m in mp4s:
        make(m)


if __name__ == "__main__":
    main()
