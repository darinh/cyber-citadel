import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
GATES = ENGINE / "gates"
sys.path[:0] = [str(ENGINE), str(GATES)]
import audit_narration as gate


class NarrationAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name)
        gate.PROJECT = self.project
        gate.TRUTH = self.project / "course" / "data" / "truth.json"
        gate.REPORTS = self.project / "course" / "reports"
        gate.TRUTH.parent.mkdir(parents=True)
        gate.TRUTH.write_text(json.dumps({
            "source": "Pattern Guide",
            "facts": {
                "F-1": {
                    "title": "Trend",
                    "statement": "A trend is a sustained change in one direction.",
                }
            },
        }), encoding="utf-8")
        self.spec = self.project / "course" / "scripts" / "ep01.json"
        self.spec.parent.mkdir(parents=True)
        self.spec.write_text(json.dumps({
            "id": "ep01",
            "title": "Read the Pattern",
            "beats": [{
                "scene": "chart",
                "fact_ids": ["F-1"],
                "say": [["NARRATOR", "A trend sustains one direction."]],
                "min_seconds": 5,
            }],
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_fixture_passes_and_writes_report(self):
        passed, report = gate.audit(
            self.spec,
            model="fixture",
            response_text='{"verdict":"CLEAN","findings":[]}',
        )
        self.assertTrue(passed)
        self.assertEqual("CLEAN", report["verdict"])
        self.assertTrue((gate.REPORTS / "ep01.narration-audit.fixture.json").exists())

    def test_p1_fixture_blocks(self):
        response = json.dumps({
            "verdict": "NEEDS_REVIEW",
            "findings": [{
                "severity": "P1",
                "beat": 0,
                "scene": "chart",
                "claim": "One point proves a trend.",
                "fact_ids": ["F-1"],
                "problem": "The source requires sustained change.",
                "correction": "Several observations must sustain one direction.",
            }],
        })
        passed, report = gate.audit(self.spec, model="fixture", response_text=response)
        self.assertFalse(passed)
        self.assertEqual("P1", report["findings"][0]["severity"])

    def test_malformed_response_fails_loud(self):
        with self.assertRaises(gate.AuditError):
            gate.parse_response('{"verdict":"CLEAN","findings":[{"severity":"P1"}]}')

    def test_prompt_contains_truth_and_learner_claim(self):
        spec = json.loads(self.spec.read_text(encoding="utf-8"))
        truth = gate._truth_payload()
        prompt = gate.build_prompt(spec, truth)
        self.assertIn("sustained change in one direction", prompt)
        self.assertIn("A trend sustains one direction", prompt)
        self.assertNotIn("min_seconds", prompt)

    def test_empty_local_response_retries_same_model(self):
        class Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return json.dumps(self.payload).encode("utf-8")

        responses = [
            Response({"done": True, "message": {"content": ""}}),
            Response({"done": True, "message": {
                "content": '{"verdict":"CLEAN","findings":[]}',
            }}),
        ]
        with mock.patch.object(gate.urllib.request, "urlopen", side_effect=responses):
            text = gate._call_ollama("fixture", "audit this")
        self.assertEqual('{"verdict":"CLEAN","findings":[]}', text)


if __name__ == "__main__":
    unittest.main()
