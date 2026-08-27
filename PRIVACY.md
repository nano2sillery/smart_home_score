# 🛡️ Engagement de Confidentialité — Smart Home Score

**Auteur : Cyrille LEFRANC**
**Version du modèle : MODEL_VERSION 1.0**

L'intégration **Smart Home Score** a été conçue dès le premier jour avec une exigence absolue de **souveraineté et de protection de la vie privée**.

---

### 1. Fonctionnement 100 % Local
- L'intégralité du code (analyse locale, moteur de règles, calculs mathématiques, assistant d'audit et advisor) s'exécute exclusivement au sein de votre instance Home Assistant locale.

### 2. Aucune Transmission de Données
- Aucune donnée concernant votre installation, vos entités, vos habitudes, vos scores ou vos réponses n'est envoyée vers un serveur externe, un cloud ou un tiers.
- Aucun tracker, aucun outil d'analyse comportementale, aucune télémétrie cachée n'est embarqué dans le composant.

### 3. Sanctuaire des Secrets & Sécurité
- Smart Home Score **ne lit jamais** vos fichiers contenant des secrets (`secrets.yaml`, tokens d'accès, mots de passe, clés d'API).
- L'analyse environnementale s'appuie uniquement sur les décomptes et métadonnées structurelles non sensibles (types d'intégrations locales vs cloud, présences d'espaces/zones, typologies de protocoles).

### 4. Diagnostics Anonymisés
- Les diagnostics exportables pour le support technique masquent et anonymisent automatiquement les adresses IP, adresses MAC, adresses email et identifiants personnels.

---
*Smart Home Score : Mesurer la maturité sans jamais compromettre votre intimité.*
