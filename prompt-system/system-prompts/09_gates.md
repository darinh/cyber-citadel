# 09 — Text-first quality gates

Run all gates before voice, image generation, or video assembly. P1/blocking findings stop render.

```powershell
$env:CC_PROJECT = "projects\<slug>"
$env:PYTHONUTF8 = "1"

python engine/gates/lint_instruction.py
python engine/gates/verify_facts.py course/scripts/ep01.json
python engine/gates/audit_narration.py course/scripts/ep01.json
python engine/gates/lint_prompts.py
python engine/gates/lint_script.py ep01
```

| Gate | Blocks |
|---|---|
| `lint_instruction.py` | Missing source coverage decisions; vague or unaligned objectives; recall-only higher-order evidence; missing prerequisite order, practice, feedback, transfer, representation, media, narrative rationale, or beat traceability; passive monotony and redundant channels. |
| `verify_facts.py` | Unknown fact IDs, mismatched titles/quotes, unsupported on-screen facts, and source gaps. |
| `audit_narration.py` | Unsupported paraphrases, contradictions, and overclaims in narration or learner-visible text. Uses a local Ollama model only as a hostile reviewer; `truth.json` remains authoritative. |
| `lint_prompts.py` | Third-party franchise/IP references and unsafe copied prompts across project, blueprint, media, and scripts. |
| `lint_script.py` | Craft defects: broken dialogue, repeated phrasing, pacing problems, incomplete quiz read-aloud, and persona slips where cast exists. |

Deterministic gates verify contracts, not educational impact. Also run a subject-matter review, a
multi-model instructional review, and an accessibility/provenance review. Do not waive a P1 because
a reviewer likes the script. Treat P2 warnings as review-required and document whether each is
fixed or intentionally accepted. Reject any LLM-auditor finding that conflicts with the truth layer.

Continue to `10_assemble.md` only when all blocking findings are zero.
