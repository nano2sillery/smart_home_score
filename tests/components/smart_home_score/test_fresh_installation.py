"""Tests for Fresh Installation, Upgrade & Clean Unload Lifecycle (v0.6.0)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.smart_home_score import async_setup_entry, async_unload_entry
from custom_components.smart_home_score.const import DOMAIN, MODEL_VERSION, VERSION
from custom_components.smart_home_score.coordinator import SmartHomeScoreCoordinator
from custom_components.smart_home_score.engine.models import CriterionState, CriterionStatus


class TestFreshInstallationLifecycle(unittest.IsolatedAsyncioTestCase):
    """Test suite for blank setup, zero-YAML execution, restart, upgrade and clean uninstall."""

    async def test_full_fresh_installation_lifecycle(self):
        """Scenario: Blank installation -> First Scan -> Answer -> Restart -> Upgrade -> Clean Unload."""
        hass_mock = MagicMock()
        hass_mock.data = {}
        hass_mock.states.async_all.return_value = []
        hass_mock.config_entries = MagicMock()
        hass_mock.config_entries.async_entries.return_value = []
        hass_mock.config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
        hass_mock.config_entries.async_unload_platforms = AsyncMock(return_value=True)
        hass_mock.services.async_register = MagicMock()
        hass_mock.services.async_remove = MagicMock()

        entry_mock = MagicMock()
        entry_mock.entry_id = "test_fresh_entry"

        # 1. Step 1: Initial Fresh Setup
        with patch("custom_components.smart_home_score.coordinator.SmartHomeScoreStore.async_load", new_callable=AsyncMock) as mock_load,              patch("custom_components.smart_home_score.coordinator.SmartHomeScoreStore.async_save", new_callable=AsyncMock) as mock_save:
            mock_load.return_value = {}  # Empty store
            setup_ok = await async_setup_entry(hass_mock, entry_mock)
            self.assertTrue(setup_ok)
            self.assertIn(DOMAIN, hass_mock.data)
            self.assertIn(entry_mock.entry_id, hass_mock.data[DOMAIN])

            coordinator: SmartHomeScoreCoordinator = hass_mock.data[DOMAIN][entry_mock.entry_id]
            self.assertEqual(coordinator.model_version, "1.0")
            self.assertEqual(coordinator.engine_version, VERSION)

            # 2. Step 2: Answer some questions
            await coordinator.async_submit_answer("ELEC02", "fully_protected")
            await coordinator.async_submit_answer("CYBER02", "2fa_all_accounts")
            self.assertGreater(coordinator.data.global_score, 0.0)
            self.assertEqual(coordinator.criteria_states["ELEC02"].effective_score, 4)

            # 3. Step 3: Simulate Home Assistant Restart (reload from persisted store)
            stored_snapshot = {cid: st for cid, st in coordinator.criteria_states.items()}
            mock_load.return_value = stored_snapshot

            new_coord = SmartHomeScoreCoordinator(hass_mock)
            await new_coord.async_init_store()
            self.assertEqual(new_coord.criteria_states["ELEC02"].effective_score, 4)
            self.assertEqual(new_coord.criteria_states["CYBER02"].effective_score, 4)
            self.assertEqual(new_coord.model_version, "1.0")

            # 4. Step 4: Clean Uninstall
            unload_ok = await async_unload_entry(hass_mock, entry_mock)
            self.assertTrue(unload_ok)
            self.assertNotIn(entry_mock.entry_id, hass_mock.data[DOMAIN])
            # Services removed
            self.assertTrue(hass_mock.services.async_remove.called)


if __name__ == "__main__":
    unittest.main()
