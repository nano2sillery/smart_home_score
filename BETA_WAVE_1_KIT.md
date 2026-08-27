# 📦 Kit de Lancement & Suivi — Beta Wave 1 (v0.7.0-beta.1)

Ce document rassemble l'ensemble des éléments prêts à l'emploi pour piloter la **Beta Wave 1** de **Smart Home Score**.

---

## 1. ✉️ Texte à transmettre aux Bêta-Testeurs

```markdown
Bonjour,

Merci d'avoir accepté de tester la première version bêta de **Smart Home Score** (version 0.7.0-beta.1) !

Smart Home Score est une intégration 100 % locale pour Home Assistant qui calcule un **indice de maturité domotique** (0 à 100) sur 8 domaines vitaux (Électricité, Cybersécurité, Résilience, Automatisations, Énergie, Protocoles locaux, Expérience utilisateur, Maintenance) et propose un plan d'amélioration personnalisé.

### 🔒 Confidentialité & Souveraineté
- **100 % Local** : Aucun cloud, aucun compte externe, aucune télémétrie masquée.
- Vos données ne quittent jamais votre Home Assistant.

---

### 🚀 Guide d'Installation Rapide (Zéro YAML)

**Prérequis** : Home Assistant 2024.7.0 ou supérieur avec HACS installé.

1. Dans Home Assistant, ouvrez **HACS** (barre latérale).
2. Cliquez sur les **3 petits points** (en haut à droite) ➔ **Dépôts personnalisés** (*Custom repositories*).
3. Collez l'adresse du dépôt GitHub : `https://github.com/nano2sillery/smart_home_score`
4. Choisissez la catégorie : **Intégration** puis cliquez sur **Ajouter**.
5. Recherchez **Smart Home Score** dans HACS et cliquez sur **Télécharger** (version `0.7.0-beta.1`).
6. **Redémarrez Home Assistant**.
7. Rendez-vous dans **Paramètres** ➔ **Appareils et services** ➔ **Ajouter une intégration** ➔ Sélectionnez **Smart Home Score**.
8. L'analyse démarre automatiquement et la carte Cockpit s'affiche sur votre tableau de bord !

---

### ⏱️ Déroulement du Test (5 à 10 minutes)
1. Laissez le premier scan automatique s'exécuter.
2. Parcourez l'assistant d'audit (répondez simplement en français : *Oui totalement*, *Partiellement*, *Non*, ou *Je ne sais pas*).
3. Si une note attribuée automatiquement vous semble inexacte, cliquez sur **« Cette évaluation est incorrecte ? »** sur la fiche du critère pour indiquer votre situation réelle.
4. Consultez votre score global, vos scores par domaine et vos recommandations d'actions.

Une fois terminé, merci de me renvoyer vos impressions via le court formulaire ci-dessous !
```

---

## 2. 📋 Modèle de Formulaire de Retour Bêta

*(À copier/coller ou transmettre à chaque testeur)*

```markdown
---
### 📝 Formulaire de Retour — Smart Home Score (Bêta)

- **Votre identifiant testeur** : [ex: BETA-001]
- **Version de Home Assistant** : [ex: 2024.11.2 / 2025.1.0 / 2026.x]
- **Type de logement / Profil** : [ex: Maison 120m² avec solaire + Zigbee / Appartement 60m² Wi-Fi...]

#### 1. Installation & Prise en main
- L'installation s'est-elle faite en un clic sans encombre ? [Oui / Non (précisez)] :
- L'interface s'est-elle affichée correctement après le redémarrage ? [Oui / Non] :
- Durée approximative de l'audit : [ex: 6 minutes]

#### 2. Compréhension & Précision
- Le nombre de critères évalués automatiquement vous a-t-il semblé cohérent ? :
- Avez-vous contesté des notes automatiques ? Si oui, sur quels critères (ex: ELEC02, RES05) et pourquoi ? :
- Y a-t-il des questions que vous avez laissées en "Je ne sais pas" ? :
- Les recommandations d'amélioration générées sont-elles claires et pertinentes ? :

#### 3. Problèmes & Suggestions
- Avez-vous rencontré des bugs ou des comportements anormaux ? :
- Vos suggestions pour améliorer l'expérience :
- Diagnostic anonymisé joint ? [Oui / Non] (voir guide d'export ci-dessous)
---
```

---

## 3. 📊 Tableau de Suivi — Beta Wave 1

| Beta ID | Profil Général | Version HA | Version SHS | Install OK | Audit Terminé | Durée | Nb AUTO | Contestations AUTO | Je ne sais pas | Bugs identifiés | Gravité Bug | Suggestions | Diag Joint | Statut |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BETA-001** | *En attente* | — | 0.7.0-beta.1 | — | — | — | — | — | — | — | — | — | — | 🟡 Attribué |
| **BETA-002** | *En attente* | — | 0.7.0-beta.1 | — | — | — | — | — | — | — | — | — | — | 🟡 Attribué |
| **BETA-003** | *En attente* | — | 0.7.0-beta.1 | — | — | — | — | — | — | — | — | — | — | 🟡 Attribué |
| **BETA-004** | *En attente* | — | 0.7.0-beta.1 | — | — | — | — | — | — | — | — | — | — | 🟡 Attribué |
| **BETA-005** | *En attente* | — | 0.7.0-beta.1 | — | — | — | — | — | — | — | — | — | — | 🟡 Attribué |
| **BETA-006** | *En attente* | — | 0.7.0-beta.1 | — | — | — | — | — | — | — | — | — | — | 🟡 Attribué |
| **BETA-007** | *En attente* | — | 0.7.0-beta.1 | — | — | — | — | — | — | — | — | — | — | 🟡 Attribué |
| **BETA-008** | *En attente* | — | 0.7.0-beta.1 | — | — | — | — | — | — | — | — | — | — | 🟡 Attribué |
| **BETA-009** | *En attente* | — | 0.7.0-beta.1 | — | — | — | — | — | — | — | — | — | — | 🟡 Attribué |
| **BETA-010** | *En attente* | — | 0.7.0-beta.1 | — | — | — | — | — | — | — | — | — | — | 🟡 Attribué |

---

## 4. 🛡️ Procédure pour Exporter et Transmettre un Diagnostic Anonymisé

*(À communiquer au testeur s'il accepte de joindre son fichier de diagnostic)*

1. Dans Home Assistant, allez dans **Paramètres** ➔ **Appareils et services**.
2. Cliquez sur l'intégration **Smart Home Score**.
3. Cliquez sur les **3 petits points verticaux** (ou le menu d'options de l'entrée) ➔ **Télécharger les données de diagnostic** (*Download diagnostics*).
4. Un fichier `.json` ou `.txt` se télécharge sur votre ordinateur.
5. **Garantie de confidentialité** : Ce fichier est automatiquement filtré :
   - Les adresses IP sont masquées (`xxx.xxx.xxx.xxx`).
   - Les adresses MAC sont masquées (`xx:xx:xx:xx:xx:xx`).
   - Les e-mails, chemins de fichiers locaux et noms de réseaux Wi-Fi (SSID) sont masqués.
   - Aucun mot de passe ni identifiant personnel n'est inclus.
6. Transmettez ce fichier en pièce jointe de votre retour.

---

## 5. 🔄 Protocole de Communication Cyrille ➔ Agent IA

Dès que vous recevez le retour d'un testeur, transmettez-le moi sous la forme :

```text
Retour BETA-XXX :
[Coller le formulaire de retour rempli ou le texte du testeur]
[Coller éventuellement le diagnostic JSON ou l'extrait]
```

### Mon Rôle et Mes Engagements :
1. **Enregistrement & Synthèse** : Mise à jour immédiate du tableau de suivi `Beta Wave 1`.
2. **Classification Structurée des Anomalies** :
   - 🔴 **BLOCKER** : Crash HA, blocage d'installation, corruption de configuration.
   - 🟠 **CRITICAL** : Faux positif majeur sur critère critique, calcul faussé.
   - 🟡 **MAJOR** : Question bloquée, contestation de règle AUTO reproductible.
   - 🔵 **MINOR** : Erreur de libellé, coquille, alignement visuel, warning dans les logs.
   - 💡 **SUGGESTION** : Idée d'ergonomie ou proposition de critère.
3. **Reproduction de Bug** : Création d'une fixture reproduisant le profil exact de l'anomalie.
4. **Correction Déterministe & Test de Non-Régression** :
   - Écriture préalable du test unitaire reproduisant le problème.
   - Application du correctif minimal et ciblé.
   - Validation que les 59 tests historiques et le benchmark (83,1 pts) restent stricts et intacts.
5. **Préparation de Version** : Proposition du changelog pour `0.7.0-beta.2`, `0.7.0-beta.3`, etc., sous votre validation préalable.
