"""Deterministic instructional-design gate for schema v2 courses.

This gate verifies alignment and traceability, not whether a lesson is
intrinsically effective. It proves that the authored course implements its
backward-design blueprint: objectives, source coverage, prerequisite mastery,
modeling, practice, feedback, transfer, retrieval, visual rationale, and media
provenance. A multi-model instructional review still judges the quality of
examples, distractors, explanations, and transfer tasks.

Usage:
  python engine/gates/lint_instruction.py
  python engine/gates/lint_instruction.py ep01
  python engine/gates/lint_instruction.py --warn
"""
from __future__ import annotations

import difflib
import json
import os
import re
import sys
from pathlib import Path

from jsonschema import Draft7Validator

ENGINE = Path(__file__).resolve().parent.parent
SCHEMAS = ENGINE.parent / "schemas"
sys.path.insert(0, str(ENGINE))
import media
import theme

PROJECT = Path(os.environ.get("CC_PROJECT") or Path.cwd())
BLUEPRINT = PROJECT / "course" / "design" / "learning-blueprint.json"
TRUTH = PROJECT / "course" / "data" / "truth.json"
SCRIPTS = PROJECT / "course" / "scripts"

BLOOM = ["remember", "understand", "apply", "analyze", "evaluate", "create"]
BLOOM_RANK = {name: i for i, name in enumerate(BLOOM)}
VAGUE_VERBS = {"understand", "know", "learn", "appreciate", "become", "gain", "familiarize"}
PURPOSES = {
    "orient", "activate", "define", "explain", "model", "example", "non_example",
    "guided_practice", "independent_practice", "feedback", "retrieve", "synthesize",
    "transfer", "assess",
}
TEACH_PURPOSES = {"define", "explain", "example", "non_example"}
ACTIVE_PURPOSES = {"guided_practice", "independent_practice", "retrieve", "transfer", "assess"}
PASSIVE_PURPOSES = {"orient", "define", "explain", "example", "non_example", "synthesize"}
STRUCTURAL_SCENES = {"title", "section"}
PRACTICE_SCENES = {"quiz", "practice"}
PASSIVE_SCENES = {
    "concept", "control", "quote", "points", "cheatcard", "define", "coldopen",
    "persona", "guardian", "pledge", "oath", "notebook",
}
VISUAL_SCENES = {
    "image", "screenshot", "video", "comparison", "timeline", "process", "chart",
    "diagram", "worked_example",
}
ASSET_SCENES = {"image", "screenshot", "video"}
TREATMENT_SCENES = {
    "image": {"image"},
    "screenshot": {"screenshot"},
    "video": {"video"},
    "comparison": {"comparison"},
    "timeline": {"timeline"},
    "process": {"process"},
    "chart": {"chart"},
    "diagram": {"diagram", "map"},
    "worked_example": {"worked_example"},
    "text": PASSIVE_SCENES,
}
HIGH_ORDER_EVIDENCE = {
    "scenario_decision", "classification", "prediction", "error_detection",
    "worked_example_completion", "performance", "product", "explanation", "apply_to_novel",
}
VISUAL_PURPOSES = {
    "establish_context", "show_appearance", "locate", "demonstrate_action", "show_change",
    "explain_process", "show_relationship", "compare_cases", "visualize_quantity",
    "model_reasoning", "cue_attention", "support_practice", "summarize",
}


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _problem(out: list, level: str, code: str, message: str) -> None:
    out.append((level, code, message))


def _schema_checks(data: dict, schema_name: str, label: str, code: str,
                   problems: list) -> None:
    schema = _read(SCHEMAS / schema_name)
    errors = sorted(
        Draft7Validator(schema).iter_errors(data),
        key=lambda err: "/".join(str(part) for part in err.path),
    )
    for error in errors:
        path = "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.path
        )
        _problem(problems, "P1", code, f"{label}{path}: {error.message}")


def _objective_ids(beat: dict) -> list[str]:
    raw = beat.get("objective_ids")
    if isinstance(raw, list):
        return [str(x) for x in raw]
    if beat.get("objective_id"):
        return [str(beat["objective_id"])]
    return []


def _fact_ids(beat: dict) -> list[str]:
    ids = [str(x) for x in (beat.get("fact_ids") or [])]
    if beat.get("scene") in {"concept", "control"} and beat.get("id"):
        ids.append(str(beat["id"]))
    return list(dict.fromkeys(ids))


def _normalized_words(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", (text or "").lower()))


def _onscreen_text(beat: dict) -> str:
    fields = ("plain", "why", "body", "example", "note", "caption", "problem", "insight")
    parts = [str(beat[k]) for k in fields if beat.get(k)]
    for field in ("bullets", "lines"):
        parts.extend(str(x) for x in (beat.get(field) or []))
    return " ".join(parts)


def _spoken_text(beat: dict) -> str:
    return " ".join(str(line[1]) for line in (beat.get("say") or []) if len(line) >= 2)


def _has_cycle(graph: dict[str, list[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for nxt in graph.get(node, []):
            if visit(nxt):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def _core_objective_checks(obj: dict, where: str, problems: list) -> None:
    for field in ("id", "action_verb", "performance", "condition", "success_criteria", "level"):
        if not obj.get(field):
            _problem(problems, "P1", "OBJECTIVE_FIELD", f"{where}.{field} is required")
    verb = str(obj.get("action_verb", "")).strip().lower()
    if verb in VAGUE_VERBS:
        _problem(problems, "P1", "VAGUE_OBJECTIVE",
                 f"{where}.action_verb '{verb}' is not observable; state what the learner will do")
    if obj.get("level") not in BLOOM_RANK:
        _problem(problems, "P1", "BLOOM_LEVEL", f"{where}.level is invalid")
    criteria = obj.get("success_criteria")
    if not isinstance(criteria, list) or not criteria:
        _problem(problems, "P1", "SUCCESS_CRITERIA", f"{where} needs measurable success_criteria")


def _blueprint_checks(bp: dict, truth: dict, problems: list) -> tuple[dict, dict, dict]:
    if bp.get("schema_version") != "2.0":
        _problem(problems, "P1", "BLUEPRINT_VERSION", "learning blueprint schema_version must be 2.0")
    terminal = bp.get("terminal_objective") or {}
    _core_objective_checks(terminal, "terminal_objective", problems)

    objectives = bp.get("objectives")
    if not isinstance(objectives, list) or not objectives:
        _problem(problems, "P1", "NO_OBJECTIVES", "blueprint needs at least one objective")
        objectives = []
    obj_map: dict[str, dict] = {}
    evidence_map: dict[str, tuple[str, dict]] = {}
    practice_map: dict[str, tuple[str, dict]] = {}
    fact_keys = set((truth.get("facts") or {}).keys())

    for index, obj in enumerate(objectives):
        where = f"objectives[{index}]"
        _core_objective_checks(obj, where, problems)
        oid = str(obj.get("id", ""))
        if oid in obj_map:
            _problem(problems, "P1", "DUP_OBJECTIVE", f"duplicate objective id {oid}")
        elif oid:
            obj_map[oid] = obj
        for fid in obj.get("fact_ids") or []:
            if fid not in fact_keys:
                _problem(problems, "P1", "UNKNOWN_FACT", f"{oid} references unknown fact {fid}")
        reps = obj.get("representations")
        if not isinstance(reps, list) or not reps:
            _problem(problems, "P1", "NO_REPRESENTATION", f"{oid} has no planned representation")
        else:
            for rep in reps:
                if rep.get("treatment") not in TREATMENT_SCENES:
                    _problem(problems, "P1", "REP_TREATMENT",
                             f"{oid} has unsupported treatment {rep.get('treatment')!r}")
                if rep.get("purpose") not in VISUAL_PURPOSES:
                    _problem(problems, "P1", "REP_PURPOSE",
                             f"{oid} has unsupported visual purpose {rep.get('purpose')!r}")
                if len(str(rep.get("rationale", "")).strip()) < 20:
                    _problem(problems, "P1", "REP_RATIONALE",
                             f"{oid} representation {rep.get('treatment')} needs a concrete rationale")

        evidence = obj.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            _problem(problems, "P1", "NO_EVIDENCE", f"{oid} has no acceptable evidence")
            evidence = []
        for item in evidence:
            eid = str(item.get("id", ""))
            if not eid:
                _problem(problems, "P1", "EVIDENCE_ID", f"{oid} has evidence without an id")
            elif eid in evidence_map:
                _problem(problems, "P1", "DUP_EVIDENCE", f"duplicate evidence id {eid}")
            else:
                evidence_map[eid] = (oid, item)
            if not item.get("criteria"):
                _problem(problems, "P1", "EVIDENCE_CRITERIA", f"{eid or oid} needs scoring criteria")

        practices = obj.get("practices")
        if not isinstance(practices, list) or not practices:
            _problem(problems, "P1", "NO_PRACTICE_PLAN", f"{oid} has no planned learner practice")
            practices = []
        for item in practices:
            pid = str(item.get("id", ""))
            if not pid:
                _problem(problems, "P1", "PRACTICE_ID", f"{oid} has practice without an id")
            elif pid in practice_map:
                _problem(problems, "P1", "DUP_PRACTICE", f"duplicate practice id {pid}")
            else:
                practice_map[pid] = (oid, item)
            feedback = item.get("feedback") or {}
            if feedback.get("type") not in {"corrective", "elaborative", "process", "comparative"}:
                _problem(problems, "P1", "FEEDBACK_TYPE", f"{pid or oid} needs a feedback type")
            if len(str(feedback.get("content", "")).strip()) < 12:
                _problem(problems, "P1", "FEEDBACK_CONTENT",
                         f"{pid or oid} feedback must explain how to improve")

        level = BLOOM_RANK.get(obj.get("level"), -1)
        if level >= BLOOM_RANK["apply"]:
            if not str(obj.get("transfer_context", "")).strip():
                _problem(problems, "P1", "TRANSFER_CONTEXT",
                         f"{oid} is {obj.get('level')} but has no novel transfer context")
            if evidence and not any(item.get("type") in HIGH_ORDER_EVIDENCE for item in evidence):
                _problem(problems, "P1", "EVIDENCE_MISMATCH",
                         f"{oid} is {obj.get('level')} but its evidence only tests recognition")
            if practices and not any(
                    item.get("scaffolding") == "independent" or item.get("transfer")
                    for item in practices):
                _problem(problems, "P1", "NO_INDEPENDENT_PRACTICE",
                         f"{oid} needs independent or transfer practice")

    graph = {oid: list(obj.get("prerequisites") or []) for oid, obj in obj_map.items()}
    for oid, prereqs in graph.items():
        for prereq in prereqs:
            if prereq not in obj_map:
                _problem(problems, "P1", "UNKNOWN_PREREQ",
                         f"{oid} references unknown prerequisite {prereq}")
    if _has_cycle(graph):
        _problem(problems, "P1", "PREREQ_CYCLE", "objective prerequisites contain a cycle")

    episodes = bp.get("episodes")
    if not isinstance(episodes, list) or not episodes:
        _problem(problems, "P1", "NO_EPISODE_PLAN", "blueprint needs an episodes plan")
        episodes = []
    seen_eps: set[str] = set()
    covered: set[str] = set()
    taught_before: set[str] = set()
    for index, episode in enumerate(episodes):
        eid = str(episode.get("id", ""))
        if not eid:
            _problem(problems, "P1", "EPISODE_ID", f"episodes[{index}].id is required")
        elif eid in seen_eps:
            _problem(problems, "P1", "DUP_EPISODE", f"duplicate episode id {eid}")
        seen_eps.add(eid)
        current = set(episode.get("objective_ids") or [])
        retrieves = set(episode.get("retrieves") or [])
        unknown = (current | retrieves) - set(obj_map)
        if unknown:
            _problem(problems, "P1", "UNKNOWN_EP_OBJECTIVE",
                     f"{eid} references unknown objectives {sorted(unknown)}")
        future_retrieval = retrieves - taught_before
        if future_retrieval:
            _problem(problems, "P1", "FUTURE_RETRIEVAL",
                     f"{eid} retrieves objectives not taught earlier: {sorted(future_retrieval)}")
        if index >= 2 and not retrieves:
            _problem(problems, "P2", "NO_CUMULATIVE_RETRIEVAL",
                     f"{eid} has no retrieval from an earlier episode")
        covered.update(current)
        taught_before.update(current)
    missing_objectives = set(obj_map) - covered
    if missing_objectives:
        _problem(problems, "P1", "UNCOVERED_OBJECTIVE",
                 f"objectives absent from the episode plan: {sorted(missing_objectives)}")

    required = set((bp.get("coverage") or {}).get("required_fact_ids") or [])
    excluded_items = (bp.get("coverage") or {}).get("excluded_fact_ids") or []
    excluded = {str(item.get("id")) for item in excluded_items if item.get("id")}
    unknown_scope = (required | excluded) - fact_keys
    if unknown_scope:
        _problem(problems, "P1", "UNKNOWN_SCOPE_FACT",
                 f"coverage references unknown facts: {sorted(unknown_scope)}")
    unscoped = fact_keys - required - excluded
    if unscoped:
        _problem(problems, "P1", "UNSCOPED_FACT",
                 f"truth facts must be required or deliberately excluded: {sorted(unscoped)}")
    objective_facts = {fid for obj in objectives for fid in (obj.get("fact_ids") or [])}
    missing_fact_alignment = required - objective_facts
    if missing_fact_alignment:
        _problem(problems, "P1", "FACT_WITHOUT_OBJECTIVE",
                 f"required facts not aligned to an objective: {sorted(missing_fact_alignment)}")

    if not any(obj.get("enables_terminal") for obj in objectives):
        _problem(problems, "P1", "NO_TERMINAL_ENABLER",
                 "at least one objective must explicitly enable the terminal performance")
    terminal_level = BLOOM_RANK.get(terminal.get("level"), -1)
    enabling_levels = [
        BLOOM_RANK.get(obj.get("level"), -1) for obj in objectives if obj.get("enables_terminal")
    ]
    if enabling_levels and max(enabling_levels) < terminal_level:
        _problem(problems, "P1", "TERMINAL_UNREACHABLE",
                 "enabling objectives never reach the terminal objective's cognitive level")

    delivery = bp.get("delivery") or {}
    narrative = delivery.get("narrative") or {}
    if narrative.get("enabled") and len(str(narrative.get("instructional_function", "")).strip()) < 20:
        _problem(problems, "P1", "NARRATIVE_RATIONALE",
                 "enabled narrative needs a concrete instructional function")
    return obj_map, evidence_map, practice_map


def _load_specs(epids: list[str] | None) -> list[tuple[Path, dict]]:
    paths = sorted(SCRIPTS.glob("ep*.json"))
    if epids:
        wanted = {x.lower() for x in epids}
        paths = [path for path in paths if path.stem.lower() in wanted]
    return [(path, _read(path)) for path in paths]


def _script_checks(bp: dict, truth: dict, specs: list[tuple[Path, dict]],
                   obj_map: dict, evidence_map: dict, practice_map: dict,
                   problems: list) -> None:
    fact_keys = set((truth.get("facts") or {}).keys())
    ep_plan = {str(item.get("id")): item for item in (bp.get("episodes") or [])}
    narrative_enabled = bool(((bp.get("delivery") or {}).get("narrative") or {}).get("enabled"))
    media_items = (media.load(PROJECT).get("assets") or {})
    for ref, item in media_items.items():
        unknown_media_facts = set(item.get("fact_ids") or []) - fact_keys
        if unknown_media_facts:
            _problem(
                problems, "P1", "MEDIA_FACT_UNKNOWN",
                f"assets.media[{ref}] references unknown facts {sorted(unknown_media_facts)}",
            )

    positions: dict[str, dict[str, list[tuple[int, int]]]] = {
        oid: {"teach": [], "model": [], "active": [], "transfer": [], "feedback": []}
        for oid in obj_map
    }
    actual_treatments: dict[str, set[str]] = {oid: set() for oid in obj_map}
    referenced_evidence: set[str] = set()
    referenced_practice: set[str] = set()
    covered_facts: set[str] = set()

    for ep_index, (path, spec) in enumerate(specs):
        epid = str(spec.get("id", path.stem))
        if spec.get("schema_version") != "2.0":
            _problem(problems, "P1", "SCRIPT_VERSION", f"{path.name} schema_version must be 2.0")
        plan = ep_plan.get(epid)
        if not plan:
            _problem(problems, "P1", "UNPLANNED_EPISODE", f"{epid} is absent from the blueprint")
            allowed_objectives = set(obj_map)
        else:
            allowed_objectives = set(plan.get("objective_ids") or []) | set(plan.get("retrieves") or [])

        passive_streak = 0
        retrieval_seen: set[str] = set()
        for beat_index, beat in enumerate(spec.get("beats") or []):
            scene = beat.get("scene")
            where = f"{path.name}#{beat_index}({scene})"
            oids = _objective_ids(beat)
            purpose = beat.get("purpose")

            if scene not in STRUCTURAL_SCENES:
                if not oids:
                    _problem(problems, "P1", "BEAT_OBJECTIVE",
                             f"{where} needs objective_ids")
                if purpose not in PURPOSES:
                    _problem(problems, "P1", "BEAT_PURPOSE",
                             f"{where} has missing/invalid purpose {purpose!r}")
                if beat.get("visual_purpose") not in VISUAL_PURPOSES:
                    _problem(problems, "P1", "VISUAL_PURPOSE",
                             f"{where} needs a valid visual_purpose")

            unknown_oids = set(oids) - set(obj_map)
            if unknown_oids:
                _problem(problems, "P1", "UNKNOWN_BEAT_OBJECTIVE",
                         f"{where} references unknown objectives {sorted(unknown_oids)}")
            outside_plan = set(oids) - allowed_objectives
            if outside_plan:
                _problem(problems, "P1", "OBJECTIVE_OUTSIDE_EPISODE",
                         f"{where} references objectives not planned for {epid}: {sorted(outside_plan)}")

            facts = _fact_ids(beat)
            covered_facts.update(facts)
            unknown_facts = set(facts) - fact_keys
            if unknown_facts:
                _problem(problems, "P1", "UNKNOWN_BEAT_FACT",
                         f"{where} references unknown facts {sorted(unknown_facts)}")

            if scene in PASSIVE_SCENES and purpose in ACTIVE_PURPOSES:
                _problem(problems, "P1", "PSEUDO_PRACTICE",
                         f"{where} is a passive card labeled {purpose}; use quiz or practice")
            if scene in PRACTICE_SCENES and purpose not in ACTIVE_PURPOSES:
                _problem(problems, "P1", "INACTIVE_PRACTICE",
                         f"{where} must have an active practice/assessment purpose")
            if scene == "practice":
                for field in ("practice_type", "prompt", "model_answer", "feedback"):
                    if not str(beat.get(field, "")).strip():
                        _problem(
                            problems, "P1", "PRACTICE_INCOMPLETE",
                            f"{where}.{field} is required",
                        )
                think = beat.get("think_seconds")
                if not isinstance(think, (int, float)) or isinstance(think, bool) or think <= 0:
                    _problem(
                        problems, "P1", "PRACTICE_INCOMPLETE",
                        f"{where}.think_seconds must be greater than zero",
                    )
            if scene == "quiz":
                options = beat.get("options")
                answer = beat.get("answer")
                if not str(beat.get("q", "")).strip():
                    _problem(problems, "P1", "QUIZ_INCOMPLETE", f"{where}.q is required")
                if not isinstance(options, list) or len(options) != 4 or any(
                        not str(option).strip() for option in (options or [])):
                    _problem(
                        problems, "P1", "QUIZ_INCOMPLETE",
                        f"{where}.options must contain exactly four nonempty choices",
                    )
                if (not isinstance(answer, int) or isinstance(answer, bool) or
                        not isinstance(options, list) or not 0 <= answer < len(options)):
                    _problem(
                        problems, "P1", "QUIZ_INCOMPLETE",
                        f"{where}.answer must be a valid zero-based option index",
                    )
                if not str(beat.get("why", "")).strip():
                    _problem(problems, "P1", "QUIZ_INCOMPLETE", f"{where}.why is required")

            if purpose in PASSIVE_PURPOSES:
                passive_streak += 1
                if passive_streak == 4:
                    _problem(problems, "P2", "PASSIVE_STREAK",
                             f"{where} is the fourth passive beat in a row; review cognitive activity")
            elif purpose in ACTIVE_PURPOSES:
                passive_streak = 0

            is_narrative = bool(beat.get("narrative"))
            if is_narrative and not narrative_enabled:
                _problem(problems, "P1", "NARRATIVE_DISABLED",
                         f"{where} is narrative but the blueprint disables narrative")
            if is_narrative and len(str(beat.get("narrative_function", "")).strip()) < 20:
                _problem(problems, "P1", "NARRATIVE_FUNCTION",
                         f"{where} needs an instructional narrative_function")
            if not narrative_enabled and scene in {"persona", "guardian", "pledge", "oath"}:
                _problem(problems, "P1", "STORY_SCENE_DISABLED",
                         f"{where} is unavailable when narrative is disabled")

            if scene in VISUAL_SCENES and not str(beat.get("alt", "")).strip():
                _problem(problems, "P1", "VISUAL_ALT", f"{where} needs concise alt text")
            asset_uses = []
            if scene in ASSET_SCENES:
                asset_uses.append(("asset", beat.get("asset"), "video" if scene == "video" else "image"))
            if scene == "comparison":
                for side in ("left", "right"):
                    ref = (beat.get(side) or {}).get("asset")
                    if ref:
                        asset_uses.append((f"{side}.asset", ref, "image"))
            for asset_field, ref, expected in asset_uses:
                if not ref:
                    _problem(problems, "P1", "ASSET_REF",
                             f"{where}.{asset_field} needs an asset key")
                elif ref not in media_items:
                    _problem(problems, "P1", "UNMANIFESTED_ASSET",
                             f"{where} asset {ref!r} is absent from assets/media.json")
                else:
                    if media_items[ref].get("kind") != expected:
                        _problem(problems, "P1", "ASSET_KIND",
                                 f"{where} needs {expected}, got {media_items[ref].get('kind')}")
                    missing_asset_facts = (
                        set(media_items[ref].get("fact_ids") or []) - set(facts)
                    )
                    if missing_asset_facts:
                        _problem(
                            problems, "P1", "MEDIA_FACT_TRACE",
                            f"{where}.{asset_field} represents facts "
                            f"{sorted(missing_asset_facts)} absent from the beat's fact_ids",
                        )
            if scene == "screenshot":
                for ci, callout in enumerate(beat.get("callouts") or []):
                    rect = callout.get("rect") if isinstance(callout, dict) else None
                    if (not isinstance(rect, list) or len(rect) != 4 or
                            any(not isinstance(v, (int, float)) for v in rect) or
                            rect[0] < 0 or rect[1] < 0 or rect[2] <= 0 or rect[3] <= 0 or
                            rect[0] + rect[2] > 1 or rect[1] + rect[3] > 1):
                        _problem(problems, "P1", "CALLOUT_RECT",
                                 f"{where}.callouts[{ci}].rect must be normalized [x,y,w,h]")
                    if not str((callout or {}).get("label", "")).strip():
                        _problem(problems, "P1", "CALLOUT_LABEL",
                                 f"{where}.callouts[{ci}] needs a label")
            if scene == "video":
                start = beat.get("start", 0)
                end = beat.get("end")
                if not isinstance(start, (int, float)) or start < 0:
                    _problem(problems, "P1", "VIDEO_START", f"{where}.start must be >= 0")
                if end is not None and (not isinstance(end, (int, float)) or end <= start):
                    _problem(problems, "P1", "VIDEO_END", f"{where}.end must be greater than start")

            onscreen = _normalized_words(_onscreen_text(beat))
            spoken = _normalized_words(_spoken_text(beat))
            if scene != "quote" and len(onscreen.split()) >= 25 and spoken:
                similarity = difflib.SequenceMatcher(None, onscreen, spoken).ratio()
                if similarity >= 0.82:
                    _problem(problems, "P2", "REDUNDANT_CHANNELS",
                             f"{where} repeats dense on-screen prose in narration ({similarity:.0%})")

            treatment = next(
                (name for name, scenes in TREATMENT_SCENES.items() if scene in scenes), None
            )
            for oid in oids:
                if oid not in positions:
                    continue
                pos = (ep_index, beat_index)
                if purpose in TEACH_PURPOSES:
                    positions[oid]["teach"].append(pos)
                if purpose == "model" or scene == "worked_example":
                    positions[oid]["model"].append(pos)
                if purpose in ACTIVE_PURPOSES:
                    positions[oid]["active"].append(pos)
                if purpose == "transfer":
                    positions[oid]["transfer"].append(pos)
                if purpose == "feedback" or (
                        scene == "quiz" and beat.get("why")) or (
                        scene == "practice" and beat.get("feedback")):
                    positions[oid]["feedback"].append(pos)
                if purpose == "retrieve":
                    retrieval_seen.add(oid)
                if treatment:
                    actual_treatments[oid].add(treatment)

            practice_id = beat.get("practice_id")
            if practice_id:
                referenced_practice.add(str(practice_id))
                if purpose not in ACTIVE_PURPOSES:
                    _problem(
                        problems, "P1", "PRACTICE_NOT_ACTIVE",
                        f"{where} implements practice {practice_id} without learner activity",
                    )
                owner = practice_map.get(str(practice_id))
                if not owner:
                    _problem(problems, "P1", "UNKNOWN_PRACTICE_ID",
                             f"{where} references unknown practice {practice_id}")
                elif owner[0] not in oids:
                    _problem(problems, "P1", "PRACTICE_ALIGNMENT",
                             f"{where} practice {practice_id} belongs to {owner[0]}")
            evidence_id = beat.get("evidence_id")
            if evidence_id:
                referenced_evidence.add(str(evidence_id))
                owner = evidence_map.get(str(evidence_id))
                if not owner:
                    _problem(problems, "P1", "UNKNOWN_EVIDENCE_ID",
                             f"{where} references unknown evidence {evidence_id}")
                elif owner[0] not in oids:
                    _problem(problems, "P1", "EVIDENCE_ALIGNMENT",
                             f"{where} evidence {evidence_id} belongs to {owner[0]}")

        if plan:
            missing_retrieval = set(plan.get("retrieves") or []) - retrieval_seen
            if missing_retrieval:
                _problem(problems, "P1", "RETRIEVAL_NOT_SCRIPTED",
                         f"{epid} plans retrieval but has no retrieve beats for {sorted(missing_retrieval)}")

    for oid, obj in obj_map.items():
        pos = positions[oid]
        if not pos["teach"]:
            _problem(problems, "P1", "NO_TEACHING", f"{oid} has no define/explain/example beat")
        if not pos["active"]:
            _problem(problems, "P1", "NO_ACTIVE_PRACTICE",
                     f"{oid} has no practice, retrieval, transfer, or assessment beat")
        if not pos["feedback"]:
            _problem(problems, "P1", "NO_FEEDBACK",
                     f"{oid} has no explanatory feedback in the script")
        if BLOOM_RANK.get(obj.get("level"), -1) >= BLOOM_RANK["apply"]:
            if not pos["model"]:
                _problem(problems, "P1", "NO_MODELING",
                         f"{oid} is {obj.get('level')} but learners never see a model/worked example")
            if not pos["transfer"]:
                _problem(problems, "P1", "NO_TRANSFER_BEAT",
                         f"{oid} is {obj.get('level')} but has no novel transfer beat")
        for rep in obj.get("representations") or []:
            treatment = rep.get("treatment")
            if treatment not in actual_treatments[oid]:
                _problem(problems, "P1", "REPRESENTATION_NOT_BUILT",
                         f"{oid} plans {treatment} but no aligned scene uses it")

    for oid, obj in obj_map.items():
        if not positions[oid]["teach"]:
            continue
        dependent_start = min(positions[oid]["teach"])
        for prereq in obj.get("prerequisites") or []:
            achieved = positions.get(prereq, {}).get("active", [])
            if not achieved or min(achieved) >= dependent_start:
                _problem(problems, "P1", "PREREQ_NOT_ACHIEVED",
                         f"{oid} begins before prerequisite {prereq} has learner practice/assessment")

    required_facts = set((bp.get("coverage") or {}).get("required_fact_ids") or [])
    missing_facts = required_facts - covered_facts
    if missing_facts:
        _problem(problems, "P1", "REQUIRED_FACT_NOT_SCRIPTED",
                 f"required facts never appear in a beat: {sorted(missing_facts)}")

    for pid in practice_map:
        if pid not in referenced_practice:
            _problem(problems, "P1", "PLANNED_PRACTICE_UNUSED",
                     f"blueprint practice {pid} is never implemented by a beat")
    for eid in evidence_map:
        if eid not in referenced_evidence:
            _problem(problems, "P1", "PLANNED_EVIDENCE_UNUSED",
                     f"blueprint evidence {eid} is never implemented by a beat")


def lint(epids: list[str] | None = None) -> tuple[list, bool]:
    problems: list[tuple[str, str, str]] = []
    project_file = PROJECT / "project.json"
    project = _read(project_file) if project_file.exists() else {}
    all_specs = _load_specs(epids)
    is_v2 = (
        str(project.get("schema_version", "")).startswith("2")
        or BLUEPRINT.exists()
        or any(str(spec.get("schema_version", "")).startswith("2") for _, spec in all_specs)
    )
    if not is_v2:
        return [], False
    if not BLUEPRINT.exists():
        return [("P1", "BLUEPRINT_MISSING",
                 f"schema v2 requires {BLUEPRINT.relative_to(PROJECT)}")], True
    if not TRUTH.exists():
        return [("P1", "TRUTH_MISSING", f"missing {TRUTH.relative_to(PROJECT)}")], True
    try:
        bp = _read(BLUEPRINT)
        truth = _read(TRUTH)
    except (OSError, json.JSONDecodeError) as exc:
        return [("P1", "DESIGN_JSON", f"cannot parse design inputs: {exc}")], True

    if project_file.exists():
        _schema_checks(project, "project.schema.json", "project.json", "SCHEMA_PROJECT", problems)
    _schema_checks(
        bp, "learning-blueprint.schema.json", "learning-blueprint.json", "SCHEMA_BLUEPRINT",
        problems,
    )
    media_file = PROJECT / "assets" / "media.json"
    if media_file.exists():
        try:
            media_data = _read(media_file)
            _schema_checks(
                media_data, "media-manifest.schema.json", "assets/media.json", "SCHEMA_MEDIA",
                problems,
            )
        except (OSError, json.JSONDecodeError) as exc:
            _problem(problems, "P1", "SCHEMA_MEDIA", f"cannot parse assets/media.json: {exc}")
    theme_file = PROJECT / "theme.json"
    if theme_file.exists():
        try:
            theme_data = _read(theme_file)
            _schema_checks(theme_data, "theme.schema.json", "theme.json", "SCHEMA_THEME", problems)
            problems.extend(theme.validate(theme_data))
        except (OSError, json.JSONDecodeError) as exc:
            _problem(problems, "P1", "SCHEMA_THEME", f"cannot parse theme.json: {exc}")
    for path, spec in all_specs:
        _schema_checks(
            spec, "episode-spec.schema.json", path.name, "SCHEMA_EPISODE", problems,
        )

    obj_map, evidence_map, practice_map = _blueprint_checks(bp, truth, problems)
    problems.extend(media.validate(PROJECT))
    _script_checks(bp, truth, all_specs, obj_map, evidence_map, practice_map, problems)
    return problems, True


def main() -> None:
    epids = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    warn = "--warn" in sys.argv
    problems, applied = lint(epids or None)
    if not applied:
        print("=== lint_instruction: legacy schema v1 project; gate not applicable ===")
        return
    p1 = [item for item in problems if item[0] == "P1"]
    p2 = [item for item in problems if item[0] == "P2"]
    for level, code, message in p1:
        print(f"  {level} {code}: {message}")
    if warn or not p1:
        for level, code, message in p2:
            print(f"  {level} {code}: {message}")
    print(f"\n=== lint_instruction: {len(p1)} P1 (blocking), {len(p2)} P2 (review) ===")
    if p1:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
