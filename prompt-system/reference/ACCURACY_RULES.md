# Accuracy Rules

Accuracy is enforced before rendering. Treat the truth layer as the source of record.

## Source of truth
- `course/data/truth.json` is the only source for on-screen factual ids, titles, and quotes.
- Do not invent ids, titles, quotes, incidents, case details, or source names.
- If a fact is not in the truth layer, add it there with its source before using it on screen.
- Cite where each fact comes from; include page or section when available.
- Clearly label fictional teaching datasets/scenarios as illustrative and record their exact values
  and events in the truth layer. "Fictional" does not mean "ungated."
- Media containing data or factual labels declares `fact_ids` in `assets/media.json`; consuming
  beats repeat those IDs.

## Quotes
- A `quote` beat must display a verbatim substring from the cited truth-layer statement.
- The `cite` must identify the source/fact clearly enough for `verify_facts` to match it.
- The spoken quote must equal the on-screen quote; do not truncate, summarize, or add lead-in text to the quote narration.
- If a quote is too long, choose a shorter verbatim substring and cite it; do not rewrite it.

## Required pre-render gates
Run these from `prompt-system/` before rendering:

```bash
python engine/gates/lint_instruction.py
python engine/gates/verify_facts.py course/scripts/ep01.json
python engine/gates/audit_narration.py course/scripts/ep01.json
python engine/gates/lint_prompts.py
python engine/gates/lint_script.py ep01
```

`lint_instruction` checks source-coverage decisions, media facts, and objective/beat traceability.
`verify_facts` checks each beat's `fact_ids`, structured numeric visual claims, ids and titles,
quote substrings, spoken quote equality, and cited definition expansions. `audit_narration` sends
the truth layer and learner-visible claims to a local, source-bound hostile auditor to catch
unsupported paraphrases and overclaims. Its report is written to `course/reports/`; P1 findings
block, P2 findings require documented review against `truth.json`. Never accept an auditor claim
from model memory. `lint_prompts` blocks existing-IP/style-imitation problems. `lint_script`
catches script issues such as duplicate headings, overflow risks, and incomplete or mismatched
quotes.

## Authoring discipline
- Separate teaching interpretation from source text: explain in `plain`/`why`, quote exactly in `quote`.
- Use neutral examples unless the truth layer supports a specific incident.
- When uncertain, omit the claim or source it first.
## What belongs in each layer
- Truth layer: stable facts, source statements, ids, titles, citations, sections, pages.
- Learning blueprint: objectives, evidence, practice, representations, sequence, and scope decisions.
- Script layer: scene order, explanations, narration/dialogue, practice, quizzes, and verbatim quotes.
- Media manifest: visual/source asset provenance, licenses, credits, and alt text.
- Theme layer: colors, fonts, optional cast, vocabulary, pronunciations, and music choices.

## Quiz accuracy
- The correct option must be supported by the truth layer or by already-sourced teaching in the episode.
- The `why` line should explain the fact, not merely repeat the correct option.
- Distractors may be plausible, but they must not teach false information as if it were true.
- If a question depends on a source quote, place the quote before the quiz.

## Red flags
- A fact appears only in a model response or draft notes.
- A quote has changed punctuation, wording, or order.
- A citation points to a broad document but not the matching fact/section.
- A narrator paraphrases a quote on a `quote` beat.
