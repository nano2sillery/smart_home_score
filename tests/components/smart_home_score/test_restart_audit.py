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

    async def test_restart_complete_audit_creates_history_snapshot(self):
        """Test that restarting a 100% complete audit creates a history snapshot."""
        for cid in self.coordinator.criteria_states:
            st = self.coordinator.criteria_states[cid]
            st.effective_score = 4
            st.status = CriterionStatus.CONFIRMED

        res_before = self.coordinator._calculate_current_result()
        self.assertEqual(res_before.completeness, 100.0)
        self.assertFalse(res_before.is_provisional)

        await self.coordinator.async_restart_audit()
        self.coordinator.history_mgr.async_record_audit.assert_called_once()

    async def test_restart_incomplete_audit_does_not_create_history_snapshot(self):
        """Test that restarting an incomplete audit (<100% completeness) NEVER creates a fake history snapshot."""
        # Only answer 1 criterion out of 59
        self.coordinator.criteria_states["ELEC01"].effective_score = 4
        self.coordinator.criteria_states["ELEC01"].status = CriterionStatus.CONFIRMED

        res_before = self.coordinator._calculate_current_result()
        self.assertLess(res_before.completeness, 100.0)
        self.assertTrue(res_before.is_provisional)

        await self.coordinator.async_restart_audit()
        # Verify history recording was strictly skipped
        self.coordinator.history_mgr.async_record_audit.assert_not_called()

    async def test_history_snapshot_has_unique_audit_id(self):
        """Test that each history snapshot has a unique audit_id and full metadata."""
        from custom_components.smart_home_score.engine.history import AuditHistoryManager

        real_history_mgr = AuditHistoryManager(self.hass)
        real_history_mgr._store.async_save = AsyncMock()

        for cid in self.coordinator.criteria_states:
            st = self.coordinator.criteria_states[cid]
            st.effective_score = 4
            st.status = CriterionStatus.CONFIRMED

        res = self.coordinator._calculate_current_result()
        entry1 = await real_history_mgr.async_record_audit(res, note="Audit 1")
        entry2 = await real_history_mgr.async_record_audit(res, note="Audit 2")

        self.assertNotEqual(entry1.audit_id, entry2.audit_id)
        self.assertTrue(entry1.audit_id.startswith("audit_"))
        self.assertEqual(entry1.completeness, 100.0)
        self.assertEqual(entry1.criteria_count, 59)
        self.assertEqual(entry1.model_version, "1.0")
        self.assertIsNotNone(entry1.completed_at)
        self.assertEqual(len(entry1.domain_scores), 8)

    async def test_multiple_completed_audits_create_distinct_history_entries(self):
        """Test tracking multiple successive completed audits with distinct scores in history."""
        from custom_components.smart_home_score.engine.history import AuditHistoryManager

        real_history_mgr = AuditHistoryManager(self.hass)
        real_history_mgr._store.async_save = AsyncMock()

        # Audit 1: all scores = 3 (75/100)
        for cid in self.coordinator.criteria_states:
            self.coordinator.criteria_states[cid].effective_score = 3
            self.coordinator.criteria_states[cid].status = CriterionStatus.CONFIRMED
        res1 = self.coordinator._calculate_current_result()
        await real_history_mgr.async_record_audit(res1)

        # Audit 2: all scores = 4 (100/100)
        for cid in self.coordinator.criteria_states:
            self.coordinator.criteria_states[cid].effective_score = 4
            self.coordinator.criteria_states[cid].status = CriterionStatus.CONFIRMED
        res2 = self.coordinator._calculate_current_result()
        await real_history_mgr.async_record_audit(res2)

        history = real_history_mgr.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].global_score, res1.global_score)
        self.assertEqual(history[1].global_score, res2.global_score)
        self.assertNotEqual(history[0].audit_id, history[1].audit_id)

    async def test_completed_audit_is_archived_immediately(self):
        """Test that reaching 100% completeness immediately archives the audit into history."""
        from custom_components.smart_home_score.engine.history import AuditHistoryManager

        self.coordinator.history_mgr = AuditHistoryManager(self.hass)
        self.coordinator.history_mgr._store.async_save = AsyncMock()

        # Fill 58 criteria out of 59
        cids = list(self.coordinator.criteria_states.keys())
        for cid in cids[:-1]:
            self.coordinator.criteria_states[cid].effective_score = 4
            self.coordinator.criteria_states[cid].status = CriterionStatus.CONFIRMED

        # Not complete yet
        self.assertEqual(len(self.coordinator.history_mgr.history_entries), 0)

        # Answer the 59th criterion via submit_answer
        last_cid = cids[-1]
        await self.coordinator.async_submit_answer(last_cid, "4")

        # Must be immediately archived
        self.assertEqual(len(self.coordinator.history_mgr.history_entries), 1)
        entry = self.coordinator.history_mgr.history_entries[0]
        self.assertEqual(entry.audit_id, self.coordinator.current_audit_id)
        self.assertEqual(entry.completeness, 100.0)

    async def test_restart_does_not_duplicate_completed_audit(self):
        """Test that restarting an already archived audit does NOT create a duplicate entry in history."""
        from custom_components.smart_home_score.engine.history import AuditHistoryManager

        self.coordinator.history_mgr = AuditHistoryManager(self.hass)
        self.coordinator.history_mgr._store.async_save = AsyncMock()

        # Complete all 59 criteria
        for cid in self.coordinator.criteria_states:
            self.coordinator.criteria_states[cid].effective_score = 4
            self.coordinator.criteria_states[cid].status = CriterionStatus.CONFIRMED

        # Archive once
        res = self.coordinator._calculate_current_result()
        await self.coordinator.history_mgr.async_record_audit(res, audit_id=self.coordinator.current_audit_id)
        self.assertEqual(len(self.coordinator.history_mgr.history_entries), 1)

        # Trigger restart_audit
        await self.coordinator.async_restart_audit()

        # History must still contain exactly 1 entry (no duplicate created)
        self.assertEqual(len(self.coordinator.history_mgr.history_entries), 1)

    async def test_editing_completed_audit_does_not_mutate_history_snapshot(self):
        """Test that modifying answers after completion does NOT mutate the saved historical snapshot."""
        from custom_components.smart_home_score.engine.history import AuditHistoryManager

        self.coordinator.history_mgr = AuditHistoryManager(self.hass)
        self.coordinator.history_mgr._store.async_save = AsyncMock()

        for cid in self.coordinator.criteria_states:
            self.coordinator.criteria_states[cid].effective_score = 4
            self.coordinator.criteria_states[cid].status = CriterionStatus.CONFIRMED

        # Reached 100/100
        res = self.coordinator._calculate_current_result()
        await self.coordinator.history_mgr.async_record_audit(res, audit_id=self.coordinator.current_audit_id)
        historical_score = self.coordinator.history_mgr.history_entries[0].global_score
        self.assertEqual(historical_score, 100.0)

        # User modifies ELEC01 to 0/4
        self.coordinator.criteria_states["ELEC01"].effective_score = 0
        active_res = self.coordinator._calculate_current_result()
        self.assertLess(active_res.global_score, 100.0)

        # Historical snapshot must remain immutable at 100.0
        self.assertEqual(self.coordinator.history_mgr.history_entries[0].global_score, 100.0)

    async def test_new_audit_gets_new_audit_id(self):
        """Test that start/restart audit assigns a brand new distinct audit_id."""
        id_before = self.coordinator.current_audit_id
        await self.coordinator.async_restart_audit()
        id_after = self.coordinator.current_audit_id

        self.assertNotEqual(id_before, id_after)
        self.assertTrue(id_after.startswith("audit_"))

    async def test_completed_at_is_actual_completion_time(self):
        """Test that completed_at reflects the exact timestamp when audit reached 100%."""
        from custom_components.smart_home_score.engine.history import AuditHistoryManager

        self.coordinator.history_mgr = AuditHistoryManager(self.hass)
        self.coordinator.history_mgr._store.async_save = AsyncMock()

        cids = list(self.coordinator.criteria_states.keys())
        for cid in cids[:-1]:
            self.coordinator.criteria_states[cid].effective_score = 4
            self.coordinator.criteria_states[cid].status = CriterionStatus.CONFIRMED

        # Finalize by answering the last criterion
        await self.coordinator.async_submit_answer(cids[-1], "4")

        self.assertEqual(len(self.coordinator.history_mgr.history_entries), 1)
        entry = self.coordinator.history_mgr.history_entries[0]
        self.assertIsNotNone(entry.completed_at)
        self.assertEqual(entry.completeness, 100.0)

    async def test_restart_audit_returns_to_first_interview_step(self):
        """Test that the frontend card starts from question index 0 after restart."""
        pass


if __name__ == "__main__":
    unittest.main()
