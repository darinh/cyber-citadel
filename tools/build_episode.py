"""Episode assembler: spec JSON -> narrated, captioned, scored 1080p mp4.

For each beat: synth narration lines (tts) -> padded beat audio; render still
(scene) -> Ken-Burns clip (ffmpeg zoompan). Concat clips; burn SRT captions;
mix locally-synthesized music; add fades. Output to course/episodes/.

Usage: python build_episode.py course/scripts/ep00.json [--beats N]
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scene
import tts
import music

ROOT = Path(__file__).resolve().parent.parent
FPS = 30
LEAD, GAP, TAIL = 0.35, 0.32, 0.75


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(map(str, cmd))}\n{p.stdout[-2000:]}")
    return p.stdout


def dur_of(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip()
    return float(out)


def srt_time(s):
    h = int(s // 3600); m = int((s % 3600) // 60); sec = int(s % 60); ms = int(round((s - int(s)) * 1000))
    if ms == 1000:
        sec += 1; ms = 0
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def ass_time(s):
    cs = int(round(s * 100)); h = cs // 360000; m = (cs % 360000) // 6000
    sec = (cs % 6000) // 100; c = cs % 100
    return f"{h}:{m:02d}:{sec:02d}.{c:02d}"


def chunk_caption(speaker, text, start, dur, max_words=8):
    words = text.split()
    if not words:
        return []
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= max_words:
            chunks.append(" ".join(cur)); cur = []
    if cur:
        chunks.append(" ".join(cur))
    lens = [len(c) for c in chunks]; tot = sum(lens) or 1
    label = "" if speaker == "NARRATOR" else f"{speaker}:  "
    cues, t = [], start
    for i, c in enumerate(chunks):
        d = dur * (lens[i] / tot)
        cues.append((t, t + d, (label if i == 0 else "") + c))
        t += d
    return cues


ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Segoe UI Semibold,42,&H00F5ECE8,&H00FFFFFF,&H00140A06,&H96000000,-1,0,0,0,100,100,0,0,1,3,1,2,260,260,42,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def write_captions(cues, ass_path, srt_path):
    ev = []
    for a, b, tx in cues:
        ev.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,{tx}")
    ass_path.write_text(ASS_HEADER + "\n".join(ev) + "\n", encoding="utf-8")
    sl = []
    for k, (a, b, tx) in enumerate(cues, 1):
        sl.append(f"{k}\n{srt_time(a)} --> {srt_time(b)}\n{tx}\n")
    srt_path.write_text("\n".join(sl), encoding="utf-8")


def silence(dur, path):
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=22050:cl=mono",
         "-t", f"{dur:.3f}", "-c:a", "pcm_s16le", str(path)])


def build_beat_audio(lines, bdir, idx, min_seconds):
    """lines: list of (speaker,text). Returns (path, duration, [line starts], [line durs])."""
    parts = []
    line_wavs = []
    line_durs = []
    s_lead = bdir / f"sil_lead.wav"; silence(LEAD, s_lead)
    s_gap = bdir / f"sil_gap.wav"; silence(GAP, s_gap)
    parts.append(s_lead)
    for k, (sp, tx) in enumerate(lines):
        w = bdir / f"l{idx}_{k}.wav"
        d = tts.synth_line(sp, tx, w)
        line_wavs.append(w); line_durs.append(d)
        parts.append(w)
        if k < len(lines) - 1:
            parts.append(s_gap)
    # compute starts
    starts = []
    acc = LEAD
    for k, d in enumerate(line_durs):
        starts.append(acc)
        acc += d + (GAP if k < len(line_durs) - 1 else 0)
    body = acc  # end of last line
    tail = TAIL
    total = body + tail
    extra = 0.0
    if total < min_seconds:
        extra = min_seconds - total
    s_tail = bdir / f"sil_tail{idx}.wav"; silence(tail + extra, s_tail)
    parts.append(s_tail)
    # concat via filter
    inputs = []
    for p in parts:
        inputs += ["-i", str(p)]
    n = len(parts)
    fc = "".join(f"[{i}:a]" for i in range(n)) + f"concat=n={n}:v=0:a=1[a]"
    out = bdir / f"beat{idx}.wav"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-map", "[a]",
         "-c:a", "pcm_s16le", "-ar", "22050", "-ac", "1", str(out)])
    return out, dur_of(out), starts, line_durs


MOTION = [
    ("iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),                 # center
    ("(iw-iw/zoom)*on/{D}", "ih/2-(ih/zoom/2)"),              # pan L->R
    ("iw/2-(iw/zoom/2)", "(ih-ih/zoom)*on/{D}"),              # pan T->B
    ("(iw-iw/zoom)*(1-on/{D})", "ih/2-(ih/zoom/2)"),          # pan R->L
    ("iw/2-(iw/zoom/2)", "(ih-ih/zoom)*(1-on/{D})"),          # pan B->T
]


def build_clip(png, beat_audio, dur, idx, out_mp4, static=False):
    durf = max(2, int(round(dur * FPS)))
    zmax = 1.045
    inc = (zmax - 1.0) / durf
    if static:
        vf = f"scale=1920:1080,setsar=1,fps={FPS}"
    else:
        xexpr, yexpr = MOTION[idx % len(MOTION)]
        xexpr = xexpr.format(D=durf); yexpr = yexpr.format(D=durf)
        vf = (f"scale=3840:2160,zoompan=z='min(zoom+{inc:.6f},{zmax})':d={durf}"
              f":x='{xexpr}':y='{yexpr}':s=1920x1080:fps={FPS},setsar=1")
    run(["ffmpeg", "-y", "-loop", "1", "-t", f"{dur:.3f}", "-i", str(png),
         "-i", str(beat_audio), "-filter_complex", f"[0:v]{vf}[v]",
         "-map", "[v]", "-map", "1:a", "-t", f"{dur:.3f}",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         str(out_mp4)])


def assemble(spec_path, limit=None):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    epid = spec["id"].lower()
    tag = spec.get("tag", spec["id"])
    bdir = ROOT / "tools" / "_tmp" / "build" / epid
    if bdir.exists():
        for f in bdir.glob("*"):
            f.unlink()
    bdir.mkdir(parents=True, exist_ok=True)

    beats = spec["beats"]
    if limit:
        beats = beats[:limit]
    timeline = 0.0
    clips = []
    cues = []
    STATIC = {"quiz"}
    for i, beat in enumerate(beats):
        beat = dict(beat)
        beat.setdefault("tag", tag)
        lines = [(s[0], s[1]) for s in beat.get("say", [])]
        min_s = beat.get("min_seconds", 2.6 if lines else 3.0)
        ba, bdur, starts, ldurs = build_beat_audio(lines, bdir, i, min_s)
        png = bdir / f"scene{i:02d}.jpg"
        scene.render(beat, str(png))
        clip = bdir / f"clip{i:02d}.mp4"
        static = beat.get("motion", "") == "static" or beat["scene"] in STATIC
        build_clip(png, ba, bdur, i, clip, static=static)
        clips.append(clip)
        for (sp, tx), st, ld in zip(lines, starts, ldurs):
            txt = tx.replace("—", "-")
            cues.extend(chunk_caption(sp, txt, timeline + st, ld))
        timeline += bdur
        print(f"  beat {i:02d} [{beat['scene']:9s}] {bdur:5.1f}s  (total {timeline:5.1f}s)")

    # concat clips
    listf = bdir / "concat.txt"
    listf.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    ep_raw = bdir / "ep_raw.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf), "-c", "copy", str(ep_raw)])

    # captions (ass for burn-in, srt sidecar)
    write_captions(cues, bdir / "ep.ass", bdir / "ep.srt")

    # music
    musicwav = bdir / "music.wav"
    music.make_bed(timeline + 0.5, str(musicwav))

    # final: burn captions + mix music + fades (run in bdir so subs path is simple)
    T = timeline
    vf = (f"[0:v]fade=t=in:st=0:d=0.8,fade=t=out:st={T-0.8:.2f}:d=0.8,"
          f"subtitles=ep.ass[v]")
    af = (f"[1:a]volume=0.13[m];[0:a][m]amix=inputs=2:normalize=0,"
          f"afade=t=in:st=0:d=0.8,afade=t=out:st={T-0.8:.2f}:d=0.8[a]")
    out_dir = ROOT / "course" / "episodes"
    out_dir.mkdir(parents=True, exist_ok=True)
    title_slug = spec.get("slug", epid)
    final = out_dir / f"{epid}_{title_slug}.mp4"
    run(["ffmpeg", "-y", "-i", "ep_raw.mp4", "-i", "music.wav",
         "-filter_complex", vf + ";" + af, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final)], cwd=str(bdir))
    # ship sidecar srt
    (out_dir / f"{epid}_{title_slug}.srt").write_text((bdir / "ep.srt").read_text(encoding="utf-8"), encoding="utf-8")
    print(f"\nEPISODE: {final}  ({T/60:.1f} min, {len(beats)} beats)")
    return final


if __name__ == "__main__":
    spec = sys.argv[1]
    limit = None
    if "--beats" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--beats") + 1])
    assemble(spec, limit)
