"""v2 episode assembler.

Upgrades over v1:
- Kokoro voices + per-character mastering (tts2)
- Two-phase quizzes: question + on-screen COUNTDOWN (think time) -> answer reveal
- Global audio mix: narration + music DUCKED under speech + procedural SFX bed
- Per-speaker caption colors (ASS)
- Emits course/episodes/epNN.cues.json (chapters + quiz cues) for the interactive player

Video is hard-cut concat (video duration == narration duration, perfect sync);
transition SFX (whoosh/boom) cover the cuts so they read as "produced".
"""
from __future__ import annotations
import json
import shutil
import subprocess
import sys
import wave
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scene
import tts2 as tts
import music
import music2
import sfx as SFX

ROOT = Path(__file__).resolve().parent.parent
FPS = 30
ASR = 24000          # narration sample rate (kokoro)
MSR = 48000          # final mix sample rate
LEAD, GAP, TAIL = 0.35, 0.30, 0.7
QUIZ_THINK = 6.0     # seconds of think time during the question phase
REVEAL_HOLD = 3.6
FONTB = "C\\:/Windows/Fonts/segoeuib.ttf"

SPEAKER_COLOR = {  # ASS &HBBGGRR
    "NARRATOR": "&H00F5ECE8", "VEGA": "&H00FFE138", "NOVA": "&H00D4EA5E",
    "ARCHIVIST": "&H0057C8FF", "NULL": "&H00AC3CFF", "HERALD": "&H00FA8EA7",
}

EP_BG = {  # per-episode atmospheric backdrop (course/art/backgrounds/<name>.png)
    "ep00": "citadel", "ep01": "walls", "ep02": "watch", "ep03": "people",
    "ep04": "council", "ep05": "forge", "ep06": "vault", "ep07": "network",
    "ep08": "network", "ep09": "council", "ep10": "forge", "ep11": "council",
}

AVATAR_DIR = ROOT / "course" / "art" / "avatars"
AV_X, AV_Y = 48, 900     # avatar position (bottom-left, beside the subtitle)

# preload sfx wavs (48k stereo)
_SFX = {}
for p in (ROOT / "tools" / "sfx").glob("*.wav"):
    with wave.open(str(p)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32767
        _SFX[p.stem] = a.reshape(-1, 2) if w.getnchannels() == 2 else np.stack([a, a], 1)


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(map(str, cmd))}\n{p.stdout[-2000:]}")
    return p.stdout


def dur_of(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip()
    return float(out)


def tcode(s, sep=","):
    h = int(s // 3600); m = int((s % 3600) // 60); sec = int(s % 60); ms = int(round((s - int(s)) * 1000))
    if ms == 1000: sec += 1; ms = 0
    return f"{h:02d}:{m:02d}:{sec:02d}{sep}{ms:03d}"


def ass_time(s):
    cs = int(round(s * 100)); h = cs // 360000; m = (cs % 360000) // 6000
    return f"{h}:{m:02d}:{(cs % 6000) // 100:02d}.{cs % 100:02d}"


def silence(dur, path, sr=ASR):
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={sr}:cl=mono",
         "-t", f"{dur:.3f}", "-c:a", "pcm_s16le", str(path)])


def build_beat_audio(lines, bdir, idx, min_seconds, extra_tail=0.0):
    parts = []
    s_lead = bdir / "sil_lead.wav"; silence(LEAD, s_lead)
    s_gap = bdir / "sil_gap.wav"; silence(GAP, s_gap)
    parts.append(s_lead)
    line_durs = []
    for k, (sp, tx) in enumerate(lines):
        w = bdir / f"l{idx}_{k}.wav"
        line_durs.append(tts.synth_line(sp, tx, w))
        parts.append(w)
        if k < len(lines) - 1:
            parts.append(s_gap)
    starts, acc = [], LEAD
    for k, d in enumerate(line_durs):
        starts.append(acc); acc += d + (GAP if k < len(line_durs) - 1 else 0)
    total = acc + TAIL + extra_tail
    if total < min_seconds:
        total = min_seconds
    s_tail = bdir / f"tail{idx}.wav"; silence(total - acc, s_tail)
    parts.append(s_tail)
    inputs = []
    for p in parts:
        inputs += ["-i", str(p)]
    fc = "".join(f"[{i}:a]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[a]"
    out = bdir / f"beat{idx}.wav"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-map", "[a]",
         "-c:a", "pcm_s16le", "-ar", str(ASR), "-ac", "1", str(out)])
    return out, dur_of(out), starts, line_durs


MOTION = [("iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
          ("(iw-iw/zoom)*on/{D}", "ih/2-(ih/zoom/2)"),
          ("iw/2-(iw/zoom/2)", "(ih-ih/zoom)*on/{D}"),
          ("(iw-iw/zoom)*(1-on/{D})", "ih/2-(ih/zoom/2)"),
          ("iw/2-(iw/zoom/2)", "(ih-ih/zoom)*(1-on/{D})")]


def build_clip(png, dur, idx, out_mp4, static=False, countdown=None, fade_in=False):
    durf = max(2, int(round(dur * FPS)))
    zmax = 1.045; inc = (zmax - 1.0) / durf
    if static:
        vf = f"scale=1920:1080,setsar=1,fps={FPS}"
    else:
        xe, ye = MOTION[idx % len(MOTION)]
        vf = (f"scale=3840:2160,zoompan=z='min(zoom+{inc:.6f},{zmax})':d={durf}"
              f":x='{xe.format(D=durf)}':y='{ye.format(D=durf)}':s=1920x1080:fps={FPS},setsar=1")
    if fade_in:
        vf += ",fade=t=in:st=0:d=0.45"
    if countdown is not None:
        # gold countdown number, top-center, showing THINK-time remaining
        vf += (f",drawtext=fontfile='{FONTB}':text='%{{eif\\:max(0\\,ceil(min({countdown}\\,{dur:.2f}-t)))\\:d}}'"
               f":fontsize=96:fontcolor=0xFFC857:x=(w-text_w)/2:y=92:"
               f"box=1:boxcolor=0x0A0E27AA:boxborderw=18")
    run(["ffmpeg", "-y", "-loop", "1", "-t", f"{dur:.3f}", "-i", str(png),
         "-filter_complex", f"[0:v]{vf}[v]", "-map", "[v]", "-t", f"{dur:.3f}",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-an", str(out_mp4)])


ANIM = 1.4               # entrance-animation seconds for map/diagram beats
ANIM_SCENES = {"map", "diagram"}


def build_clip_anim(beat, dur, idx, out_mp4, bdir):
    """Render a beat as an entrance animation (scene rendered at progress t)
    over ANIM seconds, then hold the final frame for the remaining duration."""
    F = max(2, int(round(ANIM * FPS)))
    fdir = bdir / f"anim{idx:03d}"
    fdir.mkdir(exist_ok=True)
    for k in range(F):
        t = k / (F - 1)
        te = 1 - (1 - t) ** 2            # ease-out
        scene.render(beat, str(fdir / f"f{k:04d}.jpg"), t=te)
    hold = max(0.0, dur - ANIM)
    run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(fdir / "f%04d.jpg"),
         "-vf", f"tpad=stop_mode=clone:stop_duration={hold:.3f},scale=1920:1080,setsar=1,fps={FPS}",
         "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-an", str(out_mp4)])


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
        cues.append((t, t + d, (label if i == 0 else "") + c, speaker)); t += d
    return cues


ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Segoe UI Semibold,42,&H00F5ECE8,&H00FFFFFF,&H00140A06,&H96000000,-1,0,0,0,100,100,0,0,1,3,1,2,240,240,42,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def write_captions(cues, ass_path, srt_path):
    ev = []
    for a, b, tx, sp in cues:
        col = SPEAKER_COLOR.get(sp, "&H00F5ECE8")
        ital = "\\i1" if sp == "NULL" else ""
        ev.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,{{\\c{col}{ital}\\fad(120,120)}}{tx}")
    ass_path.write_text(ASS_HEAD + "\n".join(ev) + "\n", encoding="utf-8")
    sl = [f"{k}\n{tcode(a)} --> {tcode(b)}\n{tx}\n" for k, (a, b, tx, sp) in enumerate(cues, 1)]
    srt_path.write_text("\n".join(sl), encoding="utf-8")


def build_sfx_bed(cues, total, out_path):
    n = int(total * MSR) + MSR
    bed = np.zeros((n, 2), dtype=np.float32)
    for t, name, gain_db in cues:
        a = _SFX.get(name)
        if a is None:
            continue
        g = 10 ** (gain_db / 20.0)
        i0 = int(t * MSR); i1 = min(n, i0 + len(a))
        bed[i0:i1] += a[:i1 - i0] * g
    bed = np.clip(bed, -1, 1)
    data = (bed * 32767).astype(np.int16)
    with wave.open(str(out_path), "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(MSR); w.writeframes(data.tobytes())


def assemble(spec_path, limit=None):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    epid = spec["id"].lower(); tag = spec.get("tag", spec["id"])
    bgp = ROOT / "course" / "art" / "backgrounds" / f"{EP_BG.get(epid, 'citadel')}.png"
    scene.set_background(str(bgp) if bgp.exists() else None)
    bdir = ROOT / "tools" / "_tmp" / "build2" / epid
    if bdir.exists():
        shutil.rmtree(bdir, ignore_errors=True)
    bdir.mkdir(parents=True, exist_ok=True)
    beats = spec["beats"][:limit] if limit else spec["beats"]

    timeline = 0.0
    clips, beat_audios, cap_cues, sfx_cues, quiz_cues, chapters = [], [], [], [], [], []
    avatar_cues = []

    def add_clip(beat, idx, lines, min_s, static, countdown=None, extra_tail=0.0):
        nonlocal timeline
        ba, bdur, starts, ldurs = build_beat_audio(lines, bdir, idx, min_s, extra_tail)
        beat = dict(beat); beat.setdefault("tag", tag)
        clip = bdir / f"c{idx:03d}.mp4"
        sc = beat["scene"]
        if sc in ANIM_SCENES:
            build_clip_anim(beat, bdur, idx, clip, bdir)
        else:
            png = bdir / f"s{idx:03d}.jpg"
            scene.render(beat, str(png))
            build_clip(png, bdur, idx, clip, static=static, countdown=countdown,
                       fade_in=(sc in ("title", "section")))
        clips.append(clip); beat_audios.append(ba)
        sname, sgain = SFX.SCENE_SFX.get(sc, ("whoosh", -17))
        sfx_cues.append((timeline + 0.02, sname, sgain))
        if any(sp == "NULL" for sp, _ in lines):
            sfx_cues.append((timeline + 0.05, "rumble", -16))
        for (sp, tx), st, ld in zip(lines, starts, ldurs):
            cap_cues.extend(chunk_caption(sp, tx.replace("—", "-"), timeline + st, ld))
            avatar_cues.append((sp, timeline + st, timeline + st + ld))
        narr_end = (starts[-1] + ldurs[-1]) if ldurs else 0.0
        start = timeline
        timeline += bdur
        return start, bdur, narr_end

    qn = 0
    for i, beat in enumerate(beats):
        sc = beat.get("scene")
        lines = [(s[0], s[1]) for s in beat.get("say", [])]
        if sc == "quiz":
            qn += 1
            # phase 1: question + think countdown (answer hidden)
            qbeat = dict(beat); qbeat["reveal"] = False
            q_start, q_dur, q_narr = add_clip(qbeat, i * 10, lines, beat.get("min_seconds", 6),
                                              static=True, countdown=QUIZ_THINK, extra_tail=QUIZ_THINK)
            # phase 2: reveal
            letter = chr(65 + beat.get("answer", 0))
            rbeat = dict(beat); rbeat["reveal"] = True
            r_start, r_dur, _ = add_clip(rbeat, i * 10 + 1,
                                         [["VEGA", f"The answer is {letter}."]],
                                         REVEAL_HOLD, static=True)
            sfx_cues.append((r_start + 0.02, "chime", -12))
            quiz_cues.append({"n": qn, "q": beat.get("q", ""), "options": beat.get("options", []),
                              "answer": beat.get("answer", 0),
                              "t_question": round(q_start, 2),
                              "t_quiz": round(q_start + q_narr, 2),
                              "t_reveal": round(r_start, 2),
                              "t_resume": round(r_start + r_dur, 2)})
            chapters.append({"t": round(q_start, 2), "title": f"Quiz {qn}"})
        else:
            static = sc in ("control", "quote", "cheatcard", "points", "diagram",
                            "define", "coldopen", "oath", "notebook")
            ms = beat.get("min_seconds", 2.6 if lines else 3.0)
            if sc in ("points", "cheatcard"):     # dense slides need time to read
                ms = max(ms, 3.5 + 1.7 * len(beat.get("bullets", [])))
            elif sc == "notebook":
                ms = max(ms, 3.5 + 1.4 * len(beat.get("lines", [])))
            elif sc == "define":                  # let beginners read the definition
                ms = max(ms, 6.0)
            elif sc == "coldopen":
                ms = max(ms, 6.5)
            elif sc == "control":
                ms = max(ms, 6.5)
            st, du, _ = add_clip(beat, i * 10, lines, ms, static=static)
            if sc in ("title", "section", "map"):
                chapters.append({"t": round(st, 2),
                                 "title": beat.get("title", sc).title()})

    # concat video (hard cut)
    listf = bdir / "v.txt"
    listf.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    video = bdir / "video.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf), "-c", "copy", str(video)])

    # concat narration
    alist = bdir / "a.txt"
    alist.write_text("".join(f"file '{a.as_posix()}'\n" for a in beat_audios), encoding="utf-8")
    narr = bdir / "narr.wav"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(alist), "-c", "copy", str(narr)])

    T = timeline
    write_captions(cap_cues, bdir / "ep.ass", bdir / "ep.srt")
    musicwav = bdir / "music.wav"; music2.make_bed(T + 0.5, str(musicwav), epid=epid)
    sfxbed = bdir / "sfx.wav"; build_sfx_bed(sfx_cues, T, sfxbed)

    out_dir = ROOT / "course" / "episodes"; out_dir.mkdir(parents=True, exist_ok=True)
    slug = spec.get("slug", epid)
    final = out_dir / f"{epid}_{slug}.mp4"
    # avatar overlays: speaker portrait beside their subtitle
    speakers = {}
    for sp, s0, e0 in avatar_cues:
        if (AVATAR_DIR / f"{sp}.png").exists():
            speakers.setdefault(sp, []).append((s0, e0))
    av_inputs, av_chain, prev = [], "", "[vb]"
    for k, (sp, wins) in enumerate(speakers.items()):
        av_inputs += ["-loop", "1", "-i", str(AVATAR_DIR / f"{sp}.png")]
        en = "+".join(f"between(t,{s:.2f},{e:.2f})" for s, e in wins)
        av_chain += f"{prev}[{4 + k}:v]overlay={AV_X}:{AV_Y}:enable='{en}'[av{k}];"
        prev = f"[av{k}]"
    audio_fc = (
        f"[1:a]aresample={MSR},aformat=channel_layouts=stereo[narr];"
        f"[2:a]aresample={MSR},aformat=channel_layouts=stereo,volume=0.42[mus];"
        f"[3:a]aformat=channel_layouts=stereo[sfx];"
        f"[narr]asplit=2[narrA][narrSC];"
        f"[mus][narrSC]sidechaincompress=threshold=0.05:ratio=7:attack=5:release=320[mduck];"
        f"[narrA][mduck][sfx]amix=inputs=3:normalize=0:dropout_transition=0[mix];"
        f"[mix]afade=t=in:st=0:d=0.6,afade=t=out:st={T-0.8:.2f}:d=0.8[a];"
    )
    video_fc = (f"[0:v]fade=t=in:st=0:d=0.6,fade=t=out:st={T-0.8:.2f}:d=0.8[vb];"
                + av_chain + f"{prev}subtitles=ep.ass[v]")
    run(["ffmpeg", "-y", "-i", "video.mp4", "-i", "narr.wav", "-i", "music.wav", "-i", "sfx.wav",
         *av_inputs, "-filter_complex", audio_fc + video_fc, "-map", "[v]", "-map", "[a]",
         "-t", f"{T:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final)], cwd=str(bdir))

    (out_dir / f"{epid}_{slug}.srt").write_text((bdir / "ep.srt").read_text(encoding="utf-8"), encoding="utf-8")
    cues = {"id": spec["id"], "title": spec.get("tag", spec["id"]), "duration": round(T, 2),
            "chapters": chapters, "quizzes": quiz_cues}
    (out_dir / f"{epid}.cues.json").write_text(json.dumps(cues, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"EPISODE: {final}  ({T/60:.1f} min, {len(beats)} beats, {len(quiz_cues)} quizzes)")
    return final


if __name__ == "__main__":
    spec = sys.argv[1]
    limit = int(sys.argv[sys.argv.index("--beats") + 1]) if "--beats" in sys.argv else None
    assemble(spec, limit)
