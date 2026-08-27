# 🏠 Smart Home Score — Indice de Maturité Domotique

> **Statut : Bêta Communautaire (v0.7.0)**  
> **Avertissement :** Smart Home Score est en phase de validation communautaire. Les résultats sont indicatifs et le référentiel peut encore évoluer au fil des retours utilisateurs. Il s'agit d'un **Indice de maturité** déterministe et explicable, et non d'une certification officielle.

---

## 🌟 Principes Fondamentaux
- **100 % Local & Privé** : Zéro cloud, zéro compte externe, zéro télémétrie masquée, zéro IA distante.
- **59 Critères Objectifs** : Répartis sur 8 domaines vitaux (Électricité, Cybersécurité, Résilience, Automatisations, Énergie, Protocoles locaux, Expérience utilisateur, Maintenance).
- **Zéro YAML** : Installation en un clic via l'interface Home Assistant.
- **Advisor Intégré** : Recommandations d'actions hiérarchisées et identification des *Quick Wins*.

---

## 🚀 Installation via HACS (Custom Repository)

1. Ouvrez **HACS** dans votre barre latérale Home Assistant.
2. Cliquez sur les trois petits points en haut à droite ➔ **Dépôts personnalisés** (*Custom repositories*).
3. Ajoutez l'URL de votre dépôt GitHub et sélectionnez la catégorie **Intégration**.
4. Cliquez sur **Télécharger** la version `0.7.0-beta.1`.
5. **Redémarrez Home Assistant**.
6. Allez dans **Paramètres** ➔ **Appareils et services** ➔ **Ajouter une intégration** ➔ Recherchez **Smart Home Score**.
7. L'interface et les capteurs sont immédiatement disponibles !

---

## ⚖️ Contestation d'une Note Automatique & Retours Bêta

Si le moteur automatique attribue une note qui ne reflète pas votre réalité :
1. Dans la fiche du critère concerné, cliquez sur **« Cette évaluation est incorrecte ? »**.
2. Saisissez votre note réelle et laissez un court commentaire explicatif.
3. La preuve originale est conservée et le critère est marqué pour amélioration dans le diagnostic.

### 🐞 Signaler un Problème / Proposer une Amélioration
- Rendez-vous sur notre [GitHub Issues](https://github.com/nano2sillery/smart_home_score/issues).
- Utilisez les modèles dédiés :
  - **⚖️ Contestation d'Évaluation AUTO**
  - **🐞 Rapport de Bug**
  - **💡 Suggestion de Critère**
- Vous pouvez joindre facultativement votre **diagnostic anonymisé** exportable depuis Home Assistant (*Paramètres > Appareils et services > Smart Home Score > Télécharger les diagnostics*). Aucun identifiant privé ou adresse IP n'est collecté.

---

## 🔄 Mise à Jour & Retour Arrière (Rollback)

- **Mise à jour** : Via HACS ➔ Télécharger la nouvelle version ➔ Redémarrer Home Assistant. Le cache navigateur est automatiquement invalidé (`?v=0.7.0`).
- **Retour Arrière** : Dans HACS ➔ Smart Home Score ➔ Redémarrer ➔ Choisir la version précédente souhaitée. Vos réponses et l'historique de vos audits sont conservés en toute sécurité dans `.storage`.

---

## 📄 Licence & Auteur
- **Auteur** : Cyrille LEFRANC
- **Licence** : Apache 2.0
