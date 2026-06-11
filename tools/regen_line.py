"""Surgically regenerate ONE narration line clip and re-mux its episode — no full re-render.

Why: TTS occasionally produces an acoustically bad take (artifact/echo/garble) that the text
gate can't catch. When a clip is flagged (by ear or by tools/_tmp audio QA), re-roll just that
clip: this busts its voice cache for a fresh take, invalidates only its beat, and reassembles
the episode (every other beat is reused from course/render/<ep>/).

Usage (run with the same engine as the render, e.g. $env:CC_TTS='chatterbox'):
  python tools/regen_line.py ep00 --list                 # list every clip + its text
  python tools/regen_line.py ep00 b010_l01_NULL          # re-roll that one clip + re-mux ep00
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_episode2 as B


def lines_for_episode(s):
    """(render_idx, line_idx, speaker, text) for every persisted clip — mirrors build_episode2."""
    out = []
    for i, beat in enumerate(s["beats"]):
        say = [(x[0], x[1]) for x in beat.get("say", [])]
        if beat.get("scene") == "quiz":
            opts = beat.get("options", []); ans = beat.get("answer", 0)
            letter = chr(65 + ans); letters = [chr(65 + j) for j in range(len(opts))]
            read_opts = "   ".join(f"{letters[j]}.  {o}." for j, o in enumerate(opts))
            why = beat.get("why", "")
            ql = list(say) + [("NARRATOR", beat.get("q", "")),
                              ("NARRATOR", f"Your options.   {read_opts}"),
                              ("NOVA", "Pause here and lock in your answer.")]
            for k, (sp, tx) in enumerate(ql):
                out.append((i * 10, k, sp, tx))
            correct = opts[ans] if ans < len(opts) else ""
            out.append((i * 10 + 1, 0, "VEGA",
                        f"The answer is {letter}.   {correct}." + (f"   {why}" if why else "")))
        else:
            for k, (sp, tx) in enumerate(say):
                out.append((i * 10, k, sp, tx))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    ep = sys.argv[1]
    spec = Path(f"course/scripts/{ep}.json")
    s = json.loads(spec.read_text(encoding="utf-8"))
    rows = lines_for_episode(s)
    if len(sys.argv) < 3 or sys.argv[2] in ("--list", "-l"):
        for idx, k, sp, tx in rows:
            print(f"b{idx:03d}_l{k:02d}_{sp:9s}  {tx[:84]}")
        return
    target_args = [a.replace(".wav", "") for a in sys.argv[2:]]
    rdir = B.RENDER_ROOT / ep
    mf = B._load_manifest(rdir)
    done = []
    for target in target_args:
        match = [(idx, k, sp, tx) for idx, k, sp, tx in rows if f"b{idx:03d}_l{k:02d}_{sp}" == target]
        if not match:
            print("clip not found:", target, "(use --list)"); continue
        idx, k, sp, tx = match[0]
        (rdir / "lines" / f"{target}.wav").unlink(missing_ok=True)
        try:                                   # bust the voice cache so we get a NEW take
            cached = B.tts.CACHE / f"{B.tts._key(sp, tx)}.wav"
            cached.unlink(missing_ok=True)
        except Exception as e:
            print("cache bust skipped:", e)
        mf["beats"].pop(str(idx), None)        # invalidate this beat
        done.append(f"{target} :: {tx}")
    if not done:
        return
    B._save_manifest(rdir, mf)
    print(f"re-rolling {len(done)} clip(s):")
    for d in done:
        print("  ", d)
    B.assemble(str(spec))
    print(f"done — {ep} re-muxed")


if __name__ == "__main__":
    main()
