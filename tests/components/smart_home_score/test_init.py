"""Tests for the Smart Home Score integration setup and lifecycle."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.smart_home_score.const import (
    DOMAIN,
    MODEL_VERSION,
    NAME,
    VERSION,
)
from custom_components.smart_home_score.coordinator import SmartHomeScoreCoordinator
from custom_components.smart_home_score.engine.models import CriterionState, CriterionStatus
from custom_components.smart_home_score import (
    async_setup_entry,
    async_unload_entry,
    async_reload_entry,
)


class TestSmartHomeScoreLifecycle(unittest.IsolatedAsyncioTestCase):
    """Test suite for integration setup, update and unload."""

    async def test_coordinator_update_data_initial_and_recalc(self):
        """Test the coordinator computes real audit results from the engine."""
        hass_mock = MagicMock()
        hass_mock.states.async_all.return_value = []
        hass_mock.config_entries.async_entries.return_value = []
        coordinator = SmartHomeScoreCoordinator(hass_mock)
        coordinator.store.async_load = AsyncMock(return_value={})
        coordinator.store.async_save = AsyncMock(return_value=None)

        # Initial unpopulated state
        data = await coordinator._async_update_data()
        self.assertGreaterEqual(data.global_score, 0.0)
        self.assertTrue(data.is_provisional)
        self.assertEqual(data.total_count, 59)
        self.assertEqual(data.model_version, MODEL_VERSION)

        # Update a criterion
        await coordinator.async_submit_answer("ELEC02", "fully_protected")
        self.assertGreater(coordinator.data.global_score, 0.0)
        self.assertGreaterEqual(coordinator.data.evaluated_count, 1)

    async def test_setup_and_unload_entry(self):
        """Test successful setup and clean unload of config entry."""
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
        entry_mock.entry_id = "test_entry_123"

        with patch("custom_components.smart_home_score.coordinator.SmartHomeScoreStore.async_load", new_callable=AsyncMock) as mock_load:
            mock_load.return_value = {}
            # 1. Setup
            result = await async_setup_entry(hass_mock, entry_mock)
            self.assertTrue(result)
            self.assertIn(DOMAIN, hass_mock.data)
            self.assertIn("test_entry_123", hass_mock.data[DOMAIN])

            # 2. Unload
            unload_result = await async_unload_entry(hass_mock, entry_mock)
            self.assertTrue(unload_result)
            self.assertNotIn("test_entry_123", hass_mock.data[DOMAIN])


if __name__ == "__main__":
    unittest.main()
