import json
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
GATES = ENGINE / "gates"
sys.path[:0] = [str(ENGINE), str(GATES)]
import verify_facts as gate


class StructuredFactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        gate.PROJECT = self.root
        gate.TRUTH = self.root / "course" / "data" / "truth.json"
        gate.TRUTH.parent.mkdir(parents=True)
        gate.TRUTH.write_text(json.dumps({
            "facts": {
                "EX-1": {
                    "title": "Illustrative values",
                    "statement": "The fictional values are 4 and 9 at 09:30.",
                }
            }
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def write_spec(self, value=9):
        path = self.root / "course" / "scripts" / "ep01.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "id": "ep01",
            "beats": [{
                "scene": "chart",
                "fact_ids": ["EX-1"],
                "data": [{"label": "A", "value": 4}, {"label": "B", "value": value}],
                "events": [{"when": "09:30", "label": "Example"}],
            }],
        }), encoding="utf-8")
        return path

    def test_structured_numbers_present_in_truth_pass(self):
        self.assertTrue(gate.verify(self.write_spec()))

    def test_project_relative_spec_path_resolves(self):
        self.write_spec()
        self.assertTrue(gate.verify("course/scripts/ep01.json"))

    def test_unsourced_structured_number_fails(self):
        self.assertFalse(gate.verify(self.write_spec(value=10)))


if __name__ == "__main__":
    unittest.main()
