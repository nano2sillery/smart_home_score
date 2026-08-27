"""Tests for the Home Assistant Analyzer."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest
from unittest.mock import MagicMock

from custom_components.smart_home_score.engine.analyzer import HomeAssistantAnalyzer
from custom_components.smart_home_score.engine.models import InstallationSnapshot


class TestHomeAssistantAnalyzer(unittest.IsolatedAsyncioTestCase):
    """Test suite for the Home Assistant environment analyzer."""

    async def test_analyzer_collects_snapshot_cleanly(self):
        """Test collecting a snapshot with mocked registries."""
        hass = MagicMock()
        hass.states.async_all.return_value = []
        hass.config_entries.async_entries.return_value = []

        analyzer = HomeAssistantAnalyzer(hass)
        snapshot = await analyzer.async_collect_snapshot()

        self.assertIsInstance(snapshot, InstallationSnapshot)
        self.assertEqual(snapshot.total_entities, 0)
        self.assertFalse(snapshot.has_zigbee)


if __name__ == "__main__":
    unittest.main()
