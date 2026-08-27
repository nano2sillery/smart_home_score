# 📝 Journal des Modifications (CHANGELOG)

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
