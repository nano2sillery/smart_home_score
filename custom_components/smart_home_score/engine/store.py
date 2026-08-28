"""Persistence manager for Smart Home Score using Home Assistant Store."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .models import CriterionState

_LOGGER = logging.getLogger(__name__)

STORAGE_KEY = "smart_home_score_data"
STORAGE_VERSION = 1


class SmartHomeScoreStore:
    """Manage persistent storage of Smart Home Score audit data."""

    def __init__(self, hass: HomeAssistant, model_version: str = "1.0") -> None:
        """Initialize the storage helper."""
        self.hass = hass
        self.model_version = model_version
        self._store = Store[dict[str, Any]](hass, STORAGE_VERSION, STORAGE_KEY)
        self._data: dict[str, Any] = {}

    async def async_load(self) -> dict[str, CriterionState]:
        """Load stored criteria states safely."""
        try:
            stored = await self._store.async_load()
            if not stored:
                _LOGGER.debug("No existing Smart Home Score store found, starting fresh")
                return {}

            self._data = stored
            criteria_raw = stored.get("criteria", {})
            states: dict[str, CriterionState] = {}
            for cid, c_dict in criteria_raw.items():
                states[cid] = CriterionState.from_dict(c_dict)

            return states
        except Exception as err:
            _LOGGER.error("Error loading Smart Home Score persistent store, starting with safe defaults: %s", err)
            return {}

    async def async_save(
        self,
        criteria_states: dict[str, CriterionState],
        last_audit_date: str | None = None,
        history_snapshot: dict[str, Any] | None = None,
    ) -> None:
        """Save criteria states and audit history safely."""
        try:
            criteria_dict = {cid: state.to_dict() for cid, state in criteria_states.items()}
            history = self._data.get("history", [])
            if history_snapshot:
                history.append(history_snapshot)

            self._data = {
                "schema_version": STORAGE_VERSION,
                "model_version": self.model_version,
                "last_audit_date": last_audit_date,
                "criteria": criteria_dict,
                "history": history,
            }
            await self._store.async_save(self._data)
        except Exception as err:
            _LOGGER.warning("Could not persist Smart Home Score data to store (will continue in-memory): %s", err)
