# 12 — Optional reinforcement and performance support

Create only the materials selected in `project.json`. Derive them from the learning blueprint and
truth layer, not from memory or generic summaries.

## Choose the right artifact

- **Job aid / quick reference:** concise steps, decision cues, thresholds, examples, and escalation
  points used while performing the task.
- **Study guide:** objective-organized explanations, examples/non-examples, misconceptions, and
  source citations.
- **Retrieval set:** prompts that require recall or reconstruction before showing answers.
- **Transfer set:** unfamiliar scenarios requiring application, justification, or artifact creation.
- **Quiz bank:** parallel items mapped to objective/evidence IDs, with full answer text and
  explanatory feedback.

Do not create a glossy recap that merely repeats headings. For delayed retention, schedule a small
number of effortful follow-ups at increasing intervals and mix earlier objectives into later sets.
Avoid exact repeats: preserve the principle while varying surface context.

Validate every factual statement and citation against `truth.json`. Include objective/fact IDs in
source data even if the learner-facing document hides them. Add all generated artifacts to the
package manifest and verify their links locally.
