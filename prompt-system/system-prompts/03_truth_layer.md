# 03 — Truth layer → `course/data/truth.json`

Build the authoritative fact layer from the user’s source material. Every on-screen fact, title, ID, and quote later comes from this file — not from LLM memory.

---

## Goal
Write `course/data/truth.json` with short IDs, exact titles, one verbatim quotable statement per fact, and a source section/page.

Create only the truth artifact for this phase. Do not script episodes yet.

---

## Schema
Use exactly this shape:

```json
{
  "source": "<name>",
  "facts": {
    "<ID>": {
      "title": "<exact or concise source-backed title>",
      "statement": "<verbatim quotable sentence>",
      "section": "<page/section>"
    }
  }
}
```

IDs can be any short stable code: `KN-1`, `STEP-3`, `RULE-2`, `MOD-4`, etc.

The working example is `examples/kitchen-academy/course/data/truth.json`:

```json
{
  "source": "Kitchen Academy Handbook",
  "facts": {
    "KN-1": {
      "title": "Pinch Grip",
      "statement": "Pinch the blade just ahead of the handle between thumb and forefinger so the knife becomes an extension of your hand.",
      "section": "2.1"
    }
  }
}
```

---

## Step 1 — ingest source material
Use the source entries from `project.json`.

- PDFs/docs: read the supplied files directly.
- URLs: read only user-approved source URLs.
- Notes: treat the notes as source, but quote only text actually present.
- Expert-only source: interview the user for exact wording and mark the source as expert notes.

If no source exists, interview the expert-user before writing `truth.json`. Do not invent facts to fill gaps.

---

## Step 2 — extract key facts
For each key concept, capture:

1. A stable ID.
2. A title.
3. Exactly one quotable statement.
4. A page, section, heading, URL anchor, or note label.

Prefer facts that will appear on-screen as concept cards or Archivist quote cards. Keep statements short enough to read aloud and display cleanly.

---

## Verbatim statement rules
- `statement` must be real source text, copied exactly enough to be a substring check target.
- Do not paraphrase inside `statement`.
- Do not combine two source sentences into one invented sentence.
- Do not “clean up” terminology unless the source itself says it that way.
- If the source has no quotable sentence, ask the expert-user for exact wording and document the note section.

Narration can explain later, but the truth layer is the quoteable source of record.

---

## Step 3 — write and validate JSON
Create the directory and write the file:

```powershell
New-Item -ItemType Directory -Force course\data | Out-Null
```

Then write `course\data\truth.json` as UTF-8 JSON.

Quick parse check:

```powershell
python -m json.tool course\data\truth.json > $null
```

macOS/Linux:

```bash
mkdir -p course/data
python -m json.tool course/data/truth.json >/dev/null
```

---

## Self-review before routing
- Is every `statement` verbatim from a real source or explicit expert note?
- Does each fact include `title`, `statement`, and `section`?
- Are IDs stable and short?
- Are there enough facts for the requested video/course scope?
- Did you avoid using LLM memory as a source?

Then route to `system-prompts/04_world_and_cast.md`.
