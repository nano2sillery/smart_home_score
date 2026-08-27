"""Tests for the Smart Home Score Store."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest
from unittest.mock import AsyncMock, MagicMock

from custom_components.smart_home_score.engine.models import CriterionState, CriterionStatus, EvaluationSource
from custom_components.smart_home_score.engine.store import SmartHomeScoreStore


class TestSmartHomeScoreStore(unittest.IsolatedAsyncioTestCase):
    """Test suite for persistence store."""

    async def test_store_save_and_load(self):
        """Test saving and loading criteria states via store."""
        hass_mock = MagicMock()
        store = SmartHomeScoreStore(hass_mock, model_version="1.0")

        # Mock the underlying HA Store
        saved_payload = {}
        async def mock_save(data):
            nonlocal saved_payload
            saved_payload = data
        async def mock_load():
            return saved_payload

        store._store.async_save = mock_save
        store._store.async_load = mock_load

        # 1. Save states
        test_states = {
            "ELEC01": CriterionState(
                criterion_id="ELEC01",
                status=CriterionStatus.CONFIRMED,
                effective_score=4,
                evaluation_source=EvaluationSource.TEST,
                confidence=100.0,
                evidence="Test evidence"
            )
        }
        await store.async_save(test_states, last_audit_date="2026-08-27")

        self.assertEqual(saved_payload["schema_version"], 1)
        self.assertEqual(saved_payload["model_version"], "1.0")
        self.assertIn("ELEC01", saved_payload["criteria"])

        # 2. Load states
        loaded_states = await store.async_load()
        self.assertIn("ELEC01", loaded_states)
        self.assertEqual(loaded_states["ELEC01"].effective_score, 4)
        self.assertEqual(loaded_states["ELEC01"].status, CriterionStatus.CONFIRMED)
        self.assertEqual(loaded_states["ELEC01"].evidence, "Test evidence")


if __name__ == "__main__":
    unittest.main()
