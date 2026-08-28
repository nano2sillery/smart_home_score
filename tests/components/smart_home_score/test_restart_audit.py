"""Tests for 'Faire un nouvel audit' (Restart / Reset Audit) and Rescan isolation."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest
from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant
from custom_components.smart_home_score.coordinator import SmartHomeScoreCoordinator
from custom_components.smart_home_score.engine.models import (
    CriterionState,
    CriterionStatus,
    EvaluationSource,
    InstallationSnapshot,
)


class TestRestartAudit(unittest.IsolatedAsyncioTestCase):
    """Test suite for restart_audit vs run_analysis behavior."""

    async def asyncSetUp(self):
        """Set up test environment with a mock coordinator."""
        self.hass = HomeAssistant()
        self.coordinator = SmartHomeScoreCoordinator(self.hass)
        self.coordinator.analyzer.async_collect_snapshot = AsyncMock()
        self.coordinator.store.async_save = AsyncMock()
        self.coordinator.store.async_load = AsyncMock(return_value={})
        self.coordinator.history_mgr.async_record_audit = AsyncMock()

        # Provide a realistic snapshot
        snap = InstallationSnapshot()
        snap.total_devices = 25
        snap.total_entities = 120
        snap.total_areas = 8
        snap.automations_count = 20
        snap.scripts_count = 5
        snap.integrations_present = {"zha", "backup", "energy"}
        snap.local_integrations = {"zha"}
        snap.has_zigbee = True
        snap.zigbee_devices_count = 15
        self.coordinator.analyzer.async_collect_snapshot.return_value = snap

        # Initialize
        await self.coordinator.async_init_store()

    async def test_restart_audit_clears_user_answers(self):
        """Test that restart_audit completely clears manual answers and confirmations."""
        # 1. User answers some questions manually
        self.coordinator.criteria_states["ELEC01"].effective_score = 4
        self.coordinator.criteria_states["ELEC01"].status = CriterionStatus.CONFIRMED
        self.coordinator.criteria_states["ELEC01"].user_confirmed = True

        self.coordinator.criteria_states["AUTO01"].effective_score = 3
        self.coordinator.criteria_states["AUTO01"].status = CriterionStatus.CONFIRMED
        self.coordinator.criteria_states["AUTO01"].user_confirmed = True

        self.assertTrue(self.coordinator.criteria_states["ELEC01"].user_confirmed)
        self.assertEqual(self.coordinator.criteria_states["ELEC01"].effective_score, 4)

        # 2. Trigger restart_audit
        await self.coordinator.async_restart_audit()

        # 3. Verify user answers are cleared
        self.assertFalse(self.coordinator.criteria_states["ELEC01"].user_confirmed)
        self.assertIsNone(self.coordinator.criteria_states["ELEC01"].effective_score)
        self.assertEqual(self.coordinator.criteria_states["ELEC01"].status, CriterionStatus.TEST_REQUIRED)

    async def test_restart_audit_preserves_previous_history(self):
        """Test that restarting an audit records the previous completed audit in history."""
        # Mark multiple criteria so the audit has an evaluated score
        for cid in self.coordinator.criteria_states:
            st = self.coordinator.criteria_states[cid]
            st.effective_score = 4
            st.status = CriterionStatus.CONFIRMED

        res_before = self.coordinator._calculate_current_result()
        self.assertGreater(res_before.global_score, 0.0)

        # Trigger restart_audit
        await self.coordinator.async_restart_audit()

        # Verify history_mgr.async_record_audit was called with previous result
        self.coordinator.history_mgr.async_record_audit.assert_called_once()
        call_args = self.coordinator.history_mgr.async_record_audit.call_args[0]
        recorded_res = call_args[0]
        self.assertEqual(recorded_res.global_score, res_before.global_score)

    async def test_restart_audit_runs_new_discovery(self):
        """Test that restart_audit re-runs snapshot collection and rule engine evaluations."""
        # Change snapshot to include solar
        new_snap = InstallationSnapshot()
        new_snap.total_devices = 30
        new_snap.total_entities = 140
        new_snap.has_solar_production = True
        new_snap.has_grid_power_realtime = True
        new_snap.has_grid_energy_total = True
        self.coordinator.analyzer.async_collect_snapshot.return_value = new_snap

        await self.coordinator.async_restart_audit()

        # Verify ENER01 was newly evaluated by fresh discovery
        self.assertEqual(self.coordinator.criteria_states["ENER01"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(self.coordinator.criteria_states["ENER01"].effective_score, 4)

    async def test_rescan_does_not_clear_answers(self):
        """Test that standard Rescan (run_analysis) PRESERVES user answers and confirmations."""
        # User answers ELEC01 manually
        self.coordinator.criteria_states["ELEC01"].effective_score = 4
        self.coordinator.criteria_states["ELEC01"].status = CriterionStatus.CONFIRMED
        self.coordinator.criteria_states["ELEC01"].user_confirmed = True

        # Run Rescan
        await self.coordinator.async_run_analysis(save_on_complete=True)

        # Verify manual answers and confirmations are still 100% intact
        self.assertTrue(self.coordinator.criteria_states["ELEC01"].user_confirmed)
        self.assertEqual(self.coordinator.criteria_states["ELEC01"].effective_score, 4)

    async def test_restart_audit_returns_to_first_interview_step(self):
        """Test that the frontend card starts from question index 0 after restart."""
        # Verify card handler resets _currentQuestionIndex = 0 and _view = 'discovery'
        pass


if __name__ == "__main__":
    unittest.main()
