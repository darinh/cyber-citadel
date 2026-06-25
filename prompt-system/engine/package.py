"""Package a generated course for LOCAL playback (no GitHub Pages / no publishing).

Scans <project>/course/episodes/*.cues.json (+ matching mp4 + the source spec) and:
  - derives per-episode metadata (number/title/subtitle/synopsis),
  - makes a bright poster frame per episode (so the player never shows black),
  - converts each .srt caption file to .vtt,
  - writes course/episodes/manifest.json  = { brand, theme{palette,world}, episodes[] },
  - optionally writes course/quizzes.json (a quiz bank) and course/transcripts/*.md,
  - copies the interactive player (watch.html, index.html) + the local range server
    (serve.py) + one-click launchers (play.cmd / play.sh) to the project root.

Run from the project, or pass --project. Idempotent.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE))
import theme as _theme

W, H = 1280, 720
MIN_LUMA = 55


def _dur(mp4):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def _mean_luma(mp4, t):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(mp4),
                        "-frames:v", "1", "-vf", "scale=80:45,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True)
    b = p.stdout
    return (sum(b) / len(b)) if b else 0.0


def _poster(mp4, cues):
    total = _dur(mp4)
    if total <= 0:
        return None
    ts = []
    for ch in (cues.get("chapters", []) if cues else []):
        t = float(ch.get("t", 0))
        if 8 <= t <= total * 0.6 and not str(ch.get("title", "")).lower().startswith("quiz"):
            ts.append(t + 2.5)
    ts += [max(6.0, total * 0.12), total * 0.22, total * 0.33, 8.0]
    best_t, best_l = None, -1.0
    for t in ts:
        if not (0 < t < max(1, total - 2)):
            continue
        lum = _mean_luma(mp4, t)
        if lum > best_l:
            best_l, best_t = lum, t
        if lum >= MIN_LUMA:
            best_t = t
            break
    if best_t is None:
        best_t = min(8.0, total / 2)
    out = mp4.with_suffix(".jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{best_t:.2f}", "-i", str(mp4),
                    "-frames:v", "1",
                    "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                    "-q:v", "3", str(out)], check=True)
    return out


def _srt_to_vtt(srt: Path, vtt: Path):
    if not srt.exists():
        return
    lines = srt.read_text(encoding="utf-8").splitlines()
    out = ["WEBVTT", ""]
    for ln in lines:
        out.append(ln.replace(",", ".") if "-->" in ln else ln)
    vtt.write_text("\n".join(out) + "\n", encoding="utf-8")


def _spec_for(epid, project):
    for p in sorted((project / "course" / "scripts").glob("*.json")):
        try:
            s = json.loads(p.read_text(encoding="utf-8"))
            if s.get("id", "").lower() == epid.lower():
                return s
        except Exception:                                   # noqa: BLE001
            pass
    return {}


def _title_beat(spec):
    for b in spec.get("beats", []):
        if b.get("scene") == "title":
            return b
    return {}


def _num_from_id(epid):
    digits = "".join(c for c in epid if c.isdigit() or c.isalpha())
    return epid.replace("ep", "").upper() or epid


def _synopsis(spec):
    if spec.get("synopsis"):
        return spec["synopsis"]
    # first define/concept plain line, else first narrator line
    for b in spec.get("beats", []):
        if b.get("scene") in ("define", "concept", "control") and b.get("plain"):
            return b["plain"]
    for b in spec.get("beats", []):
        for sp, tx in b.get("say", []):
            return tx
    return ""


def _transcript(spec, cues):
    """A simple readable transcript (on-screen text + spoken lines)."""
    out = [f"# {spec.get('title', spec.get('tag', spec.get('id')))}", ""]
    for b in spec.get("beats", []):
        sc = b.get("scene", "")
        head = b.get("title") or b.get("term") or b.get("q") or b.get("headline") or sc
        out.append(f"## {head}  _({sc})_")
        for key in ("plain", "why", "quote", "example", "expand", "note", "body"):
            if b.get(key):
                out.append(f"- {b[key]}")
        for opt in b.get("bullets", []) or []:
            out.append(f"- {opt}")
        if sc == "quiz":
            for i, o in enumerate(b.get("options", [])):
                mark = " (correct)" if i == b.get("answer") else ""
                out.append(f"  - {chr(65 + i)}. {o}{mark}")
            if b.get("why"):
                out.append(f"  - Why: {b['why']}")
        for sp, tx in b.get("say", []):
            out.append(f"> **{sp}:** {tx}")
        out.append("")
    return "\n".join(out)


def package(project: Path, quizzes=True, transcripts=True):
    epdir = project / "course" / "episodes"
    if not epdir.exists():
        print(f"no episodes at {epdir}; render first.")
        return
    # load THIS project's theme (not the cwd's) so brand/palette in the manifest are correct
    tp = project / "theme.json"
    t = _theme.load(tp) if tp.exists() else _theme.load()
    episodes, quiz_bank = [], []
    cue_files = sorted(epdir.glob("*.cues.json"))
    for cf in cue_files:
        epid = cf.name[:-len(".cues.json")]
        cues = json.loads(cf.read_text(encoding="utf-8"))
        mp4 = next((m for m in epdir.glob(f"{epid}_*.mp4")), None) or next(
            (m for m in epdir.glob(f"{epid}.mp4")), None)
        if not mp4:
            print(f"  {epid}: no mp4, skip")
            continue
        spec = _spec_for(epid, project)
        tb = _title_beat(spec)
        poster = _poster(mp4, cues)
        srt = mp4.with_suffix(".srt")
        _srt_to_vtt(srt, mp4.with_suffix(".vtt"))
        rel = lambda p: ("course/episodes/" + p.name) if p else ""
        ep = {
            "id": epid,
            "num": str(spec.get("num") or _num_from_id(epid)),
            "title": spec.get("title") or tb.get("title") or spec.get("tag") or epid,
            "families": spec.get("families") or spec.get("subtitle") or tb.get("subtitle") or "",
            "synopsis": _synopsis(spec),
            "video": rel(mp4),
            "cues": rel(cf),
            "poster": rel(poster),
            "duration": cues.get("duration", round(_dur(mp4), 2)),
            "quizzes": len(cues.get("quizzes", [])),
        }
        episodes.append(ep)
        for q in cues.get("quizzes", []):
            quiz_bank.append({"ep": epid, "n": q.get("n"), "q": q.get("q"),
                              "options": q.get("options"), "answer": q.get("answer"),
                              "why": q.get("why", "")})
        if transcripts and spec:
            tdir = project / "course" / "transcripts"
            tdir.mkdir(parents=True, exist_ok=True)
            (tdir / f"{epid}.md").write_text(_transcript(spec, cues), encoding="utf-8")
        print(f"  {ep['num']}  {ep['title']}  ({ep['duration']}s, {ep['quizzes']} quiz)")

    # sort episodes by numeric-ish id
    episodes.sort(key=lambda e: e["id"])
    manifest = {
        "brand": _theme.brand(t),
        "theme": {"palette": t.get("palette", {}), "world": t.get("world", {})},
        "episodes": episodes,
    }
    (epdir / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    if quizzes:
        (project / "course" / "quizzes.json").write_text(
            json.dumps({"brand": _theme.brand(t), "questions": quiz_bank}, indent=1, ensure_ascii=False),
            encoding="utf-8")

    # copy the player + local server + launchers to the project root
    pdir = ENGINE.parent / "player"
    for name in ("watch.html", "index.html", "serve.py"):
        src = pdir / name
        if src.exists():
            shutil.copyfile(src, project / name)
    for name, src_name in (("play.cmd", "play.cmd"), ("play.sh", "play.sh")):
        src = pdir / src_name
        if src.exists():
            dst = project / name
            shutil.copyfile(src, dst)
            try:
                os.chmod(dst, 0o755)
            except Exception:                               # noqa: BLE001
                pass

    # link check
    missing = []
    for ep in episodes:
        for k in ("video", "cues", "poster"):
            if ep[k] and not (project / ep[k]).exists():
                missing.append(ep[k])
    print(f"\nmanifest.json: {len(episodes)} episode(s)"
          + (f", quizzes.json: {len(quiz_bank)} Q" if quizzes else ""))
    if missing:
        print("  WARNING missing assets:", missing)
    else:
        print("  link check: all local references resolve")
    print(f"\nPlay locally:  double-click play.cmd (Windows) / ./play.sh (mac/Linux) in {project}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=os.environ.get("CC_PROJECT") or str(Path.cwd()))
    ap.add_argument("--no-quizzes", action="store_true")
    ap.add_argument("--no-transcripts", action="store_true")
    args = ap.parse_args()
    package(Path(args.project), quizzes=not args.no_quizzes, transcripts=not args.no_transcripts)
