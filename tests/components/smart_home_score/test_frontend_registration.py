"""Tests for Modern Async Frontend Registration, Custom Card Catalog & Resilient Card Setup (v0.7.0-beta.3)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import os
import subprocess
import unittest
from unittest.mock import AsyncMock, MagicMock

from custom_components.smart_home_score import async_setup_entry, async_unload_entry, async_reload_entry
from custom_components.smart_home_score.const import DOMAIN, URL_FRONTEND_CARD_VERSIONED, VERSION
from homeassistant.components.frontend import active_frontend_urls


class TestFrontendRegistration(unittest.IsolatedAsyncioTestCase):
    """Test suite for modern async static paths, custom card catalog, getStubConfig and zero JS syntax errors."""

    def test_frontend_file_is_strictly_embedded_in_integration_directory(self):
        """Test that JS file is present inside custom_components/.../frontend/ and self-contained."""
        frontend_path = "/Users/LEFRANCC/HomeAssistant/custom_components/smart_home_score/frontend/smart-home-score-card.js"
        self.assertTrue(os.path.exists(frontend_path), "Embedded frontend JS file must exist inside integration directory")

    def test_javascript_syntax_is_strictly_valid(self):
        """Test that frontend card JS file contains zero syntax errors."""
        frontend_path = "/Users/LEFRANCC/HomeAssistant/custom_components/smart_home_score/frontend/smart-home-score-card.js"
        res = subprocess.run(["node", "-c", frontend_path], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"JavaScript syntax error in card: {res.stderr}")

    def test_custom_cards_catalog_registration_and_stub_config(self):
        """Test that the JS card defines getStubConfig and registers into window.customCards."""
        frontend_path = "/Users/LEFRANCC/HomeAssistant/custom_components/smart_home_score/frontend/smart-home-score-card.js"
        with open(frontend_path, "r", encoding="utf-8") as f:
            code = f.read()

        # 1. Verification of window.customCards catalog
        self.assertIn("window.customCards = window.customCards || [];", code)
        self.assertIn("smart-home-score-card", code)
        self.assertIn("Smart Home Score", code)
        self.assertIn("preview: true", code)

        # 2. Verification of getStubConfig & setConfig resilience
        self.assertIn("getStubConfig", code)
        self.assertIn("setConfig(config)", code)
        self.assertIn("this._config = config || {};", code)

        # 3. Verification of Zero-Audit / Welcome screen
        self.assertIn("Bienvenue dans Smart Home Score", code)
        self.assertIn("Lancer mon premier audit", code)

    def test_no_deprecated_register_static_path_in_codebase(self):
        """Test that deprecated synchronous register_static_path is completely absent from component code."""
        component_dir = "/Users/LEFRANCC/HomeAssistant/custom_components/smart_home_score"
        for root, _, files in os.walk(component_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("."):
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()
                        self.assertNotIn("hass.http.register_static_path(", code, f"Deprecated register_static_path found in {file}")

    def test_no_direct_frontend_extra_module_url_in_production_code(self):
        """Test that internal hass.data['frontend_extra_module_url'] is absent from production code."""
        component_dir = "/Users/LEFRANCC/HomeAssistant/custom_components/smart_home_score"
        for root, _, files in os.walk(component_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("."):
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()
                        self.assertNotIn('frontend_extra_module_url', code, f"Direct internal hass.data access found in {file}")

    async def test_setup_unload_setup_lifecycle_prevents_duplicate_js_urls(self):
        """Test setup -> unload -> setup lifecycle uses add_extra_js_url / remove_extra_js_url without accumulating duplicate URLs."""
        hass_mock = MagicMock()
        hass_mock.data = {}
        hass_mock.http = MagicMock()
        hass_mock.http.async_register_static_paths = AsyncMock()
        hass_mock.config_entries = MagicMock()
        hass_mock.config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
        hass_mock.config_entries.async_unload_platforms = AsyncMock(return_value=True)

        entry_mock = MagicMock()
        entry_mock.entry_id = "test_frontend_entry"

        # 1. Setup Entry 1
        active_frontend_urls.clear()
        setup_ok = await async_setup_entry(hass_mock, entry_mock)
        self.assertTrue(setup_ok)
        self.assertIn(URL_FRONTEND_CARD_VERSIONED, active_frontend_urls)
        self.assertEqual(len(active_frontend_urls), 1)

        # 2. Unload Entry 1
        unload_ok = await async_unload_entry(hass_mock, entry_mock)
        self.assertTrue(unload_ok)
        self.assertNotIn(URL_FRONTEND_CARD_VERSIONED, active_frontend_urls)
        self.assertEqual(len(active_frontend_urls), 0)

        # 3. Setup Entry 2 (re-setup / reload)
        setup_again_ok = await async_setup_entry(hass_mock, entry_mock)
        self.assertTrue(setup_again_ok)
        self.assertIn(URL_FRONTEND_CARD_VERSIONED, active_frontend_urls)
        self.assertEqual(len(active_frontend_urls), 1)

    async def test_setup_reload_x10_stability_and_singleton_static_path(self):
        """Test 10 consecutive reloads: static path registered once, exactly 1 active JS URL, no exceptions."""
        hass_mock = MagicMock()
        hass_mock.data = {}
        hass_mock.http = MagicMock()
        hass_mock.http.async_register_static_paths = AsyncMock()
        hass_mock.config_entries = MagicMock()
        hass_mock.config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
        hass_mock.config_entries.async_unload_platforms = AsyncMock(return_value=True)

        entry_mock = MagicMock()
        entry_mock.entry_id = "test_reload_10_entry"

        active_frontend_urls.clear()
        # Initial Setup
        await async_setup_entry(hass_mock, entry_mock)
        self.assertEqual(hass_mock.http.async_register_static_paths.call_count, 1)

        # 10 Consecutive Reloads
        for _ in range(10):
            await async_reload_entry(hass_mock, entry_mock)
            self.assertEqual(len(active_frontend_urls), 1)
            self.assertIn(URL_FRONTEND_CARD_VERSIONED, active_frontend_urls)
            self.assertEqual(hass_mock.http.async_register_static_paths.call_count, 1)


if __name__ == "__main__":
    unittest.main()
