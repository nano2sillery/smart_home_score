# 📝 Journal des Modifications (CHANGELOG)

## [0.7.0-beta.13] - 2026-08-28
### Protection d'Historique Strict (100% Completeness) & Snapshot Unique
- **Archivage Conditionné aux Audits Complets** : `restart_audit` n'archive désormais dans l'historique que les audits ayant atteint 100% de complétude (les audits partiels ou interrompus sont ignorés).
- **Structure de Snapshot d'Historique Enrichie** : Ajout d'un `audit_id` unique par UUID, `completed_at`, `criteria_count` (59), `critical_risks` et `completeness` (100.0).
- **Couverture de Tests** : 4 nouveaux tests unitaires dédiés à la protection de l'historique (75 tests validés à 100%).

## [0.7.0-beta.12] - 2026-08-28
### Action 'Faire un nouvel audit', Archivage Automatique & Boîte de Confirmation
- **Action 'Faire un nouvel audit' (`restart_audit`)** : Permet de repartir d'un scan 100% vierge sans réinjecter les anciennes réponses de l'utilisateur.
- **Archivage Automatique en Historique** : L'audit précédent terminé est automatiquement sauvegardé dans l'historique d'évolution avant la réinitialisation.
- **Boîte de Confirmation UX** : Fenêtre modale de confirmation explicite prévenant toute fausse manipulation.
- **Différenciation Nette Rescan vs Nouvel Audit** : `Rescan` conserve les réponses acquises et vérifie les dérives ; `Faire un nouvel audit` relance un cycle complet depuis zéro.
- **Suite de 71 Tests Automatisés** (100% de succès).

## [0.7.0-beta.11] - 2026-08-28
### Ligne Synthétique d'Analyse, Potentiel Cliquable & Feedback Visuel Loader
- **Bannière Synthétique d'Inspection Réelle** : Affichage systématique en tête de la ligne `🔎 Analyse : X appareils • Y entités • Z automatisations • W intégrations`.
- **Raccourci Interactif Potentiel** : Le badge `⚡ Potentiel : +X.X pts` dans le bloc de score est désormais cliquable et ouvre immédiatement l'onglet **Actions**.
- **Indicateur de Chargement / Loader Réactif** : Affichage d'un spinner semi-transparent élégant lors des actions et calculs de synchronisation pour un feedback instantané.

## [0.7.0-beta.10] - 2026-08-28
### Onglet Actions Opérationnel, Transparence d'Analyse du Scan & Compteurs Clairs
- **Onglet Actions & Recommandations Riches** : Génération systématique des fiches d'action pour chaque critère perfectible (< 4/4) avec Situation actuelle, Objectif suivant, Gain potentiel précis (+X pt), Effort (Facile/Moyen/Avancé), Type d'action et conseils d'amélioration officiels du référentiel v1.0.
- **Transparence d'Analyse Approfondie** : Ajout du bloc « Votre installation analysée » affichant les nombres réels d'appareils, entités, intégrations, automatisations, scripts, zones et protocoles locaux (Zigbee, Matter, Z-Wave).
- **Compteurs de Découverte Clairs et Explicites** : Remplacement des compteurs ambigus par 3 métriques non équivoques : Critères validés automatiquement / Réponses déjà suggérées / Questions sans réponse détectable (59 critères au total).
- **Test de Non-Régression** : Couverture automatisée validant que l'onglet Actions n'est jamais vide lorsque le score est inférieur à 100 (66 tests validés à 100%).

## [0.7.0-beta.9] - 2026-08-28
### Détection Universelle de l'Entité Score & Domaines Multilingues
- **Résolution Multilingue Universelle** : Découverte automatique et indépendante de la langue (français/anglais) de l'entité Score Global via la signature de ses attributs `criteria_states`.
- **Exposition Directe des Scores de Domaines** : Intégration de l'attribut `domain_scores` sur le capteur global pour un affichage immédiat sans dépendre du nommage des entités individuelles.
- **Affichage Découverte Automatique Garanti** : Le bilan de scan (critères auto-évalués et pré-remplis) s'affiche désormais avec 100% de fiabilité sur toute instance Home Assistant.

## [0.7.0-beta.8] - 2026-08-28
### Correction Critique 'Erreur de configuration' & Rendu Lovelace Robuste
- **Résolution 'Erreur de configuration'** : Correction de `_getEntity()` qui levait une exception `TypeError: Cannot read properties of undefined (reading 'startsWith')` sur les dictionnaires d'états non homogènes.
- **Rendu Résilient** : Encapsulation complète de la fonction de rendu dans un bloc try/catch prévenant tout plantage dans le tableau de bord Lovelace.
- **Test Automatisé de Cycle de Vie Frontend** : Ajout d'un test complet simulant l'instanciation, le passage de configuration vide, les états hétérogènes et les transitions de vue en environnement navigateur simulé (64 tests au vert).

## [0.7.0-beta.7] - 2026-08-27
### Correction Critique de l'Exécution du Scan & Détection Réelle
- **Exécution Réelle du Moteur de Scan** : Correction du ChangeTracker qui ignorait les critères non confirmés lors des scans successifs.
- **Propagation Temps Réel vers le Frontend** : Notification immédiate des capteurs et de la carte Lovelace dès la fin de l'analyse automatique.
- **Bilan Découverte Effectif** : Remplissage instantané des critères auto-évalués et des propositions pré-remplies selon les équipements réels de Home Assistant.

## [0.7.0-beta.6] - 2026-08-27
### Scan Automatique Intelligent & Entretien Ciblé
- **Scanner Visuel Interactif** : Lancement d'un scan automatique direct des entités, intégrations et sauvegardes dès le début.
- **Bilan Découverte Instantané** : Affichage des critères évalués automatiquement (preuves directes), des propositions pré-remplies et du nombre de questions ciblées restantes.
- **Filtrage Intelligent** : L'entretien ne pose plus 59 questions aveugles mais se concentre uniquement sur les éléments nécessitant une confirmation ou invisibles par logiciel.
- **Bouton de Confirmation Rapide 1-Clic** : Validation immédiate des observations détectées par Home Assistant.

## [0.7.0-beta.5] - 2026-08-27
### Amélioration UX Entretien d'Audit Humain & Fidélité Référentiel v1.0
- **Questions en Langage Naturel** : 59 questions formulées concrètement sur la vie du logement.
- **Réponses Contextualisées** : Choix de réponses fidèles aux niveaux 0 à 4 historiques, sans note apparente pour l'utilisateur.
- **Boutons 'Pourquoi cette question ?'** : Explication du sens et de l'intérêt de chaque critère en un clic.
- **Séparation Stricte** : Distinction nette entre *Je ne sais pas / Plus tard* (NEEDS_REVIEW) et *Non applicable* (NOT_APPLICABLE).
- **Non-régression Validée** : 63 tests unitaires au vert, conservation exacte du benchmark officiel à 83,1 / 100.

## [0.7.0-beta.4] - 2026-08-27
### Corrigé (Assistant d'Audit Interactif Intégré)
- **Déclenchement Interactif Immédiat** : Le bouton *« 🚀 Lancer mon premier audit »* ouvre immédiatement le questionnaire interactif pas-à-pas directement sur la carte Lovelace.
- **Formulation Naturelle des Choix** : 🟢 Oui totalement, 🟡 Partiellement, 🔴 Non, ⚪ Je ne sais pas / Plus tard.
- **Progression et Navigation Fluide** : Jauge de progression par question, passage fluide vers le cockpit final avec score global et bilan par domaine.

## [0.7.0-beta.3] - 2026-08-27
### Amélioration (Frontend Auto-Loader & Lovelace Discovery)
- **Auto-enregistrement Lovelace Resources** : Enregistrement automatique dans la collection des ressources Lovelace Home Assistant lors du démarrage de l'intégration pour un chargement instantané sans rechargement forcé de page.
- **Console Banner Développeur** : Ajout du message de confirmation `SMART-HOME-SCORE v0.7.0-beta.3` dans la console navigateur pour faciliter le diagnostic.
- **Résolution Dynamique des Entités** : Mécanisme de découverte d'entités résilient aux variations d'identifiants Home Assistant.
- **Nettoyage HACS Integration** : Suppression du champ ambigu `filename` dans `hacs.json` pour garantir une distribution standard d'intégration.

## [0.7.0-beta.2] - 2026-08-27
### Corrigé (Bug Bloquant Frontend / UX)
- **Catalogue des cartes Home Assistant (`window.customCards`)** : Enregistrement officiel avec `preview: true` permettant d'ajouter la carte en 1 clic sans aucun YAML.
- **Résilience `setConfig()` & `getStubConfig()`** : Support natif d'une configuration vide `{}` sans exception.
- **Correction SyntaxError JavaScript** : Résolution de l'échappement de chaîne qui bloquait l'exécution du script frontend dans le navigateur.
- **Écran d'accueil Zéro-Audit** : Affichage d'un panneau d'accueil bienveillant *« Bienvenue dans Smart Home Score — Lancer mon premier audit »* lorsque l'intégration est fraîchement installée.

## [0.7.0-beta.1] - 2026-08-27 (Bêta Communautaire)
### Ajouté
- **Garde-fou Singleton HTTP** : Enregistrement de `async_register_static_paths` garanti strictly unique par processus Home Assistant (résiste à 10 reloads consécutifs).
- **Service de Contestation (`dispute_auto_evaluation`)** : Permet aux testeurs de contester une note AUTO, de saisir leur score réel avec feedback tout en conservant la preuve originale.
- **Fixtures de Profils Anonymisés** : 6 installations types (Appartement minimal, Zigbee dense, Z-Wave/Matter, Solaire/Batterie, Cloud-heavy, Grande villa).
- **Feuille de Route Bêta (`BETA_ROADMAP.md`)** : Critères objectifs et métriques de validation pour la sortie de bêta.
- **Modèles GitHub Issues** : Templates structurés pour les contestations AUTO, rapports de bugs et suggestions.
- **Diagnostics Enrichis** : Export détaillé de l'état des 59 critères, des contestations et de la répartition AUTO/QUESTION/TEST sans donnée privée.

### Modifié
- Mention officielle : « Indice de maturité Smart Home Score — Bêta v0.7.0 ».
- `MODEL_VERSION = "1.0"` (59 critères inchangés).

---

## [0.6.2] - 2026-08-27
- Migration complète vers `async_register_static_paths` avec `StaticPathConfig`.
- Utilisation exclusive de `add_extra_js_url` et `remove_extra_js_url`.
- Zéro occurrence de `register_static_path` ou de `hass.data` fallback.

## [0.6.1] - 2026-08-27
- Packaging HACS officiel, Frontend embarqué, Cache-busting `?v=0.6.1`.

## [0.5.1] - 2026-08-27
- Séparation stricte Maturité vs Health, taxonomie 7 types d'action, isolation historique.
