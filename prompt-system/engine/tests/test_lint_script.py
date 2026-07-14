import json
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
GATES = ENGINE / "gates"
sys.path[:0] = [str(ENGINE), str(GATES)]
import lint_script as gate


class ScriptCraftGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name)
        gate.SCRIPTS = self.project / "course" / "scripts"
        gate.SCRIPTS.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write_quiz(self, question):
        (gate.SCRIPTS / "ep01.json").write_text(json.dumps({
            "id": "ep01",
            "beats": [{
                "scene": "quiz",
                "q": question,
                "options": ["First choice", "Second choice", "Third choice", "Fourth choice"],
                "answer": 1,
                "why": "The second choice is supported.",
            }],
        }), encoding="utf-8")

    def codes(self):
        p1, _p2 = gate.lint("ep01")
        return {code for _ep, code, _message in p1}

    def test_three_line_question_stays_above_captions(self):
        self.write_quiz(
            "A data point stands above its neighbors, then returns to its earlier range. "
            "Which conclusion is defensible?"
        )
        self.assertNotIn("QUIZ_CAPTION_COLLISION", self.codes())

    def test_long_question_is_blocked_before_render(self):
        self.write_quiz(
            "This deliberately long knowledge-check question repeats enough explanatory context "
            "to wrap across far too many lines and push all four interactive answer options into "
            "the lower caption-safe region where subtitles would obscure the final choice."
        )
        self.assertIn("QUIZ_CAPTION_COLLISION", self.codes())


if __name__ == "__main__":
    unittest.main()
