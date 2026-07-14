# Build local video instruction for any subject

This folder is a reusable engine and prompt system for GitHub Copilot CLI. It turns authoritative
source material into accurate, accessible video instruction with meaningful visuals, active
practice, explanatory feedback, captions, and an optional interactive quiz player.

The system is **not a story generator or a slide theme**. It begins with what learners must be able
to do, what evidence would demonstrate that performance, what prerequisite knowledge they need, and
how they will practice and transfer it. It then chooses the best treatment for each task: direct
explanation, image, annotated screenshot, source video demonstration, comparison, timeline,
animated process, chart, diagram, worked example, or practice. Story and characters remain available
but are opt-in and must have an instructional purpose.

## Quick start

1. Open this folder in GitHub Copilot CLI; `AGENTS.md` loads automatically.
2. Describe the topic and source, for example:
   > Create one video that teaches new analysts to distinguish a trend from an anomaly using
   > unfamiliar charts. Use direct narration and interactive practice.
3. The agent builds a dedicated `projects/<slug>/` folder and follows the numbered prompts.
4. When complete, run `play.cmd` or `./play.sh` to watch locally.

The agent may ask about audience, prior knowledge, use context, desired performance, scope, and
accessibility. Aesthetic, world, cast, avatars, and music are optional—not prerequisites.

## What the pipeline enforces

- **Backward alignment:** observable objectives -> evidence -> practice/feedback -> instruction.
- **Comprehensive sourcing:** every truth-layer fact is covered or deliberately excluded with a reason.
- **Learning for use:** modeling, scaffolded practice, retrieval, cumulative review, and novel transfer.
- **Multimedia discipline:** signaling and complementary visuals; no decorative churn or narrated text walls.
- **Varied visual grammar:** real images/clips, callouts, comparisons, timelines, processes, charts,
  worked examples, and practice—not one repeated slide.
- **Accuracy and provenance:** source-backed claims plus licensed, accessible media manifests.
- **Production quality:** neural narration, captions, two-pass audio/video mux, final-artifact QA, and
  the existing pixel-aligned interactive answer hotspots.

## Requirements

Python 3.10+ and ffmpeg/ffprobe are required. A GPU is optional. The same high-quality Chatterbox,
SDXL, and large-v3 paths run on CPU more slowly; the engine never silently downgrades quality.

## Layout

| Path | Purpose |
|---|---|
| `AGENTS.md` | Objective-first orchestration and non-negotiable rules. |
| `system-prompts/` | Numbered production phases. |
| `engine/` | Renderers, assembler, voice, media registry, and gates. |
| `reference/` | Pedagogy, visual-language, scene, accuracy, and production contracts. |
| `schemas/` | Project, truth, learning blueprint, media, theme, and episode schemas. |
| `examples/data-literacy/` | Primary direct, non-story worked example. |
| `examples/kitchen-academy/` | Legacy v1 narrative example retained for compatibility. |

See `reference/PEDAGOGY_RULES.md` for the research basis and `AGENTS.md` for the full workflow.
