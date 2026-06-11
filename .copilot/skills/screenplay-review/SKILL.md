---
name: screenplay-review
description: >-
  Review a narrated course's scripts/transcripts as a screenplay/stage-play editor BEFORE
  rendering audio or video, using a multi-LLM adversarial council. Catches phrasing
  distractions (word echoes), character-voice slips (a learner character lecturing), flow
  and transition breaks, redundancy, and pacing problems while they are still cheap to fix in
  text. Use when asked to review dialogue/scripts/transcripts, edit a screenplay, check that
  episodes "flow", or before any (re-)render of narrated content.
---

# Screenplay / Dialogue Review (text-first editorial gate)

Reviewing **text** is an order of magnitude cheaper than rendering audio/video and listening
for problems. This skill runs a disciplined, multi-LLM "writers' room" over the **scripts**
(`course/scripts/epNN.json`) and their generated **transcripts** (`course/transcripts/epNN.md`)
to find the kinds of issues a director/script editor would catch at a table read — *before* TTS
and video assembly.

> Canonical example this skill exists to catch (real, from EP00 Orientation):
> NOVA says *"Confidentiality, Integrity, Availability. The reason every guardian exists."* and
> on the **next** slide asks *"But why does any of this even exist?"* — two defects in two
> lines: (1) **word echo** ("exist" twice), and (2) **character slip** — NOVA is the *new
> learner*, but the first line makes her sound like she's *teaching*. Both are obvious in text,
> invisible until you listen if you skip this gate.

---

## When to use
- "Read through the transcripts and make sure they flow / sound natural."
- "Edit the dialogue like a screenplay/stage play."
- Before **any** render or re-render of narrated episodes (it is a gate, like accuracy).
- After large script edits, new episodes, or a re-cast.

## When NOT to use
- On-screen **control facts** (IDs/titles/quotes/baseline numbers) — those are owned by the
  **accuracy-verification** skill (`verify_script.py` + `audit_narration.py` vs `truth.json`).
  This skill is about *craft* (voice, flow, phrasing), not factual correctness. Flag suspected
  factual issues for that gate; don't "fix" facts here.
- Final encoded audio QA — that's `verify_episode.py` (the rendered-mp4 gate).

---

## Inputs & source of truth
- **Edit the JSON specs** (`course/scripts/epNN.json`), never the generated transcripts. The
  `say` arrays (and quiz `q`/`options`/`why`) are the spoken lines; `scene`/`bullets`/`plain`/
  `quote` etc. are on-screen text. Regenerate transcripts with `python tools/package.py`.
- Read the **character bible** (below + `course/PRODUCTION_BIBLE.md`) before judging voice.

## Cast voice rubric (the lens for "in character")
| Character | Role | Must sound… | Red flags (slips) |
|-----------|------|-------------|-------------------|
| **NOVA** | new, young apprentice / the audience surrogate | curious, informal, a little uncertain; asks naive "beginner" questions ("So who writes all this stuff?") | **lecturing/explaining**, defining terms, sounding expert, over-formal |
| **VEGA** | mentor / guide | clear, warm, authoritative but not stiff; teaches | dumbing-down to the point of error; rambling |
| **ARCHIVIST** | precise loremaster (British) | measured, precise; delivers **verbatim, cited** catalog quotes | paraphrasing a quote; chatty; emotional |
| **NULL** | the antagonist | disdainful, distrustful, menacing; never helpful or agreeable; tempts shortcuts | helping, agreeing, sounding friendly, conceding the heroes are right |
| **NARRATOR** | neutral frame | concise scene-setting | opinions, character emotion |
| **HERALD** | announcements | formal, brief | exposition dumps |

## Issue taxonomy (what to hunt for)
1. **Word echo / repetition** — the same distinctive word/root in adjacent lines or across a
   slide boundary ("exist"→"exist"; "protect"→"protection"). Most common, most distracting.
2. **Character slip** — a line that contradicts the rubric (esp. NOVA teaching, NULL helping).
3. **Flow / transition break** — a beat that doesn't follow from the previous; a question whose
   setup was removed; an abrupt topic jump with no bridge.
4. **Redundancy** — the same idea stated twice in nearby beats with no new value.
5. **Pacing** — a dense slide with too little narration (or vice-versa); reads rushed. (Dense
   slides also need on-screen time — see GENERATION_PLAYBOOK §1 and the `min_seconds` field.)
6. **Setup/payoff & callbacks** — a promised callback that never lands; a term used before it's
   introduced.
7. **Naturalness** — tongue-twisters, awkward TTS phrasing, ambiguous homographs, unpronounceable
   strings (route those to the TTS preprocessor, not a misspelling).
8. **Quiz craft** — question/answer wording clarity; the `why` actually explains; options are
   mutually exclusive and plausible.

## Severity
- **P1 blocker**: character slip that breaks the premise; factual-sounding error; broken
  setup/payoff; a line that misleads the learner.
- **P2 distraction**: word echoes, redundancy, awkward phrasing, pacing — the user *will* notice.
- **P3 polish**: minor word choice, optional tightening.

---

## Process (multi-LLM council → consensus → apply → re-verify)

**1. Prep.** Ensure transcripts are current: `python tools/package.py`. List episodes
(`course/transcripts/ep*.md`). Note any recent script changes.

**2. Dispatch the council (diverse models, in parallel).** Use the `task` tool with
`agent_type: general-purpose` and **different `model`s** for genuine diversity — e.g.
`gpt-5.5`, `gemini-3.1-pro-preview`, `claude-sonnet-4.6` — plus, optionally, a local pass via
`tools/council_ollama.py`. Give every reviewer:
   - the **full cast voice rubric** and **issue taxonomy** above (paste it; agents are stateless),
   - the exact files to read (`course/transcripts/epNN.md`, and `course/scripts/epNN.json` for
     locators),
   - the **output contract** (next section),
   - the instruction to read **whole episodes in order** (flow is cross-beat), and to read across
     episode boundaries for series-level callbacks/continuity.
   Split episodes across agents if context is tight, but each episode must be read end-to-end by
   at least **two** different models.

**3. Output contract (every finding).** Require a table/JSONL, one row per finding:
   `episode · locator (scene/term/id or a quoted snippet) · speaker · type (from taxonomy) ·
   severity (P1/P2/P3) · the offending quote · a concrete suggested rewrite · 1-line rationale`.
   Suggestions must preserve meaning and stay in character; for NOVA, rewrites should sound like
   a learner, not a teacher.

**4. Merge to consensus.** Deduplicate across reviewers; a finding corroborated by ≥2 models is
   high-confidence. For conflicts, prefer the option that best fits the rubric and prior delivered
   style. **Validate each finding against established conventions before accepting it** — a
   reviewer's stylistic "fix" can regress consistency with already-shipped episodes (e.g. don't
   "correct" an intentional running gag or a house spelling). Record the merged list (e.g. in the
   session SQL `findings` table or a checklist) with an accept/reject decision + reason.

**5. Apply** accepted edits to `course/scripts/epNN.json` (the `say`/quiz fields). Keep ARCHIVIST
   quotes verbatim. Re-run `python tools/package.py` to refresh transcripts; re-read the changed
   beats to confirm the echo/slip is gone and nothing new was introduced.

**6. Gate before render.** Edits that touch on-screen facts must pass **accuracy-verification**
   (`verify_script.py` + `audit_narration.py`). Only then render (see **video-assembly**) and
   finally confirm the delivered mp4 with `verify_episode.py`.

## Definition of done
- Every episode read end-to-end by ≥2 diverse models; findings merged to consensus.
- All P1 fixed; P2 fixed or explicitly deferred with reason; P3 optional.
- Transcripts regenerated; spot re-read clean; accuracy gate still green.
- Findings + decisions recorded so the same notes aren't rediscovered next time.

## Pitfalls (hard-won)
- **Don't apply a reviewer's fix blindly** — check it against conventions/prior episodes first.
- **Don't fix facts here** — wrong IDs/quotes/numbers go to the accuracy gate, not creative edits.
- **Read in order.** Many issues (echoes, callbacks, "Nova already knows this") only appear in
  sequence, not line-by-line.
- **Keep NOVA a learner and NULL a villain** — these are the two most common slips.
- This gate is **cheap**; skipping it and finding problems in a render is **expensive**. Always
  run it before (re-)rendering narrated content.
