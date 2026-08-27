"""Tests for the Rule Engine on synthetic installations (v0.3.2 Hardened)."""
import tests.components.smart_home_score.conftest  # noqa: F401
import unittest

from custom_components.smart_home_score.criteria.repository import CriteriaRepository
from custom_components.smart_home_score.engine.models import (
    CriterionStatus,
    EvidenceType,
    InstallationSnapshot,
)
from custom_components.smart_home_score.engine.rules import RuleEngine


class TestRuleEngine(unittest.TestCase):
    """Test suite for hardened deterministic rules engine."""

    def setUp(self):
        """Set up test repository and rule engine."""
        self.repo = CriteriaRepository(model_version="1.0")
        self.engine = RuleEngine(self.repo)

    def test_minimal_installation(self):
        """Test a minimal installation with few entities generates questions and no fake scores."""
        snap = InstallationSnapshot(
            total_entities=5,
            total_devices=2,
            domains_present={"light", "switch"},
            lights_count=2,
            switches_count=1,
        )
        results = self.engine.evaluate_all(snap)

        # Physical criteria must be QUESTION or TEST
        self.assertEqual(results["ELEC01"].status, CriterionStatus.TEST_REQUIRED)
        self.assertEqual(results["ELEC02"].status, CriterionStatus.QUESTION_REQUIRED)
        self.assertEqual(results["RES01"].status, CriterionStatus.TEST_REQUIRED)
        self.assertEqual(results["RES07"].status, CriterionStatus.TEST_REQUIRED)

        # Solar should ask question, not arbitrarily mark 0 or not applicable
        self.assertEqual(results["ENER04"].status, CriterionStatus.QUESTION_REQUIRED)

    def test_advanced_local_installation(self):
        """Test advanced installation gets strictly DIRECT_EVIDENCE AUTO evaluations."""
        snap = InstallationSnapshot(
            total_entities=150,
            total_devices=45,
            total_areas=8,
            domains_present={"light", "cover", "climate", "sensor", "switch", "binary_sensor", "person", "fan", "update", "backup"},
            integrations_present={"zha", "zigbee2mqtt", "mqtt", "esphome", "backup", "systemmonitor"},
            local_integrations={"zha", "zigbee2mqtt", "mqtt", "esphome", "systemmonitor"},
            has_zigbee=True,
            zigbee_devices_count=35,
            has_mqtt=True,
            has_esphome=True,
            has_grid_power_realtime=True,
            has_grid_energy_total=True,
            has_solar_production=True,
            solar_power_entity="sensor.solar_inverter_power",
            individual_energy_devices_count=12,
            has_water_meter=True,
            has_water_leak_sensors=True,
            water_leak_sensors_count=4,
            has_connected_valve=False,
            has_motion_presence_sensors=True,
            has_humidity_sensors=True,
            fans_count=2,
            persons_count=3,
            entities_with_area_count=140,
            devices_with_area_count=45,
            entities_with_proper_naming_count=145,
            automations_count=25,
            automations_with_description_count=20,  # 80% -> score 3
            batteries_count=15,
            has_custom_dashboards=True,
        )
        results = self.engine.evaluate_all(snap)

        # Direct evidence AUTO evaluations
        self.assertEqual(results["ENER01"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(results["ENER01"].evidence_type, EvidenceType.DIRECT_EVIDENCE)
        self.assertEqual(results["ENER01"].proposed_score, 4)

        self.assertEqual(results["ENER02"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(results["ENER02"].evidence_type, EvidenceType.DIRECT_EVIDENCE)
        self.assertEqual(results["ENER02"].proposed_score, 4)

        self.assertEqual(results["ENER03"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(results["ENER03"].evidence_type, EvidenceType.DIRECT_EVIDENCE)
        self.assertEqual(results["ENER03"].proposed_score, 4)

        self.assertEqual(results["ENER04"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(results["ENER04"].evidence_type, EvidenceType.DIRECT_EVIDENCE)
        self.assertEqual(results["ENER04"].proposed_score, 4)

        self.assertEqual(results["ENER08"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(results["ENER08"].evidence_type, EvidenceType.DIRECT_EVIDENCE)
        self.assertEqual(results["ENER08"].proposed_score, 4)

        self.assertEqual(results["INTER04"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(results["INTER04"].evidence_type, EvidenceType.DIRECT_EVIDENCE)
        self.assertEqual(results["INTER04"].proposed_score, 4)

        self.assertEqual(results["MAINT01"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(results["MAINT01"].evidence_type, EvidenceType.DIRECT_EVIDENCE)
        self.assertEqual(results["MAINT01"].proposed_score, 3)

        self.assertEqual(results["MAINT03"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(results["MAINT03"].evidence_type, EvidenceType.DIRECT_EVIDENCE)
        self.assertEqual(results["MAINT03"].proposed_score, 3)

        # Hardened to QUESTION_REQUIRED (CAPABILITY_EVIDENCE)
        self.assertEqual(results["INTER01"].status, CriterionStatus.QUESTION_REQUIRED)
        self.assertEqual(results["INTER01"].evidence_type, EvidenceType.CAPABILITY_EVIDENCE)
        self.assertEqual(results["INTER01"].proposed_score, 4)

        self.assertEqual(results["CYBER06"].status, CriterionStatus.QUESTION_REQUIRED)
        self.assertEqual(results["CYBER06"].evidence_type, EvidenceType.CAPABILITY_EVIDENCE)
        self.assertEqual(results["RES05"].status, CriterionStatus.QUESTION_REQUIRED)
        self.assertEqual(results["RES05"].evidence_type, EvidenceType.CAPABILITY_EVIDENCE)

    # -------------------------------------------------------------------------
    # Anti-overfitting scenarios (Hardening validation)
    # -------------------------------------------------------------------------
    def test_anti_overfit_update_entities_but_no_proven_routine(self):
        """Scenario 1: HA with update entities does not get AUTO 4/4 without proven update routine."""
        snap = InstallationSnapshot(domains_present={"update"})
        results = self.engine.evaluate_all(snap)
        self.assertEqual(results["CYBER06"].status, CriterionStatus.QUESTION_REQUIRED)
        self.assertEqual(results["CYBER06"].evidence_type, EvidenceType.CAPABILITY_EVIDENCE)

    def test_anti_overfit_backup_configured_without_execution_proof(self):
        """Scenario 2: Backup module present does not give automatic 4/4 without human confirmation."""
        snap = InstallationSnapshot(integrations_present={"backup"})
        results = self.engine.evaluate_all(snap)
        self.assertEqual(results["RES05"].status, CriterionStatus.QUESTION_REQUIRED)
        self.assertEqual(results["RES05"].evidence_type, EvidenceType.CAPABILITY_EVIDENCE)

    def test_anti_overfit_presence_and_lights_without_automation(self):
        """Scenario 3: Presence sensors + lights do not automatically score 4 without proven logic."""
        snap = InstallationSnapshot(
            lights_count=15,
            has_motion_presence_sensors=True,
            persons_count=2,
        )
        results = self.engine.evaluate_all(snap)
        self.assertEqual(results["AUTO01"].status, CriterionStatus.QUESTION_REQUIRED)
        self.assertEqual(results["AUTO07"].status, CriterionStatus.QUESTION_REQUIRED)

    def test_anti_overfit_solar_detected_without_surplus_optimization(self):
        """Scenario 4: Solar production detected does NOT mark surplus optimization as 4/4."""
        snap = InstallationSnapshot(
            has_solar_production=True,
            solar_power_entity="sensor.solar_inverter",
        )
        results = self.engine.evaluate_all(snap)
        self.assertEqual(results["ENER04"].status, CriterionStatus.AUTO_EVALUATED)
        self.assertEqual(results["ENER06"].status, CriterionStatus.QUESTION_REQUIRED)
        self.assertEqual(results["ENER07"].status, CriterionStatus.QUESTION_REQUIRED)

    def test_anti_overfit_water_valve_and_meter_without_closing_automation(self):
        """Scenario 5: Water sensors + valve require confirmation of automatic shutoff."""
        snap = InstallationSnapshot(
            has_water_leak_sensors=True,
            water_leak_sensors_count=3,
            has_connected_valve=True,
        )
        results = self.engine.evaluate_all(snap)
        self.assertEqual(results["AUTO05"].status, CriterionStatus.QUESTION_REQUIRED)
        self.assertEqual(results["AUTO05"].proposed_score, 3)


if __name__ == "__main__":
    unittest.main()
