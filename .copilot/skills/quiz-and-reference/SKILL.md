---
name: quiz-and-reference
description: >-
  Author retention-first quizzes and reference materials (cheat sheets, roll-call, quiz bank) for
  a narrated course. Encodes the read-aloud quiz contract (read the full question + all options +
  the correct ANSWER TEXT + a one-line why — never just the letter) and how quizzes/references are
  rendered and packaged. Use when adding quizzes, cheat sheets, or reference guides.
---

# Quiz & Reference Generation (retention-first)

Quizzes and references turn watching into learning. Read `course/GENERATION_PLAYBOOK.md` §3 and
the quiz logic in `tools/build_episode2.py`.

## Read-aloud quiz contract (the rule that was wrong before)
A narrated quiz MUST, on screen and in audio:
1. Read the **full question** aloud, then **all options** aloud ("A. … B. … C. …"), then a
   think-time countdown (pause to lock in an answer).
2. On reveal, read the **correct ANSWER TEXT** plus a **one-line "why"** — **never just the
   letter** ("The answer is B. In SP 800-53B. Baselines moved to the companion doc in Rev 5.").
This is enforced by `build_episode2.py` (it appends the question + `Your options. …` + a NOVA
"pause" line, then a reveal line `The answer is {letter}. {correct text}. {why}`).

## Quiz spec fields (in `course/scripts/epNN.json`, `scene: "quiz"`)
`q` (question), `options` (array), `answer` (0-based index), `why` (one-line rationale),
`min_seconds` (think time). Authoring rules:
- Options mutually exclusive and plausible; one unambiguous correct answer.
- `why` must actually explain (teach), not restate the option.
- Keep questions in-world but testing the real concept; NOVA/VEGA framing stays in character.

## References
- **Cheat sheets**: one page per control family in `course/cheatsheets/*.png` (+ the master map
  `00_MASTER_the_twenty_guardians.png`), surfaced on `index.html`.
- **Quiz bank + roll call**: `python tools\package.py` extracts all quizzes to
  `course/quizzes.json` and builds the interactive **Guardian Roll Call** in `index.html`; the
  per-episode quiz cues drive the in-video pauses in `watch.html`.
- Every episode should map the Citadel metaphor back to real-world meaning (RMF tie-in) and end
  Act I/the series with a cumulative quiz.

## Gates
- Quiz `q`/`options`/`why` text is dialogue → run **screenplay-review** (clarity) and
  **accuracy-verification** (the correct answer must be factually right vs `truth.json`).
- After render, `verify_episode.py` confirms the quiz lines (incl. options + answer text) are
  actually spoken in the final mp4.

## Definition of done
- Each quiz reads Q + all options + correct answer TEXT + why; options clean; answer factually
  verified; cheat sheets present; `package.py` regenerated (quiz bank + roll call); link check clean.
