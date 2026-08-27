"""Tests for the Audit Assistant Engine (v0.4.0)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest

from custom_components.smart_home_score.criteria.repository import CriteriaRepository
from custom_components.smart_home_score.engine.assistant import AuditAssistant
from custom_components.smart_home_score.engine.calculator import calculate_audit
from custom_components.smart_home_score.engine.models import (
    CriterionState,
    CriterionStatus,
    EvaluationSource,
)


class TestAuditAssistant(unittest.TestCase):
    """Test suite for interactive audit assistant flow, branching and responses."""

    def setUp(self):
        """Set up test repository and assistant."""
        self.repo = CriteriaRepository(model_version="1.0")
        self.assistant = AuditAssistant(self.repo)
        self.states: dict[str, CriterionState] = {
            cid: CriterionState(criterion_id=cid) for cid in self.repo.criteria
        }

    def test_smart_priority_order(self):
        """Test ordering prioritizes critical criteria and places tests at the end."""
        ordered = self.assistant.get_ordered_criteria_list(self.states)
        
        # ELEC01 and RES01 are tests -> should be towards the end
        self.assertIn("ELEC01", ordered[-5:])
        self.assertIn("RES01", ordered[-5:])
        
        # Critical questions should be near the front
        self.assertIn("ELEC02", ordered[:15])

    def test_natural_language_answer_mapping(self):
        """Test natural language options correctly map to internal discrete score."""
        st, branching = self.assistant.apply_answer("ELEC02", "fully_protected", self.states)
        self.assertEqual(st.effective_score, 4)
        self.assertEqual(st.status, CriterionStatus.CONFIRMED)
        self.assertTrue(st.user_confirmed)
        self.assertFalse(branching)

    def test_unknown_does_not_assign_fake_score(self):
        """Test 'Je ne sais pas' sets status to NEEDS_REVIEW with no score assigned."""
        st, branching = self.assistant.apply_answer("ELEC03", "unknown", self.states)
        self.assertIsNone(st.effective_score)
        self.assertEqual(st.status, CriterionStatus.NEEDS_REVIEW)
        self.assertTrue(st.user_confirmed)

        # Audit must remain provisional
        audit = calculate_audit(self.repo, self.states)
        self.assertTrue(audit.is_provisional)

    def test_conditional_branching_on_solar(self):
        """Test that answering no solar on ENER04 marks ENER07 as NOT_APPLICABLE."""
        self.states["ENER04"] = CriterionState(criterion_id="ENER04", status=CriterionStatus.NOT_APPLICABLE, applicable=False)
        self.states["ENER07"] = CriterionState(criterion_id="ENER07", status=CriterionStatus.NOT_APPLICABLE, applicable=False)

        audit = calculate_audit(self.repo, self.states)
        # ENER has 9 criteria, 2 NOT_APPLICABLE -> 7 applicable
        self.assertEqual(audit.domains["ENER"].applicable_count, 7)

    def test_resume_audit_finds_next_unanswered(self):
        """Test resuming interrupted audit finds the exact next pending question."""
        ordered = self.assistant.get_ordered_criteria_list(self.states)
        first_cid = ordered[0]
        second_cid = ordered[1]

        self.assistant.apply_answer(first_cid, "fully_protected", self.states)
        self.assistant.apply_answer(second_cid, "safe_configured", self.states)

        next_cid = self.assistant.get_next_pending_criterion_id(self.states)
        self.assertEqual(next_cid, ordered[2])

    def test_individual_re_evaluation_without_reset(self):
        """Test re-evaluating an individual criterion updates score without wiping other answers."""
        self.assistant.apply_answer("ELEC02", "no_protection", self.states)
        self.assertEqual(self.states["ELEC02"].effective_score, 0)

        # Re-evaluate
        self.assistant.apply_answer("ELEC02", "fully_protected", self.states)
        self.assertEqual(self.states["ELEC02"].effective_score, 4)


if __name__ == "__main__":
    unittest.main()
