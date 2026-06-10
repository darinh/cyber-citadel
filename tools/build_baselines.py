"""Parse the official 800-53B OSCAL baseline profiles into baselines.json.

Outputs accurate membership + counts (base controls vs enhancements) for the
Low / Moderate / High / Privacy baselines so the 800-53B episode is correct.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "course" / "data"
FILES = {
    "LOW": "NIST_SP-800-53_rev5_LOW-baseline_profile.json",
    "MODERATE": "NIST_SP-800-53_rev5_MODERATE-baseline_profile.json",
    "HIGH": "NIST_SP-800-53_rev5_HIGH-baseline_profile.json",
    "PRIVACY": "NIST_SP-800-53_rev5_PRIVACY-baseline_profile.json",
}


def ids_of(profile_file):
    p = json.loads((D / profile_file).read_text(encoding="utf-8"))["profile"]
    ids = []
    for imp in p.get("imports", []):
        for g in imp.get("include-controls", []):
            ids += g.get("with-ids", [])
    return [i.upper() for i in ids]


def is_enh(cid):
    return ("." in cid) or ("(" in cid)


out = {}
for name, f in FILES.items():
    ids = ids_of(f)
    base = sorted({i for i in ids if not is_enh(i)},
                  key=lambda c: (c.split("-")[0], int(c.split("-")[1].split(".")[0])))
    enh = [i for i in ids if is_enh(i)]
    fam = {}
    for b in base:
        fam.setdefault(b.split("-")[0], []).append(b)
    out[name] = {"total": len(ids), "base_controls": len(base), "enhancements": len(enh),
                 "families": len(fam), "base_ids": base}

(D / "baselines.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
for name, d in out.items():
    print(f"{name:9s} total={d['total']:4d}  base={d['base_controls']:3d}  enh={d['enhancements']:4d}  families={d['families']}")
