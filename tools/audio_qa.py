"""Per-line audio QA: transcribe EVERY persisted line clip with faster-whisper and compare to the
intended (preprocessed) text. Flags dropped/garbled/truncated/repeated audio. Reconstructs the
exact clip list the renderer produced (including generated quiz narration). .venv_tts."""
import json, re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, "tools")
from tts import preprocess
from faster_whisper import WhisperModel

RENDER = Path("course/render")


def lines_for_episode(s):
    out = []
    for i, beat in enumerate(s["beats"]):
        say = [(x[0], x[1]) for x in beat.get("say", [])]
        if beat.get("scene") == "quiz":
            opts = beat.get("options", []); ans = beat.get("answer", 0)
            letter = chr(65 + ans); letters = [chr(65 + j) for j in range(len(opts))]
            read_opts = "   ".join(f"{letters[j]}.  {o}." for j, o in enumerate(opts))
            why = beat.get("why", "")
            qlines = list(say) + [("NARRATOR", beat.get("q", "")),
                                  ("NARRATOR", f"Your options.   {read_opts}"),
                                  ("NOVA", "Pause here and lock in your answer.")]
            for k, (sp, tx) in enumerate(qlines):
                out.append((i * 10, k, sp, tx))
            correct = opts[ans] if ans < len(opts) else ""
            reveal = f"The answer is {letter}.   {correct}." + (f"   {why}" if why else "")
            out.append((i * 10 + 1, 0, "VEGA", reveal))
        else:
            for k, (sp, tx) in enumerate(say):
                out.append((i * 10, k, sp, tx))
    return out


def words(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def recall(iw, hw):
    if not iw:
        return 1.0
    hc = Counter(hw); hit = 0
    for w in iw:
        if hc.get(w, 0) > 0:
            hit += 1; hc[w] -= 1
    return hit / len(iw)


def main(eps):
    model = WhisperModel("small", device="cuda", compute_type="float16")
    flagged = []
    total = 0
    for ep in eps:
        s = json.loads(Path(f"course/scripts/{ep}.json").read_text(encoding="utf-8"))
        ldir = RENDER / ep / "lines"
        for idx, k, sp, tx in lines_for_episode(s):
            clip = ldir / f"b{idx:03d}_l{k:02d}_{sp}.wav"
            total += 1
            if not clip.exists():
                flagged.append((ep, clip.name, "MISSING", tx, "")); continue
            segs, _ = model.transcribe(str(clip), language="en", beam_size=5)
            hyp = " ".join(seg.text for seg in segs).strip()
            hw = words(hyp)
            iw_raw, iw_pre = words(tx), words(preprocess(tx))
            r = max(recall(iw_raw, hw), recall(iw_pre, hw))
            lr = (len(hw) / max(1, len(iw_raw)))
            if r < 0.75 or lr < 0.55 or lr > 1.7:
                flagged.append((ep, clip.name, f"recall={r:.2f} lenratio={lr:.2f}", tx, hyp))
    for ep, clip, metric, tx, hyp in flagged:
        print(f"\n[{ep}] {clip}  {metric}")
        print(f"  WANT: {tx}")
        print(f"  GOT : {hyp}")
    print(f"\n=== {len(flagged)} flagged of {total} clips ===")


if __name__ == "__main__":
    main(sys.argv[1:] or ["ep00"])
