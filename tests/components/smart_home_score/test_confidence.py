"""Tests for the confidence thresholds and evaluation decisions."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest

from custom_components.smart_home_score.criteria.repository import CriteriaRepository
from custom_components.smart_home_score.engine.models import (
    CriterionStatus,
    InstallationSnapshot,
)
from custom_components.smart_home_score.engine.rules import (
    CONFIDENCE_AUTO_THRESHOLD,
    CONFIDENCE_PREFILL_THRESHOLD,
    RuleEngine,
)


class TestConfidencePolicy(unittest.TestCase):
    """Test suite for strict confidence policy enforcement."""

    def setUp(self):
        """Set up test repository and rule engine."""
        self.repo = CriteriaRepository(model_version="1.0")
        self.engine = RuleEngine(self.repo)

    def test_confidence_threshold_values(self):
        """Test confidence threshold constants adhere to specification (90% / 70%)."""
        self.assertEqual(CONFIDENCE_AUTO_THRESHOLD, 90.0)
        self.assertEqual(CONFIDENCE_PREFILL_THRESHOLD, 70.0)

    def test_insufficient_information_never_gives_auto_score(self):
        """Test that criteria with confidence < 90% are never marked AUTO_EVALUATED."""
        empty_snap = InstallationSnapshot()
        results = self.engine.evaluate_all(empty_snap)

        for cid, res in results.items():
            if res.confidence < CONFIDENCE_AUTO_THRESHOLD:
                self.assertNotEqual(
                    res.status,
                    CriterionStatus.AUTO_EVALUATED,
                    f"Criterion {cid} has confidence {res.confidence}% but marked AUTO_EVALUATED"
                )

    def test_temporary_unavailable_entities_does_not_break_evaluation(self):
        """Test that temporary unavailable entities do not destroy score calculation."""
        snap_with_unavailable = InstallationSnapshot(
            total_entities=100,
            unavailable_count=15,
            domains_present={"light", "sensor", "person"},
            has_grid_power_realtime=True,
            has_grid_energy_total=True,
        )
        results = self.engine.evaluate_all(snap_with_unavailable)
        # Should still detect energy reliably
        self.assertEqual(results["ENER01"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(results["ENER01"].proposed_score, 4)


if __name__ == "__main__":
    unittest.main()
