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

    async def async_record_audit(self, audit_result: AuditResult, note: str = "") -> AuditHistoryEntry:
        """Record an audit summary entry without saving heavy snapshots."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry_id = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

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
        _LOGGER.info("Recorded audit history entry %s (Score: %.1f)", entry_id, entry.global_score)
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

        first_score = entries[0].global_score
        latest_score = entries[-1].global_score
        progression = round(latest_score - first_score, 1)

        return EvolutionSummary(
            total_audits=len(entries),
            first_audit_score=first_score,
            latest_audit_score=latest_score,
            total_progression=progression,
            history_entries=entries,
        )
