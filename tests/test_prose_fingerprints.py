from pathlib import Path
import importlib.util
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "prose_fingerprints.py"
SPEC = importlib.util.spec_from_file_location("prose_fingerprints", MODULE_PATH)
assert SPEC and SPEC.loader
prose_fingerprints = importlib.util.module_from_spec(SPEC)
sys.modules["prose_fingerprints"] = prose_fingerprints
SPEC.loader.exec_module(prose_fingerprints)
detect_negative_positive_restatement = prose_fingerprints.detect_negative_positive_restatement


class NegativePositiveRestatementTests(unittest.TestCase):
    def test_detects_adjacent_sentence_restatement(self):
        text = "This is not a productivity trick. It is a new operating model for teams."
        findings = detect_negative_positive_restatement(text)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].pattern_id, "negative-positive-restatement")
        self.assertEqual(findings[0].kind, "not_x_it_is_y")

    def test_detects_not_about_about_frame(self):
        text = "The goal is not about replacing judgment. The goal is about putting judgment in the right place."
        findings = detect_negative_positive_restatement(text)
        self.assertTrue(any(item.kind == "not_about_about" for item in findings))

    def test_detects_not_just_but_frame(self):
        text = "It is not just a checklist, but a complete operating model."
        findings = detect_negative_positive_restatement(text)
        self.assertTrue(any(item.kind == "not_just_but" for item in findings))

    def test_allows_specific_contrast_without_immediate_positive_restating(self):
        text = "The job did not finish because the database was unavailable. The retry queue preserved the failed work item."
        self.assertEqual(detect_negative_positive_restatement(text), [])


if __name__ == "__main__":
    unittest.main()
