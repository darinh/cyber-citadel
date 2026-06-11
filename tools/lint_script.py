"""Deterministic CRAFT gate for episode scripts (complements verify_script.py = facts,
audit_narration.py = claims, screenplay-review skill = LLM table-read).

Fails the build on whole CLASSES of distraction the team has been burned by, so we never
ship them again:
  1. WORD ECHO   - a distinctive word repeated across adjacent spoken lines / slide
                   boundaries (e.g. EP00 "...every guardian exists." -> "why does any of
                   this even exist?").
  2. DUP HEADING - the same section/map/title heading used twice in one episode
                   (e.g. EP01 had two subsections titled "The Outer Walls").
  3. LONG TITLE  - a title/subtitle so long it overflows the slide container.
  4. QUIZ PAUSE  - a quiz scenario line that itself says "pause", which duplicates the
                   pause prompt the assembler always appends ("...twice per question").

Usage:  python tools/lint_script.py            # all episodes (exit 1 on any P1)
        python tools/lint_script.py ep01        # one episode
        python tools/lint_script.py --warn       # also print P2 warnings (long titles)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "course" / "scripts"

# Common domain words that legitimately recur across adjacent lines (not echoes).
ALLOW = set("""about above after again against because before being below between control
controls system systems security risk data guardian guardians citadel every never always
nist baseline baselines family families access privacy network would could should there
their they're these those which while where what when your you're their here this that
with from into over under more most less only just like make makes made need needs first
then they them have has had will shall must can could three triad means meaning matters
matter work works working into out outer inner""".split())

# Heading scene types whose titles must be unique + fit the container.
HEAD_SCENES = {"section", "title", "map"}

# Measurement-based overflow check: import the REAL renderer (scene.py) and its fonts, then
# verify every content-driven text field actually fits its container at the auto-fit floor.
# (char-length heuristics lie; this measures pixels with the same fonts the renderer uses.)
try:
    import scene as _S
    from PIL import Image as _Img, ImageDraw as _ImgDraw
    _W = _S.W
    _D = _ImgDraw.Draw(_Img.new("RGB", (_S.W, _S.H)))
    _SITES = {  # (scene, field): (fontfn, base_size, max_w)  — must mirror scene.py draw sites
        ("title", "title"): (_S.FB, 120, _W - 320), ("title", "subtitle"): (_S.FSL, 46, _W - 280),
        ("section", "title"): (_S.FB, 96, _W - 320), ("section", "subtitle"): (_S.FSL, 40, _W - 260),
        ("map", "title"): (_S.FB, 54, _W - 200),
        ("control", "title"): (_S.FB, 56, _W - 644 - 150),
        ("diagram", "title"): (_S.FB, 58, _W - 300),
        ("points", "title"): (_S.FB, 62, _W - 210 - 180),
        ("cheatcard", "title"): (_S.FB, 60, _W - 210 - 320), ("cheatcard", "mnemonic"): (_S.FSB, 40, _W - 180 - 420),
        ("notebook", "title"): (_S.FB, 50, _W - 282 - 280), ("notebook", "mnemonic"): (_S.FSB, 34, _W - 280 - 566),
        ("guardian", "family_name"): (_S.FB, 64, 1020), ("guardian", "persona"): (_S.FSL, 44, 1020),
        ("define", "term"): (_S.FB, 74, _W - 440), ("define", "cite"): (_S.MONO, 26, _W - 420),
        ("quote", "cite"): (_S.MONO, 32, _W - 560),
        ("coldopen", "mitre"): (_S.MONO, 34, 560), ("coldopen", "teaches"): (_S.FSB, 34, 760),
        ("quiz", "options"): (_S.FSB, 40, 980),
    }
    _HAVE_SCENE = True
except Exception:
    _HAVE_SCENE = False


def stem(w):
    for suf in ("ing", "edly", "ed", "es", "s"):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def content_words(text, minlen=5):
    out = []
    for w in re.findall(r"[A-Za-z']+", text.lower()):
        if len(w) < minlen or w in ALLOW:
            continue
        out.append(stem(w))
    return out


def spoken_lines(beat):
    """Spoken lines a viewer HEARS for a beat, in order (incl. quiz question/why)."""
    lines = [(s[0], s[1]) for s in beat.get("say", [])]
    if beat.get("scene") == "quiz":
        if beat.get("q"):
            lines.append(("NARRATOR", beat["q"]))
        if beat.get("why"):
            lines.append(("VEGA", beat["why"]))
    return lines


def lint(ep):
    spec = json.loads((SCRIPTS / f"{ep}.json").read_text(encoding="utf-8"))
    beats = spec["beats"]
    ep_title = (spec.get("tag") or spec.get("title") or "").strip()
    p1, p2 = [], []

    # ---- episode-wide word frequency over ALL spoken + on-screen text ----
    # (used to keep WORD_ECHO high-signal: only DISTINCTIVE words that occur a couple
    #  of times and are NOT the on-screen subject being taught are real echoes.)
    onscreen = []
    for b in beats:
        for f in ("title", "subtitle", "plain", "term", "why", "mnemonic", "example", "kicker"):
            if b.get(f):
                onscreen.append(str(b[f]))
        for f in ("bullets", "lines"):
            for it in b.get(f, []):
                onscreen.append(str(it))
        for o in b.get("options", []):
            onscreen.append(str(o))
    onscreen_words = set()
    for t in onscreen:
        onscreen_words.update(content_words(t, minlen=5))
    freq = {}
    seq = []
    for i, b in enumerate(beats):
        for sp, tx in spoken_lines(b):
            seq.append((i, b.get("scene"), sp, tx))
            for w in content_words(tx, minlen=5):
                freq[w] = freq.get(w, 0) + 1

    # ---- WORD ECHO (conservative / advisory): same DISTINCTIVE word in two adjacent
    #      dialogue lines. Skip quiz Q/why and ARCHIVIST verbatim; skip topic words
    #      (occur >2x in the episode or appear in on-screen text). Catches the "exist"
    #      class without flagging legitimate teaching repetition. ----
    for (i0, s0, sp0, t0), (i1, s1, sp1, t1) in zip(seq, seq[1:]):
        if sp0 == "ARCHIVIST" or sp1 == "ARCHIVIST":
            continue
        if s0 == "quiz" or s1 == "quiz":
            continue
        a, bset = content_words(t0), set(content_words(t1))
        for w in dict.fromkeys(a):
            if w in bset and freq.get(w, 0) <= 2 and w not in onscreen_words:
                p2.append((ep, "WORD_ECHO", f'distinctive "{w}" in adjacent lines: '
                           f'[{sp0}] "...{t0[-34:].strip()}" -> [{sp1}] "{t1[:34].strip()}..."'))

    # ---- duplicate headings within the episode (BLOCKING) ----
    seen = {}
    for b in beats:
        if b.get("scene") in HEAD_SCENES:
            t = (b.get("title") or "").strip()
            if not t:
                continue
            key = t.lower()
            if key in seen:
                p1.append((ep, "DUP_HEADING", f'heading "{t}" used 2x+ in episode '
                           f'(differentiate the section vs the map/title)'))
            seen[key] = seen.get(key, 0) + 1

    # ---- overflow check: measure ACTUAL fit at the auto-shrink floor (deterministic) ----
    if _HAVE_SCENE:
        for b in beats:
            sc = b.get("scene")
            checks = [(f, b.get(f)) for f in ("title", "subtitle", "family_name", "persona",
                                              "term", "mnemonic", "cite", "mitre", "teaches")]
            if sc == "quiz":
                checks += [("options", o) for o in b.get("options", [])]
            for fname, val in checks:
                site = _SITES.get((sc, fname))
                if not site or not val:
                    continue
                fontfn, size, maxw = site
                f = _S.fit_font(_D, val, fontfn, size, maxw, min_size=18)
                if _D.textlength(val, font=f) > maxw + 1:          # cannot fit even shrunk
                    p1.append((ep, "OVERFLOW", f'{sc}.{fname} does NOT fit ({int(_D.textlength(val, font=f))}'
                               f'>{maxw}px at floor): "{val}"'))
                elif f.size <= size * 0.6:                          # had to shrink a lot
                    p2.append((ep, "TIGHT_FIT", f'{sc}.{fname} shrunk {size}->{f.size}px to fit: "{val}"'))

    # ---- duplicate quiz pause prompt (BLOCKING: assembler always appends one) ----
    for b in beats:
        if b.get("scene") == "quiz":
            for sp, tx in [(s[0], s[1]) for s in b.get("say", [])]:
                if re.search(r"\bpause\b", tx, re.I):
                    p1.append((ep, "QUIZ_PAUSE", f'quiz scenario line says "pause" (assembler '
                               f'already appends the pause prompt -> heard twice): [{sp}] "{tx}"'))
    # ---- incomplete / mismatched Archivist quote ----
    #   (a) the on-screen `quote` is truncated mid-list (ends ':' or dangling conjunction);
    #   (b) the SPOKEN `say` must read the SAME complete quote. This is the class behind the
    #       EP04 "the archivist never finishes speaking" report: the *displayed* quote was
    #       completed earlier but the *spoken* line was left truncated at the colon. Convention
    #       (holds for every good quote scene): a quote scene's ARCHIVIST line == its `quote`.
    def _normq(s):
        return re.sub(r"\s+", " ", (s or "")).strip()

    def _wordsq(s):
        return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())).strip()

    _MIDCLAUSE = re.compile(r"[ ,]\b(by|and|or|the|following|to|that|manage)\b$", re.I)
    for b in beats:
        if b.get("scene") != "quote":
            continue
        raw = _normq(b.get("quote"))
        q = raw.rstrip('\u201d"\u201c').strip()
        if q.endswith(":") or _MIDCLAUSE.search(q):
            p1.append((ep, "QUOTE_INCOMPLETE", f'on-screen quote ends mid-clause: "...{q[-46:]}"'))
        elif q and q[-1] not in ".;?!":
            p2.append((ep, "QUOTE_OPEN", f'on-screen quote lacks terminal punctuation: "...{q[-46:]}"'))
        # the Archivist must SPEAK the full quote (not stop at the lead-in / colon)
        spoken = _normq(" ".join(t for s, t in [(x[0], x[1]) for x in b.get("say", [])] if s == "ARCHIVIST"))
        if spoken:
            sp = spoken.rstrip('\u201d"\u201c').strip()
            if sp.endswith(":") or _MIDCLAUSE.search(sp):
                p1.append((ep, "QUOTE_SPOKEN_INCOMPLETE",
                           f'Archivist SPEAKS a truncated quote: "...{sp[-46:]}"'))
            elif _wordsq(spoken) != _wordsq(raw):
                p1.append((ep, "QUOTE_SAY_MISMATCH",
                           f'Archivist spoken line != on-screen quote '
                           f'(speaks {len(_wordsq(spoken).split())}/{len(_wordsq(raw).split())} words): '
                           f'spoken "...{sp[-40:]}"'))

    return p1, p2


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    warn = "--warn" in sys.argv
    eps = args or [p.stem for p in sorted(SCRIPTS.glob("ep*.json"))]
    all_p1, all_p2 = [], []
    for ep in eps:
        p1, p2 = lint(ep)
        all_p1 += p1
        all_p2 += p2
    for ep, kind, msg in all_p1:
        print(f"  P1 {ep} {kind}: {msg}")
    if warn or not all_p1:
        for ep, kind, msg in all_p2:
            print(f"  P2 {ep} {kind}: {msg}")
    print(f"\n=== {len(all_p1)} P1 (blocking), {len(all_p2)} P2 (warning) "
          f"across {len(eps)} episode(s) ===")
    if all_p1:
        sys.exit(1)


if __name__ == "__main__":
    main()
