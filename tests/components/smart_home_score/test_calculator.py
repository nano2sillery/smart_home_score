"""Tests for the independent scoring calculator (Tests A to J)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest

from custom_components.smart_home_score.criteria.repository import CriteriaRepository
from custom_components.smart_home_score.engine.calculator import calculate_audit, get_maturity_level
from custom_components.smart_home_score.engine.models import CriterionState, CriterionStatus, EvaluationSource


class TestScoringCalculator(unittest.TestCase):
    """Test suite for pure mathematical scoring engine."""

    def setUp(self):
        """Set up test repository."""
        self.repo = CriteriaRepository(model_version="1.0")

    def test_a_all_not_evaluated(self):
        """Test A: 59 criteria NOT_EVALUATED -> Score 0.0, Completeness 0.0%, is_provisional True, no crash."""
        states = {
            cid: CriterionState(criterion_id=cid, status=CriterionStatus.NOT_EVALUATED)
            for cid in self.repo.criteria
        }
        result = calculate_audit(self.repo, states)
        self.assertEqual(result.global_score, 0.0)
        self.assertEqual(result.completeness, 0.0)
        self.assertTrue(result.is_provisional)
        self.assertEqual(result.evaluated_count, 0)
        self.assertEqual(result.applicable_count, 59)
        self.assertEqual(result.total_count, 59)
        self.assertEqual(result.critical_count, 0)
        self.assertEqual(result.maturity_level, "Insuffisant")

    def test_b_single_criterion_evaluated(self):
        """Test B: 1 criterion evaluated (ELEC01 = 4/4) -> exact contribution."""
        states = {
            cid: CriterionState(criterion_id=cid, status=CriterionStatus.NOT_EVALUATED)
            for cid in self.repo.criteria
        }
        # ELEC01 has weight 20 in ELEC (weight 15) -> contribution = (20/100)*15 = 3.0 pts
        states["ELEC01"] = CriterionState(
            criterion_id="ELEC01",
            status=CriterionStatus.CONFIRMED,
            effective_score=4,
            evaluation_source=EvaluationSource.TEST
        )
        result = calculate_audit(self.repo, states)
        self.assertEqual(result.global_score, 3.0)
        self.assertEqual(result.evaluated_count, 1)
        self.assertEqual(result.domains["ELEC"].score, 20.0)
        self.assertEqual(result.domains["ELEC"].contribution, 3.0)
        self.assertTrue(result.is_provisional)

    def test_c_all_criteria_perfect(self):
        """Test C: All criteria at 4/4 -> Global Score 100.0 / 100, Completeness 100.0%, Exceptionnel."""
        states = {
            cid: CriterionState(criterion_id=cid, status=CriterionStatus.CONFIRMED, effective_score=4)
            for cid in self.repo.criteria
        }
        result = calculate_audit(self.repo, states)
        self.assertEqual(result.global_score, 100.0)
        self.assertEqual(result.completeness, 100.0)
        self.assertFalse(result.is_provisional)
        self.assertEqual(result.maturity_level, "Exceptionnel")
        self.assertEqual(result.potential_gain, 0.0)
        self.assertEqual(len(result.recommendations), 0)

    def test_d_not_applicable_renormalisation(self):
        """Test D: NOT_APPLICABLE criteria are excluded and weights properly renormalised without penalty."""
        states = {
            cid: CriterionState(criterion_id=cid, status=CriterionStatus.CONFIRMED, effective_score=4)
            for cid in self.repo.criteria
        }
        # Set ENER04 (Production locale, weight 10 in ENER) to NOT_APPLICABLE
        states["ENER04"] = CriterionState(
            criterion_id="ENER04",
            status=CriterionStatus.NOT_APPLICABLE,
            applicable=False
        )
        result = calculate_audit(self.repo, states)
        # All remaining applicable criteria are at 4, so domain score and global score must still be 100.0!
        self.assertEqual(result.domains["ENER"].score, 100.0)
        self.assertEqual(result.global_score, 100.0)
        self.assertEqual(result.applicable_count, 58)
        self.assertEqual(result.evaluated_count, 58)
        self.assertEqual(result.completeness, 100.0)

    def test_e_critical_risk_at_zero(self):
        """Test E: Critical criterion at 0/4 is immediately flagged as a critical risk."""
        states = {
            cid: CriterionState(criterion_id=cid, status=CriterionStatus.CONFIRMED, effective_score=4)
            for cid in self.repo.criteria
        }
        # ELEC01 is critical
        states["ELEC01"] = CriterionState(
            criterion_id="ELEC01",
            status=CriterionStatus.CONFIRMED,
            effective_score=0
        )
        result = calculate_audit(self.repo, states)
        self.assertEqual(result.critical_count, 1)
        self.assertIn("ELEC01", result.critical_items)
        # ELEC01 should be the #1 priority recommendation
        self.assertEqual(result.recommendations[0].criterion_id, "ELEC01")
        self.assertEqual(result.recommendations[0].priority, 1)

    def test_f_incomplete_audit_is_provisional(self):
        """Test F: When evaluated < applicable -> is_provisional = True."""
        states = {
            cid: CriterionState(criterion_id=cid, status=CriterionStatus.CONFIRMED, effective_score=4)
            for cid in self.repo.criteria
        }
        states["MAINT07"] = CriterionState(criterion_id="MAINT07", status=CriterionStatus.NOT_EVALUATED)
        result = calculate_audit(self.repo, states)
        self.assertTrue(result.is_provisional)
        self.assertLess(result.completeness, 100.0)

    def test_g_complete_audit_not_provisional(self):
        """Test G: When evaluated == applicable -> is_provisional = False."""
        states = {
            cid: CriterionState(criterion_id=cid, status=CriterionStatus.CONFIRMED, effective_score=3)
            for cid in self.repo.criteria
        }
        result = calculate_audit(self.repo, states)
        self.assertFalse(result.is_provisional)
        self.assertEqual(result.completeness, 100.0)

    def test_h_domain_internal_weights_sum_to_100(self):
        """Test H: Each domain internal weights sum to 100%."""
        for dom_code in self.repo.domains:
            crits = self.repo.get_domain_criteria(dom_code)
            self.assertEqual(sum(c.weight for c in crits), 100)

    def test_i_global_domain_weights_sum_to_100(self):
        """Test I: Sum of 8 domain global weights equals 100."""
        self.assertEqual(sum(d["weight"] for d in self.repo.domains.values()), 100)

    def test_j_global_score_bounded_between_0_and_100(self):
        """Test J: Global score is strictly bounded in [0.0, 100.0]."""
        # Min
        states_min = {cid: CriterionState(criterion_id=cid, effective_score=0) for cid in self.repo.criteria}
        result_min = calculate_audit(self.repo, states_min)
        self.assertEqual(result_min.global_score, 0.0)

        # Max
        states_max = {cid: CriterionState(criterion_id=cid, effective_score=4) for cid in self.repo.criteria}
        result_max = calculate_audit(self.repo, states_max)
        self.assertEqual(result_max.global_score, 100.0)


if __name__ == "__main__":
    unittest.main()
