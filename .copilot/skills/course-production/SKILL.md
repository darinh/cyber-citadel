---
name: course-production
description: >-
  Orchestrate end-to-end production of a binge-watchable, accurate, narrated video training
  course (the Cyber Citadel engine): from authoritative truth layer through script, text-first
  review, accuracy gates, avatars, voice, music, assembly, verification, and deploy. Use to plan
  or drive a full course/episode build, onboard to the pipeline, or reuse the engine for a new
  topic. Points to the focused sub-skills for each step.
---

# Course Production (orchestrator)

The umbrella for producing the Cyber Citadel video course (and reusing the engine on new topics).
It sequences the focused sub-skills and the authoritative docs. **Work autonomously; review plans
and artifacts with a multi-LLM council (adversarial → consensus) before scaling.**

## Authoritative docs (read first)
- `course/PRODUCTION_BIBLE.md` — creative + technical spec (concept, cast, episode map, rules).
- `course/GENERATION_PLAYBOOK.md` — hard-won learnings, exact commands, §11 production rules, §12
  incremental render, §14 changelog. **Keep current every session that changes pipeline/prompts/
  seeds/voice.**
- `course/AUTHORING_NEW_COURSE.md` — reuse the engine for a different standard/topic.
- `course/seed_registry.yaml` — machine-readable seeds/prompts/voice knobs/licenses.
- Work backlog: GitHub issues (`gh issue list`), labels skill/pipeline/content/web.

## Pipeline order (and which sub-skill owns each step)
1. **Truth layer** → `accuracy-verification` (build `truth.json` from OSCAL; it's the fact source).
2. **Script** the episodes as declarative `course/scripts/epNN.json` `beats` (scene types in
   AUTHORING_NEW_COURSE). Cast the four archetypes: expert (VEGA), learner-surrogate (NOVA),
   loremaster (ARCHIVIST), antagonist (NULL); + NARRATOR/HERALD.
3. **Text-first review** → `screenplay-review` (multi-LLM table read for voice/flow/echoes)
   BEFORE any render — cheapest place to fix wording.
4. **Accuracy gates** → `accuracy-verification` (`verify_script.py` + `audit_narration.py`). Both
   must pass.
5. **Avatars** → `base-avatar-creation` (fixed-seed base portraits) + `avatar-expression-variants`
   (IP-Adapter expression variants, same character).
6. **Voice** → `tts-narration` (Chatterbox + verify gate; persona-matched clones).
7. **Music** → `music-bed` (license-clean orchestral, ducked under narration).
8. **Quizzes & references** → `quiz-and-reference` (read-aloud quizzes; cheat sheets).
9. **Assemble + verify + deploy** → `video-assembly` (incremental render, two-pass mux, grade,
   `verify_episode.py` on the FINAL mp4, package, push, verify live).

## Non-negotiables (the rules that cost us re-renders)
- **Accuracy** from `truth.json`, never LLM memory; baselines are 800-53B.
- **Review text before rendering**; render ONE episode and spot-check before bulk re-render.
- **QA the delivered mp4**, not upstream clips; two-pass mux; no temporal grain; files < 95 MB.
- **Keep NOVA a learner and NULL a villain.** Read-aloud quizzes read the full Q + options +
  correct ANSWER TEXT + a one-line why.
- **Persist learnings**: update GENERATION_PLAYBOOK (+ seed_registry) and the relevant SKILL.md in
  the same change; close the GitHub issue.

## Council
Use the `task` tool with varied `model` (gpt-5.5, gemini-3.1-pro-preview, claude-sonnet-4.6) +
local ollama (`tools/council_ollama.py`) for diverse failure modes. Reach consensus before scaling.
Validate any reviewer "fix" against existing conventions before applying.

## Definition of done (every session)
If you changed pipeline code/prompts/seeds/voice or settled a creative decision, append a
GENERATION_PLAYBOOK changelog entry (+ seed_registry) and update the relevant skill BEFORE exiting.
Render one episode and spot-check before any bulk re-render.
