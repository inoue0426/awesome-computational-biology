import datetime as dt
import unittest
from unittest.mock import patch

from scripts import weekly_resource_discovery as w


class WeeklyDiscoveryTests(unittest.TestCase):
    def article(self):
        return {
            "title": "A single-cell drug perturbation benchmark for cancer",
            "abstractText": "Data and code are available at https://github.com/example/sc-benchmark.",
            "doi": "10.1234/test2026",
            "journalTitle": "Nature Methods",
            "firstPublicationDate": "2026-11-10",
        }

    def test_extracts_verified_source_metadata(self):
        c = w.extract_candidate(self.article())
        self.assertEqual(c["category"], "dataset")
        self.assertEqual(c["url"], "https://github.com/example/sc-benchmark")
        self.assertIn("10.1234/test2026", c["description"])

    def test_does_not_accept_unlinked_repo(self):
        article = self.article()
        article["abstractText"] = "Code will be available later."
        self.assertIsNone(w.extract_candidate(article))

    def test_skips_reviews_and_non_biology(self):
        self.assertIsNone(w.classify("A systematic review of genomics databases"))
        self.assertIsNone(w.classify("A benchmark for database indexing algorithms"))

    def test_deduplication(self):
        data = "- [Prior paper](https://github.com/example/sc-benchmark) — Existing.\n"
        names, repos = w.existing_resources(data)
        self.assertIn("https://github.com/example/sc-benchmark", repos)

    def test_insertion_uses_known_section(self):
        original = "### General Biological ML & Knowledge Graph Benchmarks\n\n- [Old](https://example.org) — Existing.\n"
        c = w.extract_candidate(self.article())
        result = w.add_resources(original, [c])
        self.assertIn(c["url"], result)
        self.assertEqual(result.count(c["url"]), 1)

    def test_never_accepts_ambiguous_repo_or_nonpublic_repo(self):
        self.assertIsNone(w.normalize_repo("https://github.com/topics/biomedicine"))
        with patch.object(w, "fetch_json", return_value={
            "full_name": "example/sc-benchmark",
            "archived": False,
            "disabled": False,
            "private": True,
        }):
            self.assertFalse(w.verify_repo("https://github.com/example/sc-benchmark"))

    def test_no_addition_when_all_candidates_are_already_listed(self):
        article = self.article()
        listing = {"resultList": {"result": [article]}}
        old = "- [Old](https://github.com/example/sc-benchmark) — Existing.\n"
        with patch.object(w, "fetch_json", return_value=listing):
            self.assertEqual(w.discover(dt.date(2026, 11, 16), old), [])


if __name__ == "__main__":
    unittest.main()
