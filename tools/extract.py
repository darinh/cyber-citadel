"""Extract structured content from NIST SP 800-53r5 PDF.

Outputs:
  course/data/full_text.txt        - full plain text
  course/data/families.json        - 20 control families with control IDs/titles
"""
import json
import re
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "NIST.SP.800-53r5.pdf"
DATA = ROOT / "course" / "data"
DATA.mkdir(parents=True, exist_ok=True)

FAMILIES = {
    "AC": "Access Control",
    "AT": "Awareness and Training",
    "AU": "Audit and Accountability",
    "CA": "Assessment, Authorization, and Monitoring",
    "CM": "Configuration Management",
    "CP": "Contingency Planning",
    "IA": "Identification and Authentication",
    "IR": "Incident Response",
    "MA": "Maintenance",
    "MP": "Media Protection",
    "PE": "Physical and Environmental Protection",
    "PL": "Planning",
    "PM": "Program Management",
    "PS": "Personnel Security",
    "PT": "PII Processing and Transparency",
    "RA": "Risk Assessment",
    "SA": "System and Services Acquisition",
    "SC": "System and Communications Protection",
    "SI": "System and Information Integrity",
    "SR": "Supply Chain Risk Management",
}

reader = PdfReader(str(PDF))
pages = [p.extract_text() or "" for p in reader.pages]
full = "\n".join(pages)
(DATA / "full_text.txt").write_text(full, encoding="utf-8")
print("PAGES:", len(pages), "CHARS:", len(full))

# Base controls appear as e.g. "AC-2 ACCOUNT MANAGEMENT" (title often in caps).
ctrl_re = re.compile(r"\b([A-Z]{2})-(\d{1,2})\s+([A-Z][A-Za-z0-9 ,/()\-&]{3,90})")
found = {}
for m in ctrl_re.finditer(full):
    fam, num, title = m.group(1), m.group(2), m.group(3).strip()
    if fam not in FAMILIES:
        continue
    cid = f"{fam}-{int(num)}"
    title = re.sub(r"\s+", " ", title)
    if cid not in found and len(title.split()) <= 12:
        found[cid] = title

out = {}
for fam, name in FAMILIES.items():
    ctrls = {cid: t for cid, t in found.items() if cid.split("-")[0] == fam}
    ordered = [{"id": c, "title": ctrls[c]} for c in sorted(ctrls, key=lambda c: int(c.split("-")[1]))]
    out[fam] = {"name": name, "controls": ordered}

(DATA / "families.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
for fam, d in out.items():
    print(f"{fam} {d['name']}: {len(d['controls'])} controls")
