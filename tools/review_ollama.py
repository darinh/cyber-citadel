"""Local-LLM (ollama) beginner-accessibility + engagement review of the course
transcripts. Adds LLM-platform diversity to the cloud council per user's
"multiple agent llms" requirement. Writes one report per model.
"""
import sys
from pathlib import Path
from llm import ask

ROOT = Path(__file__).resolve().parent.parent
transcript = (ROOT / "course" / "transcripts" / "_ALL_EPISODES.md").read_text(encoding="utf-8")

SYSTEM = (
    "You are on a tough review council with two jobs: (1) act as an intelligent "
    "adult who knows NOTHING about NIST, cybersecurity, or federal IT and flag "
    "every term used before it is explained; (2) act as a story editor improving "
    "engagement. You are specific and high-signal; you never rubber-stamp. You "
    "know NIST SP 800-53 Rev 5 and the RMF well."
)
PROMPT = f"""Below is the full transcript of a 12-episode animated video course that
teaches NIST SP 800-53 and the Risk Management Framework through a 'Cyber Citadel'
story (an information system dramatized as a fortified city; 20 control families =
guardians; cast = VEGA the expert, NOVA the apprentice/learner, THE ARCHIVIST who
reads verbatim NIST text, THE NULL the antagonist/threats).

=== TRANSCRIPT START ===
{transcript}
=== TRANSCRIPT END ===

Answer concisely with specifics (quote the offending lines):

A) BEGINNER GAPS: List the top 12 terms or concepts used WITHOUT a plain-language
   definition a novice would need (e.g., control, baseline, framework, FISMA, PII,
   authorization, categorize, CIA triad). For each: episode, the line, and a one-
   sentence beginner definition you'd insert.
B) MISSING FOUNDATIONS: 5 things a total novice needs that are absent or rushed
   (e.g., 'what is an information system', 'who is NIST', 'what a control is with an
   everyday example', 'law vs standard vs framework', 'threat vs vulnerability vs risk').
C) PACING/CLARITY: places that move too fast or pack too much into one beat.
D) ENGAGEMENT IDEAS: 6 concrete, production-friendly ways to make it more memorable
   and improve the storytelling (motion-graphics + avatar portraits only, no full
   animation). Give sample lines.
E) ACCURACY PITFALLS: any NIST 800-53r5 statements that look wrong or risky.
Rank the 5 most important fixes overall."""

models = sys.argv[1:] or ["gemma3:27b", "gpt-oss:20b"]
for m in models:
    print(f"\n\n===== OLLAMA REVIEW: {m} =====", flush=True)
    out = ask(m, PROMPT, system=SYSTEM, temperature=0.5, num_ctx=16384)
    safe = m.replace(":", "_").replace("/", "_")
    (ROOT / "course" / "data" / f"review_{safe}.md").write_text(out, encoding="utf-8")
    print(out, flush=True)
    print(f"\n[wrote course/data/review_{safe}.md]", flush=True)
