"""Audit History & Progression Tracking Manager (v0.5.0)."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .models import (
    AuditHistoryEntry,
    AuditResult,
    EvolutionSummary,
)

_LOGGER = logging.getLogger(__name__)

HISTORY_STORAGE_KEY = "smart_home_score_history"
HISTORY_STORAGE_VERSION = 1


class AuditHistoryManager:
    """Manages audit snapshots over time and computes score evolution."""

    def __init__(self, hass: HomeAssistant, model_version: str = "1.0") -> None:
        """Initialize history manager."""
        self.hass = hass
        self.model_version = model_version
        self._store = Store[dict[str, Any]](hass, HISTORY_STORAGE_VERSION, HISTORY_STORAGE_KEY)
        self.history_entries: list[AuditHistoryEntry] = []

    async def async_load(self) -> list[AuditHistoryEntry]:
        """Load history entries from persistent storage."""
        data = await self._store.async_load()
        if data and isinstance(data, dict):
            raw_entries = data.get("entries", [])
            self.history_entries = [
                AuditHistoryEntry.from_dict(entry) for entry in raw_entries
            ]
        return self.history_entries

    def has_entry(self, audit_id: str) -> bool:
        """Check if an audit_id is already recorded in history."""
        return any(e.audit_id == audit_id for e in self.history_entries)

    async def async_record_audit(
        self,
        audit_result: AuditResult,
        audit_id: str | None = None,
        completed_at: str | None = None,
        note: str = "",
    ) -> AuditHistoryEntry:
        """Record an audit summary entry upon completion without duplicating."""
        now_str = completed_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry_id = audit_id or f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        # Prevent duplicate recording of the exact same audit_id
        for existing in self.history_entries:
            if existing.audit_id == entry_id:
                _LOGGER.debug("Audit %s already archived in history, skipping duplicate", entry_id)
                return existing

        domain_scores = {
            dom_code: dom_res.score for dom_code, dom_res in audit_result.domains.items()
        }

        entry = AuditHistoryEntry(
            audit_id=entry_id,
            date=now_str,
            completed_at=now_str,
            global_score=audit_result.global_score,
            domain_scores=domain_scores,
            completeness=audit_result.completeness,
            critical_count=audit_result.critical_count,
            critical_risks=audit_result.critical_count,
            criteria_count=audit_result.total_count if audit_result.total_count else 59,
            model_version=audit_result.model_version,
            note=note,
        )

        self.history_entries.append(entry)
        await self._store.async_save({
            "model_version": self.model_version,
            "entries": [e.to_dict() for e in self.history_entries],
        })
        _LOGGER.info("Recorded official audit history entry %s (Score: %.1f, Completed: %s)", entry_id, entry.global_score, now_str)
        return entry

    def get_history(self, model_version: str | None = None) -> list[AuditHistoryEntry]:
        """Get history entries filtered by model version (default 1.0)."""
        target_version = model_version or self.model_version
        return [e for e in self.history_entries if e.model_version == target_version]

    def get_evolution_summary(self, model_version: str | None = None) -> EvolutionSummary:
        """Calculate evolution progression metrics."""
        entries = self.get_history(model_version)
        if not entries:
            return EvolutionSummary(
                total_audits=0,
                first_audit_score=0.0,
                latest_audit_score=0.0,
                total_progression=0.0,
                history_entries=[],
            )

        first = entries[0]
        latest = entries[-1]
        first_score = first.global_score
        latest_score = latest.global_score
        progression = round(latest_score - first_score, 1)

        domain_names = {
            "ELEC": "⚡ Sécurité électrique",
            "CYBER": "🔒 Cybersécurité",
            "RES": "🛡️ Résilience",
            "AUTO": "⚙️ Automatisations",
            "ENER": "☀️ Énergie",
            "INTER": "🔌 Interopérabilité",
            "UX": "📱 Expérience / UX",
            "MAINT": "🛠️ Maintenance",
        }

        domain_progressions: dict[str, dict[str, Any]] = {}
        all_dom_deltas: list[dict[str, Any]] = []

        for dom_code, dom_name in domain_names.items():
            f_val = first.domain_scores.get(dom_code, 0.0)
            l_val = latest.domain_scores.get(dom_code, 0.0)
            d_val = round(l_val - f_val, 1)
            domain_progressions[dom_code] = {
                "name": dom_name,
                "first": f_val,
                "latest": l_val,
                "delta": d_val,
                "is_positive": d_val > 0,
                "is_neutral": d_val == 0,
            }
            if d_val > 0:
                all_dom_deltas.append({
                    "domain_code": dom_code,
                    "domain_name": dom_name,
                    "delta": d_val,
                })

        # Top 3 progressions sorted descending
        all_dom_deltas.sort(key=lambda x: x["delta"], reverse=True)
        top_progressions = all_dom_deltas[:3]

        all_models = {e.model_version for e in self.history_entries}
        has_mismatch = len(all_models) > 1

        return EvolutionSummary(
            total_audits=len(entries),
            first_audit_score=first_score,
            latest_audit_score=latest_score,
            total_progression=progression,
            history_entries=entries,
            first_completed_at=first.completed_at or first.date,
            latest_completed_at=latest.completed_at or latest.date,
            domain_progressions=domain_progressions,
            top_progressions=top_progressions,
            has_model_version_mismatch=has_mismatch,
        )
