"""Tests for the Smart Home Score Advisor & Simulation Engine (v0.5.1)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest

from custom_components.smart_home_score.criteria.repository import CriteriaRepository
from custom_components.smart_home_score.engine.advisor import SmartHomeAdvisor
from custom_components.smart_home_score.engine.calculator import calculate_audit
from custom_components.smart_home_score.engine.models import (
    ActionType,
    CriterionState,
    CriterionStatus,
    DifficultyLevel,
)


class TestSmartHomeAdvisor(unittest.TestCase):
    """Test suite for recommendations, priorities, quick wins and simulations."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo = CriteriaRepository(model_version="1.0")
        self.advisor = SmartHomeAdvisor(self.repo)
        self.states: dict[str, CriterionState] = {
            cid: CriterionState(criterion_id=cid, effective_score=4, status=CriterionStatus.CONFIRMED)
            for cid in self.repo.criteria
        }

    def test_critical_risk_has_highest_priority(self):
        """Test a critical criterion at score 0 is assigned Priority 1 (CRITIQUE)."""
        self.states["ELEC02"].effective_score = 0  # Critical criterion
        self.states["CYBER02"].effective_score = 1 # Quick win
        self.states["RES06"].effective_score = 2   # Resilience

        recs = self.advisor.generate_recommendations(self.states)
        self.assertGreater(len(recs), 0)
        self.assertEqual(recs[0].criterion_id, "ELEC02")
        self.assertEqual(recs[0].priority, 1)
        self.assertEqual(recs[0].priority_label, "CRITIQUE")

    def test_res07_is_not_quick_win_and_is_advanced_test(self):
        """Test RES07 is classified as AVANCEE / TEST and NEVER as a Quick Win."""
        self.states["RES07"].effective_score = 1

        recs = self.advisor.generate_recommendations(self.states)
        rec_res07 = next(r for r in recs if r.criterion_id == "RES07")

        self.assertEqual(rec_res07.difficulty, DifficultyLevel.AVANCEE)
        self.assertEqual(rec_res07.action_type, ActionType.TEST)
        self.assertFalse(rec_res07.is_quick_win)

        # Confirm not in quick wins filter
        quick_wins = self.advisor.generate_recommendations(self.states, filter_quick_wins=True)
        self.assertNotIn("RES07", [qw.criterion_id for qw in quick_wins])

    def test_quick_wins_formal_rule(self):
        """Test Quick Wins combines FACILE, FAIBLE risk, not hardware/test, and exact_gain >= 0.3."""
        self.states["CYBER02"].effective_score = 1 # FACILE / CONFIGURATION -> Quick win
        self.states["ELEC01"].effective_score = 2  # AVANCEE / TEST -> NOT Quick win
        self.states["ENER04"].effective_score = 0  # AVANCEE / MATERIEL -> NOT Quick win

        quick_wins = self.advisor.generate_recommendations(self.states, filter_quick_wins=True)
        self.assertTrue(all(qw.is_quick_win for qw in quick_wins))
        self.assertTrue(all(qw.difficulty == DifficultyLevel.FACILE for qw in quick_wins))
        self.assertTrue(all(qw.action_type not in [ActionType.MATERIEL, ActionType.TEST] for qw in quick_wins))
        self.assertIn("CYBER02", [qw.criterion_id for qw in quick_wins])
        self.assertNotIn("ELEC01", [qw.criterion_id for qw in quick_wins])
        self.assertNotIn("ENER04", [qw.criterion_id for qw in quick_wins])

    def test_exact_mathematical_gain_calculation(self):
        """Test that recommendation gain equals exact difference produced by calculator."""
        self.states["CYBER02"].effective_score = 1
        initial_score = calculate_audit(self.repo, self.states).global_score

        recs = self.advisor.generate_recommendations(self.states)
        rec_cyber02 = next(r for r in recs if r.criterion_id == "CYBER02")

        # Simulate manually via calculator
        self.states["CYBER02"].effective_score = 4
        target_score = calculate_audit(self.repo, self.states).global_score
        expected_gain = round(target_score - initial_score, 2)

        self.assertEqual(rec_cyber02.exact_gain, expected_gain)

    def test_simulation_does_not_mutate_original_states(self):
        """Test simulation is pure and leaves original states completely untouched."""
        self.states["CYBER02"].effective_score = 1
        initial_cyber02_score = self.states["CYBER02"].effective_score

        sim_res = self.advisor.simulate_improvement(self.states, "CYBER02", 4)
        self.assertGreater(sim_res.exact_gain, 0.0)
        self.assertGreater(sim_res.simulated_global_score, sim_res.current_global_score)

        # Verify no state mutation
        self.assertEqual(self.states["CYBER02"].effective_score, initial_cyber02_score)

    def test_actions_tab_not_empty_when_score_below_100(self):
        """Test that whenever the global score is below 100, recommendations are NEVER empty."""
        # Scenario: real audit at 92.4 / 100 with 5 criteria not at 4/4
        self.states["AUTO04"].effective_score = 3
        self.states["ENER06"].effective_score = 2
        self.states["MAINT06"].effective_score = 3
        self.states["CYBER07"].effective_score = 2
        self.states["RES04"].effective_score = 3

        audit = calculate_audit(self.repo, self.states)
        self.assertLess(audit.global_score, 100.0)
        self.assertGreater(audit.potential_gain, 0.0)

        recs = self.advisor.generate_recommendations(self.states)
        self.assertGreater(len(recs), 0, "Recommendations list must NEVER be empty when score < 100")
        self.assertEqual(len(recs), 5)

        # Verify exact sum of potential gains matches potential_gain
        total_rec_gains = sum(r.exact_gain for r in recs)
        self.assertAlmostEqual(total_rec_gains, audit.potential_gain, delta=0.2)

    def test_action_rich_fields_populated(self):
        """Test that recommendations populate current_level_desc, target_level_desc and why_it_matters."""
        self.states["AUTO04"].effective_score = 3
        recs = self.advisor.generate_recommendations(self.states)
        rec = next(r for r in recs if r.criterion_id == "AUTO04")

        rec_dict = rec.to_dict()
        self.assertIn("current_level_desc", rec_dict)
        self.assertIn("target_level_desc", rec_dict)
        self.assertIn("why_it_matters", rec_dict)
        self.assertTrue(len(rec_dict["current_level_desc"]) > 0)
        self.assertTrue(len(rec_dict["target_level_desc"]) > 0)


if __name__ == "__main__":
    unittest.main()
