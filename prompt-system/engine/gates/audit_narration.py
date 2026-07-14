"""Source-bound local-LLM audit of narration and learner-visible claims.

This hostile review complements verify_facts.py: deterministic checks prove exact IDs, quotes,
and structured values, while this gate looks for unsupported paraphrases, overclaims, and
contradictions. The model is a reviewer, never a source of truth.

Usage:
  python engine/gates/audit_narration.py course/scripts/ep01.json
  python engine/gates/audit_narration.py course/scripts/ep01.json --model gpt-oss:20b
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(os.environ.get("CC_PROJECT") or Path.cwd())
TRUTH = PROJECT / "course" / "data" / "truth.json"
REPORTS = PROJECT / "course" / "reports"
DEFAULT_MODEL = os.environ.get("CC_AUDIT_MODEL", "gpt-oss:20b")
OLLAMA_URL = os.environ.get("CC_OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
AUDIT_NUM_CTX = int(os.environ.get("CC_AUDIT_NUM_CTX", "16384"))
AUDIT_NUM_PREDICT = int(os.environ.get("CC_AUDIT_NUM_PREDICT", "4096"))
AUDIT_ATTEMPTS = int(os.environ.get("CC_AUDIT_ATTEMPTS", "2"))

_DROP_FIELDS = {
    "_integrity", "_t", "deps", "end", "evidence_id", "fit", "focus", "min_seconds",
    "narrative", "narrative_function", "objective_ids", "order", "practice_id", "purpose",
    "reveal", "start", "think_seconds", "visual_purpose",
}
_REQUIRED_FINDING_FIELDS = {"severity", "beat", "claim", "problem", "correction"}

SYSTEM_PROMPT = """You are a hostile, source-bound factual auditor for an instructional video.
The supplied truth layer is the ONLY authority. Do not use your memory as evidence and do not
invent missing support. Find learner-visible or spoken claims that contradict the truth layer,
overstate what it supports, erase an important qualification, or assert an unsupported fact.

Do not review style, pedagogy, spelling, pacing, or visual taste. Do not flag questions,
instructions, transitions, clearly labeled hypotheses, or fictional examples whose exact details
are supported by the truth layer. Incorrect quiz options are candidate answers, not asserted facts:
evaluate the declared correct answer and explanation, and flag a distractor only if the episode
presents it as correct. A claim can be a faithful plain-language paraphrase without being verbatim.
Treat a fact ID as a pointer, not proof: compare the actual claim with the fact.

Return JSON only:
{
  "verdict": "CLEAN" | "NEEDS_REVIEW",
  "findings": [
    {
      "severity": "P1" | "P2",
      "beat": 0,
      "scene": "scene type",
      "claim": "exact problematic text",
      "fact_ids": ["F-1"],
      "problem": "specific source-bound reason",
      "correction": "replacement supported by the truth layer"
    }
  ]
}

P1 means a clear contradiction, fabricated fact, or materially misleading overclaim. P2 means a
real ambiguity or omitted qualification that a human must review. Return CLEAN with an empty list
when no factual defect exists. Never create a finding merely to appear thorough."""


class AuditError(RuntimeError):
    pass


def _resolve(path_value):
    path = Path(path_value)
    if path.is_absolute():
        return path
    candidate = PROJECT / path
    return candidate if candidate.exists() else path


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _truth_payload():
    if not TRUTH.exists():
        raise AuditError(f"truth layer not found: {TRUTH}")
    payload = json.loads(TRUTH.read_text(encoding="utf-8"))
    facts = payload.get("facts", payload)
    if not isinstance(facts, dict) or not facts:
        raise AuditError(f"truth layer contains no facts: {TRUTH}")
    return {
        "source": payload.get("source", ""),
        "facts": facts,
    }


def _auditable_beats(spec):
    beats = []
    for index, beat in enumerate(spec.get("beats", [])):
        content = {
            key: value for key, value in beat.items()
            if key not in _DROP_FIELDS and not key.startswith("_")
        }
        content["beat"] = index
        beats.append(content)
    return beats


def build_prompt(spec, truth):
    episode = {
        "id": spec.get("id", ""),
        "title": spec.get("title", ""),
        "beats": _auditable_beats(spec),
    }
    return (
        "Audit every factual claim in this episode against the truth layer. Claims without support "
        "are defects even when they sound plausible. Cite the beat number and exact claim.\n\n"
        "TRUTH LAYER:\n"
        f"{json.dumps(truth, ensure_ascii=False, indent=2)}\n\n"
        "EPISODE CONTENT:\n"
        f"{json.dumps(episode, ensure_ascii=False, indent=2)}"
    )


def _call_ollama(model, prompt):
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_ctx": AUDIT_NUM_CTX,
            "num_predict": AUDIT_NUM_PREDICT,
        },
    }).encode("utf-8")
    last_error = None
    for attempt in range(AUDIT_ATTEMPTS):
        request = urllib.request.Request(
            f"{OLLAMA_URL}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=900) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = AuditError(
                f"local Ollama audit failed at {OLLAMA_URL}: {exc}. "
                f"Start Ollama and ensure model '{model}' is installed."
            )
        else:
            if payload.get("done") is not True:
                raise AuditError(
                    f"Ollama returned an incomplete audit "
                    f"({payload.get('done_reason') or 'no reason'}); increase "
                    "CC_AUDIT_NUM_PREDICT or inspect the local model"
                )
            text = (payload.get("message") or {}).get("content")
            if isinstance(text, str) and text.strip():
                return text
            last_error = AuditError("Ollama returned no audit response")
        if attempt + 1 < AUDIT_ATTEMPTS:
            print("  auditor returned no usable response; retrying the same model once",
                  file=sys.stderr)
    raise last_error or AuditError("local Ollama audit failed without an error")


def parse_response(text):
    cleaned = text.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", cleaned, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        cleaned = fence.group(1)
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AuditError(f"auditor returned malformed JSON: {exc}") from exc
    if not isinstance(result, dict):
        raise AuditError("auditor response must be a JSON object")
    verdict = result.get("verdict")
    findings = result.get("findings")
    if verdict not in {"CLEAN", "NEEDS_REVIEW"} or not isinstance(findings, list):
        raise AuditError("auditor response requires verdict CLEAN|NEEDS_REVIEW and findings[]")
    if verdict == "CLEAN" and findings:
        raise AuditError("auditor returned CLEAN with findings")
    if verdict == "NEEDS_REVIEW" and not findings:
        raise AuditError("auditor returned NEEDS_REVIEW without findings")
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict) or not _REQUIRED_FINDING_FIELDS <= finding.keys():
            raise AuditError(f"finding {index} is missing required fields")
        if finding["severity"] not in {"P1", "P2"}:
            raise AuditError(f"finding {index} has invalid severity '{finding['severity']}'")
        if not isinstance(finding["beat"], int):
            raise AuditError(f"finding {index} beat must be an integer")
        for field in ("claim", "problem", "correction"):
            if not isinstance(finding[field], str) or not finding[field].strip():
                raise AuditError(f"finding {index} field '{field}' must be non-empty text")
    return result


def audit(spec_path, model=DEFAULT_MODEL, response_text=None):
    path = _resolve(spec_path)
    if not path.exists():
        raise AuditError(f"episode spec not found: {path}")
    spec = json.loads(path.read_text(encoding="utf-8"))
    truth = _truth_payload()
    response = response_text if response_text is not None else _call_ollama(
        model, build_prompt(spec, truth)
    )
    result = parse_response(response)
    episode = spec.get("id", path.stem)
    report = {
        "schema_version": "1.0",
        "episode": episode,
        "model": model,
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "truth_sha256": _sha256(TRUTH),
        "script_sha256": _sha256(path),
        "verdict": result["verdict"],
        "findings": result["findings"],
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    model_slug = re.sub(r"[^A-Za-z0-9._-]+", "-", model)
    report_path = REPORTS / f"{episode}.narration-audit.{model_slug}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")

    p1_count = sum(finding["severity"] == "P1" for finding in result["findings"])
    p2_count = sum(finding["severity"] == "P2" for finding in result["findings"])
    print(f"=== audit_narration {episode}: {p1_count} P1, {p2_count} P2 ===")
    for finding in result["findings"]:
        print(
            f"  {finding['severity']} beat {finding['beat']}: {finding['problem']} "
            f"[claim: {finding['claim']}]"
        )
    print(f"  report: {report_path}")
    if p2_count:
        print("  P2 findings require documented human review; verify them against truth.json.")
    return p1_count == 0, report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("specs", nargs="+", help="Episode spec paths")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Installed local Ollama model")
    args = parser.parse_args(argv)
    ok = True
    try:
        for spec_path in args.specs:
            passed, _report = audit(spec_path, model=args.model)
            ok = passed and ok
    except (AuditError, json.JSONDecodeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
