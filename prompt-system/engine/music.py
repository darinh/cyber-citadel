"""Music bed — SOURCED public-domain / Creative-Commons orchestral underscore only.

Per the project rule, music is NEVER generated (AI music is low quality + license-murky).
A bed is produced ONLY from a real, license-clean source track that the course author has
placed in `<project>/assets/music/` (CC0 / public-domain / CC-BY-with-attribution). If a
beat/episode has no source track, this writes SILENCE — the render still succeeds, it just
has no music. (See system-prompts/07_music_and_sfx.md for sourcing + attribution.)

A track is selected, in order:
  1. spec["music"]  (a filename in assets/music/, or an absolute path)
  2. theme music mood map: theme["music"]["tracks"][epid]  (filename in assets/music/)
  3. theme["music"]["default"]                              (filename in assets/music/)
  4. none -> silent bed.

The chosen track is loop-extended (seamless crossfade) to the needed length and mastered
to sit UNDER narration: high-pass, a presence dip ~3 kHz to carve room for the voice,
gentle compression, loudnorm to a consistent bed level, and long fades.
"""
from __future__ import annotations

import math
import os
import subprocess
from pathlib import Path

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme as _theme

PROJECT = Path(os.environ.get("CC_PROJECT") or Path.cwd())
MUSIC_DIR = PROJECT / "assets" / "music"
XFADE = 2.6          # seconds, seamless-loop crossfade
SR = 44100


def _run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _probe_dur(path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


def _resolve(name):
    if not name:
        return None
    p = Path(name)
    if p.is_absolute() and p.exists():
        return p
    cand = MUSIC_DIR / name
    return cand if cand.exists() else None


def _select_track(epid, spec):
    t = _theme.load()
    music_cfg = t.get("music", {}) or {}
    for cand in (
        (spec or {}).get("music"),
        (music_cfg.get("tracks", {}) or {}).get((epid or "").lower()),
        music_cfg.get("default"),
    ):
        p = _resolve(cand)
        if p:
            return p
    return None


def _silence(duration, out_path):
    _run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo",
          "-t", f"{max(0.1, duration):.3f}", "-ar", str(SR), "-ac", "2", str(out_path)])
    return str(out_path)


def _build_loop(src: Path, need: float, offset: float, tmp: Path):
    """Produce a >= need-seconds clip from src (seamless crossfade-loop if short)."""
    src_dur = _probe_dur(src)
    usable = max(1.0, src_dur - offset)
    if usable >= need:
        _run(["ffmpeg", "-y", "-ss", f"{offset}", "-i", str(src), "-t", f"{need:.2f}",
              "-ar", str(SR), "-ac", "2", str(tmp)])
        return tmp
    n = math.ceil((need + XFADE) / (usable - XFADE)) + 1
    inputs = []
    for _ in range(n):
        inputs += ["-ss", f"{offset}", "-i", str(src)]
    fc, prev = "", "[0:a]"
    for i in range(1, n):
        lbl = f"[a{i}]"
        fc += f"{prev}[{i}:a]acrossfade=d={XFADE}:c1=tri:c2=tri{lbl};"
        prev = lbl
    fc += f"{prev}atrim=0:{need:.2f}[out]"
    _run(["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-map", "[out]",
          "-ar", str(SR), "-ac", "2", str(tmp)])
    return tmp


def make_bed(duration: float, out_path: str, epid: str | None = None,
             spec: dict | None = None, seed: int = 7):
    """Write a mastered orchestral bed of `duration` seconds, OR silence if no source
    track is configured. Returns out_path. NEVER synthesizes music."""
    out = Path(out_path)
    src = _select_track(epid, spec)
    if src is None:
        return _silence(duration, out)

    offset = float(((spec or {}).get("music_offset")) or 0)
    need = duration + 0.4
    loop = _build_loop(src, need, offset, out.with_suffix(".loop.wav"))
    fout = duration - 1.4
    af = (
        "highpass=f=72,"
        "equalizer=f=3000:width_type=q:w=1.2:g=-4.5,"          # carve voice room
        "acompressor=threshold=-20dB:ratio=3:attack=20:release=320:makeup=3,"
        "loudnorm=I=-20:TP=-2:LRA=11,"
        f"afade=t=in:st=0:d=1.4,afade=t=out:st={max(0.0, fout):.2f}:d=1.4"
    )
    _run(["ffmpeg", "-y", "-i", str(loop), "-af", af, "-t", f"{duration:.3f}",
          "-ar", str(SR), "-ac", "2", str(out)])
    try:
        loop.unlink(missing_ok=True)
    except Exception:                                   # noqa: BLE001
        pass
    return str(out)


if __name__ == "__main__":
    import sys
    dur = float(sys.argv[1]) if len(sys.argv) > 1 else 20.0
    ep = sys.argv[2] if len(sys.argv) > 2 else None
    out = sys.argv[3] if len(sys.argv) > 3 else str(PROJECT / ".cache" / "bed_test.wav")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    make_bed(dur, out, epid=ep)
    print("wrote", out, dur, "s  (source:", _select_track(ep, None) or "NONE -> silent", ")")
