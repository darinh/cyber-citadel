"""Local-LLM hostile-auditor pass over an episode's narration + on-screen text.

Flags factual inaccuracies about NIST SP 800-53r5. Complements the deterministic
verify_script.py (which guarantees on-screen control facts) by scrutinizing the
narrative claims. Writes a report next to the spec.
"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm import ask

ROOT = Path(__file__).resolve().parent.parent


def extract(spec):
    lines = []
    for i, b in enumerate(spec["beats"]):
        onscreen = []
        for k in ("title", "subtitle", "q", "quote", "cite"):
            if b.get(k):
                onscreen.append(str(b[k]))
        for k in ("bullets", "options"):
            onscreen += [str(x) for x in b.get(k, [])]
        narr = " ".join(t for _, t in b.get("say", []))
        lines.append(f"[beat {i:02d} {b['scene']}] SCREEN: {' | '.join(onscreen)}\n   NARR: {narr}")
    return "\n".join(lines)


SYSTEM = ("You are a meticulous NIST SP 800-53 Rev 5 fact-checker. Flag ONLY real "
          "inaccuracies, misleading simplifications, or unsupported claims. Use this checklist:\n"
          "- FISMA framing (a federal law to protect information and systems): correct?\n"
          "- Rev 5 integrated security AND privacy into one catalog; PT family is new: correct?\n"
          "- 20 control families; ~1000+ controls with enhancements: correct?\n"
          "- Control BASELINES (Low/Moderate/High) live in SP 800-53B, NOT 800-53: correct?\n"
          "- RMF (SP 800-37r2) has 7 steps: Prepare, Categorize, Select, Implement, Assess, "
          "Authorize, Monitor: any step missing or out of order?\n"
          "- Control anatomy order: Identifier, Control, Discussion, RELATED controls, then "
          "ENHANCEMENTS, then References (Related BEFORE Enhancements). Flag wrong order.\n"
          "- Discussion is INFORMATIVE, not normative/prescriptive (don't call it 'how').\n"
          "- In the catalog, enhancements are OPTIONAL augmentations; required only via a "
          "baseline or tailoring. Flag 'requirements'/'mandatory' framing.\n"
          "- PM (Program Management) controls are organization-wide and NOT selected per-system "
          "from baselines.\n"
          "- Any control ID/title that looks wrong.\n"
          "If something is correct, do not nitpick style.")


def audit(spec_path, model="gpt-oss:20b"):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    body = extract(spec)
    prompt = (f"Episode {spec['id']} script (on-screen + narration). Flag every factual "
              f"problem about NIST 800-53r5. For each: quote the text, say why it's wrong, "
              f"give the correct fact. End with a VERDICT: CLEAN or NEEDS-FIXES.\n\n{body}")
    out = ask(model, prompt, system=SYSTEM, temperature=0.2, num_ctx=8192)
    rep = ROOT / "course" / "data" / f"audit_{spec['id'].lower()}_{model.replace(':','_').replace('/','_')}.md"
    rep.write_text(out, encoding="utf-8")
    print(out)
    print("\nwrote", rep)


if __name__ == "__main__":
    audit(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "gpt-oss:20b")
