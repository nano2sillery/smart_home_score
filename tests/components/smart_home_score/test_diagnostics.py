"""Tests for Anonymized Diagnostics Module (v0.6.1)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest
from unittest.mock import MagicMock

from custom_components.smart_home_score.const import DOMAIN, MODEL_VERSION, VERSION
from custom_components.smart_home_score.coordinator import SmartHomeScoreCoordinator
from custom_components.smart_home_score.diagnostics import (
    async_get_config_entry_diagnostics,
    sanitize_diagnostic_text,
)
from custom_components.smart_home_score.engine.models import CriterionState, CriterionStatus


class TestDiagnostics(unittest.IsolatedAsyncioTestCase):
    """Test suite for diagnostics redaction (IPs, MACs, emails, local paths, SSIDs)."""

    def test_sanitize_diagnostic_text_redacts_private_info(self):
        """Test redaction of IPv4, MAC, emails, paths and SSIDs."""
        raw_text = (
            "Serveur sur 192.168.1.50 avec MAC 00:1A:2B:3C:4D:5E, email user@example.com, "
            "fichier dans /Users/LEFRANCC/HomeAssistant/configuration.yaml et SSID: Livebox-4A20."
        )
        sanitized = sanitize_diagnostic_text(raw_text)
        self.assertNotIn("192.168.1.50", sanitized)
        self.assertNotIn("00:1A:2B:3C:4D:5E", sanitized)
        self.assertNotIn("user@example.com", sanitized)
        self.assertNotIn("/Users/LEFRANCC/HomeAssistant", sanitized)
        self.assertNotIn("Livebox-4A20", sanitized)
        self.assertIn("xxx.xxx.xxx.xxx", sanitized)
        self.assertIn("xx:xx:xx:xx:xx:xx", sanitized)
        self.assertIn("[REDACTED_EMAIL]", sanitized)
        self.assertIn("[REDACTED_PATH]", sanitized)
        self.assertIn("[REDACTED_SSID]", sanitized)

    async def test_diagnostics_payload_structure(self):
        """Test structure and metadata of exported diagnostics payload."""
        hass_mock = MagicMock()
        entry_mock = MagicMock()
        entry_mock.entry_id = "test_entry_diag"

        coordinator = SmartHomeScoreCoordinator(hass_mock)
        coordinator.criteria_states = {
            "CYBER01": CriterionState(
                criterion_id="CYBER01",
                effective_score=4,
                status=CriterionStatus.CONFIRMED,
                evidence="Accès distant chiffré via Nabu Casa sur 192.168.1.254 avec fichier /home/user/cert.pem",
            )
        }
        hass_mock.data = {DOMAIN: {entry_mock.entry_id: coordinator}}

        diag = await async_get_config_entry_diagnostics(hass_mock, entry_mock)
        self.assertEqual(diag["integration_version"], VERSION)
        self.assertEqual(diag["model_version"], MODEL_VERSION)
        self.assertEqual(diag["author"], "Cyrille LEFRANC")
        self.assertIn("CYBER01", diag["criteria"])
        self.assertNotIn("192.168.1.254", diag["criteria"]["CYBER01"]["sanitized_evidence"])
        self.assertNotIn("/home/user/cert.pem", diag["criteria"]["CYBER01"]["sanitized_evidence"])


if __name__ == "__main__":
    unittest.main()
