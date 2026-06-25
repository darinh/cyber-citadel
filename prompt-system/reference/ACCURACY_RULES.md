# Accuracy Rules

Accuracy is enforced before rendering. Treat the truth layer as the source of record.

## Source of truth
- `course/data/truth.json` is the only source for on-screen factual ids, titles, and quotes.
- Do not invent ids, titles, quotes, incidents, case details, or source names.
- If a fact is not in the truth layer, add it there with its source before using it on screen.
- Cite where each fact comes from; include page or section when available.

## Quotes
- A `quote` beat must display a verbatim substring from the cited truth-layer statement.
- The `cite` must identify the source/fact clearly enough for `verify_facts` to match it.
- The spoken quote must equal the on-screen quote; do not truncate, summarize, or add lead-in text to the quote narration.
- If a quote is too long, choose a shorter verbatim substring and cite it; do not rewrite it.

## Required pre-render gates
Run these from `prompt-system/` before rendering:

```bash
python engine/gates/verify_facts.py course/scripts/ep01.json
python engine/gates/lint_prompts.py
python engine/gates/lint_script.py ep01
```

`verify_facts` checks concept/control ids and titles, quote substrings, spoken quote equality, and cited definition expansions. `lint_prompts` blocks existing-IP/style-imitation problems. `lint_script` catches script issues such as duplicate headings, overflow risks, and incomplete or mismatched quotes.

## Authoring discipline
- Separate teaching interpretation from source text: explain in `plain`/`why`, quote exactly in `quote`.
- Use neutral examples unless the truth layer supports a specific incident.
- When uncertain, omit the claim or source it first.
## What belongs in each layer
- Truth layer: stable facts, source statements, ids, titles, citations, sections, pages.
- Script layer: scene order, plain explanations, dialogue, quizzes, and selected verbatim quotes.
- Theme layer: colors, fonts, cast, vocabulary, pronunciations, and music choices.

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
