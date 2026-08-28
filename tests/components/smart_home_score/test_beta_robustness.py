"""Robustness, Performance, Recovery and Privacy Verification for Beta External Release."""
import tests.components.smart_home_score.conftest  # noqa: F401
import time
import unittest
from unittest.mock import AsyncMock, MagicMock

from homeassistant.core import HomeAssistant
from custom_components.smart_home_score.const import DOMAIN, MODEL_VERSION, VERSION
from custom_components.smart_home_score.coordinator import SmartHomeScoreCoordinator
from custom_components.smart_home_score.diagnostics import (
    async_get_config_entry_diagnostics,
    sanitize_diagnostic_text,
)
from custom_components.smart_home_score.engine.analyzer import InstallationSnapshot
from custom_components.smart_home_score.engine.models import (
    CriterionState,
    CriterionStatus,
    EvaluationSource,
)
from custom_components.smart_home_score.engine.store import SmartHomeScoreStore


class TestBetaRobustness(unittest.IsolatedAsyncioTestCase):
    """Deep robustness validation suite for external beta preparation."""

    async def asyncSetUp(self):
        """Set up test environment."""
        self.hass = HomeAssistant()
        self.coordinator = SmartHomeScoreCoordinator(self.hass)
        self.coordinator.analyzer.async_collect_snapshot = AsyncMock(
            return_value=InstallationSnapshot(
                total_entities=100,
                total_devices=20,
                total_areas=5,
                integrations_present={"zigbee", "matter", "backup"},
                automations_count=10,
                scripts_count=2,
            )
        )
        self.coordinator.store.async_save = AsyncMock()
        self.coordinator.store.async_load = AsyncMock(return_value={})
        self.coordinator.history_mgr._store.async_save = AsyncMock()
        self.coordinator.history_mgr._store.async_load = AsyncMock(return_value={})
        await self.coordinator.async_init_store()

    async def test_store_upgrade_from_legacy_data(self):
        """1. Test that store safely loads legacy data structures without error."""
        legacy_data = {
            "criteria": {
                "ELEC01": {
                    "criterion_id": "ELEC01",
                    "status": "CONFIRMED",
                    "effective_score": 4,
                    # Missing new fields (confidence, evidence_type, reason_if_not_auto)
                }
            }
        }
        store = SmartHomeScoreStore(self.hass)
        store._store.async_load = AsyncMock(return_value=legacy_data)
        loaded = await store.async_load()

        self.assertIn("ELEC01", loaded)
        self.assertEqual(loaded["ELEC01"].effective_score, 4)
        self.assertEqual(loaded["ELEC01"].status, CriterionStatus.CONFIRMED)

    async def test_session_recovery_after_restart(self):
        """2. Test restoring interview session after unexpected restart or interruption."""
        # Answer 5 criteria
        for cid in ["ELEC01", "CYBER01", "RES01", "AUTO01", "ENER01"]:
            await self.coordinator.async_submit_answer(cid, "4")

        # Simulate browser refresh / HA restart
        saved_states = self.coordinator.criteria_states
        fresh_coordinator = SmartHomeScoreCoordinator(self.hass)
        fresh_coordinator.store.async_load = AsyncMock(return_value=saved_states)
        fresh_coordinator.history_mgr._store.async_load = AsyncMock(return_value={})
        fresh_coordinator.analyzer.async_collect_snapshot = AsyncMock(return_value=self.coordinator.last_snapshot)
        await fresh_coordinator.async_init_store()

        self.assertEqual(fresh_coordinator.criteria_states["ELEC01"].effective_score, 4)
        self.assertEqual(fresh_coordinator.criteria_states["CYBER01"].effective_score, 4)

    async def test_resilience_to_store_save_failure(self):
        """3. Test that unexpected store failure does not crash coordinator or stop audit."""
        real_store = SmartHomeScoreStore(self.hass)
        real_store._store.async_save = AsyncMock(side_effect=IOError("Simulated disk error"))

        # Must not raise exception
        await real_store.async_save(self.coordinator.criteria_states)

    async def test_resilience_to_analyzer_glitch(self):
        """4. Test that analyzer glitch retains previous valid states without halting."""
        self.coordinator.analyzer.async_collect_snapshot = AsyncMock(side_effect=RuntimeError("Transient HA error"))
        # Must execute cleanly and return valid current result
        res = await self.coordinator.async_run_analysis(save_on_complete=False)
        self.assertIsNotNone(res)
        self.assertEqual(len(self.coordinator.criteria_states), 59)

    async def test_large_scale_performance_5000_entities(self):
        """5. Stress test with 5,000 entities, 500 devices, 300 automations."""
        large_snapshot = InstallationSnapshot(
            total_entities=5000,
            total_devices=500,
            total_areas=40,
            integrations_present={"zigbee", "matter", "zwave", "backup", "enphase_envoy", "hue"},
            automations_count=300,
            scripts_count=50,
            has_zigbee=True,
            zigbee_devices_count=120,
            has_matter=True,
            has_zwave=True,
        )

        start_time = time.perf_counter()
        evaluations = self.coordinator.rule_engine.evaluate_all(large_snapshot)
        recs = self.coordinator.advisor.generate_recommendations(self.coordinator.criteria_states)
        calc_res = self.coordinator._calculate_current_result()
        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # Entire evaluation across 59 criteria + advisor + calculator must take < 150ms
        self.assertLess(duration_ms, 150.0, f"Analysis took too long: {duration_ms:.2f} ms")
        self.assertEqual(len(evaluations), 59)
        self.assertIsNotNone(calc_res)

    def test_diagnostics_sanitization_redacts_all_pii(self):
        """6. Validate 100% local privacy and zero leak of secrets, IP, MAC, paths or emails."""
        raw_text = (
            "Connected to Envoy at 192.168.1.55 with MAC 00:11:22:33:44:55. "
            "Admin email: test.user@example.com, config file /config/custom_components/secret.yaml. "
            "SSID: MySecretWifi_5G."
        )
        sanitized = sanitize_diagnostic_text(raw_text)

        self.assertNotIn("192.168.1.55", sanitized)
        self.assertNotIn("00:11:22:33:44:55", sanitized)
        self.assertNotIn("test.user@example.com", sanitized)
        self.assertNotIn("/config/custom_components/secret.yaml", sanitized)
        self.assertNotIn("MySecretWifi_5G", sanitized)

    async def test_config_entry_diagnostics_anonymity(self):
        """7. Test async_get_config_entry_diagnostics produces complete, anonymous report."""
        entry = MagicMock()
        entry.entry_id = "test_entry_123"
        self.hass.data = {DOMAIN: {entry.entry_id: self.coordinator}}

        diag = await async_get_config_entry_diagnostics(self.hass, entry)

        self.assertEqual(diag["integration_version"], VERSION)
        self.assertEqual(diag["model_version"], MODEL_VERSION)
        self.assertEqual(diag["author"], "Cyrille LEFRANC")
        self.assertIn("audit_summary", diag)
        self.assertIn("criteria", diag)
        self.assertIn("domains", diag)


if __name__ == "__main__":
    unittest.main()
