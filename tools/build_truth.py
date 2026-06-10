"""Build the authoritative 'truth layer' from the official NIST OSCAL catalog.

Every control ID/title/statement/discussion comes verbatim (params resolved)
from NIST_SP-800-53_rev5_catalog.json so scripts + cheat sheets are accurate.

Output: course/data/truth.json
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "course" / "data"
oscal = json.loads((DATA / "oscal_catalog.json").read_text(encoding="utf-8"))
cat = oscal["catalog"]

# Curated flagship controls per family (domain pick of most teachable controls);
# titles/text are pulled authoritatively from OSCAL below.
FLAGSHIP = {
    "AC": ["AC-1", "AC-2", "AC-3", "AC-6", "AC-17"],
    "AT": ["AT-2", "AT-3", "AT-4"],
    "AU": ["AU-2", "AU-3", "AU-6", "AU-9", "AU-12"],
    "CA": ["CA-2", "CA-5", "CA-6", "CA-7"],
    "CM": ["CM-2", "CM-3", "CM-6", "CM-7", "CM-8"],
    "CP": ["CP-2", "CP-4", "CP-9", "CP-10"],
    "IA": ["IA-2", "IA-4", "IA-5", "IA-8"],
    "IR": ["IR-2", "IR-4", "IR-6", "IR-8"],
    "MA": ["MA-2", "MA-4", "MA-5"],
    "MP": ["MP-2", "MP-4", "MP-6", "MP-7"],
    "PE": ["PE-2", "PE-3", "PE-6", "PE-13"],
    "PL": ["PL-2", "PL-4", "PL-8"],
    "PM": ["PM-2", "PM-9", "PM-11", "PM-31"],
    "PS": ["PS-3", "PS-4", "PS-5", "PS-7"],
    "PT": ["PT-2", "PT-3", "PT-4", "PT-5"],
    "RA": ["RA-3", "RA-5", "RA-7", "RA-9"],
    "SA": ["SA-3", "SA-4", "SA-8", "SA-11", "SA-22"],
    "SC": ["SC-7", "SC-8", "SC-12", "SC-13", "SC-28"],
    "SI": ["SI-2", "SI-3", "SI-4", "SI-7"],
    "SR": ["SR-3", "SR-5", "SR-8", "SR-11"],
}

INSERT_RE = re.compile(r"\{\{\s*insert:\s*param,\s*([\w.\-]+)\s*\}\}")


def build_param_map(control):
    pmap = {}
    for p in control.get("params", []):
        pid = p["id"]
        if "label" in p:
            disp = p["label"]
        elif "select" in p:
            choices = p["select"].get("choice", [])
            how = p["select"].get("how-many", "")
            disp = "selection: " + "; ".join(choices) if choices else "selection"
        elif "values" in p:
            disp = ", ".join(p["values"])
        else:
            disp = "assignment"
        pmap[pid] = disp
    return pmap


def resolve(text, pmap):
    if not text:
        return ""
    def rep(m):
        return "[" + pmap.get(m.group(1), m.group(1)) + "]"
    return INSERT_RE.sub(rep, text)


def flatten_statement(control, pmap):
    out = []

    def walk(part, depth=0):
        prose = resolve(part.get("prose", ""), pmap)
        if prose:
            out.append(("  " * depth) + prose)
        for sp in part.get("parts", []) or []:
            walk(sp, depth + 1)

    for part in control.get("parts", []):
        if part.get("name") == "statement":
            walk(part)
    return "\n".join(out).strip()


def get_part_prose(control, name, pmap):
    for part in control.get("parts", []):
        if part.get("name") == name:
            return resolve(part.get("prose", ""), pmap)
    return ""


def related(control):
    rels = []
    for ln in control.get("links", []):
        if ln.get("rel") == "related":
            rels.append(ln["href"].lstrip("#").upper())
    return rels


def control_record(control):
    pmap = build_param_map(control)
    cid = control["id"].upper()
    enh = []
    for e in control.get("controls", []):
        enh.append({"id": e["id"].upper(), "title": e["title"]})
    return {
        "id": cid,
        "title": control["title"],
        "statement": flatten_statement(control, pmap),
        "discussion": get_part_prose(control, "guidance", pmap),
        "related": related(control),
        "enhancements": enh,
    }


truth = {}
for g in cat["groups"]:
    fam = g["id"].upper()
    controls = {}
    for c in g["controls"]:
        rec = control_record(c)
        controls[rec["id"]] = rec
    flags = FLAGSHIP.get(fam, [])
    missing = [f for f in flags if f not in controls]
    truth[fam] = {
        "name": g["title"],
        "control_count": len(controls),
        "flagship": flags,
        "controls": controls,
    }
    if missing:
        print(f"!! {fam} missing flagship {missing}")

(DATA / "truth.json").write_text(json.dumps(truth, indent=1, ensure_ascii=False), encoding="utf-8")
total = sum(d["control_count"] for d in truth.values())
print(f"truth.json built: {len(truth)} families, {total} base controls")
for fam, d in truth.items():
    print(f"  {fam} {d['name']}: {d['control_count']} controls | flagship {d['flagship']}")
