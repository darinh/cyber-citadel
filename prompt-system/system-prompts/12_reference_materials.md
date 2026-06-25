# 12 — Reference Materials → OPTIONAL quizzes / study guide / quick reference

Optional, opt-in extras — build these only if the user asked. The signature interactive quiz already
ships in-video and is aggregated to a quiz bank automatically; everything here is lightweight extra.

---

## Goal
Offer optional, license-clean study aids derived from the truth layer + transcripts: a study guide and a
quick-reference / cheat-sheet. Keep them thin and accurate.

---

## What you already have for free
- **Interactive quizzes** ship in every episode (phases 08 + 10), and `engine/package.py` already
  aggregates them into `course/quizzes.json` — a `{ brand, questions[] }` bank — during phase 11.
- **Transcripts** are written by `package.py` to `course/transcripts/epNN.md` (on-screen text + spoken
  lines). Use these + `course/data/truth.json` as the source for any extra material — never invent facts.

---

## Optional study guide (only if requested)
Summarize each episode from its transcript + the truth layer: the 2–3 concepts (plain + why), the
verbatim quote with its citation, and the recap mnemonic. One short section per episode. The phase-03/09
sourcing rules still apply — every id / title / quote must trace to `truth.json`. Write plain Markdown,
e.g. `course/study_guide.md`.

---

## Optional quick-reference / cheat-sheet (only if requested)
A one-page table or card per group/topic: `id → title → one-line plain meaning`, plus the episode's
mnemonic. Mirror the on-screen `cheatcard` content so the page and the video agree. Write plain Markdown,
e.g. `course/quick_reference.md`.

---

## Read-aloud quiz contract (reminder)
Whether a quiz is in-video or written into a study aid, it follows the same contract
(`reference/PRODUCTION_RULES.md` → "Quiz contract"):

> Read the full **question** + **every option** ("A… B… C…") + the correct **ANSWER TEXT** (never just
> the letter) + a **one-line why**. Options must be plausible, mutually exclusive, and unambiguous.

The engine already does this for in-video quizzes — match it in any written quiz so they stay consistent.

---

## Keep it lightweight
- Plain Markdown under `course/`. No new engine code, no heavy formatting.
- Don't duplicate the whole transcript — link to it.
- If the user didn't ask for these, skip the phase entirely.

---

## Definition of Done
You are finished when `reference/DEFINITION_OF_DONE.md` is satisfied:

- `verify_facts` + `lint_prompts` + `lint_script` pass (0 blocking);
- ONE episode was rendered first and spot-checked before any bulk render;
- every final mp4 reads `verify_episode OK`;
- `package.py` link-check is clean and the player files are at the project root;
- music is sourced and every CC-BY track is attributed in `THIRD_PARTY_NOTICES.md`;
- there are **zero references to any existing franchise**;
- the user can double-click `play.cmd` (or run `python serve.py`) and watch with the interactive quiz
  working.

Keep `plan.md` and `THIRD_PARTY_NOTICES.md` current. To add more episodes, loop back to
`system-prompts/08_script.md`; to re-render, return to `system-prompts/10_assemble.md`.
