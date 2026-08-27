"""Config flow for Smart Home Score integration."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, NAME


class SmartHomeScoreConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Smart Home Score."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title=NAME, data={})

        return self.async_show_form(step_id="user")
