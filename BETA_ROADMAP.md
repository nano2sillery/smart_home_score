# 🎯 Feuille de Route & Critères de Sortie de Bêta (v0.7.0 ➔ v1.0.0)

**Auteur : Cyrille LEFRANC**
**Référentiel Métier : MODEL_VERSION 1.0 (59 critères)**

La phase Bêta v0.7.x a pour objectif d'éprouver la robustesse, la clarté et la fiabilité de Smart Home Score en conditions réelles sur une diversité d'installations Home Assistant.

---

### 📋 Critères Objectifs de Sortie de Bêta (Passage en v1.0.0)

1. **Diversité Validée** :
   - Au moins 10 installations réelles et hétérogènes testées avec succès (Zigbee, Matter, Z-Wave, Photovoltaïque, Cloud-heavy, Appartements, Villas).
2. **Précision du Moteur AUTO** :
   - Zéro faux positif critique non corrigé.
   - Taux de contestation des notes AUTO inférieur à 5 % sur les critères automatisés.
3. **Clarté du Questionnaire** :
   - Moins de 5 % de réponses *« Je ne sais pas »* sur les critères applicables standards.
   - Temps d'audit médian constaté entre 5 et 8 minutes.
4. **Stabilité & Compatibilité** :
   - Aucune erreur bloquante lors de l'installation, de la mise à jour ou de la désinstallation.
   - Compatibilité vérifiée sur les versions Home Assistant supportées.
5. **Gouvernance & Transparence** :
   - Maintien strict du caractère 100 % local (zéro cloud, zéro télémétrie masquée, zéro IA distante).
   - Intégrité mathématique absolue du score (8 domaines pondérés sommant à 100 %).
