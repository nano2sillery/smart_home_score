"""Deterministic Evaluation Rules Engine for Smart Home Score (v0.3.2 Hardened).

Evidence Classification Hierarchy:
1. DIRECT_EVIDENCE: Direct, incontestable fact proven via public APIs -> AUTO_EVALUATED if Confidence >= 90%.
2. CAPABILITY_EVIDENCE: Infrastructure allows feature, but human usage/routine not guaranteed -> QUESTION_REQUIRED (with pre-filled proposed_score).
3. BEHAVIORAL_EVIDENCE: Physical observation or human validation needed -> QUESTION_REQUIRED / TEST_REQUIRED.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .models import (
    CriterionStatus,
    EvidenceType,
    InstallationSnapshot,
    RuleEvaluationResult,
)

if TYPE_CHECKING:
    from ..criteria.repository import CriteriaRepository

CONFIDENCE_AUTO_THRESHOLD = 90.0
CONFIDENCE_PREFILL_THRESHOLD = 70.0


class RuleEngine:
    """Deterministic rule evaluator for Smart Home Score."""

    def __init__(self, repository: CriteriaRepository) -> None:
        """Initialize the rule engine."""
        self.repository = repository

    def evaluate_all(self, snapshot: InstallationSnapshot) -> dict[str, RuleEvaluationResult]:
        """Evaluate all 59 criteria against the snapshot."""
        results: dict[str, RuleEvaluationResult] = {}
        for cid in self.repository.criteria:
            results[cid] = self.evaluate_criterion(cid, snapshot)
        return results

    def evaluate_criterion(self, criterion_id: str, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        """Evaluate a single criterion using dedicated deterministic rules."""
        cid = criterion_id.upper()
        method_name = f"_eval_{cid.lower()}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(snapshot)
        return self._eval_default_fallback(cid, snapshot)

    # -------------------------------------------------------------------------
    # ELEC — Sécurité Électrique (BEHAVIORAL_EVIDENCE -> Always QUESTION / TEST)
    # -------------------------------------------------------------------------
    def _eval_elec01(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="ELEC01",
            status=CriterionStatus.TEST_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Le fonctionnement physique avec serveur éteint requiert un test d'extinction réel.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=["lights_count", "covers_count"],
            reason_if_not_auto="La réalité physique sans serveur n'est pas observable via les API Home Assistant.",
        )

    def _eval_elec02(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="ELEC02",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Le dimensionnement des contacteurs modulaires et protections divisionnaires requiert confirmation matérielle.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Le calibre matériel des disjoncteurs n'est pas accessible via l'API.",
        )

    def _eval_elec03(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="ELEC03",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La configuration du Power-on state après coupure secteur doit être confirmée pour chaque équipement.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Comportement au retour secteur hétérogène selon les marques et modules.",
        )

    def _eval_elec04(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="ELEC04",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="L'interverrouillage matériel (protection montée/descente simultanées sur volets) requiert validation matérielle.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=["covers_count"],
            reason_if_not_auto="La présence logicielle d'une entité cover ne prouve pas l'interlock mécanique ou matériel.",
        )

    def _eval_elec05(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="ELEC05",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La présence d'un déverrouillage manuel de secours sur les équipements critiques (serrure, vanne) requiert confirmation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=["has_connected_valve"],
            reason_if_not_auto="Information physique non accessible via API publique.",
        )

    # -------------------------------------------------------------------------
    # CYBER — Cybersécurité
    # -------------------------------------------------------------------------
    def _eval_cyber01(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # CAPABILITY_EVIDENCE: Presence of an integration != effective remote access topology
        return RuleEvaluationResult(
            criterion_id="CYBER01",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=50.0,
            evidence="Le moyen d'accès externe effectif (Cloudflare Access, Nabu Casa, VPN ou redirection NAT) ne peut être déduit de la seule liste des intégrations.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["integrations_present"],
            reason_if_not_auto="Le type d'accès distant sécurisé requiert confirmation de l'utilisateur.",
        )

    def _eval_cyber02(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="CYBER02",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="L'activation de la double authentification (2FA / TOTP) est une donnée de sécurité privée non exposée par l'API publique.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Donnée de sécurité privée inaccessible.",
        )

    def _eval_cyber03(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="CYBER03",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=50.0,
            evidence=f"{snapshot.persons_count} personnes déclarées dans le registre. Les comptes utilisateurs associés doivent être confirmés.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["persons_count"],
            reason_if_not_auto="Une entité person ne prouve pas l'existence d'un compte utilisateur dédié.",
        )

    def _eval_cyber04(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="CYBER04",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="L'attribution des privilèges administrateur (notamment sur tablettes partagées) requiert confirmation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Rôles détaillés non vérifiables sans accès aux comptes.",
        )

    def _eval_cyber05(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="CYBER05",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="L'absence de mots de passe ou tokens exposés dans les cartes ou notifications requiert confirmation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Smart Home Score ne scanne jamais les fichiers de secrets ni les tokens.",
        )

    def _eval_cyber06(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # Hardened: Presence of update entities is CAPABILITY_EVIDENCE, not proof of human update routine
        if "update" in snapshot.domains_present:
            return RuleEvaluationResult(
                criterion_id="CYBER06",
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=3,
                confidence=75.0,
                evidence="Entités de mise à jour pour HA Core et OS actives. La régularité de la routine humaine de mise à jour mensuelle requiert validation.",
                evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
                observations_used=["domains_present"],
                reason_if_not_auto="La présence d'entités update ne prouve pas à elle seule une routine régulière de mise à jour appliquée par l'utilisateur.",
            )
        return RuleEvaluationResult(
            criterion_id="CYBER06",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=2,
            confidence=70.0,
            evidence="Politique de mise à jour régulière à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["domains_present"],
            reason_if_not_auto="Entités de mise à jour non présentes.",
        )

    def _eval_cyber07(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="CYBER07",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="L'isolation réseau des objets connectés (VLAN IoT / Wi-Fi Invité) dépend du routeur externe.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Architecture réseau externe non accessible par l'API.",
        )

    def _eval_cyber08(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="CYBER08",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La routine de surveillance des réparations et alertes de sécurité requiert confirmation humaine.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Comportement de surveillance utilisateur non automatisable.",
        )

    # -------------------------------------------------------------------------
    # RES — Résilience & Continuité
    # -------------------------------------------------------------------------
    def _eval_res01(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="RES01",
            status=CriterionStatus.TEST_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Le fonctionnement autonome lors d'une coupure Internet nécessite un test en débranchant la box.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=["local_integrations"],
            reason_if_not_auto="Un test physique de déconnexion réseau est indispensable.",
        )

    def _eval_res02(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="RES02",
            status=CriterionStatus.TEST_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="L'utilisation des commandes physiques avec serveur éteint requiert un test réel.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Validation physique nécessaire.",
        )

    def _eval_res03(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="RES03",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=3,
            confidence=75.0,
            evidence=f"{snapshot.unavailable_count} entités indisponibles identifiées sur {snapshot.total_entities}. La présence d'une alerte automatique proactive requiert validation.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["total_entities", "unavailable_count"],
            reason_if_not_auto="La supervision active avec notification proactive n'est pas prouvable par le seul état instantané.",
        )

    def _eval_res04(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        if snapshot.has_zigbee and snapshot.zigbee_devices_count > 0:
            return RuleEvaluationResult(
                criterion_id="RES04",
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=3,
                confidence=75.0,
                evidence=f"Réseau Zigbee présent ({snapshot.zigbee_devices_count} appareils). La stabilité et la densité de routeurs doivent être confirmées.",
                evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
                observations_used=["has_zigbee", "zigbee_devices_count"],
                reason_if_not_auto="Le nombre de périphériques ne garantit pas la qualité radio du maillage.",
            )
        return RuleEvaluationResult(
            criterion_id="RES04",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Qualité du maillage domotique à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["has_zigbee"],
            reason_if_not_auto="Aucun réseau maillé Zigbee détecté.",
        )

    def _eval_res05(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # Hardened: Presence of backup integration is CAPABILITY_EVIDENCE (requires confirmation of schedule/retention/success)
        has_backup = bool("backup" in snapshot.integrations_present or "backup" in snapshot.domains_present)
        if has_backup:
            return RuleEvaluationResult(
                criterion_id="RES05",
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=4,
                confidence=85.0,
                evidence="Système de sauvegarde natif actif dans Home Assistant. La planification automatique régulière et la rétention tournante requièrent validation.",
                evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
                observations_used=["integrations_present"],
                reason_if_not_auto="L'exécution réussie et régulière des sauvegardes automatiques requiert validation.",
            )
        return RuleEvaluationResult(
            criterion_id="RES05",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=2,
            confidence=70.0,
            evidence="Planification des sauvegardes régulières à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["integrations_present"],
            reason_if_not_auto="Module backup non détecté.",
        )

    def _eval_res06(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="RES06",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La copie des sauvegardes hors du serveur (NAS / Google Drive / Clé USB) requiert confirmation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Destination externe non vérifiable par API standard.",
        )

    def _eval_res07(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # Guided test procedure
        return RuleEvaluationResult(
            criterion_id="RES07",
            status=CriterionStatus.TEST_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La réalisation et validation d'un test réel de restauration requièrent un test guidé ou confirmation d'antériorité.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Un test de restauration ne peut être prouvé que par exécution humaine.",
        )

    def _eval_res08(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        if snapshot.has_ups_monitoring:
            return RuleEvaluationResult(
                criterion_id="RES08",
                status=CriterionStatus.AUTO_EVALUATED,
                proposed_score=4,
                confidence=95.0,
                evidence="Onduleur communicant (NUT/APCUPSD/SNMP) actif dans Home Assistant.",
                evidence_type=EvidenceType.DIRECT_EVIDENCE,
                observations_used=["has_ups_monitoring"],
            )
        return RuleEvaluationResult(
            criterion_id="RES08",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Présence d'un onduleur (UPS) ou protection électrique sur le serveur à confirmer.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=["has_ups_monitoring"],
            reason_if_not_auto="Aucune intégration d'onduleur communicant détectée.",
        )

    # -------------------------------------------------------------------------
    # AUTO — Intelligence & Automatisations (CAPABILITY_EVIDENCE -> QUESTION_REQUIRED)
    # -------------------------------------------------------------------------
    def _eval_auto01(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="AUTO01",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=3 if (snapshot.lights_count > 5 and snapshot.has_motion_presence_sensors) else None,
            confidence=75.0 if (snapshot.lights_count > 5 and snapshot.has_motion_presence_sensors) else 50.0,
            evidence=f"{snapshot.lights_count} lumières et capteurs de présence détectés. L'adaptation contextuelle requiert confirmation.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["lights_count", "has_motion_presence_sensors"],
            reason_if_not_auto="La logique fine des scénarios d'éclairage nécessite confirmation.",
        )

    def _eval_auto02(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="AUTO02",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=3 if (snapshot.climates_count > 0 and snapshot.has_window_door_sensors) else (2 if snapshot.climates_count > 0 else None),
            confidence=75.0 if snapshot.climates_count > 0 else 0.0,
            evidence=f"{snapshot.climates_count} thermostats et capteurs d'ouverture détectés. La régulation automatique avancée requiert confirmation.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["climates_count", "has_window_door_sensors"],
            reason_if_not_auto="La logique de régulation thermique avancée requiert validation.",
        )

    def _eval_auto03(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        if snapshot.fans_count > 0 and snapshot.has_humidity_sensors:
            return RuleEvaluationResult(
                criterion_id="AUTO03",
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=3,
                confidence=78.0,
                evidence=f"Ventilation ({snapshot.fans_count} fan) et capteurs d'humidité présents. Le pilotage automatique selon l'humidité requiert validation.",
                evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
                observations_used=["fans_count", "has_humidity_sensors"],
                reason_if_not_auto="La corrélation fan + humidité ne prouve pas l'existence de l'automatisme sans accès à sa logique interne.",
            )
        return RuleEvaluationResult(
            criterion_id="AUTO03",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Pilotage de la VMC ou aération à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["fans_count", "has_humidity_sensors"],
            reason_if_not_auto="Équipements de ventilation non associés.",
        )

    def _eval_auto04(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="AUTO04",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=3 if snapshot.covers_count > 0 else None,
            confidence=75.0 if snapshot.covers_count > 0 else 0.0,
            evidence=f"{snapshot.covers_count} volets détectés. La gestion thermique et solaire automatique requiert confirmation.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["covers_count"],
            reason_if_not_auto="La logique bioclimatique requiert validation.",
        )

    def _eval_auto05(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        if snapshot.has_water_leak_sensors and snapshot.has_connected_valve:
            return RuleEvaluationResult(
                criterion_id="AUTO05",
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=3,
                confidence=80.0,
                evidence=f"{snapshot.water_leak_sensors_count} capteurs de fuite et vanne détectés. La fermeture automatique en cas de fuite requiert confirmation.",
                evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
                observations_used=["water_leak_sensors_count", "has_connected_valve"],
                reason_if_not_auto="L'automatisme liant capteurs et vanne requiert validation.",
            )
        elif snapshot.has_water_leak_sensors:
            return RuleEvaluationResult(
                criterion_id="AUTO05",
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=2,
                confidence=80.0,
                evidence=f"{snapshot.water_leak_sensors_count} capteurs de fuite détectés sans vanne connectée déclarée (notification d'alerte).",
                evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
                observations_used=["water_leak_sensors_count"],
                reason_if_not_auto="La présence de capteurs sans vanne motorisée correspond au niveau 2 (alerte) à confirmer.",
            )
        return RuleEvaluationResult(
            criterion_id="AUTO05",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=0,
            confidence=70.0,
            evidence="Aucun capteur d'inondation détecté.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["water_leak_sensors_count"],
            reason_if_not_auto="Absence de capteurs d'eau.",
        )

    def _eval_auto06(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="AUTO06",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=3 if snapshot.individual_energy_devices_count >= 3 else None,
            confidence=75.0 if snapshot.individual_energy_devices_count >= 3 else 0.0,
            evidence=f"{snapshot.individual_energy_devices_count} appareils mesurés. La notification automatique de fin de cycle requiert confirmation.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["individual_energy_devices_count"],
            reason_if_not_auto="La mesure électrique ne prouve pas l'existence d'une automatisation de détection de cycle.",
        )

    def _eval_auto07(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="AUTO07",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=3 if (snapshot.persons_count >= 1 and snapshot.has_motion_presence_sensors) else (2 if snapshot.persons_count >= 1 else None),
            confidence=80.0 if snapshot.persons_count >= 1 else 0.0,
            evidence=f"Infrastructure de présence présente ({snapshot.persons_count} personnes, capteurs de mouvement). L'adaptation effective du comportement de la maison requiert confirmation.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["persons_count", "has_motion_presence_sensors"],
            reason_if_not_auto="L'exploitation active de la présence dans les scénarios de vie requiert validation humaine.",
        )

    def _eval_auto08(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="AUTO08",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=3 if snapshot.helpers_count >= 3 else None,
            confidence=75.0 if snapshot.helpers_count >= 3 else 0.0,
            evidence=f"{snapshot.helpers_count} helpers de contexte déclarés. La contextualisation globale requiert validation.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["helpers_count"],
            reason_if_not_auto="Conditions contextuelles à valider.",
        )

    def _eval_auto09(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="AUTO09",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La présence de boucles de contrôle d'état sur actions critiques requiert confirmation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Architecture des scripts de contrôle à valider.",
        )

    # -------------------------------------------------------------------------
    # ENER — Énergie & Ressources (DIRECT_EVIDENCE factuelle)
    # -------------------------------------------------------------------------
    def _eval_ener01(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # DIRECT_EVIDENCE: Teleinfo Linky / realtime grid power and energy total entities
        if snapshot.has_grid_power_realtime and snapshot.has_grid_energy_total:
            return RuleEvaluationResult(
                criterion_id="ENER01",
                status=CriterionStatus.AUTO_EVALUATED,
                proposed_score=4,
                confidence=98.0,
                evidence="Mesure globale temps réel (TIC Linky / tore) et énergie totale active détectées.",
                evidence_type=EvidenceType.DIRECT_EVIDENCE,
                observations_used=["has_grid_power_realtime", "has_grid_energy_total"],
            )
        elif snapshot.has_grid_power_realtime or snapshot.has_grid_energy_total:
            return RuleEvaluationResult(
                criterion_id="ENER01",
                status=CriterionStatus.AUTO_EVALUATED,
                proposed_score=3,
                confidence=90.0,
                evidence="Mesure électrique globale active détectée.",
                evidence_type=EvidenceType.DIRECT_EVIDENCE,
                observations_used=["has_grid_power_realtime", "has_grid_energy_total"],
            )
        return RuleEvaluationResult(
            criterion_id="ENER01",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=0,
            confidence=75.0,
            evidence="Aucun capteur d'énergie ou de puissance générale détecté.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["has_grid_power_realtime", "has_grid_energy_total"],
            reason_if_not_auto="Absence de mesure globale détectée.",
        )

    def _eval_ener02(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # DIRECT_EVIDENCE: Energy platform configured with persistent long term statistics
        if snapshot.has_grid_energy_total:
            return RuleEvaluationResult(
                criterion_id="ENER02",
                status=CriterionStatus.AUTO_EVALUATED,
                proposed_score=4,
                confidence=95.0,
                evidence="Dashboard Énergie configuré avec statistiques à long terme actives.",
                evidence_type=EvidenceType.DIRECT_EVIDENCE,
                observations_used=["has_grid_energy_total"],
            )
        return RuleEvaluationResult(
            criterion_id="ENER02",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Historique énergétique à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            reason_if_not_auto="Aucune donnée d'énergie continue.",
        )

    def _eval_ener03(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # DIRECT_EVIDENCE: Direct count of individual submetered consumers in registry
        count = snapshot.individual_energy_devices_count
        if count >= 10:
            score = 4
        elif count >= 5:
            score = 3
        elif count >= 2:
            score = 2
        elif count == 1:
            score = 1
        else:
            score = 0

        return RuleEvaluationResult(
            criterion_id="ENER03",
            status=CriterionStatus.AUTO_EVALUATED,
            proposed_score=score,
            confidence=95.0,
            evidence=f"{count} consommateurs mesurés individuellement dans le registre d'énergie.",
            evidence_type=EvidenceType.DIRECT_EVIDENCE,
            observations_used=["individual_energy_devices_count"],
        )

    def _eval_ener04(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # DIRECT_EVIDENCE: Active solar production entity
        if snapshot.has_solar_production:
            return RuleEvaluationResult(
                criterion_id="ENER04",
                status=CriterionStatus.AUTO_EVALUATED,
                proposed_score=4,
                confidence=95.0,
                evidence=f"Production solaire photovoltaïque détectée ({snapshot.solar_power_entity}).",
                evidence_type=EvidenceType.DIRECT_EVIDENCE,
                observations_used=["has_solar_production", "solar_power_entity"],
            )
        return RuleEvaluationResult(
            criterion_id="ENER04",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Aucune entité de production solaire détectée. Disposez-vous d'une installation photovoltaïque ?",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["has_solar_production"],
            reason_if_not_auto="Absence de capteur solaire : nécessite confirmation d'application ou de note.",
        )

    def _eval_ener05(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="ENER05",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La configuration des tarifs contractuels (Tempo, HP/HC, Spot) requiert confirmation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Entités de tarification à valider.",
        )

    def _eval_ener06(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="ENER06",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="L'optimisation dynamique des gros consommateurs (chauffe-eau/recharge) requiert confirmation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Logique d'optimisation énergétique à valider.",
        )

    def _eval_ener07(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="ENER07",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="L'optimisation du taux d'autoconsommation (routeur solaire / batterie) requiert confirmation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Taux d'autoconsommation et dispositifs de routage à confirmer.",
        )

    def _eval_ener08(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # DIRECT_EVIDENCE: Water meter entity declared and active
        if snapshot.has_water_meter:
            return RuleEvaluationResult(
                criterion_id="ENER08",
                status=CriterionStatus.AUTO_EVALUATED,
                proposed_score=4,
                confidence=95.0,
                evidence="Compteur d'eau et mesure volumétrique active détectés dans Home Assistant.",
                evidence_type=EvidenceType.DIRECT_EVIDENCE,
                observations_used=["has_water_meter"],
            )
        return RuleEvaluationResult(
            criterion_id="ENER08",
            status=CriterionStatus.AUTO_EVALUATED,
            proposed_score=0,
            confidence=90.0,
            evidence="Aucun compteur ou capteur de consommation d'eau détecté.",
            evidence_type=EvidenceType.DIRECT_EVIDENCE,
            observations_used=["has_water_meter"],
        )

    def _eval_ener09(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="ENER09",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La détection automatisée d'anomalies de consommation (fuite d'eau continue, veille excessive) requiert confirmation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Algorithmes d'alerte de surconsommation à valider.",
        )

    # -------------------------------------------------------------------------
    # INTER — Interopérabilité & Fonctionnement Local
    # -------------------------------------------------------------------------
    def _eval_inter01(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # CAPABILITY_EVIDENCE: Integration count does not guarantee the proportion of actual devices/functions
        local_int = len(snapshot.local_integrations)
        cloud_int = len(snapshot.cloud_integrations)
        total_int = local_int + cloud_int

        if total_int > 0:
            ratio = (local_int / total_int) * 100.0
            score = 4 if ratio >= 80.0 else (3 if ratio >= 60.0 else (2 if ratio >= 40.0 else 1))

            return RuleEvaluationResult(
                criterion_id="INTER01",
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=score,
                confidence=80.0,
                evidence=f"{local_int} intégrations locales ({', '.join(sorted(snapshot.local_integrations))}) sur {total_int} intégrations. La proportion réelle des fonctions reposant sur des protocoles locaux requiert confirmation.",
                evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
                observations_used=["local_integrations", "cloud_integrations"],
                reason_if_not_auto="Le ratio d'intégrations locales ne garantit pas la proportion réelle d'équipements physiques fonctionnant en local.",
            )

        return RuleEvaluationResult(
            criterion_id="INTER01",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Protocoles locaux à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            reason_if_not_auto="Intégrations non catégorisées.",
        )

    def _eval_inter02(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="INTER02",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=3 if len(snapshot.cloud_integrations) > 0 else 4,
            confidence=80.0,
            evidence=f"Intégrations cloud identifiées : {', '.join(sorted(snapshot.cloud_integrations)) if snapshot.cloud_integrations else 'Aucune'}. L'indépendance cloud des fonctions vitales (lumières, volets, chauffage) requiert confirmation.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["cloud_integrations"],
            reason_if_not_auto="L'absence de dépendance cloud sur les commandes de base requiert validation humaine.",
        )

    def _eval_inter03(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="INTER03",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La remplaçabilité matérielle via couches d'abstraction (groupes/labels) requiert validation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Structure des groupes d'abstraction à confirmer.",
        )

    def _eval_inter04(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # DIRECT_EVIDENCE: Direct Registry Area assignment count of entities and devices
        if snapshot.total_entities > 0:
            ratio_ent = (snapshot.entities_with_area_count / snapshot.total_entities) * 100.0
            score = 4 if ratio_ent >= 80.0 else (3 if ratio_ent >= 50.0 else (2 if ratio_ent >= 20.0 else 1))

            return RuleEvaluationResult(
                criterion_id="INTER04",
                status=CriterionStatus.AUTO_EVALUATED,
                proposed_score=score,
                confidence=98.0,
                evidence=f"{snapshot.entities_with_area_count} entités sur {snapshot.total_entities} ({ratio_ent:.1f}%) et {snapshot.devices_with_area_count}/{snapshot.total_devices} appareils affectés à une pièce (Zone/Area).",
                evidence_type=EvidenceType.DIRECT_EVIDENCE,
                observations_used=["entities_with_area_count", "total_entities", "devices_with_area_count"],
            )
        return RuleEvaluationResult(
            criterion_id="INTER04",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Organisation des pièces à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            reason_if_not_auto="Aucune entité détectée.",
        )

    def _eval_inter05(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        if snapshot.has_zigbee or snapshot.has_matter or snapshot.has_esphome:
            return RuleEvaluationResult(
                criterion_id="INTER05",
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=3,
                confidence=80.0,
                evidence="Usage important de standards ouverts (Zigbee 3.0, MQTT, ESPHome). L'absence de protocoles propriétaires fermés résiduels requiert confirmation.",
                evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
                observations_used=["has_zigbee", "has_matter", "has_mqtt", "has_esphome"],
                reason_if_not_auto="Le niveau 4/4 exige l'absence de dépendance propriétaire sur l'ensemble de l'installation.",
            )
        return RuleEvaluationResult(
            criterion_id="INTER05",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Standards domotiques à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            reason_if_not_auto="Standards non identifiés.",
        )

    def _eval_inter06(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        covered = len(snapshot.domains_present.intersection({"light", "cover", "climate", "sensor", "switch", "binary_sensor"}))
        return RuleEvaluationResult(
            criterion_id="INTER06",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=4 if (covered >= 5 and snapshot.total_entities >= 20) else 3,
            confidence=80.0,
            evidence=f"Home Assistant regroupe {covered} domaines clés ({snapshot.total_entities} entités). Le rôle de chef d'orchestre unique pour toute la famille requiert validation.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            observations_used=["domains_present", "total_entities"],
            reason_if_not_auto="L'absence d'applications tierces parallèles pour les usagers requiert confirmation.",
        )

    # -------------------------------------------------------------------------
    # UX — Confort & Expérience Utilisateur (BEHAVIORAL_EVIDENCE -> Always QUESTION)
    # -------------------------------------------------------------------------
    def _eval_ux01(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="UX01",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La présence de commandes physiques intuitives dans chaque pièce requiert confirmation humaine.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Ergonomie physique non évaluable via API.",
        )

    def _eval_ux02(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="UX02",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="L'existence d'un dashboard simplifié pour les membres du foyer requiert confirmation humaine.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Appréciation ergonomique familiale humaine.",
        )

    def _eval_ux03(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        if snapshot.has_custom_dashboards:
            return RuleEvaluationResult(
                criterion_id="UX03",
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=4 if snapshot.dashboards_count >= 3 else 3,
                confidence=80.0,
                evidence=f"{snapshot.dashboards_count} tableaux de bord personnalisés déclarés. L'adaptation ergonomique effective sur mobile/tablette requiert confirmation.",
                evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
                observations_used=["has_custom_dashboards", "dashboards_count"],
                reason_if_not_auto="La qualité de la mise en page multi-écrans requiert confirmation utilisateur.",
            )
        return RuleEvaluationResult(
            criterion_id="UX03",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=2,
            confidence=70.0,
            evidence="Adaptation aux écrans à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            reason_if_not_auto="Tableaux de bord personnalisés non quantifiés.",
        )

    def _eval_ux04(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="UX04",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La pertinence et hiérarchisation des notifications requièrent confirmation humaine.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Pertinence des notifications subjective.",
        )

    def _eval_ux05(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="UX05",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La discrétion et satisfaction du foyer quant aux automatisations requièrent validation humaine.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Satisfaction humaine non mesurable par API.",
        )

    def _eval_ux06(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="UX06",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La priorité des commandes manuelles sur les automatismes (override) requiert confirmation.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Règle d'override utilisateur à confirmer.",
        )

    def _eval_ux07(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="UX07",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La réactivité perçue (< 300ms) lors des appuis physiques requiert validation humaine.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Mesure subjective de réactivité.",
        )

    # -------------------------------------------------------------------------
    # MAINT — Maintenance & Documentation
    # -------------------------------------------------------------------------
    def _eval_maint01(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # DIRECT_EVIDENCE: Direct lexical analysis of entity_id naming across all registry entries
        if snapshot.total_entities > 0:
            ratio = (snapshot.entities_with_proper_naming_count / snapshot.total_entities) * 100.0
            score = 4 if ratio >= 99.5 else (3 if ratio >= 80.0 else (2 if ratio >= 50.0 else 1))
            return RuleEvaluationResult(
                criterion_id="MAINT01",
                status=CriterionStatus.AUTO_EVALUATED,
                proposed_score=score,
                confidence=95.0,
                evidence=f"{snapshot.entities_with_proper_naming_count} entités sur {snapshot.total_entities} ({ratio:.1f}%) respectent une convention propre sans IDs bruts (Niveau {score}/4).",
                evidence_type=EvidenceType.DIRECT_EVIDENCE,
                observations_used=["entities_with_proper_naming_count", "total_entities"],
            )
        return RuleEvaluationResult(
            criterion_id="MAINT01",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Nomenclature des entités à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            reason_if_not_auto="Aucune entité détectée.",
        )

    def _eval_maint02(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="MAINT02",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La présence d'un document récapitulatif de l'installation (IPs, schémas, matériel) requiert confirmation humaine.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Document de maintenance externe à Home Assistant.",
        )

    def _eval_maint03(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        # DIRECT_EVIDENCE: Automations with non-empty description attribute
        if snapshot.automations_count > 0:
            ratio = (snapshot.automations_with_description_count / snapshot.automations_count) * 100.0
            score = 4 if ratio >= 95.0 else (3 if ratio >= 60.0 else (2 if ratio >= 30.0 else 1))
            return RuleEvaluationResult(
                criterion_id="MAINT03",
                status=CriterionStatus.AUTO_EVALUATED,
                proposed_score=score,
                confidence=95.0,
                evidence=f"{snapshot.automations_with_description_count} automatisations sur {snapshot.automations_count} ({ratio:.1f}%) possèdent une description explicite.",
                evidence_type=EvidenceType.DIRECT_EVIDENCE,
                observations_used=["automations_with_description_count", "automations_count"],
            )
        return RuleEvaluationResult(
            criterion_id="MAINT03",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Aucune automatisation détectée.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            reason_if_not_auto="Aucune automatisation dans le registre.",
        )

    def _eval_maint04(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="MAINT04",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La politique de nettoyage régulier des entités orphelines requiert confirmation humaine.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Nettoyage des entités résiduelles à valider.",
        )

    def _eval_maint05(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        if snapshot.batteries_count > 0:
            return RuleEvaluationResult(
                criterion_id="MAINT05",
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=3 if snapshot.batteries_count >= 5 else 2,
                confidence=80.0,
                evidence=f"{snapshot.batteries_count} capteurs de piles suivis. L'existence d'un tableau de santé global (CPU, RAM, Disque, erreurs) requiert validation.",
                evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
                observations_used=["batteries_count"],
                reason_if_not_auto="Le suivi des piles ne prouve pas à lui seul une supervision technique globale.",
            )
        return RuleEvaluationResult(
            criterion_id="MAINT05",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="Suivi des batteries à confirmer.",
            evidence_type=EvidenceType.CAPABILITY_EVIDENCE,
            reason_if_not_auto="Aucun capteur de batterie détecté.",
        )

    def _eval_maint06(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="MAINT06",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La rédaction d'une procédure d'urgence pas-à-pas pour réinstaller et restaurer requiert confirmation humaine.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Procédure de PRA externe.",
        )

    def _eval_maint07(self, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        return RuleEvaluationResult(
            criterion_id="MAINT07",
            status=CriterionStatus.QUESTION_REQUIRED,
            proposed_score=None,
            confidence=0.0,
            evidence="La tenue d'un historique de modifications (Git, journal de bord ou changelog) requiert confirmation humaine.",
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            observations_used=[],
            reason_if_not_auto="Traçabilité des révisions externe.",
        )

    def _eval_default_fallback(self, criterion_id: str, snapshot: InstallationSnapshot) -> RuleEvaluationResult:
        c_def = self.repository.get_criterion(criterion_id)
        if not c_def:
            return RuleEvaluationResult(
                criterion_id=criterion_id,
                status=CriterionStatus.QUESTION_REQUIRED,
                proposed_score=None,
                confidence=0.0,
                evidence="Critère non défini.",
                evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
                reason_if_not_auto="Critère absent du référentiel.",
            )

        status = CriterionStatus.TEST_REQUIRED if c_def.default_evaluation_type == "TEST" else CriterionStatus.QUESTION_REQUIRED
        return RuleEvaluationResult(
            criterion_id=criterion_id,
            status=status,
            proposed_score=None,
            confidence=0.0,
            evidence=c_def.question,
            evidence_type=EvidenceType.BEHAVIORAL_EVIDENCE,
            reason_if_not_auto="Nécessite une validation humaine ou un test physique réel.",
        )
