import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
GATES = ENGINE / "gates"
sys.path[:0] = [str(ENGINE), str(GATES)]
import lint_instruction as gate


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


class InstructionGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name)
        gate.PROJECT = self.project
        gate.BLUEPRINT = self.project / "course" / "design" / "learning-blueprint.json"
        gate.TRUTH = self.project / "course" / "data" / "truth.json"
        gate.SCRIPTS = self.project / "course" / "scripts"

        self.truth = {
            "source": "Data Guide",
            "facts": {
                "F-1": {
                    "title": "Pattern",
                    "statement": "A pattern is supported by multiple observations.",
                    "section": "1",
                }
            },
        }
        self.blueprint = {
            "schema_version": "2.0",
            "course_goal": "Use several observations to classify a pattern and justify the decision.",
            "audience": {
                "description": "New analysts",
                "prior_knowledge": [],
                "work_context": "Reviewing simple dashboards",
            },
            "terminal_objective": {
                "id": "TO-1",
                "action_verb": "classify",
                "performance": "Classify a visible pattern and justify the choice with evidence.",
                "condition": "Given a small unfamiliar chart",
                "success_criteria": ["Uses at least three observations"],
                "level": "apply",
            },
            "coverage": {"required_fact_ids": ["F-1"], "excluded_fact_ids": []},
            "objectives": [{
                "id": "OBJ-1",
                "action_verb": "classify",
                "performance": "Classify a chart pattern and cite the observations that support it.",
                "condition": "Given a chart not used in instruction",
                "success_criteria": ["Correct category", "Evidence names multiple points"],
                "level": "apply",
                "prerequisites": [],
                "fact_ids": ["F-1"],
                "misconceptions": ["One spike always proves a trend"],
                "enables_terminal": True,
                "transfer_context": "A new dashboard with a different scale and values.",
                "evidence": [{
                    "id": "E-1",
                    "type": "apply_to_novel",
                    "description": "Classify an unfamiliar chart.",
                    "criteria": ["Correct classification", "Evidence-based justification"],
                }],
                "practices": [{
                    "id": "P-1",
                    "type": "apply_to_novel",
                    "description": "Classify a new series and explain the evidence.",
                    "scaffolding": "independent",
                    "transfer": True,
                    "feedback": {
                        "type": "elaborative",
                        "content": "Compare the candidate point with observations on both sides.",
                    },
                }],
                "representations": [
                    {
                        "treatment": "chart",
                        "purpose": "visualize_quantity",
                        "rationale": "The learner must inspect the quantitative pattern directly.",
                    },
                    {
                        "treatment": "worked_example",
                        "purpose": "model_reasoning",
                        "rationale": "A narrated example makes the evidence-selection process visible.",
                    },
                ],
            }],
            "episodes": [{"id": "ep01", "objective_ids": ["OBJ-1"], "retrieves": []}],
            "retention": {"follow_up": [{
                "after": "24 hours",
                "objective_ids": ["OBJ-1"],
                "activity": "Classify a fresh chart without notes.",
            }]},
            "delivery": {
                "mode": "direct",
                "cast": "narrator-only",
                "narrative": {"enabled": False},
            },
        }
        self.spec = {
            "schema_version": "2.0",
            "id": "ep01",
            "beats": [
                {"scene": "title", "title": "Patterns"},
                {
                    "scene": "chart",
                    "title": "Inspect several observations",
                    "chart_type": "line",
                    "data": [{"label": "A", "value": 4}, {"label": "B", "value": 9}],
                    "objective_ids": ["OBJ-1"],
                    "purpose": "explain",
                    "visual_purpose": "visualize_quantity",
                    "fact_ids": ["F-1"],
                    "alt": "A line rises from four to nine.",
                    "say": [["NARRATOR", "Use several observations, not one isolated point."]],
                },
                {
                    "scene": "worked_example",
                    "title": "Model the classification",
                    "problem": "Does one spike establish a trend?",
                    "steps": [{"title": "Compare", "detail": "Inspect both neighbors."}],
                    "model_answer": "No. One point is not a sustained direction.",
                    "objective_ids": ["OBJ-1"],
                    "purpose": "model",
                    "visual_purpose": "model_reasoning",
                    "fact_ids": ["F-1"],
                    "alt": "A worked example compares a spike with its neighboring points.",
                    "say": [["NARRATOR", "First compare the point with both neighbors."]],
                },
                {
                    "scene": "practice",
                    "prompt": "Classify this unfamiliar pattern and name your evidence.",
                    "instructions": "Answer before the reveal.",
                    "model_answer": "It is an anomaly because adjacent values return to baseline.",
                    "feedback": "The justification uses neighboring observations, not the spike alone.",
                    "practice_type": "scenario",
                    "think_seconds": 8,
                    "practice_id": "P-1",
                    "evidence_id": "E-1",
                    "objective_ids": ["OBJ-1"],
                    "purpose": "transfer",
                    "visual_purpose": "support_practice",
                    "say": [],
                },
            ],
        }
        write_json(self.project / "project.json", {
            "schema_version": "2.0",
            "topic": "Reading short time-series charts",
            "sources": [{
                "type": "notes",
                "name": "Pattern Guide",
                "path_or_url": "guide.txt",
            }],
            "audience": {
                "description": "New analysts",
                "prior_knowledge": ["Can read a line chart"],
                "work_context": "Weekly dashboard review",
            },
            "desired_performance": "Classify an unfamiliar chart and justify the decision.",
            "scope": {"kind": "single_video", "episodes": 1},
            "options": {
                "quizzes": True,
                "study_guide": False,
                "quick_reference": False,
                "avatars": False,
                "music": False,
                "narrative": False,
            },
            "delivery": {"mode": "direct", "tone": "clear and practical"},
        })
        self.save()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        write_json(gate.TRUTH, self.truth)
        write_json(gate.BLUEPRINT, self.blueprint)
        write_json(gate.SCRIPTS / "ep01.json", self.spec)
        write_json(self.project / "assets" / "media.json",
                   {"schema_version": "2.0", "assets": {}})

    def codes(self):
        problems, applied = gate.lint()
        self.assertTrue(applied)
        return {code for _level, code, _message in problems}

    def test_valid_direct_course_passes(self):
        problems, applied = gate.lint()
        self.assertTrue(applied)
        self.assertEqual([], [problem for problem in problems if problem[0] == "P1"])

    def test_vague_objective_is_blocked(self):
        self.blueprint["objectives"][0]["action_verb"] = "understand"
        self.save()
        self.assertIn("VAGUE_OBJECTIVE", self.codes())

    def test_higher_order_objective_cannot_use_recall_only_evidence(self):
        self.blueprint["objectives"][0]["evidence"][0]["type"] = "selected_response"
        self.save()
        self.assertIn("EVIDENCE_MISMATCH", self.codes())

    def test_disabled_narrative_blocks_story_scene(self):
        self.spec["beats"].insert(1, {
            "scene": "persona",
            "objective_ids": ["OBJ-1"],
            "purpose": "orient",
            "visual_purpose": "establish_context",
            "narrative": True,
            "narrative_function": "This fictional guide is intended to make the lesson feel exciting.",
        })
        self.save()
        codes = self.codes()
        self.assertIn("NARRATIVE_DISABLED", codes)
        self.assertIn("STORY_SCENE_DISABLED", codes)

    def test_unmanifested_media_is_blocked(self):
        self.blueprint["objectives"][0]["representations"][0]["treatment"] = "image"
        self.spec["beats"][1].update({
            "scene": "image",
            "asset": "missing-image",
            "alt": "A relevant source image.",
        })
        self.save()
        self.assertIn("UNMANIFESTED_ASSET", self.codes())

    def test_unmanifested_comparison_side_media_is_blocked(self):
        self.spec["beats"].insert(-1, {
            "scene": "comparison",
            "title": "Compare the cases",
            "left": {"asset": "missing-left", "title": "Case A"},
            "right": {"title": "Case B"},
            "objective_ids": ["OBJ-1"],
            "purpose": "example",
            "visual_purpose": "compare_cases",
            "fact_ids": ["F-1"],
            "alt": "Two chart cases shown side by side.",
            "say": [["NARRATOR", "Compare the direction across both cases."]],
        })
        self.save()
        self.assertIn("UNMANIFESTED_ASSET", self.codes())

    def test_project_schema_violation_is_blocked(self):
        project_file = self.project / "project.json"
        project = json.loads(project_file.read_text(encoding="utf-8"))
        del project["desired_performance"]
        write_json(project_file, project)
        self.assertIn("SCHEMA_PROJECT", self.codes())

    def test_practice_id_requires_active_learner_work(self):
        self.spec["beats"][2]["practice_id"] = "P-1"
        self.save()
        self.assertIn("PRACTICE_NOT_ACTIVE", self.codes())

    def test_incomplete_quiz_is_blocked(self):
        self.spec["beats"][-1] = {
            "scene": "quiz",
            "q": "Which pattern is supported?",
            "options": ["Trend", "Anomaly"],
            "answer": 4,
            "objective_ids": ["OBJ-1"],
            "purpose": "assess",
            "visual_purpose": "support_practice",
            "practice_id": "P-1",
            "evidence_id": "E-1",
            "fact_ids": ["F-1"],
        }
        self.save()
        found = self.codes()
        self.assertIn("SCHEMA_EPISODE", found)
        self.assertIn("QUIZ_INCOMPLETE", found)

    def test_legacy_project_skips_v2_gate(self):
        (self.project / "project.json").write_text("{}", encoding="utf-8")
        gate.BLUEPRINT.unlink()
        self.spec.pop("schema_version")
        write_json(gate.SCRIPTS / "ep01.json", self.spec)
        problems, applied = gate.lint()
        self.assertFalse(applied)
        self.assertEqual([], problems)


if __name__ == "__main__":
    unittest.main()
