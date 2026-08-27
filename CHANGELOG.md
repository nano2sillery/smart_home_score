# 📝 Journal des Modifications (CHANGELOG)

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
