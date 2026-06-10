"""Local-LLM council critique of the concept/plan (LLM-platform diversity)."""
from pathlib import Path
from llm import ask

ROOT = Path(__file__).resolve().parent.parent
concept = (ROOT / "course" / "data" / "CONCEPT.md").read_text(encoding="utf-8")

SYSTEM = (
    "You are a demanding instructional-design + cybersecurity SME on a review "
    "council. You give critical, specific, high-signal feedback. You never "
    "rubber-stamp. You know NIST SP 800-53 Rev 5 well."
)
PROMPT = f"""Review this PLAN for a video training series. Be critical and specific.

{concept}

Answer concisely:
1) VERDICT: APPROVE / APPROVE-WITH-CHANGES / REJECT
2) Top 3-5 highest-signal, specific improvements (no vague praise).
3) The single biggest risk + mitigation.
4) Direct answers to the 5 open questions.
5) Any NIST 800-53r5 ACCURACY pitfalls to avoid (common mistakes people make)."""

models = ["gpt-oss:20b", "gemma3:27b"]
for m in models:
    print(f"\n\n===== OLLAMA COUNCIL: {m} =====")
    out = ask(m, PROMPT, system=SYSTEM, temperature=0.6, num_ctx=8192)
    safe = m.replace(":", "_").replace("/", "_")
    (ROOT / "course" / "data" / f"council_{safe}.md").write_text(out, encoding="utf-8")
    print(out)
