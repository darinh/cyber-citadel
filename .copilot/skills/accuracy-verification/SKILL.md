---
name: accuracy-verification
description: >-
  Guarantee factual accuracy of a controls/standards course by sourcing every on-screen fact from
  an authoritative truth layer and running two gates before render: a deterministic on-screen
  fact check and a local-LLM hostile narration auditor. Use when adding/editing control facts,
  quotes, IDs, titles, or baseline numbers, when authoring a new topic's truth layer, or before
  any render. Accuracy is non-negotiable.
---

# Accuracy Verification (truth layer + two gates)

**Accuracy is non-negotiable.** All control IDs/titles/text come from the authoritative truth
layer built from the official OSCAL catalog — NOT from LLM memory or loose PDF text. Read
`course/GENERATION_PLAYBOOK.md` Golden Rule #1.

## Truth layer (source of all facts)
- `python tools\build_truth.py` parses the official NIST OSCAL catalog
  (`course/data/oscal_catalog.json`) → **`course/data/truth.json`** with the stable contract
  `TRUTH[family].controls[ID] = {title, statement, discussion, related, enhancements}`.
- Verbatim authoritative text lives here; Archivist quotes must be exact substrings of the real
  control `statement`, shown with an on-screen citation.
- **Baselines live in SP 800-53B**, not 800-53. The course uses 800-53B totals Low 149 /
  Moderate 287 / High 370 / Privacy 96 (controls AND enhancements).

## The two gates (run BOTH on every script before render)
1. **Deterministic on-screen gate** — `python tools\verify_script.py course\scripts\epNN.json`.
   Checks: control-card IDs exist and titles match `truth.json` exactly; Archivist quotes are
   VERBATIM substrings of the real statement; cheat-card "ID Title" prefixes match; control IDs
   mentioned in narration exist. **Exit code 1 on any hard error** — must pass.
2. **Local-LLM hostile auditor** — `python tools\audit_narration.py course\scripts\epNN.json`.
   A hostile fact-checker over narration + on-screen text for NIST claims the deterministic gate
   can't see (paraphrased reasoning, "every system must…", counts). Writes a report next to the
   spec; review and fix real issues.

## Why both
The deterministic gate guarantees the *facts you can pin to the catalog*; the auditor scrutinizes
the *narrative claims around them*. Local LLMs hallucinate — the council previously "found"
controls (RA-2, SA-22) that were **rejected against truth.json**. That rejection is the system
working: truth.json is ground truth, the LLM is not.

## Separation of concerns
- This skill = **facts**. Craft/voice/flow = **screenplay-review** skill. Final encoded audio =
  `verify_episode.py` (tts-narration). Don't fix facts in the creative pass or vice-versa.

## New topic / re-point to another standard
Keep the `truth.json` shape; re-point `build_truth.py` at the new authoritative source so
`verify_script.py` / `audit_narration.py` keep working unchanged. You always need: a stable unit
**ID**, an exact **title**, and a **verbatim authoritative text** to quote. See
`course/AUTHORING_NEW_COURSE.md`.

## Definition of done
- `truth.json` rebuilt if the catalog/source changed.
- `verify_script.py` exits 0 for every changed spec; `audit_narration.py` report reviewed and
  real issues fixed. Only then hand off to video-assembly.
