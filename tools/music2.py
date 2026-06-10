"""High-quality orchestral underscore beds (Kevin MacLeod, CC-BY 4.0).

Replaces the thin procedural pad with real, professionally produced cinematic
orchestral music, mastered to sit UNDER narration (ducked in build_episode2):
  - high-pass to clear rumble
  - a gentle presence dip (~3 kHz) to carve room for the voice
  - gentle compression so swells never poke through the duck
  - single-pass loudnorm to a consistent bed level
  - seamless crossfade-loop for tracks shorter than the episode
  - long fades in/out

Per-episode mood mapping in TRACKS. Falls back to the synthesized bed
(music.make_bed) if a source asset is missing, so renders never break.

Source tracks are CC-BY 4.0 by Kevin MacLeod (incompetech.com); see
THIRD_PARTY_NOTICES.md. Raw tracks live in tools/music_assets/ (gitignored);
only the rendered videos (with attribution) are published.
"""
from __future__ import annotations
import math
import subprocess
from pathlib import Path

import music  # synthesized fallback

ROOT = Path(__file__).resolve().parent.parent
ASSETS = Path(__file__).resolve().parent / "music_assets"
XFADE = 2.6          # seconds, seamless-loop crossfade
SR = 44100

# Direct CC-BY 4.0 downloads (verified live); used by ensure_assets().
SOURCES = {
    "ossuary6_air.mp3":       "Ossuary 6 - Air.mp3",
    "ossuary1_beginning.mp3": "Ossuary 1 - A Beginning.mp3",
    "long_note_four.mp3":     "Long Note Four.mp3",
    "bittersweet.mp3":        "Bittersweet.mp3",
    "dark_times.mp3":         "Dark Times.mp3",
    "midnight_tale.mp3":      "Midnight Tale.mp3",
    "strength_of_titans.mp3": "Strength of the Titans.mp3",
}
_BASE = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/"

# Per-episode bed (mood-matched). All are Kevin MacLeod, CC-BY 4.0.
TRACKS = {
    "ep00": "long_note_four.mp3",       # orientation: sustained, hopeful, seam-free (10 min)
    "ep00b": "ossuary1_beginning.mp3",  # worked example: a beginning
    "ep7b": "midnight_tale.mp3",        # campaign briefing: contemplative
    "ep01": "ossuary1_beginning.mp3",   # outer walls: noble beginning
    "ep02": "ossuary6_air.mp3",         # watchtowers: dark, vigilant ambient
    "ep03": "bittersweet.mp3",          # the people: hopeful-but-tense
    "ep04": "midnight_tale.mp3",        # governance: contemplative
    "ep05": "dark_times.mp3",           # the forge / supply chain: brooding
    "ep06": "ossuary6_air.mp3",         # vaults & lifelines: disaster-resilience
    "ep07": "strength_of_titans.mp3",   # siege night: epic orchestral
    "ep08": "long_note_four.mp3",       # the campaign: steady forward motion
    "ep09": "midnight_tale.mp3",        # categorization
    "ep10": "bittersweet.mp3",          # baselines / armory
    "ep11": "ossuary1_beginning.mp3",   # the reckoning -> resolution
}
# Slight per-episode start offset (s) so reused tracks don't open identically.
_OFFSET = {"ep06": 40, "ep09": 30, "ep10": 25, "ep11": 35, "ep08": 90}


def _run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _probe_dur(path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


def ensure_assets() -> int:
    """Download any missing CC-BY source tracks. Returns count present."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    have = 0
    import urllib.parse, urllib.request
    for fn, title in SOURCES.items():
        dst = ASSETS / fn
        if dst.exists() and dst.stat().st_size > 200_000:
            have += 1
            continue
        url = _BASE + urllib.parse.quote(title)
        try:
            urllib.request.urlretrieve(url, dst)
            have += 1
        except Exception as e:                          # noqa: BLE001
            print(f"  music asset fetch failed: {fn}: {e}")
    return have


def _asset_for(epid):
    if not epid:
        return None
    fn = TRACKS.get(epid.lower())
    if not fn:
        return None
    p = ASSETS / fn
    return p if p.exists() else None


def _build_loop(src: Path, need: float, offset: float, tmp: Path):
    """Produce a >= need-seconds clip from src (seamless crossfade-loop if short)."""
    src_dur = _probe_dur(src)
    usable = max(1.0, src_dur - offset)
    if usable >= need:
        _run(["ffmpeg", "-y", "-ss", f"{offset}", "-i", str(src), "-t", f"{need:.2f}",
              "-ar", str(SR), "-ac", "2", str(tmp)])
        return tmp
    # need to loop: chain acrossfades of the (offset-trimmed) track with itself
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


def make_bed(duration: float, out_path: str, epid: str | None = None, seed: int = 7):
    """Write a mastered orchestral bed of `duration` seconds to out_path (stereo WAV)."""
    src = _asset_for(epid)
    if src is None:
        # try to fetch on demand, then fall back to the synth pad
        try:
            ensure_assets()
            src = _asset_for(epid)
        except Exception:                               # noqa: BLE001
            src = None
    if src is None:
        return music.make_bed(duration, out_path, seed=seed)

    out = Path(out_path)
    offset = float(_OFFSET.get((epid or "").lower(), 0))
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
    n = ensure_assets()
    print(f"assets present: {n}/{len(SOURCES)}")
    dur = float(sys.argv[1]) if len(sys.argv) > 1 else 30.0
    ep = sys.argv[2] if len(sys.argv) > 2 else "ep07"
    out = sys.argv[3] if len(sys.argv) > 3 else "tools/_tmp/bed2.wav"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    make_bed(dur, out, epid=ep)
    print("wrote", out, dur, "s  (", ep, "->", TRACKS.get(ep), ")")
