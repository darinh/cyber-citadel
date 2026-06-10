"""Accuracy gate for episode scripts (deterministic, council-mandated).

Checks every on-screen control fact against the OSCAL truth layer:
  * control-card IDs exist and titles match truth.json exactly
  * Archivist quotes are VERBATIM substrings of the real control statement
  * cheat-card bullets' "ID Title" prefixes match truth.json
  * control IDs mentioned in narration actually exist
Exit code 1 on any hard error.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from episode_lib import TRUTH

ID = re.compile(r"\b([A-Z]{2})-(\d{1,2})\b")


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()


def exists(cid):
    fam = cid.split("-")[0]
    return fam in TRUTH and cid in TRUTH[fam]["controls"]


def ctitle(cid):
    return TRUTH[cid.split("-")[0]]["controls"][cid]["title"]


def cstatement(cid):
    return TRUTH[cid.split("-")[0]]["controls"][cid]["statement"]


def verify(spec_path):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    errors, warns, checked = [], [], 0
    valid_ids = {cid for fam in TRUTH.values() for cid in fam["controls"]}

    for i, beat in enumerate(spec["beats"]):
        sc = beat.get("scene")
        where = f"beat {i:02d} [{sc}]"

        if sc == "control":
            cid = beat.get("id", "")
            if not exists(cid):
                errors.append(f"{where}: control id '{cid}' not in catalog")
            else:
                if norm(beat.get("title", "")) != norm(ctitle(cid)):
                    errors.append(f"{where}: title '{beat.get('title')}' != truth '{ctitle(cid)}'")
                checked += 1

        if sc == "quote":
            m = ID.search(beat.get("cite", ""))
            if not m:
                errors.append(f"{where}: quote has no control id in cite")
            else:
                cid = m.group(0)
                if not exists(cid):
                    errors.append(f"{where}: quote cid '{cid}' not in catalog")
                else:
                    q = norm(beat.get("quote", "")).rstrip("\u2026").strip()
                    if q and q not in norm(cstatement(cid)):
                        errors.append(f"{where}: quote NOT verbatim for {cid}:\n      \"{beat.get('quote')[:120]}\"")
                    else:
                        checked += 1

        if sc == "cheatcard":
            for bullet in beat.get("bullets", []):
                bm = re.match(r"\s*([A-Z]{2}-\d{1,2})\s+(.*?)\s+[\u2014-]", bullet)
                if bm:
                    cid, btitle = bm.group(1), bm.group(2)
                    if not exists(cid):
                        errors.append(f"{where}: cheat bullet id '{cid}' not in catalog")
                    elif norm(btitle) != norm(ctitle(cid)):
                        errors.append(f"{where}: cheat '{cid}' title '{btitle}' != '{ctitle(cid)}'")
                    else:
                        checked += 1

        # narration ID sanity
        for sp, tx in beat.get("say", []):
            for m in ID.finditer(tx):
                cid = m.group(0)
                if cid not in valid_ids:
                    warns.append(f"{where}: narration mentions '{cid}' which is not a base control id")

    print(f"\n=== VERIFY {spec.get('id')} : {Path(spec_path).name} ===")
    print(f"on-screen facts checked: {checked}")
    for w in warns:
        print("  WARN:", w)
    for e in errors:
        print("  ERROR:", e)
    if errors:
        print(f"FAILED with {len(errors)} error(s).")
        return False
    print("PASSED \u2713  (all on-screen control facts match the OSCAL catalog)")
    return True


if __name__ == "__main__":
    ok = True
    for p in sys.argv[1:]:
        ok = verify(p) and ok
    sys.exit(0 if ok else 1)
