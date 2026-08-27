"""Tests for Change Tracking, Transient vs Structural Drift (v0.5.1)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest

from custom_components.smart_home_score.criteria.repository import CriteriaRepository
from custom_components.smart_home_score.engine.models import (
    CriterionState,
    CriterionStatus,
    InstallationSnapshot,
)
from custom_components.smart_home_score.engine.rules import RuleEngine
from custom_components.smart_home_score.engine.tracker import ChangeTracker


class TestChangeDetection(unittest.TestCase):
    """Test suite for observable environment change detection without confusing health and maturity."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo = CriteriaRepository(model_version="1.0")
        self.rule_engine = RuleEngine(self.repo)
        self.tracker = ChangeTracker(self.rule_engine)

    def test_solar_temporarily_unavailable_leaves_maturity_unchanged(self):
        """Test transient entity outage (Envoy down 10 min) does NOT degrade maturity score or trigger review."""
        current_states = {
            "ENER04": CriterionState(
                criterion_id="ENER04",
                effective_score=4,
                user_confirmed=True,
                status=CriterionStatus.CONFIRMED,
                evidence="Production solaire active.",
            )
        }

        # Snapshot with transient outage
        outage_snapshot = InstallationSnapshot(
            has_solar_production=False,
            unavailable_count=1,
        )

        updated_states, flagged_ids = self.tracker.detect_changes_and_update(
            current_states, outage_snapshot, is_transient_outage=True
        )
        self.assertEqual(len(flagged_ids), 0)
        self.assertEqual(updated_states["ENER04"].effective_score, 4)
        self.assertEqual(updated_states["ENER04"].status, CriterionStatus.CONFIRMED)
        self.assertFalse(updated_states["ENER04"].needs_review)

    def test_solar_restored_leaves_maturity_unchanged(self):
        """Test return to available state maintains confirmed maturity without review."""
        current_states = {
            "ENER04": CriterionState(
                criterion_id="ENER04",
                effective_score=4,
                user_confirmed=True,
                status=CriterionStatus.CONFIRMED,
                evidence="Production solaire active.",
            )
        }

        restored_snapshot = InstallationSnapshot(
            has_solar_production=True,
            solar_power_entity="sensor.envoy_production",
        )

        updated_states, flagged_ids = self.tracker.detect_changes_and_update(
            current_states, restored_snapshot, is_transient_outage=False
        )
        self.assertEqual(len(flagged_ids), 0)
        self.assertEqual(updated_states["ENER04"].effective_score, 4)

    def test_solar_integration_structurally_removed_triggers_needs_review(self):
        """Test structural removal of an integration flags the criterion for review without overwriting."""
        current_states = {
            "ENER04": CriterionState(
                criterion_id="ENER04",
                effective_score=4,
                user_confirmed=True,
                status=CriterionStatus.CONFIRMED,
                evidence="Production solaire active.",
            )
        }

        # Structural removal: Solar integration completely removed from registries
        structural_snapshot = InstallationSnapshot(
            has_solar_production=False,
            integrations_present={"zha", "backup"},
        )

        updated_states, flagged_ids = self.tracker.detect_changes_and_update(
            current_states, structural_snapshot, is_transient_outage=False
        )
        self.assertIn("ENER04", flagged_ids)
        self.assertEqual(updated_states["ENER04"].status, CriterionStatus.NEEDS_REVIEW)
        self.assertTrue(updated_states["ENER04"].needs_review)
        self.assertEqual(updated_states["ENER04"].previous_score, 4)
        self.assertIn("Changement structurel détecté", updated_states["ENER04"].needs_review_reason)


if __name__ == "__main__":
    unittest.main()
