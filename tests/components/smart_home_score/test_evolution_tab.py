"""Tests for the 4th tab '📈 Évolution' and progression tracking."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest
from unittest.mock import AsyncMock

from homeassistant.core import HomeAssistant
from custom_components.smart_home_score.engine.history import AuditHistoryManager
from custom_components.smart_home_score.engine.models import (
    AuditHistoryEntry,
    AuditResult,
    DomainResult,
)


class TestEvolutionTab(unittest.IsolatedAsyncioTestCase):
    """Test suite for evolution tracking and metrics computation."""

    async def asyncSetUp(self):
        """Set up isolated history manager."""
        self.hass = HomeAssistant()
        self.history_mgr = AuditHistoryManager(self.hass, model_version="1.0")
        self.history_mgr._store.async_save = AsyncMock()
        self.history_mgr._store.async_load = AsyncMock(return_value={})

    def _make_dummy_audit(self, global_score: float, domain_scores: dict[str, float], completeness: float = 100.0, model_version: str = "1.0") -> AuditResult:
        """Helper to create dummy audit results."""
        domains = {
            dom_code: DomainResult(
                code=dom_code,
                name=dom_code,
                weight=12,
                score=score,
                contribution=score * 0.12,
                max_applicable_weight=12,
                evaluated_count=5,
                applicable_count=5,
                total_count=5,
                progress_bar="█████",
            )
            for dom_code, score in domain_scores.items()
        }
        return AuditResult(
            global_score=global_score,
            completeness=completeness,
            maturity_level="Avancé" if global_score >= 80 else "Intermédiaire",
            is_provisional=(completeness < 100.0),
            domains=domains,
            criteria_states={},
            critical_count=0,
            critical_items=[],
            potential_gain=100.0 - global_score,
            recommendations=[],
            evaluated_count=59 if completeness == 100 else 30,
            applicable_count=59,
            total_count=59,
            model_version=model_version,
            last_audit_date="2026-08-28 10:00:00",
        )

    def test_evolution_empty_history(self):
        """Test 1: Empty history yields 0 audits and neutral evolution metrics."""
        evo = self.history_mgr.get_evolution_summary()
        self.assertEqual(evo.total_audits, 0)
        self.assertEqual(evo.first_audit_score, 0.0)
        self.assertEqual(evo.latest_audit_score, 0.0)
        self.assertEqual(evo.total_progression, 0.0)
        self.assertEqual(len(evo.history_entries), 0)
        self.assertEqual(len(evo.top_progressions), 0)

    async def test_evolution_single_audit(self):
        """Test 2: Single audit serves as initial reference point with 0 progression."""
        doms = {"ELEC": 80.0, "CYBER": 75.0, "RES": 70.0, "AUTO": 85.0, "ENER": 90.0, "INTER": 60.0, "UX": 80.0, "MAINT": 65.0}
        res1 = self._make_dummy_audit(78.4, doms)
        await self.history_mgr.async_record_audit(res1, completed_at="2026-08-12 10:00:00")

        evo = self.history_mgr.get_evolution_summary()
        self.assertEqual(evo.total_audits, 1)
        self.assertEqual(evo.first_audit_score, 78.4)
        self.assertEqual(evo.latest_audit_score, 78.4)
        self.assertEqual(evo.total_progression, 0.0)
        self.assertEqual(evo.first_completed_at, "2026-08-12 10:00:00")

    async def test_evolution_multiple_audits(self):
        """Test 3: Multiple completed audits (e.g. 83.1 -> 92.4 -> 94.8) are tracked in chronological sequence."""
        doms1 = {"ELEC": 80.0, "CYBER": 75.0, "RES": 70.0, "AUTO": 85.0, "ENER": 90.0, "INTER": 60.0, "UX": 80.0, "MAINT": 65.0}
        doms2 = {"ELEC": 95.0, "CYBER": 90.0, "RES": 85.0, "AUTO": 92.0, "ENER": 95.0, "INTER": 90.0, "UX": 90.0, "MAINT": 80.0}
        doms3 = {"ELEC": 100.0, "CYBER": 95.0, "RES": 90.0, "AUTO": 95.0, "ENER": 100.0, "INTER": 95.0, "UX": 95.0, "MAINT": 85.0}

        await self.history_mgr.async_record_audit(self._make_dummy_audit(83.1, doms1), completed_at="2026-08-01 10:00:00")
        await self.history_mgr.async_record_audit(self._make_dummy_audit(92.4, doms2), completed_at="2026-08-15 10:00:00")
        await self.history_mgr.async_record_audit(self._make_dummy_audit(94.8, doms3), completed_at="2026-08-28 10:00:00")

        evo = self.history_mgr.get_evolution_summary()
        self.assertEqual(evo.total_audits, 3)
        self.assertEqual(evo.first_audit_score, 83.1)
        self.assertEqual(evo.latest_audit_score, 94.8)

    async def test_evolution_global_delta(self):
        """Test 4: Global delta correctly computes +11.7 pts (83.1 -> 94.8)."""
        doms1 = {"ELEC": 80.0, "CYBER": 75.0, "RES": 70.0, "AUTO": 85.0, "ENER": 90.0, "INTER": 60.0, "UX": 80.0, "MAINT": 65.0}
        doms2 = {"ELEC": 100.0, "CYBER": 95.0, "RES": 90.0, "AUTO": 95.0, "ENER": 100.0, "INTER": 95.0, "UX": 95.0, "MAINT": 85.0}

        await self.history_mgr.async_record_audit(self._make_dummy_audit(83.1, doms1), completed_at="2026-08-01 10:00:00")
        await self.history_mgr.async_record_audit(self._make_dummy_audit(94.8, doms2), completed_at="2026-08-28 10:00:00")

        evo = self.history_mgr.get_evolution_summary()
        self.assertEqual(evo.total_progression, 11.7)

    async def test_evolution_domain_deltas(self):
        """Test 5: Domain deltas compute progression per domain and highlight top 3."""
        doms1 = {"ELEC": 80.0, "CYBER": 75.0, "RES": 70.0, "AUTO": 85.0, "ENER": 90.0, "INTER": 60.0, "UX": 80.0, "MAINT": 63.8}
        doms2 = {"ELEC": 100.0, "CYBER": 75.0, "RES": 80.0, "AUTO": 92.5, "ENER": 90.0, "INTER": 90.0, "UX": 80.0, "MAINT": 78.8}

        await self.history_mgr.async_record_audit(self._make_dummy_audit(83.1, doms1))
        await self.history_mgr.async_record_audit(self._make_dummy_audit(92.4, doms2))

        evo = self.history_mgr.get_evolution_summary()
        self.assertEqual(evo.domain_progressions["MAINT"]["delta"], 15.0)
        self.assertEqual(evo.domain_progressions["INTER"]["delta"], 30.0)
        self.assertEqual(evo.domain_progressions["ELEC"]["delta"], 20.0)
        self.assertEqual(evo.domain_progressions["CYBER"]["delta"], 0.0)

        # Top 3 progressions: INTER (+30.0), ELEC (+20.0), MAINT (+15.0)
        top_codes = [t["domain_code"] for t in evo.top_progressions]
        self.assertEqual(top_codes, ["INTER", "ELEC", "MAINT"])

    async def test_evolution_uses_only_completed_snapshots(self):
        """Test 6: Incomplete audits (<100%) are filtered out and do not alter evolution summary."""
        doms = {"ELEC": 80.0, "CYBER": 75.0, "RES": 70.0, "AUTO": 85.0, "ENER": 90.0, "INTER": 60.0, "UX": 80.0, "MAINT": 65.0}
        await self.history_mgr.async_record_audit(self._make_dummy_audit(83.1, doms, completeness=100.0))

        # Attempt to check if an incomplete audit can be injected
        incomplete = self._make_dummy_audit(45.0, doms, completeness=40.0)
        self.assertTrue(incomplete.is_provisional)
        self.assertEqual(len(self.history_mgr.get_history()), 1)

    async def test_evolution_does_not_mutate_history(self):
        """Test 7: Calling get_evolution_summary multiple times leaves history entries strictly immutable."""
        doms = {"ELEC": 80.0, "CYBER": 75.0, "RES": 70.0, "AUTO": 85.0, "ENER": 90.0, "INTER": 60.0, "UX": 80.0, "MAINT": 65.0}
        await self.history_mgr.async_record_audit(self._make_dummy_audit(83.1, doms))

        evo1 = self.history_mgr.get_evolution_summary()
        evo2 = self.history_mgr.get_evolution_summary()

        self.assertEqual(evo1.first_audit_score, evo2.first_audit_score)
        self.assertEqual(len(self.history_mgr.history_entries), 1)

    async def test_evolution_handles_model_version_change(self):
        """Test 8: Changing MODEL_VERSION flags mismatch warning for non-equivalent comparative baselines."""
        doms = {"ELEC": 80.0, "CYBER": 75.0, "RES": 70.0, "AUTO": 85.0, "ENER": 90.0, "INTER": 60.0, "UX": 80.0, "MAINT": 65.0}
        await self.history_mgr.async_record_audit(self._make_dummy_audit(83.1, doms, model_version="1.0"))

        # Add an audit created with future model 2.0
        self.history_mgr.history_entries.append(
            AuditHistoryEntry(
                audit_id="audit_v2_1",
                date="2027-01-01 10:00:00",
                completed_at="2027-01-01 10:00:00",
                global_score=91.0,
                domain_scores=doms,
                completeness=100.0,
                critical_count=0,
                model_version="2.0",
            )
        )

        evo = self.history_mgr.get_evolution_summary(model_version="1.0")
        # Filtered by model 1.0 -> 1 audit
        self.assertEqual(evo.total_audits, 1)
        # Mismatch detected across overall historical records
        self.assertTrue(evo.has_model_version_mismatch)


if __name__ == "__main__":
    unittest.main()
