"""Tests for Audit History & Evolution Progression (v0.5.1)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest
from unittest.mock import AsyncMock, MagicMock

from custom_components.smart_home_score.criteria.repository import CriteriaRepository
from custom_components.smart_home_score.engine.calculator import calculate_audit
from custom_components.smart_home_score.engine.history import AuditHistoryManager
from custom_components.smart_home_score.engine.models import (
    AuditHistoryEntry,
    CriterionState,
    CriterionStatus,
)


class TestAuditHistory(unittest.IsolatedAsyncioTestCase):
    """Test suite for audit history records, evolution tracking and version filtering."""

    async def test_multiple_successive_audits_evolution(self):
        """Test tracking progression across successive audits (ex: 78.4 -> 81.2 -> 83.1 = +4.7 pts)."""
        hass_mock = MagicMock()
        mgr = AuditHistoryManager(hass_mock, model_version="1.0")
        mgr._store.async_save = MagicMock()

        # Manually create 3 successive entries
        mgr.history_entries = [
            AuditHistoryEntry("audit_1", "2026-01-01", 78.4, {}, 100.0, 0, "1.0"),
            AuditHistoryEntry("audit_2", "2026-02-01", 81.2, {}, 100.0, 0, "1.0"),
            AuditHistoryEntry("audit_3", "2026-03-01", 83.1, {}, 100.0, 0, "1.0"),
        ]

        summary = mgr.get_evolution_summary(model_version="1.0")
        self.assertEqual(summary.total_audits, 3)
        self.assertEqual(summary.first_audit_score, 78.4)
        self.assertEqual(summary.latest_audit_score, 83.1)
        self.assertEqual(summary.total_progression, 4.7)

    async def test_history_not_created_on_simple_reload(self):
        """Test that initializing or reloading history manager does NOT generate spurious entries."""
        hass_mock = MagicMock()
        mgr = AuditHistoryManager(hass_mock, model_version="1.0")
        mgr._store.async_load = AsyncMock(return_value={"entries": []})
        
        entries = await mgr.async_load()
        self.assertEqual(len(entries), 0)
        self.assertEqual(len(mgr.history_entries), 0)

    async def test_model_version_isolation(self):
        """Test that an audit created with model 1.0 is strictly isolated from future model versions."""
        hass_mock = MagicMock()
        mgr = AuditHistoryManager(hass_mock, model_version="1.0")
        mgr._store.async_save = MagicMock()

        mgr.history_entries = [
            AuditHistoryEntry("audit_v1_0", "2026-01-01", 83.1, {}, 100.0, 0, "1.0"),
            AuditHistoryEntry("audit_v1_1", "2026-06-01", 85.0, {}, 100.0, 0, "1.1"),
        ]

        entries_v1 = mgr.get_history(model_version="1.0")
        self.assertEqual(len(entries_v1), 1)
        self.assertEqual(entries_v1[0].audit_id, "audit_v1_0")

        entries_v2 = mgr.get_history(model_version="1.1")
        self.assertEqual(len(entries_v2), 1)
        self.assertEqual(entries_v2[0].audit_id, "audit_v1_1")


if __name__ == "__main__":
    unittest.main()
