"""Tests for the official reference audit fixture (Test K)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest

from custom_components.smart_home_score.criteria.repository import CriteriaRepository
from custom_components.smart_home_score.engine.calculator import calculate_audit
from custom_components.smart_home_score.engine.models import CriterionState, CriterionStatus, EvaluationSource

REFERENCE_AUDIT_V1_SCORES = {
    # ELEC (5)
    "ELEC01": 4, "ELEC02": 4, "ELEC03": 4, "ELEC04": 4, "ELEC05": 4,
    # CYBER (8)
    "CYBER01": 4, "CYBER02": 1, "CYBER03": 4, "CYBER04": 4,
    "CYBER05": 4, "CYBER06": 3, "CYBER07": 2, "CYBER08": 1,
    # RES (8)
    "RES01": 4, "RES02": 4, "RES03": 4, "RES04": 4,
    "RES05": 4, "RES06": 2, "RES07": 1, "RES08": 2,
    # AUTO (9)
    "AUTO01": 3, "AUTO02": 2, "AUTO03": 4, "AUTO04": 3,
    "AUTO05": 2, "AUTO06": 4, "AUTO07": 4, "AUTO08": 3, "AUTO09": 4,
    # ENER (9)
    "ENER01": 4, "ENER02": 4, "ENER03": 4, "ENER04": 4,
    "ENER05": 3, "ENER06": 2, "ENER07": 2, "ENER08": 4, "ENER09": 2,
    # INTER (6)
    "INTER01": 4, "INTER02": 3, "INTER03": 3, "INTER04": 4,
    "INTER05": 3, "INTER06": 4,
    # UX (7)
    "UX01": 4, "UX02": 4, "UX03": 4, "UX04": 4,
    "UX05": 4, "UX06": 4, "UX07": 3,
    # MAINT (7)
    "MAINT01": 3, "MAINT02": 2, "MAINT03": 3, "MAINT04": 3,
    "MAINT05": 4, "MAINT06": 2, "MAINT07": 1
}


class TestReferenceAudit(unittest.TestCase):
    """Test suite for reference house audit fixture (non-regression test)."""

    def setUp(self):
        """Set up test repository and reference fixture."""
        self.repo = CriteriaRepository(model_version="1.0")
        self.states = {
            cid: CriterionState(
                criterion_id=cid,
                status=CriterionStatus.CONFIRMED,
                effective_score=score,
                evaluation_source=EvaluationSource.MANUAL,
                confidence=100.0,
                user_confirmed=True
            )
            for cid, score in REFERENCE_AUDIT_V1_SCORES.items()
        }

    def test_k_reference_audit_exact_score(self):
        """Test K: Official house fixture produces exactly 83.1 / 100 and identical domain scores."""
        result = calculate_audit(self.repo, self.states, last_audit_date="2026-08-27 15:30:00")

        # 1. Global Metrics
        self.assertEqual(result.evaluated_count, 59)
        self.assertEqual(result.applicable_count, 59)
        self.assertEqual(result.total_count, 59)
        self.assertEqual(result.completeness, 100.0)
        self.assertFalse(result.is_provisional)
        self.assertEqual(result.critical_count, 0)
        self.assertEqual(result.maturity_level, "Très avancé")

        # 2. Exact Global Score
        self.assertEqual(result.global_score, 83.1)

        # 3. Exact 8 Domain Scores matching YAML reference
        expected_domains = {
            "ELEC": {"score": 100.0, "contribution": 15.00, "weight": 15},
            "UX": {"score": 96.2, "contribution": 9.62, "weight": 10},
            "INTER": {"score": 87.5, "contribution": 8.75, "weight": 10},
            "AUTO": {"score": 79.5, "contribution": 11.93, "weight": 15},
            "ENER": {"score": 79.5, "contribution": 11.93, "weight": 15},
            "RES": {"score": 78.8, "contribution": 11.81, "weight": 15},
            "CYBER": {"score": 72.5, "contribution": 10.88, "weight": 15},
            "MAINT": {"score": 63.7, "contribution": 3.19, "weight": 5},
        }

        for dom_code, expected in expected_domains.items():
            dom_res = result.domains[dom_code]
            self.assertEqual(dom_res.score, expected["score"], f"Domain {dom_code} score mismatch")
            self.assertAlmostEqual(dom_res.contribution, expected["contribution"], places=1, msg=f"Domain {dom_code} contrib mismatch")
            self.assertEqual(dom_res.weight, expected["weight"])

        # 4. Improvement Potential
        self.assertAlmostEqual(result.potential_gain, 16.9, places=1)
        self.assertTrue(len(result.recommendations) > 0)
        self.assertIn(result.recommendations[0].criterion_id, ["CYBER02", "RES07"])


if __name__ == "__main__":
    unittest.main()
