"""Tests for the Criteria Repository."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest

from custom_components.smart_home_score.criteria.repository import CriteriaRepository


class TestCriteriaRepository(unittest.TestCase):
    """Test suite for criteria repository."""

    def setUp(self):
        """Set up test repository."""
        self.repo = CriteriaRepository(model_version="1.0")

    def test_repository_counts(self):
        """Test repository loads exactly 59 criteria across 8 domains."""
        self.assertEqual(len(self.repo.criteria), 59)
        self.assertEqual(len(self.repo.domains), 8)

    def test_domain_weights_sum(self):
        """Test global domain weights sum to exactly 100."""
        total_dom_weight = sum(d["weight"] for d in self.repo.domains.values())
        self.assertEqual(total_dom_weight, 100)

    def test_internal_criteria_weights_sum(self):
        """Test criteria internal weights sum to exactly 100% per domain."""
        for dom_code, dom_cfg in self.repo.domains.items():
            crits = self.repo.get_domain_criteria(dom_code)
            internal_sum = sum(c.weight for c in crits)
            self.assertEqual(internal_sum, 100, f"Domain {dom_code} weights sum to {internal_sum}, expected 100")

    def test_criteria_levels_and_recommendations(self):
        """Test all 59 criteria have definitions for levels 0-4 and recommendations."""
        for cid, c_def in self.repo.criteria.items():
            self.assertEqual(set(c_def.levels.keys()), {"0", "1", "2", "3", "4"}, f"Incomplete levels in {cid}")
            self.assertEqual(set(c_def.recommendations.keys()), {"0_to_1", "1_to_2", "2_to_3", "3_to_4"}, f"Incomplete recs in {cid}")
            self.assertTrue(len(c_def.question) > 10, f"Missing question in {cid}")


if __name__ == "__main__":
    unittest.main()
