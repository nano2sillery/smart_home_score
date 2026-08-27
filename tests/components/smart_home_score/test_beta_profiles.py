"""Tests for Beta Community Profiles and Dispute Handling (v0.7.0 Bêta)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import json
import os
import unittest
from unittest.mock import AsyncMock, MagicMock

from custom_components.smart_home_score.coordinator import SmartHomeScoreCoordinator
from custom_components.smart_home_score.engine.models import CriterionStatus, EvaluationSource


class TestBetaProfilesAndDisputes(unittest.IsolatedAsyncioTestCase):
    """Test suite for beta house profiles, dispute mechanics, and anonymized diagnostic integrity."""

    def test_all_anonymized_profile_fixtures_load_correctly(self):
        """Test that all 6 representative beta profile fixtures exist and parse as valid JSON."""
        fixtures_dir = "/Users/LEFRANCC/HomeAssistant/tests/fixtures/profiles"
        expected_profiles = [
            "profile_minimal_apartment.json",
            "profile_zigbee_heavy.json",
            "profile_zwave_matter.json",
            "profile_solar_storage_resilient.json",
            "profile_cloud_heavy.json",
            "profile_highly_automated_villa.json",
        ]
        for prof_file in expected_profiles:
            path = os.path.join(fixtures_dir, prof_file)
            self.assertTrue(os.path.exists(path), f"Missing fixture {prof_file}")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIn("description", data)
                self.assertIn("total_entities", data)

    async def test_user_dispute_auto_evaluation_updates_score_and_retains_feedback(self):
        """Test user disputing an AUTO score updates effective score, retains auto evidence & marks for diagnostic."""
        hass_mock = MagicMock()
        hass_mock.data = {}
        coord = SmartHomeScoreCoordinator(hass_mock)
        await coord.async_init_store()

        # Simulate ELEC02 automatically evaluated at 2/4
        st = coord.criteria_states["ELEC02"]
        st.auto_score = 2
        st.effective_score = 2
        st.status = CriterionStatus.AUTO_EVALUATED
        st.evidence = "Detected 1 battery entity"

        # User disputes: real score is 4/4 with feedback
        await coord.async_dispute_auto_evaluation(
            criterion_id="ELEC02",
            user_score=4,
            feedback="J'ai en réalité un onduleur Schneider offline non détecté."
        )

        st_after = coord.criteria_states["ELEC02"]
        self.assertEqual(st_after.effective_score, 4)
        self.assertEqual(st_after.auto_score, 2)  # Original auto score preserved for diagnostics!
        self.assertTrue(st_after.disputed)
        self.assertEqual(st_after.dispute_feedback, "J'ai en réalité un onduleur Schneider offline non détecté.")
        self.assertEqual(st_after.evaluation_source, EvaluationSource.MANUAL)


if __name__ == "__main__":
    unittest.main()
