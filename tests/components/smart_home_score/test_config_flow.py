"""Tests for the Smart Home Score config flow."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest
from unittest.mock import MagicMock

from custom_components.smart_home_score.config_flow import SmartHomeScoreConfigFlow
from custom_components.smart_home_score.const import DOMAIN, NAME


class TestSmartHomeScoreConfigFlow(unittest.IsolatedAsyncioTestCase):
    """Test suite for Smart Home Score config flow."""

    async def test_initial_addition_shows_form(self):
        """Test initial addition presents the confirmation form with no in-progress or error."""
        flow = SmartHomeScoreConfigFlow()
        result = await flow.async_step_user(user_input=None)
        
        self.assertEqual(result["type"], "form")
        self.assertEqual(result["step_id"], "user")
        self.assertNotIn("reason", result)

    async def test_initial_submission_creates_entry(self):
        """Test submitting the form creates the single config entry immediately."""
        flow = SmartHomeScoreConfigFlow()
        result = await flow.async_step_user(user_input={})
        
        self.assertEqual(result["type"], "create_entry")
        self.assertEqual(result["title"], NAME)
        self.assertEqual(result["data"], {})

    async def test_reinstallation_after_removal(self):
        """Test that removing an entry allows normal re-installation without state residue."""
        flow1 = SmartHomeScoreConfigFlow()
        result1 = await flow1.async_step_user(user_input={})
        self.assertEqual(result1["type"], "create_entry")

        # Simulate user removing the integration and starting a fresh flow
        flow2 = SmartHomeScoreConfigFlow()
        form_result = await flow2.async_step_user(user_input=None)
        self.assertEqual(form_result["type"], "form")
        
        install_result = await flow2.async_step_user(user_input={})
        self.assertEqual(install_result["type"], "create_entry")


if __name__ == "__main__":
    unittest.main()
