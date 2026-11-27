"""Week 6 - Offline tests (no Ollama needed).

Checks the golden set itself and the keyword-scoring function, so you
can prove the project is sound before the (slow) live llama3.2 run.

Run:  python test_week6.py
Expected: all tests pass, ending with OK.
"""
import json
import unittest

from main import calculate_score


class TestGoldenSet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("golden_set.json", "r", encoding="utf-8") as f:
            cls.data = json.load(f)

    def test_has_30_questions(self):
        self.assertEqual(len(self.data), 30)

    def test_ids_are_q001_to_q030_in_order(self):
        ids = [item["id"] for item in self.data]
        self.assertEqual(ids, [f"Q{i:03d}" for i in range(1, 31)])

    def test_every_item_has_all_fields(self):
        for item in self.data:
            for field in ("id", "question", "expected_answer", "keywords", "source"):
                self.assertIn(field, item, f"{item.get('id')} missing {field}")
            self.assertTrue(item["question"].strip())
            self.assertTrue(item["expected_answer"].strip())
            self.assertTrue(item["source"].startswith("http"))
            self.assertIsInstance(item["keywords"], list)
            self.assertGreaterEqual(len(item["keywords"]), 3)


class TestCalculateScore(unittest.TestCase):
    def test_full_match_scores_100(self):
        score, matched, missing = calculate_score(
            "Tokenization is splitting text into tokens",
            ["splitting", "text", "tokens"],
        )
        self.assertEqual(score, 100.0)
        self.assertEqual(len(matched), 3)
        self.assertEqual(missing, [])

    def test_partial_match(self):
        score, matched, missing = calculate_score(
            "A token is a unit of text",
            ["unit", "text", "word", "subword"],
        )
        self.assertEqual(score, 50.0)
        self.assertEqual(matched, ["unit", "text"])
        self.assertEqual(missing, ["word", "subword"])

    def test_no_match_scores_0(self):
        score, matched, missing = calculate_score("completely unrelated", ["tokens"])
        self.assertEqual(score, 0)
        self.assertEqual(matched, [])

    def test_case_insensitive(self):
        score, _, _ = calculate_score("TOKENS and Text", ["tokens", "text"])
        self.assertEqual(score, 100.0)

    def test_empty_keywords_scores_0(self):
        score, matched, missing = calculate_score("anything", [])
        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
