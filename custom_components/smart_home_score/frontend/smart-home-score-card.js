/**
 * Smart Home Score Lovelace Custom Card (v0.7.0-beta.4)
 * Author: Cyrille LEFRANC
 * 100% Local Lovelace Card for Home Assistant.
 * Interactive Step-by-Step Audit Assistant, Live Scoring, Domain Breakdown & Advisor.
 */

console.info(
  '%c SMART-HOME-SCORE %c v0.7.0-beta.4 ',
  'color: white; background: #3b82f6; font-weight: 700; border-radius: 3px 0 0 3px;',
  'color: #3b82f6; background: #1e293b; font-weight: 700; border-radius: 0 3px 3px 0;'
);

const SHS_CRITERIA = [
  {
    "id": "AUTO01",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & Logique",
    "title": "Éclairage intelligent",
    "question": "Vos éclairages s'adaptent-ils automatiquement au niveau de lumière naturelle et à vos activités (mode nuit tamisé, extinction sur absence) ?",
    "explanation": "Scénarios d'éclairage automatisés tenant compte du contexte réel : présence, horaire, luminosité ambiante, mode nuit ou pièce occupée.",
    "critical": false
  },
  {
    "id": "AUTO02",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & Logique",
    "title": "Chauffage intelligent",
    "question": "Votre chauffage baisse-t-il automatiquement lors d'une absence ou à l'ouverture d'une fenêtre ?",
    "explanation": "Régulation thermique intelligente dépendant du besoin réel, des plannings familiaux, de la présence et de l'ouverture des fenêtres.",
    "critical": false
  },
  {
    "id": "AUTO03",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & Logique",
    "title": "Ventilation intelligente",
    "question": "Votre VMC passe-t-elle automatiquement en grande vitesse lors d'une douche puis revient-elle en vitesse normale ?",
    "explanation": "Pilotage automatique de la VMC ou de l'aération selon l'hygrométrie de la salle de bain ou la qualité d'air (CO2/COV).",
    "critical": false
  },
  {
    "id": "AUTO04",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & Logique",
    "title": "Gestion intelligente des volets",
    "question": "Vos volets se ferment-ils automatiquement sur les façades ensoleillées en été pour protéger la maison de la chaleur ?",
    "explanation": "Automatisation thermique des volets roulants : fermeture estivale anti-surchauffe au soleil et optimisation des apports solaires en hiver.",
    "critical": false
  },
  {
    "id": "AUTO05",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & Logique",
    "title": "Gestion de l'eau",
    "question": "En cas de détection d'eau au sol, recevez-vous une alerte immédiate et la vanne générale se coupe-t-elle automatiquement ?",
    "explanation": "Détection précoce des fuites d'eau ou surconsommations et protection automatique par fermeture de la vanne générale.",
    "critical": false
  },
  {
    "id": "AUTO06",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & Logique",
    "title": "Appareils domestiques",
    "question": "Recevez-vous une notification sur votre smartphone ou enceinte vocale lorsque le lave-linge ou lave-vaisselle est terminé ?",
    "explanation": "Suivi intelligent de la consommation et des cycles des appareils électroménagers (fin de cycle lave-linge/vaisselle, alertes puissance).",
    "critical": false
  },
  {
    "id": "AUTO07",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & Logique",
    "title": "Présence et occupation",
    "question": "Home Assistant sait-il si la maison est occupée ou vide de manière fiable (détection smartphone + capteurs) ?",
    "explanation": "Le système détermine la présence et l'occupation des pièces de manière fiable en combinant plusieurs sources (GPS, Wi-Fi, capteurs de mouvement/présence).",
    "critical": false
  },
  {
    "id": "AUTO08",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & Logique",
    "title": "Contextualisation",
    "question": "Vos automatisations s'adaptent-elles au contexte global (jours fériés, vacances, météo, mode télétravail) ?",
    "explanation": "Combinaison intelligente de plusieurs informations contextuelles plutôt que des horaires fixes rigides (météo, saison, mode de vie, calendrier).",
    "critical": false
  },
  {
    "id": "AUTO09",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & Logique",
    "title": "Boucle de vérification",
    "question": "Sur vos actions critiques (fermeture serrure, coupure vanne, arrêt chauffage), Home Assistant vérifie-t-il que l'action s'est réellement produite ?",
    "explanation": "Contrôle si l'action domotique demandée a réellement produit le résultat attendu (vérification d'état, relance en cas d'échec ou alerte).",
    "critical": false
  },
  {
    "id": "CYBER01",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité & Réseau",
    "title": "Accès distant sécurisé",
    "question": "Comment accédez-vous à votre Home Assistant depuis l'extérieur (Nabu Casa, Cloudflare Tunnel, VPN ou redirection de port) ?",
    "explanation": "L'accès à distance à Home Assistant utilise un protocole chiffré sécurisé (HTTPS avec certificat valide, Cloudflare Access, Nabu Casa ou VPN chiffré) sans redirection de port HTTP brut.",
    "critical": true
  },
  {
    "id": "CYBER02",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité & Réseau",
    "title": "Authentification renforcée",
    "question": "Avez-vous activé la double authentification (2FA / TOTP) sur votre compte administrateur Home Assistant ?",
    "explanation": "Activation de l'authentification à deux facteurs (2FA / TOTP) sur les comptes administrateurs de Home Assistant.",
    "critical": false
  },
  {
    "id": "CYBER03",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité & Réseau",
    "title": "Comptes individualisés",
    "question": "Chaque personne du foyer possède-t-elle son propre compte utilisateur Home Assistant ?",
    "explanation": "Chaque membre du foyer dispose d'un compte utilisateur dédié et distinct sans partage d'un compte unique.",
    "critical": false
  },
  {
    "id": "CYBER04",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité & Réseau",
    "title": "Principe du moindre privilège",
    "question": "Le statut Administrateur est-il réservé au seul gestionnaire technique de l'installation ?",
    "explanation": "Les utilisateurs ordinaires et terminaux partagés (tablettes murales, invités) ne disposent pas des privilèges administrateur.",
    "critical": false
  },
  {
    "id": "CYBER05",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité & Réseau",
    "title": "Gestion des secrets",
    "question": "Avez-vous vérifié qu'aucun mot de passe, token ou clé API n'apparaît en clair dans vos dashboards ou automatisations ?",
    "explanation": "Les mots de passe, tokens et clés d'API sont absents des dashboards publics et protégés dans des variables sécurisées.",
    "critical": true
  },
  {
    "id": "CYBER06",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité & Réseau",
    "title": "Mises à jour",
    "question": "Appliquez-vous régulièrement les mises à jour de Home Assistant et de ses composants après avoir effectué une sauvegarde ?",
    "explanation": "Home Assistant Core, le système d'exploitation et les modules complémentaires sont maintenus régulièrement à jour.",
    "critical": false
  },
  {
    "id": "CYBER07",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité & Réseau",
    "title": "Exposition réseau IoT",
    "question": "Vos objets connectés (caméras, ampoules Wi-Fi) sont-ils isolés sur un réseau Wi-Fi dédié (invité / VLAN) ou protégés par votre routeur ?",
    "explanation": "L'exposition réseau et Internet des objets connectés est limitée au strict nécessaire (isolation VLAN, Wi-Fi IoT ou filtrage box).",
    "critical": false
  },
  {
    "id": "CYBER08",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité & Réseau",
    "title": "Surveillance sécurité",
    "question": "Consultez-vous régulièrement les alertes de sécurité (menu Réparations) et surveillez-vous les tentatives de connexion anormales ?",
    "explanation": "Surveillance active des notifications système, échecs d'authentification et alertes de sécurité.",
    "critical": false
  },
  {
    "id": "ELEC01",
    "domain": "ELEC",
    "domain_name": "⚡ Électricité & Alimentation",
    "title": "Commande manuelle conservée",
    "question": "Vos éclairages, volets et chauffages restent-ils manipulables via leurs boutons physiques quand le serveur Home Assistant est totalement éteint ?",
    "explanation": "Les fonctions essentielles (éclairage, volets, chauffage, accès) restent utilisables localement et manuellement même si Home Assistant est arrêté ou hors service.",
    "critical": true
  },
  {
    "id": "ELEC02",
    "domain": "ELEC",
    "domain_name": "⚡ Électricité & Alimentation",
    "title": "Dimensionnement des actionneurs",
    "question": "Vos consommateurs de forte puissance (chauffe-eau, chauffage, recharge) sont-ils relayés par des contacteurs de puissance adaptés au tableau électrique ?",
    "explanation": "Les modules, relais, contacteurs et prises connectées sont adaptés à la puissance admissible et protégés par un disjoncteur de calibre approprié.",
    "critical": true
  },
  {
    "id": "ELEC03",
    "domain": "ELEC",
    "domain_name": "⚡ Électricité & Alimentation",
    "title": "États sûrs après redémarrage",
    "question": "Avez-vous configuré le comportement au retour du courant (Power-on state) sur vos modules connectés pour éviter tout allumage involontaire ?",
    "explanation": "Après coupure électrique ou redémarrage d'un module, retour dans un état défini et non dangereux (Power-on state configuré).",
    "critical": false
  },
  {
    "id": "ELEC04",
    "domain": "ELEC",
    "domain_name": "⚡ Électricité & Alimentation",
    "title": "Interverrouillages",
    "question": "Vos volets roulants et moteurs utilisent-ils des modules dédiés avec interverrouillage électrique matériel empêchant la montée et la descente simultanées ?",
    "explanation": "Protection contre les commandes contradictoires simultanées (ex: interverrouillage matériel montée/descente sur volets ou moteurs).",
    "critical": true
  },
  {
    "id": "ELEC05",
    "domain": "ELEC",
    "domain_name": "⚡ Électricité & Alimentation",
    "title": "Gestion des équipements critiques",
    "question": "Tous vos équipements critiques (serrure connectée, vanne générale, pompe) disposent-ils d'une solution de secours physique (clé manuelle, vanne bypass) ?",
    "explanation": "Comportement maîtrisé en cas de panne ou de défaillance sur les équipements critiques (eau, chauffage, sécurité, accès).",
    "critical": false
  },
  {
    "id": "ENER01",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & Solaire",
    "title": "Consommation électrique globale",
    "question": "Avez-vous une mesure en direct de la puissance consommée par toute la maison (module Linky TIC ou pince au tableau) ?",
    "explanation": "Mesure en temps réel de la consommation électrique globale du logement (téléinformation Linky TIC, tore de mesure au disjoncteur général, pince ampèremétrique).",
    "critical": false
  },
  {
    "id": "ENER02",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & Solaire",
    "title": "Historique énergétique",
    "question": "Votre tableau de bord Énergie natif dans Home Assistant est-il configuré et alimenté par vos capteurs ?",
    "explanation": "Conservation et exploitation d'un historique journalier, mensuel et annuel complet dans le tableau de bord Énergie natif de Home Assistant.",
    "critical": false
  },
  {
    "id": "ENER03",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & Solaire",
    "title": "Mesure des principaux usages",
    "question": "Mesurez-vous la consommation de vos principaux appareils individuellement (chauffe-eau, lave-linge, réfrigérateur, multimédia) ?",
    "explanation": "Sous-comptage individuel des consommateurs significatifs de la maison (chauffe-eau, chauffage, pompe à chaleur, électroménager, recharge VE).",
    "critical": false
  },
  {
    "id": "ENER04",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & Solaire",
    "title": "Production locale",
    "question": "Si vous avez des panneaux solaires, leur production en direct et leur historique sont-ils intégrés dans Home Assistant ?",
    "explanation": "Mesure en temps réel et historique de la production locale d'énergie (panneaux solaires photovoltaïques, micro-onduleurs ou éolien).",
    "critical": false
  },
  {
    "id": "ENER05",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & Solaire",
    "title": "Tarification",
    "question": "Home Assistant connaît-il votre contrat d'électricité (Heures Creuses, Tempo, tarif dynamique) pour calculer vos coûts ?",
    "explanation": "Home Assistant connaît les plages horaires, tarifs d'électricité et contrats dynamiques (Heures Pleines / Heures Creuses, Tempo, Spot, RTE).",
    "critical": false
  },
  {
    "id": "ENER06",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & Solaire",
    "title": "Optimisation automatique",
    "question": "Home Assistant déclenche-t-il automatiquement votre chauffe-eau, recharge ou gros appareils pendant les heures creuses ou le surplus solaire ?",
    "explanation": "Déplacement automatique des gros consommateurs (chauffe-eau, recharge, électroménager) vers les périodes énergétiquement intéressantes (heures creuses, surplus solaire).",
    "critical": false
  },
  {
    "id": "ENER07",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & Solaire",
    "title": "Autoconsommation",
    "question": "Avez-vous mis en place un dispositif actif (routeur solaire, batterie ou automatisme dynamique) pour consommer toute votre électricité solaire ?",
    "explanation": "Optimisation du taux d'autoconsommation solaire locale (routeur solaire, batterie domestique, délestage dynamique).",
    "critical": false
  },
  {
    "id": "ENER08",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & Solaire",
    "title": "Eau",
    "question": "Votre consommation d'eau (en litres ou m³) est-elle suivie en direct dans Home Assistant ?",
    "explanation": "Mesure en temps réel, historique de consommation d'eau et intégration dans Home Assistant.",
    "critical": false
  },
  {
    "id": "ENER09",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & Solaire",
    "title": "Détection des anomalies énergétiques",
    "question": "Recevez-vous une alerte si un appareil consomme anormalement longtemps ou si un écoulement d'eau continu est détecté la nuit ?",
    "explanation": "Détection automatique des surconsommations électriques anormales (talon de veille excessif, appareil resté allumé) et des fuites d'eau continues.",
    "critical": false
  },
  {
    "id": "INTER01",
    "domain": "INTER",
    "domain_name": "🔌 Protocoles Locaux & Sans Fil",
    "title": "Protocoles locaux",
    "question": "Vos équipements domotiques fonctionnent-ils en majorité via des protocoles locaux (Zigbee, Matter, ESPHome, MQTT) ?",
    "explanation": "Utilisation prioritaire de protocoles domotiques locaux sans dépendance cloud (Zigbee, Matter, Z-Wave, ESPHome, MQTT, Modbus, API locales).",
    "critical": false
  },
  {
    "id": "INTER02",
    "domain": "INTER",
    "domain_name": "🔌 Protocoles Locaux & Sans Fil",
    "title": "Dépendance au Cloud",
    "question": "Vos fonctions essentielles (lumières, volets, chauffage) peuvent-elles continuer à fonctionner si un constructeur ferme ses serveurs ?",
    "explanation": "Les fonctions vitales de la maison (éclairage, chauffage, ouvrants, sécurité) ne dépendent d'aucun cloud constructeur pour leur fonctionnement quotidien.",
    "critical": false
  },
  {
    "id": "INTER03",
    "domain": "INTER",
    "domain_name": "🔌 Protocoles Locaux & Sans Fil",
    "title": "Remplaçabilité du matériel",
    "question": "Si une ampoule ou un capteur tombe en panne, pouvez-vous le remplacer facilement sans devoir modifier toutes vos automatisations ?",
    "explanation": "Utilisation d'une couche d'abstraction (groupes d'entités, templates, scripts intermédiaires) permettant de remplacer un équipement physique défaillant sans modifier toutes les automatisations.",
    "critical": false
  },
  {
    "id": "INTER04",
    "domain": "INTER",
    "domain_name": "🔌 Protocoles Locaux & Sans Fil",
    "title": "Organisation Home Assistant",
    "question": "Tous vos appareils et entités sont-ils correctement affectés à leur pièce dans Home Assistant ?",
    "explanation": "Organisation rigoureuse et cohérente de Home Assistant : affectation de chaque appareil et entité à sa pièce (Zone/Area), labels et catégories.",
    "critical": false
  },
  {
    "id": "INTER05",
    "domain": "INTER",
    "domain_name": "🔌 Protocoles Locaux & Sans Fil",
    "title": "Standardisation",
    "question": "Vos équipements utilisent-ils des standards ouverts universels (Zigbee 3.0, Matter, MQTT, ESPHome) évitant l'enfermement ?",
    "explanation": "Les protocoles et équipements utilisés reposent sur des standards ouverts interopérables (Zigbee 3.0, Matter, Thread, ESPHome, MQTT, OpenTherm) évitant l'enfermement propriétaire.",
    "critical": false
  },
  {
    "id": "INTER06",
    "domain": "INTER",
    "domain_name": "🔌 Protocoles Locaux & Sans Fil",
    "title": "Intégration centralisée",
    "question": "Home Assistant est-il le chef d'orchestre centralisant l'ensemble des systèmes de votre maison ?",
    "explanation": "Home Assistant sert de chef d'orchestre unique : l'ensemble des systèmes de la maison sont pilotés et supervisés depuis une plateforme centrale.",
    "critical": false
  },
  {
    "id": "MAINT01",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & Supervision",
    "title": "Convention de nommage",
    "question": "Vos entités et appareils suivent-ils une nomenclature claire et ordonnée (ex: light.salon_plafonnier) ?",
    "explanation": "Les entités, appareils et automatisations suivent une nomenclature claire, structurée et cohérente (ex: domaine.piece_equipement_fonction) sans identifiants bruts obscurs.",
    "critical": false
  },
  {
    "id": "MAINT02",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & Supervision",
    "title": "Documentation de l'installation",
    "question": "Avez-vous un document récapitulatif (adresses IP, schémas, matériel) permettant de comprendre votre installation ?",
    "explanation": "Les éléments techniques importants de l'installation sont documentés dans un mémo ou dossier récapitulatif (adresses IP fixes, schémas, comptes, protocoles).",
    "critical": false
  },
  {
    "id": "MAINT03",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & Supervision",
    "title": "Automatisations documentées",
    "question": "Vos automatisations et scripts comportent-ils tous une description expliquant ce qu'ils font ?",
    "explanation": "Les automatisations et scripts possèdent des descriptions claires précisant leur rôle, déclencheurs et conditions.",
    "critical": false
  },
  {
    "id": "MAINT04",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & Supervision",
    "title": "Nettoyage des entités inutilisées",
    "question": "Nettoyez-vous régulièrement les anciennes entités et anciens appareils qui ne sont plus utilisés ?",
    "explanation": "Les entités orphelines, appareils retirés ou intégrations fantômes sont régulièrement identifiés et nettoyés.",
    "critical": false
  },
  {
    "id": "MAINT05",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & Supervision",
    "title": "Tableau de santé technique",
    "question": "Avez-vous une vue ou une alerte centralisant le niveau de toutes les piles et batteries de vos capteurs ?",
    "explanation": "Un tableau de bord technique dédié permet de surveiller rapidement l'état du système : niveau des batteries, charge CPU, mémoire, espace disque et appareils hors ligne.",
    "critical": false
  },
  {
    "id": "MAINT06",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & Supervision",
    "title": "Procédure de reprise d'urgence",
    "question": "Avez-vous une procédure écrite expliquant comment réinstaller Home Assistant et restaurer votre sauvegarde en cas de crash ?",
    "explanation": "Les informations indispensables pour redémarrer ou réinstaller le système en cas de panne matérielle majeure sont rédigées et accessibles.",
    "critical": false
  },
  {
    "id": "MAINT07",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & Supervision",
    "title": "Historique des modifications",
    "question": "Tenez-vous un historique ou un journal de vos modifications pour retrouver facilement ce qui a changé en cas de bug ?",
    "explanation": "Les évolutions significatives de l'installation sont traçables (gestionnaire de versions Git, journal de bord ou notes de révisions datées).",
    "critical": false
  },
  {
    "id": "RES01",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & Secours",
    "title": "Fonctionnement sans Internet",
    "question": "Avez-vous testé le fonctionnement de votre maison en débranchant le câble Internet de votre box ?",
    "explanation": "Les fonctions locales essentielles (lumières, volets, chauffage, automatisations internes) continuent de fonctionner parfaitement lors d'une coupure de la connexion Internet.",
    "critical": false
  },
  {
    "id": "RES02",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & Secours",
    "title": "Fonctionnement sans Home Assistant",
    "question": "Vos télécommandes et boutons physiques continuent-ils de fonctionner si la machine Home Assistant est éteinte ?",
    "explanation": "Les fonctions essentielles disposent d'un mode manuel physique ou de liaisons directes autonomes (Zigbee direct binding, télécommandes associées) en cas d'arrêt du serveur.",
    "critical": true
  },
  {
    "id": "RES03",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & Secours",
    "title": "Supervision périphériques indisponibles",
    "question": "Recevez-vous une notification si un capteur important (thermomètre, détecteur de fuite, passerelle) devient indisponible ?",
    "explanation": "Home Assistant identifie, supervise et alerte sur les périphériques importants ou capteurs critiques devenus indisponibles ou hors ligne.",
    "critical": false
  },
  {
    "id": "RES04",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & Secours",
    "title": "Qualité du réseau domotique",
    "question": "Votre réseau Zigbee/domotique est-il stable et bien maillé grâce à des prises ou modules branchés sur secteur faisant office de routeurs ?",
    "explanation": "La santé et la qualité du maillage des réseaux domotiques (Zigbee, Wi-Fi, Matter, Z-Wave) sont surveillées avec un nombre suffisant de routeurs.",
    "critical": false
  },
  {
    "id": "RES05",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & Secours",
    "title": "Sauvegardes Home Assistant",
    "question": "Avez-vous configuré des sauvegardes automatiques régulières (quotidiennes ou hebdomadaires) de votre Home Assistant ?",
    "explanation": "Des sauvegardes complètes automatiques et régulières de Home Assistant sont programmées et actives.",
    "critical": true
  },
  {
    "id": "RES06",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & Secours",
    "title": "Sauvegarde hors de Home Assistant",
    "question": "Vos sauvegardes sont-elles automatiquement copiées en dehors de votre serveur (vers un NAS, Google Drive, Nextcloud ou clé USB externe) ?",
    "explanation": "Au moins une copie des sauvegardes est automatiquement exportée et conservée hors de la machine Home Assistant (clé USB externe, NAS local, Google Drive, OneDrive, Cloud chiffré).",
    "critical": false
  },
  {
    "id": "RES07",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & Secours",
    "title": "Restauration testée",
    "question": "Avez-vous déjà testé la restauration complète d'une sauvegarde pour valider que votre maison repart sans encombre ?",
    "explanation": "La procédure de restauration d'une sauvegarde a déjà été testée et validée en situation réelle ou sur une instance de secours.",
    "critical": false
  },
  {
    "id": "RES08",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & Secours",
    "title": "Continuité électrique",
    "question": "Votre serveur Home Assistant et votre box Internet sont-ils branchés sur un onduleur (UPS) avec batterie ?",
    "explanation": "Stratégie face aux microcoupures et coupures de courant (onduleur / UPS sur serveur et équipements réseau, arrêt propre automatisé).",
    "critical": false
  },
  {
    "id": "UX01",
    "domain": "UX",
    "domain_name": "📱 Expérience & Interfaces",
    "title": "Commandes physiques intuitives",
    "question": "Les membres du foyer et les invités peuvent-ils utiliser les lumières et volets sans jamais avoir besoin d'un smartphone ?",
    "explanation": "L'utilisation quotidienne des fonctions de base ne nécessite pas de sortir son smartphone : boutons physiques intuitifs et télécommandes accessibles dans chaque pièce.",
    "critical": false
  },
  {
    "id": "UX02",
    "domain": "UX",
    "domain_name": "📱 Expérience & Interfaces",
    "title": "Dashboard famille",
    "question": "Votre famille dispose-t-elle d'un dashboard épuré et simple d'utilisation au quotidien ?",
    "explanation": "Présence d'une interface Lovelace épurée, claire et simplifiée spécialement conçue pour les membres du foyer et les invités (tablette murale ou vue mobile).",
    "critical": false
  },
  {
    "id": "UX03",
    "domain": "UX",
    "domain_name": "📱 Expérience & Interfaces",
    "title": "Adaptation aux appareils",
    "question": "Vos dashboards s'affichent-ils confortablement sur smartphone comme sur tablette sans déformation ?",
    "explanation": "Les tableaux de bord sont responsifs et parfaitement lisibles sur smartphone, tablette murale et écran d'ordinateur.",
    "critical": false
  },
  {
    "id": "UX04",
    "domain": "UX",
    "domain_name": "📱 Expérience & Interfaces",
    "title": "Notifications pertinentes",
    "question": "Vos notifications domotiques sont-elles utiles, ciblées et sans spam intempestif ?",
    "explanation": "Les notifications envoyées sont utiles, ciblées, hiérarchisées et évitent tout spam d'alertes inutiles.",
    "critical": false
  },
  {
    "id": "UX05",
    "domain": "UX",
    "domain_name": "📱 Expérience & Interfaces",
    "title": "Automatisations discrètes",
    "question": "Votre domotique est-elle discrète et naturelle pour tous les habitants (pas d'extinctions inopportunes ni de surprises) ?",
    "explanation": "Les automatisations améliorent le confort de façon transparente et silencieuse sans contraindre ni surprendre les occupants.",
    "critical": false
  },
  {
    "id": "UX06",
    "domain": "UX",
    "domain_name": "📱 Expérience & Interfaces",
    "title": "Override utilisateur",
    "question": "Si vous modifiez manuellement un volet ou une lumière, Home Assistant respecte-t-il votre choix sans forcer son automatisme ?",
    "explanation": "L'utilisateur peut facilement reprendre la main manuellement sur une automatisation (la commande manuelle reste toujours prioritaire sur l'automatisme).",
    "critical": false
  },
  {
    "id": "UX07",
    "domain": "UX",
    "domain_name": "📱 Expérience & Interfaces",
    "title": "Réactivité du système",
    "question": "Lorsque vous appuyez sur un bouton, l'allumage ou l'action se produit-elle instantanément (< 300ms) ?",
    "explanation": "Les principales actions domotiques (appui sur interrupteur, déclenchement de scène) offrent un temps de réponse instantané et prévisible (< 300 ms).",
    "critical": false
  }
];

class SmartHomeScoreCard extends HTMLElement {
  constructor() {
    super();
    this._config = {};
    this._hass = null;
    this._view = 'welcome'; // 'welcome' | 'audit' | 'cockpit'
    this._activeTab = 'overview';
    this._currentQuestionIndex = 0;
    this.attachShadow({ mode: 'open' });
  }

  static getStubConfig(hass, unusedEntities, allEntities) {
    return {};
  }

  setConfig(config) {
    this._config = config || {};
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() {
    return 7;
  }

  _getEntity(suffix) {
    if (!this._hass?.states) return null;
    if (this._hass.states['sensor.smart_home_score_' + suffix]) {
      return this._hass.states['sensor.smart_home_score_' + suffix];
    }
    if (this._hass.states['sensor.' + suffix]) {
      return this._hass.states['sensor.' + suffix];
    }
    const states = Object.values(this._hass.states);
    return states.find(s => s.entity_id.startsWith('sensor.') && s.entity_id.includes(suffix)) || null;
  }

  _render() {
    if (!this.shadowRoot) return;

    const globalScoreSensor = this._getEntity('global_score');
    const completenessSensor = this._getEntity('completeness');
    const maturitySensor = this._getEntity('maturity_level');
    const criticalSensor = this._getEntity('critical_risks');
    const potentialGainSensor = this._getEntity('potential_gain');

    const hasData = globalScoreSensor && globalScoreSensor.state !== 'unknown' && globalScoreSensor.state !== 'unavailable';
    const scoreVal = hasData ? parseFloat(globalScoreSensor.state) : 0.0;
    const completenessVal = completenessSensor && completenessSensor.state !== 'unknown' ? parseFloat(completenessSensor.state) : 0.0;
    const maturityText = maturitySensor?.state && maturitySensor.state !== 'unknown' ? maturitySensor.state : 'Non évalué';
    const criticalCount = criticalSensor?.state && criticalSensor.state !== 'unknown' ? parseInt(criticalSensor.state, 10) : 0;
    const potentialGain = potentialGainSensor?.state && potentialGainSensor.state !== 'unknown' ? parseFloat(potentialGainSensor.state) : 0.0;

    const isProvisional = globalScoreSensor?.attributes?.is_provisional ?? (completenessVal < 100);

    if (completenessVal >= 100 && this._view === 'welcome') {
      this._view = 'cockpit';
    }

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          --shs-primary: #3b82f6;
          --shs-success: #10b981;
          --shs-warning: #f59e0b;
          --shs-danger: #ef4444;
          --shs-bg: var(--ha-card-background, var(--card-background-color, #1e293b));
          --shs-text: var(--primary-text-color, #f8fafc);
          --shs-muted: var(--secondary-text-color, #94a3b8);
          font-family: var(--paper-font-body1_-_font-family, system-ui, -apple-system, sans-serif);
          display: block;
        }
        .shs-container {
          background: var(--shs-bg);
          color: var(--shs-text);
          border-radius: 16px;
          padding: 20px;
          box-shadow: var(--ha-card-box-shadow, 0 4px 20px rgba(0,0,0,0.25));
          border: 1px solid rgba(255, 255, 255, 0.08);
          box-sizing: border-box;
        }
        .shs-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 16px;
        }
        .shs-branding {
          display: flex;
          align-items: center;
          gap: 10px;
          font-size: 1.15rem;
          font-weight: 700;
          color: #60a5fa;
        }
        .shs-badge-beta {
          background: rgba(59, 130, 246, 0.18);
          color: #93c5fd;
          padding: 3px 8px;
          border-radius: 9999px;
          font-size: 0.75rem;
          font-weight: 600;
        }
        .shs-welcome-box {
          background: rgba(0, 0, 0, 0.2);
          border: 1px dashed rgba(255, 255, 255, 0.15);
          border-radius: 12px;
          padding: 24px;
          text-align: center;
          margin: 12px 0;
        }
        .shs-welcome-title {
          font-size: 1.25rem;
          font-weight: 700;
          margin-bottom: 8px;
          color: #f8fafc;
        }
        .shs-welcome-desc {
          color: var(--shs-muted);
          font-size: 0.92rem;
          margin-bottom: 20px;
          line-height: 1.5;
        }
        .shs-btn {
          background: #2563eb;
          color: white;
          border: none;
          padding: 12px 18px;
          border-radius: 10px;
          font-size: 0.95rem;
          font-weight: 600;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          width: 100%;
          transition: background 0.2s, transform 0.1s;
          box-sizing: border-box;
        }
        .shs-btn:hover {
          background: #1d4ed8;
        }
        .shs-btn:active {
          transform: scale(0.98);
        }
        .shs-btn-sec {
          background: rgba(255, 255, 255, 0.08);
          color: var(--shs-text);
        }
        .shs-btn-sec:hover {
          background: rgba(255, 255, 255, 0.15);
        }
        /* Questionnaire Styles */
        .shs-audit-box {
          background: rgba(0, 0, 0, 0.25);
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 12px;
          padding: 18px;
          margin-bottom: 16px;
        }
        .shs-domain-badge {
          display: inline-block;
          background: rgba(59, 130, 246, 0.2);
          color: #93c5fd;
          font-size: 0.8rem;
          font-weight: 700;
          padding: 4px 10px;
          border-radius: 6px;
          margin-bottom: 12px;
        }
        .shs-question-title {
          font-size: 1.15rem;
          font-weight: 700;
          color: #f8fafc;
          margin-bottom: 8px;
          line-height: 1.4;
        }
        .shs-question-desc {
          color: var(--shs-muted);
          font-size: 0.9rem;
          line-height: 1.45;
          margin-bottom: 16px;
        }
        .shs-answers-grid {
          display: flex;
          flex-direction: column;
          gap: 10px;
          margin-bottom: 16px;
        }
        .shs-ans-btn {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.12);
          color: var(--shs-text);
          padding: 12px 16px;
          border-radius: 8px;
          font-size: 0.95rem;
          font-weight: 600;
          text-align: left;
          cursor: pointer;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          gap: 10px;
        }
        .shs-ans-btn:hover {
          background: rgba(59, 130, 246, 0.2);
          border-color: #3b82f6;
          color: #93c5fd;
        }
        .shs-ans-btn.ans-yes:hover {
          background: rgba(16, 185, 129, 0.2);
          border-color: #10b981;
          color: #a7f3d0;
        }
        .shs-ans-btn.ans-partial:hover {
          background: rgba(245, 158, 11, 0.2);
          border-color: #f59e0b;
          color: #fde68a;
        }
        .shs-ans-btn.ans-no:hover {
          background: rgba(239, 68, 68, 0.2);
          border-color: #ef4444;
          color: #fca5a5;
        }
        .shs-nav-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 10px;
          margin-top: 12px;
        }
        .shs-score-hero {
          background: rgba(0, 0, 0, 0.25);
          border-radius: 12px;
          padding: 16px;
          margin-bottom: 16px;
        }
        .shs-score-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .shs-score-val {
          font-size: 1.8rem;
          font-weight: 800;
          color: #60a5fa;
        }
        .shs-provisional-tag {
          font-size: 0.75rem;
          background: rgba(245, 158, 11, 0.2);
          color: #fde68a;
          padding: 2px 6px;
          border-radius: 4px;
          margin-left: 6px;
          vertical-align: middle;
        }
        .shs-progress-bar {
          background: rgba(255, 255, 255, 0.1);
          height: 6px;
          border-radius: 9999px;
          margin: 10px 0 6px 0;
          overflow: hidden;
        }
        .shs-progress-fill {
          background: #3b82f6;
          height: 100%;
          border-radius: 9999px;
          transition: width 0.3s ease;
        }
        .shs-nav-tabs {
          display: flex;
          gap: 6px;
          margin-bottom: 14px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
          padding-bottom: 8px;
          overflow-x: auto;
        }
        .shs-tab-btn {
          background: transparent;
          color: var(--shs-muted);
          border: none;
          padding: 6px 12px;
          border-radius: 8px;
          font-weight: 600;
          font-size: 0.82rem;
          cursor: pointer;
          transition: all 0.2s;
          white-space: nowrap;
        }
        .shs-tab-btn.active {
          background: rgba(59, 130, 246, 0.2);
          color: #60a5fa;
        }
        .shs-domain-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 8px;
          margin-top: 12px;
        }
        .shs-domain-card {
          background: rgba(0, 0, 0, 0.2);
          border-radius: 8px;
          padding: 10px;
          font-size: 0.8rem;
        }
        .shs-domain-title {
          font-weight: 600;
          color: var(--shs-muted);
          margin-bottom: 4px;
        }
        .shs-domain-score {
          font-size: 1rem;
          font-weight: 700;
          color: #93c5fa;
        }
      </style>

      <div class="shs-container">
        <div class="shs-header">
          <div class="shs-branding">
            <span>🏠 Smart Home Score</span>
          </div>
          <span class="shs-badge-beta">Bêta v0.7.0-beta.4</span>
        </div>

        ${this._renderCurrentView(scoreVal, completenessVal, maturityText, criticalCount, potentialGain, isProvisional)}
      </div>
    `;

    this._bindEvents();
  }

  _renderCurrentView(scoreVal, completenessVal, maturityText, criticalCount, potentialGain, isProvisional) {
    if (this._view === 'welcome') {
      return `
        <div class="shs-welcome-box">
          <div class="shs-welcome-title">Bienvenue dans Smart Home Score</div>
          <div class="shs-welcome-desc">
            Évaluez l'autonomie, la sécurité et la résilience de votre installation Home Assistant en quelques minutes (100 % local, 0 cloud).
          </div>
          <button class="shs-btn" id="btn-start-first-audit">
            🚀 Lancer mon premier audit
          </button>
        </div>
      `;
    }

    if (this._view === 'audit') {
      const total = SHS_CRITERIA.length;
      const curIdx = Math.min(this._currentQuestionIndex, total - 1);
      const crit = SHS_CRITERIA[curIdx] || SHS_CRITERIA[0];

      return `
        <div class="shs-audit-box">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="shs-domain-badge">${crit.domain_name}</span>
            <span style="font-size:0.8rem; color:var(--shs-muted); font-weight:600;">Question ${curIdx + 1} / ${total}</span>
          </div>

          <div class="shs-progress-bar" style="margin-bottom:14px;">
            <div class="shs-progress-fill" style="width: ${((curIdx + 1) / total) * 100}%;"></div>
          </div>

          <div class="shs-question-title">${crit.id} — ${crit.title}</div>
          <div class="shs-question-desc">${crit.explanation || crit.question}</div>

          <div class="shs-answers-grid">
            <button class="shs-ans-btn ans-yes" data-answer="yes">
              <span>🟢</span> <span>Oui totalement</span>
            </button>
            <button class="shs-ans-btn ans-partial" data-answer="partial">
              <span>🟡</span> <span>Partiellement</span>
            </button>
            <button class="shs-ans-btn ans-no" data-answer="no">
              <span>🔴</span> <span>Non</span>
            </button>
            <button class="shs-ans-btn" data-answer="unknown">
              <span>⚪</span> <span>Je ne sais pas / Plus tard</span>
            </button>
          </div>

          <div class="shs-nav-row">
            ${curIdx > 0 ? `
              <button class="shs-btn shs-btn-sec" id="btn-prev-q" style="width:auto; padding:8px 14px; font-size:0.85rem;">
                ◀️ Précédent
              </button>
            ` : '<div></div>'}
            <button class="shs-btn shs-btn-sec" id="btn-view-summary" style="width:auto; padding:8px 14px; font-size:0.85rem;">
              📊 Voir mon bilan
            </button>
          </div>
        </div>
      `;
    }

    // Cockpit view
    return `
      <div class="shs-score-hero">
        <div class="shs-score-row">
          <div>
            <span style="font-weight:700; font-size:1rem;">Indice de maturité :</span>
            ${isProvisional ? '<span class="shs-provisional-tag">Provisoire</span>' : ''}
            <div style="color:var(--shs-muted); font-size:0.85rem; margin-top:2px;">
              Niveau : <strong>${maturityText}</strong> • ${criticalCount > 0 ? `<span style="color:#f87171; font-weight:700;">⚠️ ${criticalCount} risque(s) critique(s)</span>` : '✅ 0 risque critique'}
            </div>
          </div>
          <div class="shs-score-val">${scoreVal.toFixed(1)} <span style="font-size:1rem; font-weight:600; color:var(--shs-muted);">/ 100</span></div>
        </div>

        <div class="shs-progress-bar">
          <div class="shs-progress-fill" style="width: ${Math.min(100, Math.max(0, completenessVal))}%;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--shs-muted);">
          <span>Éléments traités : ${completenessVal.toFixed(0)} %</span>
          <span>Potentiel : +${potentialGain.toFixed(1)} pts</span>
        </div>
      </div>

      <div class="shs-nav-tabs">
        <button class="shs-tab-btn ${this._activeTab === 'overview' ? 'active' : ''}" id="tab-overview">📊 Synthèse</button>
        <button class="shs-tab-btn ${this._activeTab === 'domains' ? 'active' : ''}" id="tab-domains">🏛️ Domaines</button>
        <button class="shs-tab-btn ${this._activeTab === 'actions' ? 'active' : ''}" id="tab-actions">⚡ Actions</button>
      </div>

      <div id="shs-tab-body">
        ${this._renderTabBody(isProvisional)}
      </div>

      <div style="display:flex; gap:8px; margin-top:14px;">
        <button class="shs-btn" id="btn-resume-audit" style="font-size:0.85rem;">
          📝 Reprendre / Modifier l'audit
        </button>
        <button class="shs-btn shs-btn-sec" id="btn-scan" style="font-size:0.85rem; width:auto;">
          🔄 Scan
        </button>
      </div>
    `;
  }

  _renderTabBody(isProvisional) {
    if (this._activeTab === 'domains') {
      const getDom = (key) => this._getEntity(key)?.state ?? '—';
      return `
        <div class="shs-domain-grid">
          <div class="shs-domain-card"><div class="shs-domain-title">⚡ Électricité</div><div class="shs-domain-score">${getDom('elec_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🔒 Cybersécurité</div><div class="shs-domain-score">${getDom('cyber_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🛡️ Résilience</div><div class="shs-domain-score">${getDom('res_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">⚙️ Automatisations</div><div class="shs-domain-score">${getDom('auto_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">☀️ Énergie</div><div class="shs-domain-score">${getDom('ener_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🔌 Protocoles Locaux</div><div class="shs-domain-score">${getDom('inter_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">📱 Expérience / UX</div><div class="shs-domain-score">${getDom('ux_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🛠️ Maintenance</div><div class="shs-domain-score">${getDom('maint_score')} / 100</div></div>
        </div>
      `;
    }

    if (this._activeTab === 'actions') {
      return `
        <div style="font-size:0.85rem; color:var(--shs-muted); line-height:1.4;">
          <div style="background:rgba(0,0,0,0.2); border-radius:8px; padding:12px; margin-bottom:8px;">
            <strong style="color:#93c5fd;">🎯 Recommandations ciblées</strong>
            <p style="margin:4px 0 0 0;">Consultez les suggestions hiérarchisées pour augmenter la fiabilité et l'autonomie de votre logement.</p>
          </div>
        </div>
      `;
    }

    return `
      <div style="font-size:0.85rem; color:var(--shs-muted); line-height:1.5;">
        ${isProvisional ? `
          <div style="background:rgba(245,158,11,0.1); border-left:3px solid #f59e0b; padding:8px 12px; border-radius:4px; margin-bottom:8px;">
            Score provisoire : répondez aux questions restantes pour finaliser votre bilan complet.
          </div>
        ` : `
          <div style="background:rgba(16,185,129,0.1); border-left:3px solid #10b981; padding:8px 12px; border-radius:4px; margin-bottom:8px; color:#a7f3d0;">
            Audit complet validé. Consultez les recommandations pour progresser vers le niveau supérieur.
          </div>
        `}
      </div>
    `;
  }

  _bindEvents() {
    this.shadowRoot.getElementById('btn-start-first-audit')?.addEventListener('click', () => {
      this._view = 'audit';
      this._currentQuestionIndex = 0;
      this._hass?.callService('smart_home_score', 'run_analysis', {});
      this._render();
    });

    this.shadowRoot.querySelectorAll('.shs-ans-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const ansKey = e.currentTarget.getAttribute('data-answer');
        const crit = SHS_CRITERIA[this._currentQuestionIndex];
        if (crit) {
          if (ansKey === 'unknown') {
            this._hass?.callService('smart_home_score', 'skip_question', { criterion_id: crit.id });
          } else {
            this._hass?.callService('smart_home_score', 'submit_answer', { criterion_id: crit.id, answer_key: ansKey });
          }
        }
        if (this._currentQuestionIndex < SHS_CRITERIA.length - 1) {
          this._currentQuestionIndex++;
        } else {
          this._view = 'cockpit';
        }
        this._render();
      });
    });

    this.shadowRoot.getElementById('btn-prev-q')?.addEventListener('click', () => {
      if (this._currentQuestionIndex > 0) {
        this._currentQuestionIndex--;
        this._render();
      }
    });

    this.shadowRoot.getElementById('btn-view-summary')?.addEventListener('click', () => {
      this._view = 'cockpit';
      this._render();
    });

    this.shadowRoot.getElementById('btn-resume-audit')?.addEventListener('click', () => {
      this._view = 'audit';
      this._render();
    });

    this.shadowRoot.getElementById('btn-scan')?.addEventListener('click', () => {
      this._hass?.callService('smart_home_score', 'run_analysis', {});
    });

    this.shadowRoot.getElementById('tab-overview')?.addEventListener('click', () => {
      this._activeTab = 'overview';
      this._render();
    });

    this.shadowRoot.getElementById('tab-domains')?.addEventListener('click', () => {
      this._activeTab = 'domains';
      this._render();
    });

    this.shadowRoot.getElementById('tab-actions')?.addEventListener('click', () => {
      this._activeTab = 'actions';
      this._render();
    });
  }
}

if (!customElements.get('smart-home-score-card')) {
  customElements.define('smart-home-score-card', SmartHomeScoreCard);
}

window.customCards = window.customCards || [];
const existingCardIdx = window.customCards.findIndex(c => c.type === 'smart-home-score-card');
const cardEntry = {
  type: 'smart-home-score-card',
  name: 'Smart Home Score',
  preview: true,
  description: "Indice de maturité et plan d'amélioration de votre maison connectée",
  documentationURL: 'https://github.com/nano2sillery/smart_home_score'
};

if (existingCardIdx >= 0) {
  window.customCards[existingCardIdx] = cardEntry;
} else {
  window.customCards.push(cardEntry);
}
