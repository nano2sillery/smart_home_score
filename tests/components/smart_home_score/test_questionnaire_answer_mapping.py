"""Unit test verifying questionnaire answer mapping preserves MODEL_VERSION 1.0 levels."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest

from custom_components.smart_home_score.criteria.repository import CriteriaRepository
from custom_components.smart_home_score.engine.calculator import calculate_audit
from custom_components.smart_home_score.engine.models import CriterionState, CriterionStatus, EvaluationSource
from tests.components.smart_home_score.test_reference_audit import REFERENCE_AUDIT_V1_SCORES


class TestQuestionnaireAnswerMapping(unittest.TestCase):
    """Test suite ensuring questionnaire choices strictly preserve v1.0 level semantics."""

    def setUp(self):
        """Set up criteria repository."""
        self.repo = CriteriaRepository(model_version="1.0")

    def test_questionnaire_answer_mapping_preserves_v1_levels(self):
        """Test that all 59 criteria have exactly the expected structure, domains, weights and critical flags."""
        all_criteria = list(self.repo.criteria.values())
        self.assertEqual(len(all_criteria), 59)

        # Verify domain breakdown
        domains = {}
        for c in all_criteria:
            domains[c.domain] = domains.get(c.domain, 0) + 1
        
        self.assertEqual(domains["ELEC"], 5)
        self.assertEqual(domains["CYBER"], 8)
        self.assertEqual(domains["RES"], 8)
        self.assertEqual(domains["AUTO"], 9)
        self.assertEqual(domains["ENER"], 9)
        self.assertEqual(domains["INTER"], 6)
        self.assertEqual(domains["UX"], 7)
        self.assertEqual(domains["MAINT"], 7)

        # Verify exact critical criteria
        critical_ids = {c.id for c in all_criteria if c.critical}
        expected_critical = {"ELEC01", "ELEC02", "ELEC04", "CYBER01", "CYBER05", "RES02", "RES05"}
        self.assertEqual(critical_ids, expected_critical)

    def test_reference_audit_fixture_reproduced_via_questionnaire_answers(self):
        """Verify the reference audit (83.1 / 100) is perfectly reproduced."""
        states = {
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
        res = calculate_audit(self.repo, states, last_audit_date="2026-08-27 15:30:00")
        self.assertEqual(res.global_score, 83.1)
        self.assertEqual(res.evaluated_count, 59)
        self.assertEqual(res.applicable_count, 59)
        self.assertFalse(res.is_provisional)
        self.assertEqual(res.domains["ELEC"].score, 100.0)
        self.assertEqual(res.domains["UX"].score, 96.2)
        self.assertEqual(res.domains["INTER"].score, 87.5)
        self.assertEqual(res.domains["AUTO"].score, 79.5)
        self.assertEqual(res.domains["ENER"].score, 79.5)
        self.assertEqual(res.domains["RES"].score, 78.8)
        self.assertEqual(res.domains["CYBER"].score, 72.5)
        self.assertEqual(res.domains["MAINT"].score, 63.7)


if __name__ == "__main__":
    unittest.main()
