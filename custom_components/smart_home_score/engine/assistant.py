"""Audit Assistant Engine for Smart Home Score v0.4.

Provides interactive question flow, dynamic branching, natural language answers,
priority ordering, safe test protocols, and non-destructive answer updates.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .models import (
    AuditResult,
    CriterionState,
    CriterionStatus,
    EvaluationSource,
    EvidenceType,
)

if TYPE_CHECKING:
    from ..criteria.repository import CriteriaRepository


@dataclass
class AnswerOption:
    """Natural language answer choice mapped to a discrete score."""

    key: str
    label: str
    score: int | None
    is_unknown: bool = False
    is_not_applicable: bool = False


@dataclass
class AssistantQuestionCard:
    """Complete structured payload for rendering a question or test card in UI."""

    criterion_id: str
    domain_code: str
    domain_name: str
    criterion_name: str
    is_critical: bool
    is_test: bool
    step_number: int
    total_steps: int
    progress_percent: float
    question_text: str
    options: list[AnswerOption]
    
    # Pre-filled proposal (if CAPABILITY_EVIDENCE)
    has_prefilled_proposal: bool = False
    proposed_label: str = ""
    proposed_score: int | None = None
    confidence_percent: float = 0.0
    evidence_text: str = ""

    # "Pourquoi ?" Explainer box (3 clear points)
    why_it_matters: str = ""
    what_was_detected: str = ""
    what_is_missing: str = ""
    technical_details: dict[str, Any] = field(default_factory=dict)

    # Safe test instructions (if is_test)
    test_objective: str = ""
    test_duration: str = ""
    test_temporary_impact: str = ""
    test_procedure_steps: list[str] = field(default_factory=list)
    test_safety_warning: str = ""

    # Current state
    current_answer_key: str | None = None


# Detailed Natural Language Question Bank for all 59 criteria
NATURAL_QUESTIONS_CONFIG: dict[str, dict[str, Any]] = {
    # -------------------------------------------------------------------------
    # ELEC — Sécurité Électrique
    # -------------------------------------------------------------------------
    "ELEC01": {
        "question": "Vos interrupteurs et commandes physiques permettent-ils de piloter l'éclairage et les volets même si le serveur Home Assistant est totalement éteint ?",
        "is_test": True,
        "test_objective": "Vérifier la pérennité des fonctions d'éclairage et d'ouverture en cas de panne totale du serveur domotique.",
        "test_duration": "2 minutes",
        "test_temporary_impact": "Aucun impact destructif. Les automatisations logicielles sont temporairement inactives.",
        "test_safety_warning": "Ne coupez pas le disjoncteur général. Vous pouvez répondre par antériorité si vous avez déjà testé cette situation.",
        "test_procedure_steps": [
            "Éteignez temporairement votre serveur Home Assistant (ou débranchez sa prise USB/secteur).",
            "Actionnez vos interrupteurs muraux dans différentes pièces.",
            "Vérifiez que les lampes s'allument et que les volets manœuvrent normalement.",
            "Rallumez votre serveur Home Assistant."
        ],
        "options": [
            AnswerOption("fully_autonomous", "Oui totalement, toutes les commandes physiques restent 100% opérationnelles", 4),
            AnswerOption("mostly_autonomous", "En grande partie, seules quelques lampes d'ambiance connectées ne répondent plus", 3),
            AnswerOption("partially_autonomous", "Partiellement, seules les pièces principales ont des commandes directes", 2),
            AnswerOption("not_autonomous", "Non, tout passe par Home Assistant (si le serveur est éteint, rien ne répond)", 0),
            AnswerOption("unknown", "Je ne sais pas / Faire ce test plus tard", None, is_unknown=True),
        ],
        "why_it_matters": "Garantit que la maison reste habitable et sûre pour toute la famille même lors d'une panne informatique.",
        "what_is_missing": "La réalité physique du câblage direct n'est pas vérifiable par les registres logiciels.",
    },
    "ELEC02": {
        "question": "Les équipements de forte puissance (chauffe-eau, borne de recharge, radiateurs) sont-ils protégés par des contacteurs de puissance adaptés au tableau ?",
        "options": [
            AnswerOption("fully_protected", "Oui, contacteurs modulaires de puissance calibrés au tableau pour chaque gros consommateur", 4),
            AnswerOption("mostly_protected", "Oui pour le chauffe-eau et la recharge, radiateurs sur modules rail DIN dédiés", 3),
            AnswerOption("partially_protected", "Partiellement, quelques micro-modules encastrés gèrent de fortes puissances", 2),
            AnswerOption("no_protection", "Non, aucune protection de relayage de puissance dédiée", 0),
            AnswerOption("unknown", "Je ne sais pas / À vérifier au tableau électrique", None, is_unknown=True),
        ],
        "why_it_matters": "Évite la surchauffe et les risques d'incendie sur les relais électroniques soumis à de fortes charges inductives/résistives.",
        "what_is_missing": "Le calibre matériel et le câblage du tableau divisionnaire sont invisibles par l'API.",
    },
    "ELEC03": {
        "question": "Avez-vous configuré un état sécurisé défini (Power-On State) sur vos actionneurs après une coupure de courant ?",
        "options": [
            AnswerOption("safe_configured", "Oui, configuré sur l'ensemble des modules (extinction ou dernier état mémorisé)", 4),
            AnswerOption("partially_configured", "Oui sur les équipements sensibles (chauffage, prises critiques), non généralisé", 3),
            AnswerOption("default_state", "Comportement par défaut d'usine conservé sur la plupart des modules", 2),
            AnswerOption("unsafe_all_on", "Non, certains équipements se rallument à pleine puissance lors du retour secteur", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Empêche l'allumage inopiné de tous les éclairages ou chauffages en pleine nuit après une brève micro-coupure.",
        "what_is_missing": "Le paramétrage des firmwares matériels après coupure est hétérogène.",
    },
    "ELEC04": {
        "question": "Vos volets roulants motorisés disposent-ils d'un interverrouillage matériel empêchant la montée et la descente simultanées ?",
        "options": [
            AnswerOption("hardware_interlock", "Oui, interverrouillage matériel par relais croisés ou boutons bistables dédiés", 4),
            AnswerOption("local_switch_interlock", "Oui au niveau des boutons physiques de commande", 3),
            AnswerOption("software_only", "Protection logicielle uniquement configurée dans Home Assistant", 2),
            AnswerOption("no_interlock", "Aucune protection particulière", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "L'alimentation simultanée des deux phases d'un moteur tubulaire peut détruire le bobinage.",
        "what_is_missing": "La présence d'entités cover ne prouve pas l'interlock mécanique ou matériel.",
    },
    "ELEC05": {
        "question": "Les accès et vannes de sécurité disposent-ils d'un déverrouillage manuel direct sans dépendance électronique ?",
        "options": [
            AnswerOption("full_manual_override", "Oui, clé physique de secours pour chaque serrure et vanne d'arrêt manuel accessible", 4),
            AnswerOption("mostly_manual", "Oui pour les accès principaux et l'eau générale", 3),
            AnswerOption("partial_override", "Déverrouillage manuel difficile d'accès ou partiel", 2),
            AnswerOption("no_manual_override", "Non, aucun moyen de secours direct en cas de panne totale", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Garantit que personne ne reste bloqué à l'extérieur ou dans l'incapacité de couper l'eau en urgence.",
        "what_is_missing": "Présence physique de barillets à clé et vannes manuelles.",
    },

    # -------------------------------------------------------------------------
    # CYBER — Cybersécurité
    # -------------------------------------------------------------------------
    "CYBER01": {
        "question": "Comment votre accès distant à Home Assistant est-il sécurisé depuis l'extérieur ?",
        "options": [
            AnswerOption("secure_tunnel_2fa", "Accès distant chiffré et sécurisé (Nabu Casa, Cloudflare Access ou VPN WireGuard/Tailscale)", 4),
            AnswerOption("reverse_proxy_tls", "Reverse Proxy HTTPS personnel (Traefik/Nginx) avec certificat TLS valide", 3),
            AnswerOption("simple_port_forward", "Simple redirection de port NAT sur ma box opérateur (ex. port 8123 ouvert)", 1),
            AnswerOption("no_remote_access", "Aucun accès extérieur (accès strictement réservé au réseau local du domicile)", 4),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Un accès distant mal protégé expose l'intégralité de la maison aux intrusions sur Internet.",
        "what_is_missing": "La typologie exacte d'accès réseau externe ne peut être déduite des seules intégrations.",
    },
    "CYBER02": {
        "question": "Avez-vous activé l'authentification à deux facteurs (2FA / TOTP) sur les comptes utilisateurs ?",
        "options": [
            AnswerOption("2fa_all_accounts", "Oui, 2FA obligatoire pour tous les utilisateurs ayant accès à distance", 4),
            AnswerOption("2fa_admin_only", "Oui, activé sur le compte administrateur principal uniquement", 3),
            AnswerOption("no_2fa_strong_pwd", "Non, mais mots de passe longs et complexes uniques", 1),
            AnswerOption("no_2fa_weak_pwd", "Non, simples mots de passe basiques", 0),
            AnswerOption("unknown", "Je ne sais pas / À vérifier", None, is_unknown=True),
        ],
        "why_it_matters": "Protège vos accès contre le vol de mot de passe et le phishing.",
        "what_is_missing": "L'état d'activation du 2FA est une donnée de sécurité privée non exposée par l'API.",
    },
    "CYBER03": {
        "question": "Chaque membre du foyer dispose-t-il de son propre compte utilisateur nominatif ?",
        "options": [
            AnswerOption("individual_accounts", "Oui, chaque membre a son compte nominatif dédié avec ses propres droits", 4),
            AnswerOption("mostly_individual", "Comptes séparés pour les adultes, compte générique pour les tablettes murales", 3),
            AnswerOption("single_shared_account", "Non, compte unique partagé par toute la famille", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet la traçabilité des actions et évite le partage imprudent des identifiants maîtres.",
        "what_is_missing": "Les entités person ne prouvent pas l'existence de comptes utilisateurs individuels.",
    },
    "CYBER04": {
        "question": "Les comptes utilisateurs courants et tablettes murales sont-ils restreints sans droits administrateur ?",
        "options": [
            AnswerOption("least_privilege_enforced", "Oui, un seul compte admin pour la maintenance, tous les autres comptes sont standard", 4),
            AnswerOption("mostly_restricted", "Tablettes murales restreintes, adultes en administrateur", 3),
            AnswerOption("all_administrators", "Non, tous les comptes possèdent les privilèges administrateur complets", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Limite l'impact d'une mauvaise manipulation ou d'un écran tactile accessible aux invités.",
        "what_is_missing": "Rôles détaillés des utilisateurs inaccessibles sans droits d'administration de bas niveau.",
    },
    "CYBER05": {
        "question": "Vos secrets, mots de passe et clés API sont-ils protégés hors des tableaux de bord et notifications ?",
        "options": [
            AnswerOption("secrets_protected", "Oui, secrets gérés via secrets.yaml et jamais affichés dans les cartes ou alertes", 4),
            AnswerOption("mostly_protected", "Oui, aucun mot de passe visible sur les écrans partagés", 3),
            AnswerOption("secrets_exposed", "Non, certains tokens ou identifiants apparaissent en clair", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Smart Home Score ne scanne jamais vos fichiers secrets par principe de confidentialité.",
        "what_is_missing": "Vérification manuelle de la non-exposition visuelle.",
    },
    "CYBER06": {
        "question": "Appliquez-vous une routine régulière de mise à jour de Home Assistant et de ses composants ?",
        "options": [
            AnswerOption("regular_monthly_updates", "Oui, mises à jour appliquées mensuellement après lecture des notes de version", 4),
            AnswerOption("frequent_updates", "Oui, mises à jour régulières dès notification dans l'interface", 3),
            AnswerOption("occasional_updates", "Mises à jour occasionnelles (tous les 3 à 6 mois)", 2),
            AnswerOption("never_updated", "Très rarement ou jamais mis à jour depuis l'installation", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Corrige rapidement les failles de sécurité découvertes et assure la compatibilité.",
        "what_is_missing": "La présence des entités update ne prouve pas la régularité de la routine humaine.",
    },
    "CYBER07": {
        "question": "Vos objets connectés (Wi-Fi / caméras) sont-ils isolés sur un réseau dédié (VLAN IoT ou Wi-Fi Invité) ?",
        "options": [
            AnswerOption("vlan_isolated", "Oui, réseau VLAN IoT étanche séparé des ordinateurs personnels et NAS", 4),
            AnswerOption("guest_wifi_isolated", "Oui, les objets Wi-Fi sont sur le Wi-Fi Invité de la box", 3),
            AnswerOption("no_isolation_secure", "Non, réseau unique mais objets connectés 100% locaux (Zigbee/Z-Wave)", 2),
            AnswerOption("no_isolation_cloud", "Non, tout est mélangé sur le même réseau avec des objets Wi-Fi Cloud", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Empêche un objet connecté vulnérable ou piraté d'accéder aux ordinateurs du foyer.",
        "what_is_missing": "L'architecture réseau de votre routeur externe n'est pas lisible via Home Assistant.",
    },
    "CYBER08": {
        "question": "Consultez-vous régulièrement les alertes de sécurité et réparations signalées dans Home Assistant ?",
        "options": [
            AnswerOption("proactive_monitoring", "Oui, vérification régulière des réparations et alertes de sécurité", 4),
            AnswerOption("occasional_check", "Consultation occasionnelle lors des mises à jour", 3),
            AnswerOption("ignore_alerts", "Non, alertes de réparation généralement ignorées", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet de traiter rapidement les intégrations dépréciées ou les alertes de vulnérabilité.",
        "what_is_missing": "Habitude humaine de consultation non automatisable.",
    },

    # -------------------------------------------------------------------------
    # RES — Résilience & Continuité
    # -------------------------------------------------------------------------
    "RES01": {
        "question": "Vos automatisations locales et commandes physiques fonctionnent-elles lors d'une coupure de votre box Internet ?",
        "is_test": True,
        "test_objective": "Valider l'autonomie de la maison en cas de panne de fibre ou de box opérateur.",
        "test_duration": "2 minutes",
        "test_temporary_impact": "Accès distant temporairement coupé pendant le test.",
        "test_safety_warning": "Test 100% sans danger. Vous pouvez répondre par antériorité si une coupure Internet est déjà survenue.",
        "test_procedure_steps": [
            "Débranchez le câble réseau RJ45 ou éteignez le Wi-Fi de votre box opérateur.",
            "Testez l'allumage des pièces et vos automatisations essentielles.",
            "Rebranchez votre box Internet."
        ],
        "options": [
            AnswerOption("full_local_autonomy", "Oui totalement, tout fonctionne parfaitement en local sans aucune perte", 4),
            AnswerOption("most_local_autonomy", "Oui pour les fonctions vitales, seuls les services météo/cloud sont coupés", 3),
            AnswerOption("partial_local_autonomy", "Partiellement, les boutons marchent mais l'application locale est bloquée", 2),
            AnswerOption("no_autonomy_cloud_blocked", "Non, tout est bloqué dès que la box Internet est coupée", 0),
            AnswerOption("unknown", "Je ne sais pas / Faire ce test plus tard", None, is_unknown=True),
        ],
        "why_it_matters": "Votre domicile ne doit pas dépendre de la qualité de connexion de votre opérateur.",
        "what_is_missing": "Un test physique de déconnexion est indispensable pour le prouver.",
    },
    "RES02": {
        "question": "En cas de panne matérielle du serveur, vos éclairages et volets sont-ils manœuvrables directement ?",
        "is_test": True,
        "test_objective": "Vérifier la redondance des commandes matérielles sans serveur domotique.",
        "test_duration": "1 minute",
        "test_temporary_impact": "Aucun. Équivalent à la coupure du serveur.",
        "test_safety_warning": "Ne coupez pas le disjoncteur général.",
        "test_procedure_steps": [
            "Vérifiez que vos boutons muraux sont câblés directement aux télérupteurs ou modules bistables.",
            "Confirmez qu'un invité ou secours peut allumer la lumière sans interface domotique."
        ],
        "options": [
            AnswerOption("fully_redundant", "Oui, 100% des points lumineux et volets ont une commande matérielle directe", 4),
            AnswerOption("mostly_redundant", "Oui pour les pièces principales et circulations", 3),
            AnswerOption("partially_redundant", "Quelques pièces dépendent exclusivement de Home Assistant", 2),
            AnswerOption("no_redundancy", "Non, aucune commande directe sans serveur", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Assure la sécurité des occupants même si le mini-PC ou Raspberry Pi tombe en panne.",
        "what_is_missing": "Le schéma unifilaire de câblage matériel n'est pas accessible par l'API.",
    },
    "RES03": {
        "question": "Recevez-vous une alerte proactive automatique lorsqu'un capteur ou équipement devient indisponible ?",
        "options": [
            AnswerOption("proactive_alerts", "Oui, notification automatique immédiate sur smartphone en cas de panne ou déconnexion", 4),
            AnswerOption("dashboard_alert", "Oui, panneau d'alerte visible sur le tableau de bord technique", 3),
            AnswerOption("manual_check", "Non, vérification manuelle occasionnelle dans la liste des entités", 1),
            AnswerOption("no_monitoring", "Aucune surveillance des équipements déconnectés", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet de détecter immédiatement un capteur de fuite ou de sécurité hors ligne.",
        "what_is_missing": "La liste des entités indisponibles ne prouve pas l'existence d'une alerte proactive.",
    },
    "RES04": {
        "question": "Votre réseau maillé sans fil (Zigbee / Z-Wave / Matter) est-il stable avec un maillage dense de routeurs ?",
        "options": [
            AnswerOption("dense_stable_mesh", "Oui, réseau très stable avec des routeurs alimentés sur secteur dans chaque pièce", 4),
            AnswerOption("good_mesh", "Réseau globalement stable avec quelques routeurs stratégiques", 3),
            AnswerOption("weak_mesh", "Quelques déconnexions occasionnelles sur les capteurs éloignés", 2),
            AnswerOption("unstable_mesh", "Réseau instable avec pertes de connexion fréquentes", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Un bon maillage radio garantit la réactivité et évite l'épuisement prématuré des piles.",
        "what_is_missing": "Le nombre d'appareils ne renseigne pas sur la qualité radio et la stabilité dans le temps.",
    },
    "RES05": {
        "question": "Vos sauvegardes Home Assistant sont-elles automatisées de manière régulière et programmée ?",
        "options": [
            AnswerOption("automated_daily_backups", "Oui, sauvegarde automatique programmée (quotidienne ou hebdomadaire) avec rétention tournante", 4),
            AnswerOption("automated_backups", "Oui, sauvegardes automatiques activées", 3),
            AnswerOption("manual_backups_only", "Sauvegardes manuelles uniquement avant les grosses mises à jour", 2),
            AnswerOption("no_backups", "Aucune sauvegarde configurée", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet de restaurer votre installation en quelques minutes en cas de corruption de carte SD ou disque.",
        "what_is_missing": "La présence du module backup ne garantit pas la planification et le succès des exécutions.",
    },
    "RES06": {
        "question": "Vos sauvegardes sont-elles automatiquement copiées hors du serveur (Google Drive, NAS, Nextcloud, clé USB) ?",
        "options": [
            AnswerOption("offsite_automatic", "Oui, synchronisation automatique vers un stockage distant ou NAS sécurisé", 4),
            AnswerOption("local_nas_backup", "Oui, copie automatique sur un NAS local ou partage réseau", 3),
            AnswerOption("manual_download", "Téléchargement manuel occasionnel d'une copie sur mon ordinateur", 2),
            AnswerOption("server_disk_only", "Non, les sauvegardes restent uniquement stockées sur le disque du serveur", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Si le disque dur ou la carte mémoire du serveur brûle, les sauvegardes locales sont perdues.",
        "what_is_missing": "L'exportation vers un stockage tiers externe n'est pas vérifiable via l'API standard.",
    },
    "RES07": {
        "question": "Avez-vous déjà testé et validé la procédure de restauration d'une sauvegarde complète ?",
        "is_test": True,
        "test_objective": "S'assurer qu'une sauvegarde est réellement exploitable et restaurable sans mauvaise surprise.",
        "test_duration": "Procédure d'audit déclarative / Test sur machine secondaire",
        "test_temporary_impact": "Aucun sur votre serveur principal.",
        "test_safety_warning": "NE RESTAUREZ JAMAIS VOTRE SERVEUR DE PRODUCTION POUR CE TEST. Répondez selon vos tests passés ou vérifications.",
        "test_procedure_steps": [
            "Téléchargez une archive de sauvegarde .tar sur votre ordinateur.",
            "Vérifiez que le fichier n'est pas vide et s'ouvre correctement.",
            "Si possible, testez la restauration sur une machine virtuelle de test (ex. VirtualBox / Proxmox)."
        ],
        "options": [
            AnswerOption("tested_on_secondary", "Oui, restauration déjà testée avec succès sur une machine de secours / VM", 4),
            AnswerOption("archive_integrity_verified", "Oui, archive téléchargée et son intégrité/contenu ont été vérifiés", 3),
            AnswerOption("backups_created_not_tested", "Sauvegardes créées mais restauration jamais testée sur un autre matériel", 2),
            AnswerOption("never_verified", "Non, aucune sauvegarde testée ou vérifiée", 0),
            AnswerOption("unknown", "Je ne sais pas / Faire plus tard", None, is_unknown=True),
        ],
        "why_it_matters": "Une sauvegarde non testée n'offre aucune garantie de fonctionnement le jour d'un crash réel.",
        "what_is_missing": "L'exercice pratique de restauration est une action humaine externe.",
    },
    "RES08": {
        "question": "Votre serveur Home Assistant et votre box/switch sont-ils protégés par un onduleur (UPS) ou batterie de secours ?",
        "options": [
            AnswerOption("ups_monitored", "Oui, onduleur présent avec extinction propre automatique via USB/réseau", 4),
            AnswerOption("ups_unmonitored", "Oui, onduleur présent assurant le maintien de l'alimentation lors des coupures", 3),
            AnswerOption("surge_protector_only", "Non, simple prise parasurtenseur sans batterie de secours", 2),
            AnswerOption("no_ups", "Non, aucune protection électrique particulière", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Évite la corruption de la base de données SQLite/MariaDB lors des micro-coupures de courant.",
        "what_is_missing": "La présence d'un onduleur non communicant n'est pas détectable par logiciel.",
    },

    # -------------------------------------------------------------------------
    # AUTO — Intelligence & Automatisations
    # -------------------------------------------------------------------------
    "AUTO01": {
        "question": "Vos éclairages s'adaptent-ils automatiquement selon la présence, la luminosité ou le moment de la journée ?",
        "options": [
            AnswerOption("fully_adaptive_lighting", "Oui, extinction automatique et adaptation de luminosité/teinte selon le moment", 4),
            AnswerOption("presence_automations", "Oui, allumage et extinction automatique sur détection de présence dans les pièces de passage", 3),
            AnswerOption("simple_schedules", "Simples programmations horaires (ex. allumage extérieur au coucher du soleil)", 2),
            AnswerOption("manual_lighting_only", "Non, tout est allumé et éteint manuellement", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Apporte du confort au quotidien et évite le gaspillage électrique des lumières oubliées.",
        "what_is_missing": "La logique fine et les conditions des automatisations requièrent validation.",
    },
    "AUTO02": {
        "question": "Votre chauffage/climatisation s'adapte-t-il automatiquement aux présences, ouvertures de fenêtres et prévisions ?",
        "options": [
            AnswerOption("advanced_climate_control", "Oui, abaissement automatique sur ouverture de fenêtre, absence et anticipation météo", 4),
            AnswerOption("presence_climate_control", "Oui, régulation automatique selon présence/absence et plannings hebdomadaires", 3),
            AnswerOption("simple_thermostats", "Régulation par simple consigne horaire ou thermostat classique", 2),
            AnswerOption("manual_climate_only", "Non, réglage purement manuel", 0),
            AnswerOption("not_applicable", "Sans objet (Aucun chauffage ni climatisation pilotable)", None, is_not_applicable=True),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Le chauffage représente le premier poste de consommation d'un logement.",
        "what_is_missing": "La logique des scénarios thermiques avancés requiert confirmation.",
    },
    "AUTO03": {
        "question": "Votre ventilation (VMC) est-elle automatiquement asservie selon le taux d'humidité ou la qualité de l'air ?",
        "options": [
            AnswerOption("humidity_adaptive_vmc", "Oui, passage automatique en grand débit sur détection d'humidité (douche/cuisine) puis retour au calme", 4),
            AnswerOption("scheduled_vmc", "Pilotage selon horaires programmés ou présence", 3),
            AnswerOption("continuous_vmc", "VMC classique tournant en continu sans régulation intelligente", 2),
            AnswerOption("no_vmc_control", "Aucun pilotage de la ventilation", 0),
            AnswerOption("not_applicable", "Sans objet (Pas de VMC pilotable dans le logement)", None, is_not_applicable=True),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Évacue rapidement l'humidité des pièces d'eau tout en limitant les pertes de chaleur en hiver.",
        "what_is_missing": "L'association logique entre capteurs d'humidité et commande VMC doit être confirmée.",
    },
    "AUTO04": {
        "question": "Vos volets roulants s'ouvrent et se ferment-ils automatiquement selon le soleil, la saison et la météo ?",
        "options": [
            AnswerOption("bioclimatic_shading", "Oui, gestion bioclimatique (protection solaire en été, apport thermique en hiver, vent fort)", 4),
            AnswerOption("solar_schedules", "Oui, ouverture/fermeture automatique au lever et coucher du soleil", 3),
            AnswerOption("fixed_schedules", "Programmation à heures fixes uniquement", 2),
            AnswerOption("manual_covers_only", "Non, manœuvres 100% manuelles", 0),
            AnswerOption("not_applicable", "Sans objet (Aucun volet roulant motorisé)", None, is_not_applicable=True),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Améliore le confort thermique d'été passif et sécurise la fermeture des accès la nuit.",
        "what_is_missing": "L'algorithme de positionnement solaire bioclimatique requiert confirmation.",
    },
    "AUTO05": {
        "question": "En cas de détection de fuite d'eau, votre installation coupe-t-elle automatiquement l'arrivée d'eau ?",
        "options": [
            AnswerOption("auto_shutoff_valve", "Oui, fermeture automatique immédiate de la vanne générale + alerte push", 4),
            AnswerOption("alert_with_valve", "Alerte push immédiate avec bouton de fermeture à distance de la vanne", 3),
            AnswerOption("alert_only", "Alerte push uniquement (capteurs de fuite sans vanne motorisée)", 2),
            AnswerOption("no_leak_protection", "Aucune détection ni protection contre les fuites", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Limite considérablement l'ampleur des dégâts des eaux lors d'une rupture de canalisation.",
        "what_is_missing": "La liaison automatique entre les capteurs d'inondation et la vanne requiert validation.",
    },
    "AUTO06": {
        "question": "Recevez-vous une notification lorsque vos appareils électroménagers (lave-linge, lave-vaisselle) terminent leur cycle ?",
        "options": [
            AnswerOption("cycle_tracking_notifications", "Oui, notification automatique sur fin de cycle et rappel si la porte n'est pas vidée", 4),
            AnswerOption("simple_cycle_alert", "Oui, notification simple sur fin de consommation électrique", 3),
            AnswerOption("power_monitoring_only", "Mesure de consommation uniquement, sans notification de cycle", 2),
            AnswerOption("no_appliance_tracking", "Non, aucun suivi des cycles des appareils", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Évite d'oublier le linge humide dans le tambour et optimise le temps des tâches ménagères.",
        "what_is_missing": "La mesure électrique ne prouve pas l'existence de l'automatisation de notification de fin de cycle.",
    },
    "AUTO07": {
        "question": "Votre logement adapte-t-il automatiquement son comportement selon l'occupation réelle du foyer ?",
        "options": [
            AnswerOption("adaptive_occupancy", "Oui, scénarios complets Présent / Absent / Nuit / Vacances activés automatiquement selon les personnes", 4),
            AnswerOption("basic_occupancy", "Oui, passage automatique en mode Absence lorsque tout le monde quitte la maison", 3),
            AnswerOption("manual_modes", "Changement manuel des modes de maison via un bouton ou l'application", 2),
            AnswerOption("no_occupancy_modes", "Non, aucun scénario lié à la présence", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Garantit que les lumières s'éteignent et que la sécurité s'arme dès que la maison est vide.",
        "what_is_missing": "L'utilisation effective des trackers et capteurs dans les scénarios requiert confirmation.",
    },
    "AUTO08": {
        "question": "Vos automatisations prennent-elles en compte le contexte global (mode Invité, sommeil, jour férié, télétravail) ?",
        "options": [
            AnswerOption("rich_context_helpers", "Oui, prise en compte des modes Invité, télétravail, réveil et jours fériés", 4),
            AnswerOption("basic_context", "Prise en compte des modes Jour / Nuit / Travail", 3),
            AnswerOption("simple_triggers", "Automatisations simples déclenchées sans conditions contextuelles", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Évite les allumages intempestifs lorsqu'un invité dort dans le salon ou un jour férié.",
        "what_is_missing": "Les helpers de contexte déclarés doivent être confirmés dans leur usage.",
    },
    "AUTO09": {
        "question": "Vos actions critiques (arrosage, fermeture de porte de garage, pompe) sont-elles sécurisées par des boucles de vérification ?",
        "options": [
            AnswerOption("verification_loops_safety", "Oui, temporisation de sécurité (auto-off), vérification d'état et alerte si l'ordre échoue", 4),
            AnswerOption("basic_safety_timer", "Oui, minuterie d'extinction de sécurité (auto-off)", 3),
            AnswerOption("no_verification", "Non, simple envoi de commande sans contrôle de confirmation", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Évite qu'une vanne d'arrosage reste ouverte indéfiniment ou qu'un garage reste entrouvert.",
        "what_is_missing": "Structure des scripts de contrôle à valider.",
    },

    # -------------------------------------------------------------------------
    # ENER — Énergie & Ressources (Questions complémentaires)
    # -------------------------------------------------------------------------
    "ENER05": {
        "question": "Votre installation intègre-t-elle votre contrat d'électricité (Tempo, Heures Pleines / Heures Creuses, Tarif Spot) ?",
        "options": [
            AnswerOption("dynamic_tariffs", "Oui, tarification dynamique intégrée (Tempo / HP-HC / Prix Spot) avec anticipation tarifaire", 4),
            AnswerOption("static_hphc", "Oui, heures creuses intégrées pour déclencher les appareils au meilleur tarif", 3),
            AnswerOption("fixed_price", "Tarif fixe simple ou pas de prise en compte des tarifs", 2),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet de réaliser d'importantes économies en décalant les consommations sur les heures les moins chères.",
        "what_is_missing": "Entités de tarification contractuelle à valider.",
    },
    "ENER06": {
        "question": "Les gros consommateurs (chauffe-eau, recharge de véhicule, pompe) sont-ils automatiquement décalés sur les heures économiques ?",
        "options": [
            AnswerOption("automatic_load_shifting", "Oui, pilotage automatique dynamique sur les heures les moins chères ou en surplus solaire", 4),
            AnswerOption("scheduled_load_shifting", "Oui, programmation fixe sur les heures creuses", 3),
            AnswerOption("manual_shifting", "Décalage manuel par les membres du foyer", 2),
            AnswerOption("no_load_shifting", "Non, allumage à n'importe quel moment", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Réduit directement votre facture électrique sans impacter votre confort.",
        "what_is_missing": "La logique d'optimisation énergétique dynamique doit être confirmée.",
    },
    "ENER07": {
        "question": "Optimisez-vous votre taux d'autoconsommation solaire (routeur solaire, batterie ou déclenchement dynamique) ?",
        "options": [
            AnswerOption("optimized_solar_surplus", "Oui, routeur solaire vers le chauffe-eau ou batterie de stockage maximisant l'autoconsommation", 4),
            AnswerOption("automation_on_surplus", "Oui, automatisation déclenchant des appareils lors d'un excédent de production", 3),
            AnswerOption("no_solar_routing", "Non, le surplus non consommé est réinjecté sur le réseau sans routage dédié", 2),
            AnswerOption("not_applicable", "Sans objet (Aucune production solaire photovoltaïque)", None, is_not_applicable=True),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Chaque kWh solaire consommé localement évite un achat au réseau au prix fort.",
        "what_is_missing": "La présence d'un routeur de surplus ou batterie physique requiert confirmation.",
    },
    "ENER09": {
        "question": "Recevez-vous une alerte automatique en cas d'anomalie de consommation (fuite d'eau continue, surconsommation anormale) ?",
        "options": [
            AnswerOption("anomaly_alerts_water_elec", "Oui, détection automatique de fuite continue (eau la nuit) et pic électrique anormal avec alerte", 4),
            AnswerOption("water_anomaly_only", "Oui pour les fuites d'eau continues", 3),
            AnswerOption("no_anomaly_detection", "Non, aucune alerte de surconsommation continue", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet de couper une fuite d'eau invisible ou un appareil resté allumé par erreur avant la facture.",
        "what_is_missing": "Algorithmes de détection d'anomalies à valider.",
    },

    # -------------------------------------------------------------------------
    # INTER — Interopérabilité
    # -------------------------------------------------------------------------
    "INTER01": {
        "question": "Vos équipements domotiques fonctionnent-ils majoritairement sur des protocoles locaux et indépendants du Cloud ?",
        "options": [
            AnswerOption("fully_local", "Oui totalement (Plus de 80% des équipements fonctionnent en 100% local)", 4),
            AnswerOption("mostly_local", "En grande partie (Entre 50% et 80% local)", 3),
            AnswerOption("partially_local", "Partiellement (Moins de 50% local, fort usage du Cloud)", 2),
            AnswerOption("mostly_cloud", "Non, dépendance quasi-totale au Cloud", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Garantit la pérennité, la rapidité d'exécution et la vie privée de votre installation.",
        "what_is_missing": "Le ratio d'intégrations ne garantit pas la proportion exacte d'équipements physiques.",
    },
    "INTER02": {
        "question": "Les fonctions vitales de votre maison (lumières, volets, chauffage) sont-elles totalement indépendantes du Cloud ?",
        "options": [
            AnswerOption("vital_functions_100_local", "Oui, 100% des commandes vitales fonctionnent sans aucun service cloud", 4),
            AnswerOption("vital_functions_mostly_local", "Oui, seuls des services annexes (météo, notifications) utilisent le cloud", 3),
            AnswerOption("vital_functions_cloud_dependent", "Non, certaines lampes ou thermostats vitaux nécessitent le cloud fabricant", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Évite d'être privé de chauffage ou de lumière lors d'une panne de serveur distant fabricant.",
        "what_is_missing": "L'indépendance cloud des fonctions de base requiert validation humaine.",
    },
    "INTER03": {
        "question": "Utilisez-vous des couches d'abstraction (groupes, scènes, scripts génériques) facilitant le remplacement d'un matériel défaillant ?",
        "options": [
            AnswerOption("full_abstraction_layers", "Oui, utilisation de groupes et labels : remplacer une ampoule ne casse aucune automatisation", 4),
            AnswerOption("mostly_abstracted", "Oui pour les pièces principales et groupes de volets", 3),
            AnswerOption("direct_entity_binding", "Non, les entity_id physiques sont directement saisis dans chaque automatisation", 2),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet de remplacer un capteur ou module cassé en 30 secondes sans réécrire 10 scénarios.",
        "what_is_missing": "La structure des groupes d'abstraction requiert confirmation.",
    },
    "INTER05": {
        "question": "Votre installation repose-t-elle sur des protocoles et standards ouverts (Zigbee, Matter, MQTT, ESPHome, Z-Wave) ?",
        "options": [
            AnswerOption("open_standards_only", "Oui, architecture fondée quasi-exclusivement sur des standards ouverts interopérables", 4),
            AnswerOption("mostly_open_standards", "Oui majoritairement, avec quelques passerelles propriétaires spécifiques", 3),
            AnswerOption("proprietary_ecosystems", "Mélange de plusieurs écosystèmes propriétaires fermés", 2),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Évite l'enfermement propriétaire et assure la disponibilité de pièces de rechange multi-marques.",
        "what_is_missing": "Le niveau 4/4 exige l'absence de tout protocole propriétaire fermé.",
    },
    "INTER06": {
        "question": "Home Assistant centralise-t-il l'intégralité du pilotage de votre maison comme chef d'orchestre unique pour le foyer ?",
        "options": [
            AnswerOption("centralized_orchestrator", "Oui, Home Assistant est le chef d'orchestre unique utilisé par toute la famille", 4),
            AnswerOption("mostly_centralized", "Oui pour 80% des usages, quelques applications fabricants spécifiques restent ouvertes", 3),
            AnswerOption("fragmented_apps", "Non, multiplication d'applications mobiles distinctes selon les marques", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Simplifie l'expérience des occupants et permet aux différents équipements de communiquer ensemble.",
        "what_is_missing": "L'absence d'applications tierces parallèles pour les usagers requiert confirmation.",
    },

    # -------------------------------------------------------------------------
    # UX — Confort & Expérience Utilisateur
    # -------------------------------------------------------------------------
    "UX01": {
        "question": "Chaque pièce dispose-t-elle de commandes physiques évidentes et utilisables intuitivement par un invité ?",
        "options": [
            AnswerOption("fully_intuitive_switches", "Oui, boutons muraux classiques ou gravés compréhensibles immédiatement par n'importe quel invité", 4),
            AnswerOption("mostly_intuitive", "Oui, commandes claires avec quelques boutons multifonctions dans les pièces secondaires", 3),
            AnswerOption("complex_controls", "Non, certaines pièces nécessitent d'expliquer comment allumer la lumière", 1),
            AnswerOption("app_only_controls", "Certaines pièces ne se contrôlent que via smartphone ou tablette", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "La domotique doit simplifier la vie de tous, sans créer de frustration pour les proches ou invités.",
        "what_is_missing": "L'ergonomie physique et l'appréciation des occupants ne sont pas mesurables par API.",
    },
    "UX02": {
        "question": "Les membres de votre foyer disposent-ils d'un tableau de bord simplifié et épuré adapté à leurs besoins quotidiens ?",
        "options": [
            AnswerOption("dedicated_family_dashboard", "Oui, vue dédiée épurée et intuitive utilisée facilement par les proches", 4),
            AnswerOption("adapted_view", "Oui, tableau de bord unique bien organisé par pièce", 3),
            AnswerOption("technical_cluttered_dashboard", "Non, tableau de bord technique surchargé de jauges et boutons", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Favorise l'adhésion et le plaisir d'utilisation au quotidien pour l'ensemble du foyer.",
        "what_is_missing": "L'appréciation esthétique et ergonomique relève du retour utilisateur.",
    },
    "UX03": {
        "question": "Vos tableaux de bord s'adaptent-ils confortablement aux différents écrans (smartphone, tablette murale, ordinateur) ?",
        "options": [
            AnswerOption("responsive_dashboards", "Oui, vues spécifiques ou cartes adaptatives optimisées pour chaque taille d'écran", 4),
            AnswerOption("mostly_responsive", "Oui, affichage correct sur mobile et PC", 3),
            AnswerOption("poor_mobile_experience", "Non, navigation difficile sur petit écran de smartphone", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet une utilisation fluide et rapide sans défilement horizontal ou boutons tronqués.",
        "what_is_missing": "L'ergonomie multi-écrans requiert validation utilisateur.",
    },
    "UX04": {
        "question": "Vos notifications sont-elles pertinentes, ciblées et sans alertes répétitives inutiles ?",
        "options": [
            AnswerOption("relevant_targeted_alerts", "Oui, alertes uniquement sur événements utiles et ciblées sur la bonne personne", 4),
            AnswerOption("mostly_relevant", "Notifications utiles avec quelques alertes secondaires", 3),
            AnswerOption("notification_fatigue", "Trop de notifications reçues au quotidien (fatigue informationnelle)", 1),
            AnswerOption("no_notifications", "Aucune notification configurée", 2),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Une alerte n'a de valeur que si elle est lue et traitée sans lasser l'utilisateur.",
        "what_is_missing": "La pertinence perçue des messages est une notion subjective.",
    },
    "UX05": {
        "question": "Vos automatisations sont-elles discrètes et appréciées par l'ensemble des membres du foyer ?",
        "options": [
            AnswerOption("high_family_satisfaction", "Oui, forte adhésion, les automatisations fonctionnent sans se faire remarquer", 4),
            AnswerOption("good_satisfaction", "Bonne satisfaction générale du foyer", 3),
            AnswerOption("some_frustrations", "Quelques agacements occasionnels (ex. lumière qui s'éteint trop vite)", 2),
            AnswerOption("rejected_automations", "Rejet ou contestation de certaines automatisations par les proches", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "La meilleure domotique est celle qui sait se faire oublier et rend service naturellement.",
        "what_is_missing": "La satisfaction humaine du foyer ne peut être mesurée par API.",
    },
    "UX06": {
        "question": "Une action manuelle (appui sur un interrupteur) est-elle toujours prioritaire sur les automatismes ?",
        "options": [
            AnswerOption("manual_override_priority", "Oui, commande manuelle toujours prioritaire avec suspension temporaire de l'automatisme", 4),
            AnswerOption("mostly_prioritized", "Oui sur la plupart des éclairages et volets", 3),
            AnswerOption("automations_override_user", "Non, certains automatismes écrasent les actions manuelles des utilisateurs", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Garantit que l'humain garde toujours le contrôle final sur son environnement.",
        "what_is_missing": "La règle d'override manuel requiert validation.",
    },
    "UX07": {
        "question": "Les commandes physiques et éclairages réagissent-ils instantanément (en moins de 300 millisecondes) ?",
        "options": [
            AnswerOption("instant_response", "Oui, réponse instantanée sans aucun délai perceptible lors de l'appui", 4),
            AnswerOption("fast_response", "Réponse rapide (faible latence tout à fait acceptable)", 3),
            AnswerOption("noticeable_delay", "Délai perceptible gênant (latence > 1 seconde sur certains appareils)", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Une latence trop importante donne l'impression d'un dysfonctionnement et incite à réappuyer.",
        "what_is_missing": "La réactivité perçue est une mesure humaine.",
    },

    # -------------------------------------------------------------------------
    # MAINT — Maintenance & Documentation
    # -------------------------------------------------------------------------
    "MAINT02": {
        "question": "Disposez-vous d'un document récapitulatif de votre installation (schéma, adresses IP fixes, matériel, identifiants) ?",
        "options": [
            AnswerOption("complete_documentation", "Oui, documentation claire et à jour permettant à un tiers de comprendre l'installation", 4),
            AnswerOption("basic_documentation", "Oui, liste des adresses IP et notes de base conservées", 2),
            AnswerOption("no_documentation", "Non, tout est dans ma mémoire sans aucune documentation écrite", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet de dépanner sereinement des mois plus tard ou d'aider un proche en cas d'absence.",
        "what_is_missing": "Document externe à Home Assistant non lisible par logiciel.",
    },
    "MAINT04": {
        "question": "Nettoyez-vous régulièrement les entités orphelines, appareils déconnectés et intégrations inutilisées ?",
        "options": [
            AnswerOption("regular_registry_cleaning", "Oui, registre propre : entités et intégrations orphelines supprimées régulièrement", 4),
            AnswerOption("occasional_cleaning", "Nettoyage occasionnel lors des changements de matériel", 3),
            AnswerOption("no_cleaning", "Non, nombreuses entités orphelines ou résiduelles conservées", 1),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Conserve un système rapide, une base de données allégée et évite les erreurs dans les logs.",
        "what_is_missing": "La politique de nettoyage régulier requiert confirmation.",
    },
    "MAINT05": {
        "question": "Disposez-vous d'une vue de surveillance de la santé technique globale (piles des capteurs, CPU, disque, erreurs) ?",
        "options": [
            AnswerOption("full_health_dashboard", "Oui, tableau de bord technique surveillant piles, espace disque, charge CPU et erreurs", 4),
            AnswerOption("battery_and_disk_monitoring", "Oui, surveillance des piles et de l'espace disque", 3),
            AnswerOption("battery_monitoring_only", "Surveillance des niveaux de piles uniquement", 2),
            AnswerOption("no_health_dashboard", "Aucune surveillance de santé technique", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet d'anticiper le remplacement d'une pile ou la saturation du disque avant la panne.",
        "what_is_missing": "La surveillance des piles ne prouve pas à elle seule une supervision globale du serveur.",
    },
    "MAINT06": {
        "question": "Avez-vous rédigé une procédure de secours pas-à-pas pour réinstaller et restaurer votre système en cas de sinistre ?",
        "options": [
            AnswerOption("emergency_recovery_procedure", "Oui, procédure écrite étape par étape pour réinstaller et restaurer le système", 4),
            AnswerOption("basic_recovery_notes", "Quelques notes mémos sur la procédure de réinstallation", 2),
            AnswerOption("no_recovery_procedure", "Non, aucune procédure de reprise d'urgence rédigée", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Évite le stress et les erreurs lors du remplacement d'un matériel défaillant en urgence.",
        "what_is_missing": "Procédure de PRA externe.",
    },
    "MAINT07": {
        "question": "Tenez-vous un journal de bord, changelog ou historique de vos modifications importantes (Git / notes) ?",
        "options": [
            AnswerOption("git_or_changelog_tracking", "Oui, historique tenu rigoureusement (dépôt Git ou journal de bord des modifications)", 4),
            AnswerOption("occasional_notes", "Notes occasionnelles prises lors des changements majeurs", 2),
            AnswerOption("no_changelog", "Non, aucun historique des modifications", 0),
            AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
        ],
        "why_it_matters": "Permet de comprendre immédiatement ce qui a été modifié lorsqu'un comportement imprévu survient.",
        "what_is_missing": "Traçabilité des révisions externe.",
    },
}


class AuditAssistant:
    """Manages the interactive audit flow, question cards, branching and responses."""

    def __init__(self, repository: CriteriaRepository) -> None:
        """Initialize the audit assistant."""
        self.repository = repository

    def get_ordered_criteria_list(
        self,
        criteria_states: dict[str, CriterionState],
    ) -> list[str]:
        """Compute the smart prioritized list of criteria for the audit."""
        all_criteria = [self.repository.get_criterion(cid) for cid in self.repository.criteria]
        all_criteria = [c for c in all_criteria if c is not None]

        # 1. Evaluate branching to exclude NOT_APPLICABLE criteria
        applicable_criteria: list[Any] = []
        for c in all_criteria:
            st = criteria_states.get(c.id)
            if st and (st.status == CriterionStatus.NOT_APPLICABLE or not st.applicable):
                continue
            applicable_criteria.append(c)

        # Separate into categories
        critical_list = []
        high_gain_list = []
        prefilled_list = []
        other_list = []
        tests_list = []

        for c in applicable_criteria:
            st = criteria_states.get(c.id)
            status = st.status if st else CriterionStatus.NOT_EVALUATED
            is_auto = (status == CriterionStatus.AUTO_EVALUATED)
            is_test = (status == CriterionStatus.TEST_REQUIRED or c.default_evaluation_type == "TEST")
            has_prefill = (st and st.auto_score is not None and st.confidence >= 70.0 and not is_auto)

            if is_auto:
                continue

            if is_test:
                tests_list.append(c.id)
            elif c.critical:
                critical_list.append(c.id)
            elif has_prefill:
                prefilled_list.append(c.id)
            elif c.weight >= 15:
                high_gain_list.append(c.id)
            else:
                other_list.append(c.id)

        # Deterministic combined order
        return critical_list + high_gain_list + prefilled_list + other_list + tests_list

    def get_next_pending_criterion_id(
        self,
        criteria_states: dict[str, CriterionState],
    ) -> str | None:
        """Find the next unanswered criterion in priority order."""
        ordered = self.get_ordered_criteria_list(criteria_states)
        for cid in ordered:
            st = criteria_states.get(cid)
            if not st or (not st.user_confirmed and st.status not in [CriterionStatus.AUTO_EVALUATED, CriterionStatus.CONFIRMED, CriterionStatus.NOT_APPLICABLE]):
                return cid
        return None

    def build_question_card(
        self,
        criterion_id: str,
        criteria_states: dict[str, CriterionState],
    ) -> AssistantQuestionCard | None:
        """Build the structured question card payload for the UI."""
        c_def = self.repository.get_criterion(criterion_id)
        if not c_def:
            return None

        cfg = NATURAL_QUESTIONS_CONFIG.get(criterion_id, {})
        st = criteria_states.get(criterion_id)

        ordered_list = self.get_ordered_criteria_list(criteria_states)
        total_steps = len(ordered_list)
        try:
            step_number = ordered_list.index(criterion_id) + 1
        except ValueError:
            step_number = 1

        completed_count = sum(
            1 for cid in ordered_list
            if criteria_states.get(cid) and (criteria_states[cid].user_confirmed or criteria_states[cid].status == CriterionStatus.CONFIRMED)
        )
        progress_pct = (completed_count / total_steps * 100.0) if total_steps > 0 else 0.0

        # Natural language options
        options = cfg.get("options", [])
        if not options:
            options = [
                AnswerOption("yes", "Oui totalement", 4),
                AnswerOption("mostly", "Partiellement", 2),
                AnswerOption("no", "Non", 0),
                AnswerOption("unknown", "Je ne sais pas", None, is_unknown=True),
            ]

        # Prefilled proposal
        has_prefill = bool(st and st.auto_score is not None and st.confidence >= 70.0 and st.status != CriterionStatus.AUTO_EVALUATED)
        proposed_label = ""
        if has_prefill and st and st.auto_score is not None:
            # Find matching option label
            for opt in options:
                if opt.score == st.auto_score:
                    proposed_label = opt.label
                    break
            if not proposed_label:
                proposed_label = f"Conforme (Niveau {st.auto_score}/4)"

        # Find current answer key if already answered
        current_answer_key = None
        if st and st.effective_score is not None:
            for opt in options:
                if opt.score == st.effective_score:
                    current_answer_key = opt.key
                    break

        dom_info = self.repository.domains.get(c_def.domain, {"name": c_def.domain})

        return AssistantQuestionCard(
            criterion_id=c_def.id,
            domain_code=c_def.domain,
            domain_name=dom_info["name"],
            criterion_name=c_def.name,
            is_critical=c_def.critical,
            is_test=cfg.get("is_test", c_def.default_evaluation_type == "TEST"),
            step_number=step_number,
            total_steps=total_steps,
            progress_percent=round(progress_pct, 1),
            question_text=cfg.get("question", c_def.question),
            options=options,
            has_prefilled_proposal=has_prefill,
            proposed_label=proposed_label,
            proposed_score=st.auto_score if (has_prefill and st) else None,
            confidence_percent=st.confidence if st else 0.0,
            evidence_text=st.evidence if st else "",
            why_it_matters=cfg.get("why_it_matters", c_def.description),
            what_was_detected=st.evidence if st else "Aucune observation directe.",
            what_is_missing=cfg.get("what_is_missing", st.reason_if_not_auto if st else "Validation humaine requise."),
            technical_details={"observations": st.reason_if_not_auto if st else ""},
            test_objective=cfg.get("test_objective", ""),
            test_duration=cfg.get("test_duration", "2 minutes"),
            test_temporary_impact=cfg.get("test_temporary_impact", ""),
            test_procedure_steps=cfg.get("test_procedure_steps", []),
            test_safety_warning=cfg.get("test_safety_warning", ""),
            current_answer_key=current_answer_key,
        )

    def apply_answer(
        self,
        criterion_id: str,
        answer_key: str,
        criteria_states: dict[str, CriterionState],
    ) -> tuple[CriterionState, bool]:
        """Apply a natural language answer to a criterion state and handle branching."""
        cfg = NATURAL_QUESTIONS_CONFIG.get(criterion_id, {})
        options = cfg.get("options", [])
        
        selected_option = next((opt for opt in options if opt.key == answer_key), None)
        st = criteria_states.get(criterion_id)
        if not st:
            st = CriterionState(criterion_id=criterion_id)

        # 1. If "Je ne sais pas" / "Faire plus tard" -> No score assigned, NEEDS_REVIEW
        if answer_key in ("unknown", "skip") or (selected_option and selected_option.is_unknown):
            st.effective_score = None
            st.status = CriterionStatus.NEEDS_REVIEW
            st.user_confirmed = True
            st.evaluation_source = EvaluationSource.QUESTION
            criteria_states[criterion_id] = st
            return st, False

        # 2. If "Sans objet" / NOT_APPLICABLE
        if answer_key == "not_applicable" or (selected_option and selected_option.is_not_applicable):
            st.effective_score = None
            st.status = CriterionStatus.NOT_APPLICABLE
            st.applicable = False
            st.user_confirmed = True
            criteria_states[criterion_id] = st
            return st, True

        # 3. Discrete valid score (0..4)
        if answer_key in ("0", "1", "2", "3", "4"):
            score_val = int(answer_key)
        elif selected_option and selected_option.score is not None:
            score_val = selected_option.score
        else:
            st.effective_score = None
            st.status = CriterionStatus.NEEDS_REVIEW
            criteria_states[criterion_id] = st
            return st, False

        st.effective_score = score_val
        st.status = CriterionStatus.CONFIRMED
        st.user_confirmed = True
        st.needs_review = False
        st.evaluation_source = EvaluationSource.TEST if cfg.get("is_test") else EvaluationSource.QUESTION
        criteria_states[criterion_id] = st

        # 4. Conditional Branching Rules
        branching_triggered = False
        # If Solar = No or NOT_APPLICABLE -> ENER07 becomes NOT_APPLICABLE
        if criterion_id == "ENER04" and (st.effective_score == 0 or not st.applicable):
            ener07 = criteria_states.get("ENER07")
            if ener07:
                ener07.status = CriterionStatus.NOT_APPLICABLE
                ener07.applicable = False
                branching_triggered = True

        return st, branching_triggered
