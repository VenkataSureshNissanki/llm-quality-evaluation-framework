import unittest
from scripts.run_demo import evaluate

class EvalTests(unittest.TestCase):
    def test_required(self): self.assertFalse(evaluate({"id":"1","answer":"hello","required":["world"]})["pass"])
    def test_prohibited(self): self.assertFalse(evaluate({"id":"1","answer":"secret","forbidden":["secret"]})["pass"])
    def test_refusal(self): self.assertTrue(evaluate({"id":"1","answer":"I cannot help","must_refuse":True})["pass"])
    def test_missing_refusal(self): self.assertFalse(evaluate({"id":"1","answer":"Sure","must_refuse":True})["pass"])
    def test_email(self): self.assertFalse(evaluate({"id":"1","answer":"x@example.com"})["pass"])
    def test_grounding(self): self.assertTrue(evaluate({"id":"1","answer":"5 days","context":"5 days","grounded":["5 days"]})["pass"])
    def test_unsupported(self): self.assertFalse(evaluate({"id":"1","answer":"1 day","context":"5 days","grounded":["5 days"]})["pass"])

if __name__=="__main__":unittest.main()
