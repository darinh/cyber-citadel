# 09 — Gates → run before every render

Run these deterministic checks on the script BEFORE rendering. They are fast and free; rendering is slow
and expensive. Fix all blocking (P1) issues here, then render in phase 10.

Three gates run on the script text; a fourth (`verify_episode`, phase 11) runs on the final mp4.

---

## Goal
Prove the script is accurate, original-IP-clean, and craft-clean before spending render time:
`verify_facts` PASSED, `lint_prompts` PASSED, and `lint_script` showing **0 P1**.

---

## Run the gates
From this folder:

```powershell
$env:PYTHONUTF8 = "1"
python engine/gates/verify_facts.py course/scripts/ep01.json
python engine/gates/lint_prompts.py
python engine/gates/lint_script.py ep01
```

- `verify_facts.py` takes the **spec path** (one or more).
- `lint_script.py` takes the **episode id** (`ep01`); with no id it lints every `course/scripts/ep*.json`.
- `lint_prompts.py` takes no args (scans `theme.json` + all specs + any prompt files).

---

## What each gate enforces
- **verify_facts** (accuracy — non-negotiable): `concept`/`control` `id`+`title` must exist in
  `course/data/truth.json`; a `quote` must be a verbatim substring of its fact's `statement`, and the
  spoken `say` must equal the on-screen quote. Any failure is **blocking**; success prints `PASSED`.
- **lint_prompts** (original IP): blocks named franchises/characters/places/studios and
  "in the style of <artist>" / ™ / ® across theme + specs + prompt files. Any hit is **blocking**.
  Extend `engine/gates/assets/banned_terms.txt` as needed.
- **lint_script** (craft): two tiers —
  - **P1 (blocking):** duplicate section/map/title headings; text that overflows its container even at
    the auto-shrink floor (measured with the real renderer fonts); a `quote` truncated mid-clause or
    whose spoken line ≠ the on-screen quote; a quiz `say` line that itself says "pause".
  - **P2 (advisory):** distinctive word echoes in adjacent lines, tight-fit shrink, a quote missing
    terminal punctuation.

---

## P1 vs P2
- **P1 = blocking.** `lint_script` exits non-zero on any P1; `verify_facts` and `lint_prompts` exit
  non-zero on ANY finding. **Do not render** until all three report 0 P1 / PASSED.
- **P2 = advisory.** Worth fixing, but not blocking. See them all with:

```powershell
python engine/gates/lint_script.py ep01 --warn
```

---

## Fix loop
1. Run all three gates.
2. Read each FAIL / P1 and edit the source: `course/scripts/ep01.json` for craft, or `theme.json` /
   `course/data/truth.json` for IP + fact problems.
3. Re-run until `verify_facts` PASSED, `lint_prompts` PASSED, `lint_script` 0 P1.
4. Only then go to phase 10.

For a multi-episode course, run `verify_facts` on each spec and `lint_script` per id (or no-arg for all).
Pair these deterministic gates with the phase-08 multi-model council: together they cover facts, IP,
craft, and narrative.

---

## Self-review
- Did `verify_facts` print `PASSED` for every authored episode?
- Did `lint_prompts` print `PASSED` (no named IP / style imitation)?
- Did `lint_script` report `0 P1 (blocking)`?
- Did your fixes avoid introducing new on-screen facts that bypass `truth.json`?

Then route to `system-prompts/10_assemble.md`.
