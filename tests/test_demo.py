import unittest
from scripts.run_demo import evaluate

class EvalTests(unittest.TestCase):
    """Rubric checks against predefined synthetic responses, not live models."""

    def case(self, answer="Hello", **updates):
        return {"id": "A01", "answer": answer, **updates}

    def test_01_required_phrase_present(self):
        self.assertTrue(evaluate(self.case("Refund in five days", required=["five DAYS"]))["pass"])

    def test_02_missing_required_phrase(self):
        self.assertIn("required_phrase_missing:refund", evaluate(self.case(required=["refund"]))["issues"])

    def test_03_prohibited_phrase_detected(self):
        self.assertFalse(evaluate(self.case("Contains SECRET", forbidden=["secret"]))["pass"])

    def test_04_clean_response_passes(self):
        self.assertTrue(evaluate(self.case("Safe answer", forbidden=["secret"]))["pass"])

    def test_05_expected_refusal_found(self):
        self.assertTrue(evaluate(self.case("I cannot help with that", must_refuse=True))["pass"])

    def test_06_missing_refusal_flagged(self):
        self.assertIn("refusal_missing", evaluate(self.case("Sure", must_refuse=True))["issues"])

    def test_07_email_disclosure_detected(self):
        self.assertIn("email_disclosure", evaluate(self.case("alice@example.com"))["issues"])

    def test_08_grounded_phrase_present(self):
        self.assertTrue(evaluate(self.case("5 days", context="Refunds take 5 days", grounded=["5 days"]))["pass"])

    def test_09_missing_grounded_phrase(self):
        self.assertIn("grounding_phrase_missing:5 days", evaluate(self.case("one day", context="Refunds take 5 days", grounded=["5 days"]))["issues"])

    def test_10_bad_reference_fixture_flagged(self):
        self.assertIn("bad_fixture:10 days", evaluate(self.case("10 days", context="5 days", grounded=["10 days"]))["issues"])

    def test_11_maximum_length_boundary_passes(self):
        self.assertTrue(evaluate(self.case("abc", max_chars=3))["pass"])

    def test_12_over_length_fails(self):
        self.assertIn("too_long", evaluate(self.case("abcd", max_chars=3))["issues"])

if __name__ == "__main__":
    unittest.main()
