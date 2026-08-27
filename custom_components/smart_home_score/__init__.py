"""Smart Home Score integration for Home Assistant (v0.7.0 Bêta).

Author: Cyrille LEFRANC
Zero-YAML automated installation, singleton async static path registration (StaticPathConfig),
official frontend registration via add_extra_js_url / remove_extra_js_url,
dispute handling for beta feedback, deterministic audit engine and diagnostic capabilities.
"""
from __future__ import annotations

import logging
import os
from typing import Any

import voluptuous as vol

from homeassistant.components.frontend import add_extra_js_url, remove_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    SERVICE_DISPUTE_AUTO_EVALUATION,
    SERVICE_RECORD_HISTORY,
    SERVICE_REEVALUATE_CRITERION,
    SERVICE_RESET_AUDIT,
    SERVICE_RUN_ANALYSIS,
    SERVICE_SIMULATE_IMPROVEMENT,
    SERVICE_SKIP_QUESTION,
    SERVICE_SUBMIT_ANSWER,
    URL_BASE_STATIC,
    URL_FRONTEND_CARD_VERSIONED,
)
from .coordinator import SmartHomeScoreCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

STATIC_REGISTERED_KEY = "smart_home_score_static_path_registered"

SUBMIT_ANSWER_SCHEMA = vol.Schema(
    {
        vol.Required("criterion_id"): cv.string,
        vol.Required("answer_key"): cv.string,
    }
)

SKIP_QUESTION_SCHEMA = vol.Schema(
    {
        vol.Required("criterion_id"): cv.string,
    }
)

SIMULATE_SCHEMA = vol.Schema(
    {
        vol.Required("criterion_id"): cv.string,
        vol.Required("simulated_score"): vol.Coerce(int),
    }
)

REEVALUATE_SCHEMA = vol.Schema(
    {
        vol.Required("criterion_id"): cv.string,
    }
)

RECORD_HISTORY_SCHEMA = vol.Schema(
    {
        vol.Optional("note", default=""): cv.string,
    }
)

DISPUTE_SCHEMA = vol.Schema(
    {
        vol.Required("criterion_id"): cv.string,
        vol.Required("user_score"): vol.All(vol.Coerce(int), vol.Range(min=0, max=4)),
        vol.Optional("feedback", default=""): cv.string,
    }
)


async def _async_register_frontend_resource(hass: HomeAssistant) -> None:
    """Register embedded frontend card static endpoint ONCE per process, add versioned JS URL, and register in Lovelace resources."""
    static_frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
    if os.path.exists(static_frontend_path):
        # 1. Singleton HTTP static path registration
        if not hass.data.get(STATIC_REGISTERED_KEY):
            if hasattr(hass, "http") and hasattr(hass.http, "async_register_static_paths"):
                try:
                    await hass.http.async_register_static_paths(
                        [
                            StaticPathConfig(
                                URL_BASE_STATIC,
                                static_frontend_path,
                                cache_headers=False,
                            )
                        ]
                    )
                    hass.data[STATIC_REGISTERED_KEY] = True
                    _LOGGER.debug("Singleton HTTP static path registered for Smart Home Score")
                except Exception as err:
                    _LOGGER.debug("Async HTTP static path registration notice: %s", err)

        # 2. Official modern frontend JS registration (add_extra_js_url)
        add_extra_js_url(hass, URL_FRONTEND_CARD_VERSIONED, es5=False)
        _LOGGER.info("Smart Home Score frontend registered via add_extra_js_url: %s", URL_FRONTEND_CARD_VERSIONED)

        # 3. Automatic Lovelace Resource Registration (for instantaneous live dashboard loading)
        try:
            lovelace_data = hass.data.get("lovelace")
            if lovelace_data and hasattr(lovelace_data, "resources"):
                resources = lovelace_data.resources
                if hasattr(resources, "async_get_items") and hasattr(resources, "async_create_item"):
                    items = resources.async_get_items()
                    clean_url = URL_FRONTEND_CARD_VERSIONED.split("?")[0]
                    existing = any(
                        isinstance(item, dict) and item.get("url", "").split("?")[0] == clean_url
                        for item in items
                    )
                    if not existing:
                        await resources.async_create_item({"res_type": "module", "url": URL_FRONTEND_CARD_VERSIONED})
                        _LOGGER.info("Smart Home Score registered in Lovelace resources collection")
        except Exception as err:
            _LOGGER.debug("Lovelace resources auto-registration notice: %s", err)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Smart Home Score from a config entry (Zero-YAML)."""
    hass.data.setdefault(DOMAIN, {})

    # 1. Automatic Modern Frontend Resource Registration (Singleton Static Path)
    await _async_register_frontend_resource(hass)

    # 2. Coordinator & Store initialization
    coordinator = SmartHomeScoreCoordinator(hass)
    await coordinator.async_init_store()
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # 3. Forward setup to sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # 4. Register Services
    async def handle_submit_answer(call: ServiceCall) -> None:
        criterion_id = call.data["criterion_id"]
        answer_key = call.data["answer_key"]
        for coord in hass.data[DOMAIN].values():
            if isinstance(coord, SmartHomeScoreCoordinator):
                await coord.async_submit_answer(criterion_id, answer_key)

    async def handle_skip_question(call: ServiceCall) -> None:
        criterion_id = call.data["criterion_id"]
        for coord in hass.data[DOMAIN].values():
            if isinstance(coord, SmartHomeScoreCoordinator):
                await coord.async_skip_question(criterion_id)

    async def handle_reset_audit(call: ServiceCall) -> None:
        for coord in hass.data[DOMAIN].values():
            if isinstance(coord, SmartHomeScoreCoordinator):
                await coord.async_reset_audit()

    async def handle_run_analysis(call: ServiceCall) -> None:
        for coord in hass.data[DOMAIN].values():
            if isinstance(coord, SmartHomeScoreCoordinator):
                await coord.async_run_analysis(save_on_complete=True)
                await coord.async_refresh()

    async def handle_simulate_improvement(call: ServiceCall) -> None:
        criterion_id = call.data["criterion_id"]
        simulated_score = call.data["simulated_score"]
        for coord in hass.data[DOMAIN].values():
            if isinstance(coord, SmartHomeScoreCoordinator):
                coord.simulate_improvement(criterion_id, simulated_score)

    async def handle_reevaluate_criterion(call: ServiceCall) -> None:
        criterion_id = call.data["criterion_id"]
        for coord in hass.data[DOMAIN].values():
            if isinstance(coord, SmartHomeScoreCoordinator):
                await coord.async_reevaluate_criterion(criterion_id)

    async def handle_record_history(call: ServiceCall) -> None:
        note = call.data.get("note", "")
        for coord in hass.data[DOMAIN].values():
            if isinstance(coord, SmartHomeScoreCoordinator):
                await coord.async_record_history(note=note)

    async def handle_dispute_auto_evaluation(call: ServiceCall) -> None:
        criterion_id = call.data["criterion_id"]
        user_score = call.data["user_score"]
        feedback = call.data.get("feedback", "")
        for coord in hass.data[DOMAIN].values():
            if isinstance(coord, SmartHomeScoreCoordinator):
                await coord.async_dispute_auto_evaluation(criterion_id, user_score, feedback)

    hass.services.async_register(DOMAIN, SERVICE_SUBMIT_ANSWER, handle_submit_answer, schema=SUBMIT_ANSWER_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_SKIP_QUESTION, handle_skip_question, schema=SKIP_QUESTION_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_RESET_AUDIT, handle_reset_audit)
    hass.services.async_register(DOMAIN, SERVICE_RUN_ANALYSIS, handle_run_analysis)
    hass.services.async_register(DOMAIN, SERVICE_SIMULATE_IMPROVEMENT, handle_simulate_improvement, schema=SIMULATE_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_REEVALUATE_CRITERION, handle_reevaluate_criterion, schema=REEVALUATE_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_RECORD_HISTORY, handle_record_history, schema=RECORD_HISTORY_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_DISPUTE_AUTO_EVALUATION, handle_dispute_auto_evaluation, schema=DISPUTE_SCHEMA)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry cleanly with no zombie listeners, services or extra JS URLs."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.data[DOMAIN]:
            # Remove services when last instance unloads
            hass.services.async_remove(DOMAIN, SERVICE_SUBMIT_ANSWER)
            hass.services.async_remove(DOMAIN, SERVICE_SKIP_QUESTION)
            hass.services.async_remove(DOMAIN, SERVICE_RESET_AUDIT)
            hass.services.async_remove(DOMAIN, SERVICE_RUN_ANALYSIS)
            hass.services.async_remove(DOMAIN, SERVICE_SIMULATE_IMPROVEMENT)
            hass.services.async_remove(DOMAIN, SERVICE_REEVALUATE_CRITERION)
            hass.services.async_remove(DOMAIN, SERVICE_RECORD_HISTORY)
            hass.services.async_remove(DOMAIN, SERVICE_DISPUTE_AUTO_EVALUATION)

            # Official clean removal of frontend extra JS URL
            try:
                remove_extra_js_url(hass, URL_FRONTEND_CARD_VERSIONED)
            except Exception as err:
                _LOGGER.debug("remove_extra_js_url notice: %s", err)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
