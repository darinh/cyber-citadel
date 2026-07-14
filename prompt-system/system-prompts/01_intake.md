# 01 — Intake: learner, performance, source, and scope

Create `projects/<slug>/project.json`. Collect the minimum information needed to design instruction;
do not begin with a fictional world, cast, or slide style.

## Ask for

1. Topic and authoritative source material.
2. Audience role, relevant prior knowledge, and where they will use the learning.
3. **Desired performance:** complete “After this course, the learner can …” with an observable action.
4. Consequences of errors and common difficulties, if known.
5. Scope: one short video or a course.
6. Accessibility/language needs and delivery constraints.
7. Optional preferences: direct, demonstration, documentary, case-based, scenario-based, or story;
   tone; aesthetic; quizzes; job aid; study guide; avatars; sourced music.

If the user says “you decide,” default to direct narrator-only instruction, quizzes/practice on,
avatars off, music off, and a restrained visual system derived from the subject. Do not ask about
codecs, model sizes, geometry, or other fixed quality controls.

## Folder

```powershell
$slug = "topic-slug"
New-Item -ItemType Directory -Force "projects\$slug\course\data" | Out-Null
New-Item -ItemType Directory -Force "projects\$slug\course\design" | Out-Null
New-Item -ItemType Directory -Force "projects\$slug\assets\media" | Out-Null
$env:CC_PROJECT = "projects\$slug"
```

## `project.json`

```json
{
  "schema_version": "2.0",
  "topic": "Reading line charts",
  "sources": [
    {"type": "pdf", "name": "Data Literacy Guide", "path_or_url": "sources/guide.pdf"}
  ],
  "audience": {
    "description": "New operations analysts",
    "prior_knowledge": ["Can read basic numbers and percentages"],
    "work_context": "Reviewing weekly dashboards",
    "accessibility": ["Captions", "Do not rely on color alone"]
  },
  "desired_performance": "Classify a pattern and justify the decision using evidence from an unfamiliar chart.",
  "scope": {"kind": "single_video", "episodes": 1},
  "options": {
    "quizzes": true,
    "study_guide": false,
    "quick_reference": true,
    "avatars": false,
    "music": false,
    "narrative": false
  },
  "delivery": {
    "mode": "direct",
    "tone": "clear and conversational",
    "aesthetic": "",
    "voice_preferences": "one natural narrator"
  },
  "target_length": "5–7 minutes",
  "language": "English"
}
```

Check that desired performance describes something observable, the project has its own folder, and
story/aesthetic choices are truly optional. Continue to `02_environment.md`.
