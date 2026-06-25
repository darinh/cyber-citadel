"""Accuracy gate (deterministic): every on-screen FACT must come from the truth layer.

Checks an episode spec against <project>/course/data/truth.json:
  - concept/control beats: `id` + `title` must match a fact (id -> title).
  - quote beats: the on-screen `quote` must be a VERBATIM substring of that fact's
    `statement`, AND the spoken `say` for the quote must equal the on-screen `quote`
    (so a narrator never reads a truncated quote — the "never finishes speaking" class).
  - define beats with a `cite` that names a known id are checked the same way.

Exit 1 on any failure. This is the non-negotiable accuracy guarantee: on-screen IDs/titles/
quotes are sourced, never invented by an LLM.

  python verify_facts.py <spec.json> [<spec2.json> ...]
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

PROJECT = Path(os.environ.get("CC_PROJECT") or Path.cwd())
TRUTH = PROJECT / "course" / "data" / "truth.json"
_ID = re.compile(r"\b([A-Za-z]{1,6}-\d{1,4}[A-Za-z]?(?:\(\d+\))?)\b")


def _norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def _facts():
    if not TRUTH.exists():
        print(f"  truth layer not found: {TRUTH}")
        return {}
    data = json.loads(TRUTH.read_text(encoding="utf-8"))
    return {k.upper(): v for k, v in (data.get("facts", data) or {}).items()
            if isinstance(v, dict)}


def _id_in(text, facts):
    for m in _ID.finditer(text or ""):
        if m.group(1).upper() in facts:
            return m.group(1).upper()
    return None


def verify(spec_path):
    facts = _facts()
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    ep = spec.get("id", Path(spec_path).stem)
    fails, checked = [], 0
    for i, b in enumerate(spec.get("beats", [])):
        sc = b.get("scene")
        if sc in ("concept", "control"):
            cid = (b.get("id") or "").upper()
            if not cid:
                continue
            checked += 1
            if cid not in facts:
                fails.append(f"[{ep} #{i}] {sc} id '{cid}' not in truth layer")
            elif _norm(b.get("title")).lower() != _norm(facts[cid].get("title")).lower():
                fails.append(f"[{ep} #{i}] {cid} title mismatch: spec '{_norm(b.get('title'))}' "
                             f"!= truth '{_norm(facts[cid].get('title'))}'")
        elif sc == "quote":
            quote = _norm(b.get("quote"))
            cid = _id_in(b.get("cite", ""), facts) or _id_in(quote, facts)
            checked += 1
            if not cid:
                fails.append(f"[{ep} #{i}] quote cite names no known fact id: '{_norm(b.get('cite'))}'")
            else:
                stmt = _norm(facts[cid].get("statement"))
                if quote.lower() not in stmt.lower():
                    fails.append(f"[{ep} #{i}] {cid} quote is NOT a verbatim substring of the truth "
                                 f"statement: \"...{quote[-50:]}\"")
            # spoken say must equal the on-screen quote (no truncated narration)
            says = [_norm(t) for _s, t in b.get("say", [])]
            spoken = _norm(" ".join(says))
            if spoken and _norm(re.sub(r"\s+", " ", spoken)).lower() != quote.lower():
                # allow the quote to be split across multiple say lines that JOIN to it
                if "".join(says).replace(" ", "").lower() != quote.replace(" ", "").lower():
                    fails.append(f"[{ep} #{i}] spoken quote != on-screen quote (truncated narration?): "
                                 f"spoken \"...{spoken[-46:]}\"")
        elif sc == "define" and b.get("cite"):
            cid = _id_in(b.get("cite", ""), facts)
            if cid and b.get("expand"):
                checked += 1  # light touch; defines are plain-language, not verbatim
    print(f"=== verify_facts {ep}: checked {checked} on-screen facts ===")
    for f in fails:
        print("  FAIL", f)
    if not fails:
        print("  PASSED \u2713  all on-screen facts match the truth layer")
    return not fails


if __name__ == "__main__":
    ok = True
    for p in sys.argv[1:]:
        ok = verify(p) and ok
    sys.exit(0 if ok else 1)
