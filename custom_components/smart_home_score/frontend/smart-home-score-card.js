/**
 * Smart Home Score Lovelace Custom Card (v0.7.0-beta.16)
 * Author: Cyrille LEFRANC
 * 100% Local Lovelace Card for Home Assistant.
 * Intelligent Automated System Scanner, Assisted Pre-filled Proposals, Live Scoring & Human Audit.
 */

console.info(
  '%c SMART-HOME-SCORE %c v0.7.0-beta.16 ',
  'color: white; background: #3b82f6; font-weight: 700; border-radius: 3px 0 0 3px;',
  'color: #3b82f6; background: #1e293b; font-weight: 700; border-radius: 0 3px 3px 0;'
);

const SHS_CRITERIA = [
  {
    "id": "ELEC01",
    "domain": "ELEC",
    "domain_name": "⚡ Sécurité électrique & sûreté",
    "title": "Maintien des commandes manuelles",
    "critical": true,
    "question": "Pouvez-vous toujours allumer vos lumières et commander vos volets avec vos interrupteurs muraux si votre box domotique tombe en panne ?",
    "why": "En cas de défaillance matérielle ou de plantage du serveur, les occupants et les invités doivent toujours pouvoir s'éclairer et ouvrir les volets manuellement.",
    "options": [
      {
        "label": "Oui, 100 % de mes interrupteurs et boutons muraux fonctionnent de façon totalement autonome et câblée",
        "score": 4
      },
      {
        "label": "Oui pour la quasi-totalité, seuls 1 ou 2 éclairages décoratifs dépendent de l'application",
        "score": 3
      },
      {
        "label": "La plupart fonctionnent, mais plusieurs lumières ou volets importants sont bloqués sans la box",
        "score": 2
      },
      {
        "label": "Très peu d'interrupteurs physiques : la majorité des commandes impose d'utiliser un smartphone",
        "score": 1
      },
      {
        "label": "Non, la maison est paralysée sans la box domotique",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ELEC02",
    "domain": "ELEC",
    "domain_name": "⚡ Sécurité électrique & sûreté",
    "title": "Dimensionnement des actionneurs",
    "critical": true,
    "question": "Les modules et prises connectées qui pilotent vos appareils gourmands (radiateurs, chauffe-eau, four, lave-linge) sont-ils prévus pour supporter leur puissance maximale ?",
    "why": "Un micromodule sous-dimensionné qui pilote une charge trop forte peut surchauffer, souder ses contacts électriques ou provoquer un départ de feu.",
    "options": [
      {
        "label": "Oui, tous les gros consommateurs passent par des contacteurs de puissance ou des modules industriels largement dimensionnés",
        "score": 4
      },
      {
        "label": "Oui, les puissances ont été vérifiées et respectent les limites recommandées par les fabricants",
        "score": 3
      },
      {
        "label": "Les puissances sont respectées pour la plupart, mais quelques appareils chauffent un peu lors d'un usage prolongé",
        "score": 2
      },
      {
        "label": "Certains modules compacts pilotent directement de gros radiateurs ou appareils sans contacteur relais",
        "score": 1
      },
      {
        "label": "Aucune vérification des puissances : risque de surchauffe ou de soudure des relais internes",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ELEC03",
    "domain": "ELEC",
    "domain_name": "⚡ Sécurité électrique & sûreté",
    "title": "États sûrs au redémarrage",
    "critical": false,
    "question": "Après une coupure de courant, vos prises et éclairages connectés reprennent-ils un état sécurisé (par exemple rester éteints ou reprendre leur état précédent) ?",
    "why": "Évite qu'un radiateur d'appoint ou une plaque de cuisson ne s'allume tout seul après le rétablissement du courant en votre absence.",
    "options": [
      {
        "label": "Oui, chaque module est configuré individuellement avec un état sûr défini après coupure (mémoire d'état ou maintien éteint)",
        "score": 4
      },
      {
        "label": "La majorité des modules est configurée pour reprendre son état antérieur avant coupure",
        "score": 3
      },
      {
        "label": "Comportement par défaut des modules conservé sans configuration personnalisée",
        "score": 2
      },
      {
        "label": "Certains appareils s'allument à 100 % en pleine nuit après une micro-coupure",
        "score": 1
      },
      {
        "label": "Comportement totalement imprévisible et non maîtrisé après une coupure",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ELEC04",
    "domain": "ELEC",
    "domain_name": "⚡ Sécurité électrique & sûreté",
    "title": "Interverrouillages",
    "critical": true,
    "question": "Vos volets roulants, portails ou moteurs disposent-ils d'une sécurité matérielle empêchant d'activer en même temps les ordres de montée et de descente ?",
    "why": "Envoyer simultanément l'ordre de monter et de descendre sur un moteur de volet ou de portail peut griller le bobinage en quelques secondes.",
    "options": [
      {
        "label": "Oui, protection matérielle absolue (relais inverseurs mécaniques ou modules dédiés volets empêchant physiquement la double commande)",
        "score": 4
      },
      {
        "label": "Modules volets dédiés avec interverrouillage logiciel intégré et fiable",
        "score": 3
      },
      {
        "label": "Interverrouillage géré uniquement par des automatisations dans Home Assistant sans sécurité matérielle",
        "score": 2
      },
      {
        "label": "Risque théorique de commande simultanée sur certains moteurs",
        "score": 1
      },
      {
        "label": "Aucune sécurité : possibilité d'alimenter montée et descente en même temps, risquant de griller le moteur",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ELEC05",
    "domain": "ELEC",
    "domain_name": "⚡ Sécurité électrique & sûreté",
    "title": "Gestion des équipements critiques",
    "critical": false,
    "question": "Vos équipements vitaux (congélateur, pompe de relevage, ventilation, alarme) conservent-ils un fonctionnement sûr si la domotique s'arrête ?",
    "why": "Un équipement critique ne doit jamais cesser de fonctionner simplement parce qu'un composant logiciel domotique est en maintenance.",
    "options": [
      {
        "label": "Oui, les équipements critiques sont totalement indépendants et possèdent leur propre sécurité autonome",
        "score": 4
      },
      {
        "label": "Les équipements critiques sont surveillés par la domotique mais restent secourus et autonomes",
        "score": 3
      },
      {
        "label": "La domotique pilote certains appareils critiques mais avec une reprise manuelle facile",
        "score": 2
      },
      {
        "label": "Un arrêt de la domotique peut laisser un appareil critique dans un état indésirable (ex: pompe coupée)",
        "score": 1
      },
      {
        "label": "Les équipements vitaux dépendent entièrement de Home Assistant pour fonctionner",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "CYBER01",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité",
    "title": "Accès distant sécurisé",
    "critical": true,
    "question": "Comment vous connectez-vous à votre Home Assistant lorsque vous êtes à l'extérieur de chez vous ?",
    "why": "Ouvrir directement un port non chiffré sur Internet expose votre serveur domotique à des piratages automatisés permanents.",
    "options": [
      {
        "label": "Via Home Assistant Cloud officiel (Nabu Casa), un tunnel sécurisé ou un VPN privé (WireGuard / Tailscale)",
        "score": 4
      },
      {
        "label": "Via un proxy inverse sécurisé avec certificat HTTPS valide et filtrage d'adresses",
        "score": 3
      },
      {
        "label": "Via une redirection de port avec certificat HTTPS personnel (Let's Encrypt)",
        "score": 2
      },
      {
        "label": "Via un nom de domaine sans cadenas sécurisé",
        "score": 1
      },
      {
        "label": "En ouvrant directement le port HTTP non chiffré sur ma box Internet",
        "score": 0
      }
    ],
    "has_not_applicable": true,
    "not_applicable_label": "Non applicable (aucun accès distant)"
  },
  {
    "id": "CYBER02",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité",
    "title": "Double authentification (2FA)",
    "critical": false,
    "question": "Avez-vous activé la double authentification (code temporaire sur smartphone) pour vous connecter à Home Assistant ?",
    "why": "Même si votre mot de passe venait à être dérobé, la double authentification empêche un intrus de se connecter à votre maison.",
    "options": [
      {
        "label": "Oui, activée et obligatoire sur tous les comptes du foyer avec clés de secours notées",
        "score": 4
      },
      {
        "label": "Activée sur tous les comptes administrateurs",
        "score": 3
      },
      {
        "label": "Configurée sur un seul compte utilisateur",
        "score": 2
      },
      {
        "label": "Configuration commencée mais non finalisée",
        "score": 1
      },
      {
        "label": "Non, la connexion se fait uniquement par mot de passe",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "CYBER03",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité",
    "title": "Comptes utilisateurs individualisés",
    "critical": false,
    "question": "Chaque personne du foyer utilise-t-elle son propre compte personnel pour se connecter à Home Assistant ?",
    "why": "Avoir des comptes séparés permet de personnaliser l'expérience de chacun, de gérer les présences et de tracer les actions.",
    "options": [
      {
        "label": "Oui, chaque membre possède son propre compte avec des droits et tableaux de bord adaptés",
        "score": 4
      },
      {
        "label": "Chaque membre a son compte nominatif mais avec des droits identiques",
        "score": 3
      },
      {
        "label": "Deux comptes existent (un principal et un partagé pour le reste de la famille)",
        "score": 2
      },
      {
        "label": "Tout le monde utilise le même compte administrateur partagé",
        "score": 1
      },
      {
        "label": "Aucun compte configuré en dehors du compte par défaut sans mot de passe",
        "score": 0
      }
    ],
    "has_not_applicable": true,
    "not_applicable_label": "Non applicable (je vis seul)"
  },
  {
    "id": "CYBER04",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité",
    "title": "Principe du moindre privilège",
    "critical": false,
    "question": "Les personnes qui ne gèrent pas la technique (enfants, invités, conjoints) ont-elles des droits restreints sans accès aux paramètres système ?",
    "why": "Restreindre les droits d'administration évite les suppressions ou déréglages accidentels par les enfants ou les invités.",
    "options": [
      {
        "label": "Oui, seuls les gestionnaires sont administrateurs, tous les autres utilisateurs ont des profils stricts et verrouillés",
        "score": 4
      },
      {
        "label": "La plupart des utilisateurs sont en profil utilisateur simple sans accès aux paramètres",
        "score": 3
      },
      {
        "label": "Seul un compte invité est restreint, les autres sont administrateurs",
        "score": 2
      },
      {
        "label": "Tous les membres du foyer ont les pleins droits administrateur",
        "score": 1
      },
      {
        "label": "Aucun contrôle d'accès : tout utilisateur peut modifier ou supprimer la configuration",
        "score": 0
      }
    ],
    "has_not_applicable": true,
    "not_applicable_label": "Non applicable (je vis seul)"
  },
  {
    "id": "CYBER05",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité",
    "title": "Gestion des secrets et identifiants sensibles",
    "critical": true,
    "question": "Vos mots de passe, tokens et clés secrètes sont-ils isolés dans le fichier secrets.yaml ou un coffre-fort sécurisé ?",
    "why": "Centraliser les secrets évite d'exposer accidentellement vos mots de passe lors d'un partage de configuration ou d'une sauvegarde.",
    "options": [
      {
        "label": "Oui, 100 % des identifiants et clés sensibles sont isolés dans secrets.yaml sans aucune fuite",
        "score": 4
      },
      {
        "label": "La quasi-totalité des secrets est bien centralisée dans secrets.yaml",
        "score": 3
      },
      {
        "label": "La plupart des mots de passe sont protégés mais il reste quelques clés en clair dans des fichiers YAML",
        "score": 2
      },
      {
        "label": "De nombreux mots de passe sont écrits en clair directement dans les scripts et automatisations",
        "score": 1
      },
      {
        "label": "Tous les mots de passe et identifiants sont écrits en clair dans les fichiers de configuration",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "CYBER06",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité",
    "title": "Politique de mises à jour",
    "critical": false,
    "question": "À quelle fréquence appliquez-vous les mises à jour de Home Assistant et de ses composants ?",
    "why": "Les mises à jour mensuelles corrigent les failles de sécurité découvertes et assurent la stabilité de vos équipements.",
    "options": [
      {
        "label": "Régulièrement chaque mois après avoir lu les nouveautés et avec une sauvegarde automatique préalable",
        "score": 4
      },
      {
        "label": "Mises à jour appliquées au moins une fois par mois",
        "score": 3
      },
      {
        "label": "Mises à jour occasionnelles tous les 3 à 6 mois",
        "score": 2
      },
      {
        "label": "Mises à jour très rares (plus de 6 mois de retard)",
        "score": 1
      },
      {
        "label": "Aucune mise à jour appliquée depuis l'installation initiale",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "CYBER07",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité",
    "title": "Exposition et segmentation du réseau IoT",
    "critical": false,
    "question": "Vos objets connectés Wi-Fi (caméras, prises, ampoules) sont-ils séparés de vos ordinateurs personnels sur votre réseau ?",
    "why": "Si une ampoule ou une prise connectée bon marché est piratée, un réseau isolé empêche l'attaquant d'accéder à vos ordinateurs personnels.",
    "options": [
      {
        "label": "Oui, réseau Wi-Fi/VLAN dédié et isolé avec blocage d'accès vers les ordinateurs personnels",
        "score": 4
      },
      {
        "label": "Réseau Wi-Fi/VLAN séparé mais sans règles de pare-feu strictes",
        "score": 3
      },
      {
        "label": "Réseau local unique situé derrière le pare-feu/NAT de la box Internet (aucun port exposé vers l'extérieur, mais pas de séparation interne)",
        "score": 2
      },
      {
        "label": "Quelques objets isolés sur le Wi-Fi Invité, les autres mélangés aux ordinateurs",
        "score": 1
      },
      {
        "label": "Tous les objets connectés et ordinateurs mélangés sur le même réseau avec des ports ouverts vers Internet",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "CYBER08",
    "domain": "CYBER",
    "domain_name": "🔒 Cybersécurité",
    "title": "Surveillance et alertes de sécurité",
    "critical": false,
    "question": "Recevez-vous une alerte si quelqu'un tente de se connecter avec un mauvais mot de passe ou si un appareil suspect apparaît sur votre réseau ?",
    "why": "Être alerté d'une tentative de connexion anormale permet de bloquer rapidement un intrus avant qu'il n'accède au système.",
    "options": [
      {
        "label": "Oui, détection automatique des tentatives d'intrusion et alertes immédiates sur smartphone",
        "score": 4
      },
      {
        "label": "Notifications configurées pour les échecs de connexion à Home Assistant",
        "score": 3
      },
      {
        "label": "Journal des connexions vérifié manuellement de temps en temps",
        "score": 2
      },
      {
        "label": "Alertes de sécurité connues mais non configurées",
        "score": 1
      },
      {
        "label": "Aucune surveillance des connexions ni des accès réseau",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "RES01",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & continuité",
    "title": "Fonctionnement sans Internet",
    "critical": false,
    "question": "Si votre connexion Internet est coupée, vos automatisations locales, éclairages et boutons continuent-ils de fonctionner normalement dans la maison ?",
    "why": "Une maison autonome doit pouvoir s'éclairer, se chauffer et réagir aux boutons même en cas de coupure de fibre ou de panne opérateur.",
    "options": [
      {
        "label": "Oui, 100 % des commandes physiques, scénarios et régulations locales continuent de fonctionner sans Internet",
        "score": 4
      },
      {
        "label": "La très grande majorité fonctionne, seuls quelques services d'information météo ou vocaux sont indisponibles",
        "score": 3
      },
      {
        "label": "Les fonctions de base fonctionnent mais plusieurs appareils dépendants du cloud sont bloqués",
        "score": 2
      },
      {
        "label": "Seules quelques commandes très basiques fonctionnent encore",
        "score": 1
      },
      {
        "label": "Non, la maison est paralysée sans connexion Internet",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "RES02",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & continuité",
    "title": "Fonctionnement sans Home Assistant",
    "critical": true,
    "question": "Si votre serveur Home Assistant est totalement éteint ou en panne, pouvez-vous continuer à vivre normalement dans la maison (lumières, volets, chauffage) ?",
    "why": "La domotique doit apporter du confort en plus, sans jamais rendre le logement inhabitable lors d'une panne informatique.",
    "options": [
      {
        "label": "Oui, toutes les fonctions vitales restent pilotables manuellement et directement sans aucune gêne",
        "score": 4
      },
      {
        "label": "La quasi-totalité des pièces reste utilisable avec quelques scénarios avancés en moins",
        "score": 3
      },
      {
        "label": "On peut s'éclairer mais certains volets ou chauffages deviennent difficiles à commander",
        "score": 2
      },
      {
        "label": "Nombreux équipements bloqués et vie quotidienne fortement perturbée",
        "score": 1
      },
      {
        "label": "Non, les équipements sont inutilisables et la maison est bloquée sans le serveur",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "RES03",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & continuité",
    "title": "Supervision des appareils indisponibles",
    "critical": false,
    "question": "Home Assistant vous prévient-il rapidement si un capteur important ou un appareil ne répond plus ?",
    "why": "Savoir immédiatement qu'un capteur de fuite ou de température ne répond plus évite de fausses sécurités.",
    "options": [
      {
        "label": "Oui, surveillance automatique continue avec notification ciblée dès qu'un équipement devient indisponible",
        "score": 4
      },
      {
        "label": "Tableau de bord dédié regroupant clairement tous les appareils hors ligne",
        "score": 3
      },
      {
        "label": "Les appareils indisponibles sont visibles uniquement en parcourant les listes techniques",
        "score": 2
      },
      {
        "label": "Détection manuelle uniquement lorsqu'on constate qu'une commande ne répond plus",
        "score": 1
      },
      {
        "label": "Aucun suivi des appareils indisponibles",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "RES04",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & continuité",
    "title": "Qualité et stabilité des réseaux domotiques",
    "critical": false,
    "question": "Vos réseaux sans fil domotiques (Zigbee, Z-Wave, Thread, Wi-Fi) sont-ils stables et sans déconnexions intempestives ?",
    "why": "Un réseau sans fil bien maillé garantit que chaque ordre arrive instantanément sans jamais perdre de commande.",
    "options": [
      {
        "label": "Réseaux parfaitement stables, maillage dense avec relais secteur et zéro déconnexion",
        "score": 4
      },
      {
        "label": "Très bonne stabilité générale avec de rares déconnexions isolées",
        "score": 3
      },
      {
        "label": "Réseau fonctionnel mais quelques capteurs éloignés se déconnectent occasionnellement",
        "score": 2
      },
      {
        "label": "Déconnexions régulières nécessitant de redémarrer des modules",
        "score": 1
      },
      {
        "label": "Réseaux instables avec pertes d'appareils fréquentes et répétées",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "RES05",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & continuité",
    "title": "Sauvegardes Home Assistant",
    "critical": true,
    "question": "À quelle fréquence vos sauvegardes Home Assistant sont-elles créées automatiquement ?",
    "why": "En cas de panne matérielle ou de fausse manipulation, une sauvegarde récente permet de restaurer l'intégralité de sa maison en quelques clics.",
    "options": [
      {
        "label": "Sauvegarde automatique quotidienne complète avec rotation et historique sur plusieurs semaines",
        "score": 4
      },
      {
        "label": "Sauvegarde automatique au moins une fois par semaine",
        "score": 3
      },
      {
        "label": "Sauvegardes manuelles régulières faites de temps en temps",
        "score": 2
      },
      {
        "label": "Une seule sauvegarde ancienne non renouvelée",
        "score": 1
      },
      {
        "label": "Aucune sauvegarde existante",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "RES06",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & continuité",
    "title": "Sauvegarde hors de la machine Home Assistant",
    "critical": false,
    "question": "Vos sauvegardes sont-elles automatiquement envoyées hors de la machine (sur un cloud sécurisé, un NAS ou un autre ordinateur) ?",
    "why": "Si le disque du serveur grille, les sauvegardes restées sur la machine sont perdues en même temps que le système.",
    "options": [
      {
        "label": "Oui, copies automatiques externalisées sur un stockage distant sécurisé (cloud chiffré, NAS distant)",
        "score": 4
      },
      {
        "label": "Copie automatique sur un NAS local ou support réseau distinct de la machine",
        "score": 3
      },
      {
        "label": "Copie manuelle périodique sur un ordinateur ou une clé USB externe",
        "score": 2
      },
      {
        "label": "Les sauvegardes restent stockées uniquement sur le disque de Home Assistant",
        "score": 1
      },
      {
        "label": "Aucune copie de sauvegarde disponible",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "RES07",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & continuité",
    "title": "Restauration réellement testée",
    "critical": false,
    "question": "Avez-vous déjà testé au moins une fois la restauration complète d'une sauvegarde pour vérifier qu'elle fonctionne vraiment ?",
    "why": "Une sauvegarde non testée peut s'avérer corrompue ou incomplète le jour où l'on en a impérativement besoin.",
    "options": [
      {
        "label": "Oui, restauration complète testée avec succès récemment sur une machine ou un environnement de test",
        "score": 4
      },
      {
        "label": "Restauration complète déjà effectuée avec succès lors d'un changement de matériel ou d'une panne passée",
        "score": 3
      },
      {
        "label": "Restauration partielle d'un fichier ou d'une intégration testée seulement",
        "score": 2
      },
      {
        "label": "Jamais testée mais j'ai une procédure écrite étape par étape",
        "score": 1
      },
      {
        "label": "Non, je n'ai jamais testé la restauration d'une sauvegarde",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "RES08",
    "domain": "RES",
    "domain_name": "🛡️ Résilience & continuité",
    "title": "Continuité électrique / reprise après coupure",
    "critical": false,
    "question": "Comment votre installation domotique redémarre-t-elle après une coupure de courant ?",
    "why": "Après un orage ou une coupure réseau, la maison doit reprendre sa vie normale automatiquement sans exiger de manipulation complexe.",
    "options": [
      {
        "label": "Redémarrage automatique ordonné, reconnexion fluide de tous les réseaux et reprise instantanée des scénarios",
        "score": 4
      },
      {
        "label": "Redémarrage automatique complet sans intervention manuelle",
        "score": 3
      },
      {
        "label": "Redémarrage fonctionnel mais certains modules nécessitent une action manuelle pour se reconnecter",
        "score": 2
      },
      {
        "label": "Redémarrage difficile avec des états d'appareils incohérents",
        "score": 1
      },
      {
        "label": "Le système nécessite une intervention manuelle lourde pour repartir après une coupure",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "AUTO01",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & intelligence",
    "title": "Éclairage intelligent",
    "critical": false,
    "question": "Chez vous, certains éclairages s'allument-ils et s'éteignent-ils automatiquement selon la présence, l'heure ou la luminosité ?",
    "why": "Automatiser l'éclairage apporte un confort immédiat au quotidien et évite que des lumières restent allumées inutilement.",
    "options": [
      {
        "label": "Oui, éclairage intelligent complet avec allumage progressif, scènes adaptées à l'activité et extinction au départ",
        "score": 4
      },
      {
        "label": "Oui, éclairages contextualisés selon la luminosité et variation douce nuit/jour",
        "score": 3
      },
      {
        "label": "Détecteurs de mouvement basiques dans les pièces de passage allumant à 100 % quelle que soit l'heure",
        "score": 2
      },
      {
        "label": "Minuteries ou programmations horaires fixes rigides sans capteur",
        "score": 1
      },
      {
        "label": "Non, allumage et extinction 100 % manuels",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "AUTO02",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & intelligence",
    "title": "Chauffage intelligent",
    "critical": false,
    "question": "Votre chauffage ou climatisation s'ajuste-t-il automatiquement selon vos présences, horaires et ouvertures de fenêtres ?",
    "why": "Réduire le chauffage lors des absences et aérations génère d'importantes économies d'énergie sans sacrifier le confort.",
    "options": [
      {
        "label": "Oui, régulation thermique prédictive avec anticipation météo, présence et délestage",
        "score": 4
      },
      {
        "label": "Régulation avancée avec coupure sur fenêtre ouverte et abaissement automatique en absence",
        "score": 3
      },
      {
        "label": "Thermostats connectés pilotables à distance mais sans détection d'ouverture ni d'absence",
        "score": 2
      },
      {
        "label": "Thermostat programmable avec simple calendrier hebdomadaire fixe",
        "score": 1
      },
      {
        "label": "Chauffage non connecté ou consigne fixe continue sans programmation",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "AUTO03",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & intelligence",
    "title": "Ventilation intelligente",
    "critical": false,
    "question": "Votre ventilation (VMC) s'adapte-t-elle automatiquement selon l'humidité de la salle de bain ou la qualité de l'air ?",
    "why": "Booster la ventilation lors d'une douche évite les moisissures, et la ralentir le reste du temps limite les pertes de chaleur.",
    "options": [
      {
        "label": "La ventilation adapte automatiquement son fonctionnement selon l'humidité ou la qualité de l'air (ex: pic d'humidité douche), avec retour automatique à un fonctionnement normal",
        "score": 4
      },
      {
        "label": "Déclenchement automatique lié à un événement précis (ex: allumage lumière salle de bain ou seuil d'humidité fixe) sans régulation fine",
        "score": 3
      },
      {
        "label": "VMC enclenchée manuellement via bouton ou horaire fixe programmé",
        "score": 2
      },
      {
        "label": "Mesure d'humidité ou de qualité d'air existante mais sans aucun automatisme associé",
        "score": 1
      },
      {
        "label": "VMC classique permanente à vitesse fixe sans aucun pilotage domotique",
        "score": 0
      }
    ],
    "has_not_applicable": true,
    "not_applicable_label": "Non applicable (pas de VMC)"
  },
  {
    "id": "AUTO04",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & intelligence",
    "title": "Gestion intelligente des volets",
    "critical": false,
    "question": "Vos volets roulants ou stores s'ouvrent-ils et se ferment-ils automatiquement selon le soleil et la météo ?",
    "why": "La gestion bioclimatique des volets conserve la chaleur en hiver et protège le logement des fortes chaleurs estivales.",
    "options": [
      {
        "label": "Gestion dynamique ou bioclimatique tenant compte du soleil, de la température, de la saison ou des conditions thermiques",
        "score": 4
      },
      {
        "label": "Ouverture et fermeture automatiques selon le lever et le coucher du soleil (éphéméride)",
        "score": 3
      },
      {
        "label": "Ouverture et fermeture à heures fixes programmées (ex: 8h / 20h) sans tenir compte de la luminosité",
        "score": 2
      },
      {
        "label": "Quelques volets automatisés ponctuellement, la majorité manipulée manuellement",
        "score": 1
      },
      {
        "label": "Volets manipulés exclusivement à la main sans aucune programmation",
        "score": 0
      }
    ],
    "has_not_applicable": true,
    "not_applicable_label": "Non applicable (pas de volets motorisés)"
  },
  {
    "id": "AUTO05",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & intelligence",
    "title": "Gestion intelligente de l’eau",
    "critical": false,
    "question": "Votre maison dispose-t-elle de capteurs de fuite d'eau et d'un système de coupure automatique ?",
    "why": "Une coupure automatique dès la détection d'une fuite protège le logement contre les dégâts des eaux majeurs.",
    "options": [
      {
        "label": "Protection intégrale : capteurs sous tous les points d'eau sensibles, coupure vanne immédiate et alerte sonore",
        "score": 4
      },
      {
        "label": "Alerte immédiate sur smartphone + coupure automatique de la vanne générale",
        "score": 3
      },
      {
        "label": "Notification reçue en cas de fuite mais sans coupure automatique de l'eau",
        "score": 2
      },
      {
        "label": "Capteurs de fuite en place mais sans notification sonore ou push configurée",
        "score": 1
      },
      {
        "label": "Aucun capteur d'inondation ni mesure de consommation d'eau",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "AUTO06",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & intelligence",
    "title": "Suivi et automatisation des appareils domestiques",
    "critical": false,
    "question": "Suivez-vous le fonctionnement de vos appareils électroménagers (machine à laver, lave-vaisselle, sèche-linge) ?",
    "why": "Être notifié dès qu'une machine est terminée évite d'oublier le linge humide dans le tambour.",
    "options": [
      {
        "label": "Intégration complète avec détection de cycle, rappel de déchargement du linge et optimisation tarifaire",
        "score": 4
      },
      {
        "label": "Notification de fin de cycle (push ou vocale) envoyée dès que la machine est terminée",
        "score": 3
      },
      {
        "label": "Notification basique de fin de cycle sur seuil de puissance fixe",
        "score": 2
      },
      {
        "label": "Prise connectée avec mesure en place mais sans notification traitée",
        "score": 1
      },
      {
        "label": "Aucun suivi des appareils électroménagers",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "AUTO07",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & intelligence",
    "title": "Présence et occupation",
    "critical": false,
    "question": "Home Assistant sait-il automatiquement qui est à la maison, absent, endormi ou en vacances ?",
    "why": "Les modes d'occupation permettent d'éteindre tous les appareils en partant, d'activer l'alarme et de passer le chauffage en mode éco d'un seul coup.",
    "options": [
      {
        "label": "Détection d'occupation multi-niveaux (radar mmWave, états Maison/Nuit/Absence/Invités)",
        "score": 4
      },
      {
        "label": "Gestion robuste combinant zones GPS, Wi-Fi des smartphones et détecteurs de mouvement",
        "score": 3
      },
      {
        "label": "Détection combinant GPS et connexion Wi-Fi du téléphone sur le réseau local",
        "score": 2
      },
      {
        "label": "Présence basée sur un seul GPS smartphone avec retards fréquents",
        "score": 1
      },
      {
        "label": "Aucune notion de présence dans Home Assistant",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "AUTO08",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & intelligence",
    "title": "Contextualisation des automatismes",
    "critical": false,
    "question": "Vos scénarios domotiques combinent-ils plusieurs conditions intelligentes (luminosité, saison, présence, météo) ?",
    "why": "Prendre en compte le contexte réel évite les actions inopportunes (comme allumer une lumière en plein soleil ou en pleine nuit).",
    "options": [
      {
        "label": "Architecture complète avec modes de vie globaux pilotant harmonieusement tous les équipements",
        "score": 4
      },
      {
        "label": "Contextualisation riche combinant luminosité, saison, présence et météo",
        "score": 3
      },
      {
        "label": "Conditions de présence et de saison intégrées dans les automatisations principales",
        "score": 2
      },
      {
        "label": "Quelques conditions basiques (heure + jour de la semaine)",
        "score": 1
      },
      {
        "label": "Déclencheurs horaires simples sans condition contextuelle",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "AUTO09",
    "domain": "AUTO",
    "domain_name": "⚙️ Automatisations & intelligence",
    "title": "Boucle de vérification après commande",
    "critical": false,
    "question": "Vos automatisations importantes vérifient-elles que l'appareil a bien réagi après lui avoir envoyé un ordre ?",
    "why": "Vérifier l'état effectif garantit qu'un ordre de sécurité (comme fermer une vanne ou verrouiller un accès) s'est réellement exécuté.",
    "options": [
      {
        "label": "Boucle de contrôle systématique : ordre envoyé → confirmation d'état → relance automatique en cas d'échec → alerte",
        "score": 4
      },
      {
        "label": "Contrôle automatique sur les actions critiques (ex: fermeture vanne d'eau ou volets)",
        "score": 3
      },
      {
        "label": "Vérification manuelle via notifications ou capteurs d'état",
        "score": 2
      },
      {
        "label": "Simple retour visuel dans l'interface sans vérification automatique",
        "score": 1
      },
      {
        "label": "Envoi aveugle des commandes sans aucune vérification",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ENER01",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & ressources",
    "title": "Mesure électrique globale",
    "critical": false,
    "question": "Mesurez-vous en temps réel la consommation électrique globale de votre logement (Linky TIC, pince ampèremétrique ou tore au tableau) ?",
    "why": "La mesure globale en direct permet de détecter les anomalies de consommation, d'anticiper les disjonctions et d'alimenter le tableau Énergie.",
    "options": [
      {
        "label": "Mesure de la puissance instantanée et index de consommation totale en temps réel (Linky TIC, pince ampèremétrique) avec historique",
        "score": 4
      },
      {
        "label": "Suivi régulier de la puissance globale en direct",
        "score": 3
      },
      {
        "label": "Relevé périodique journalier ou mensuel uniquement",
        "score": 2
      },
      {
        "label": "Index relevé manuellement de temps en temps",
        "score": 1
      },
      {
        "label": "Aucun suivi de la consommation électrique globale",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ENER02",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & ressources",
    "title": "Historique énergétique",
    "critical": false,
    "question": "Conservez-vous un historique de vos consommations pour comparer vos dépenses d'un mois ou d'une année sur l'autre ?",
    "why": "Comparer vos consommations d'une année sur l'autre permet d'évaluer l'efficacité de vos travaux d'isolation ou de vos nouveaux réglages.",
    "options": [
      {
        "label": "Oui, historique long terme complet avec comparatifs saisonniers et analyses d'évolution",
        "score": 4
      },
      {
        "label": "Historique d'énergie conservé sur plus d'un an avec graphiques de suivi",
        "score": 3
      },
      {
        "label": "Historique récent disponible sur quelques semaines ou mois",
        "score": 2
      },
      {
        "label": "Données conservées sur quelques jours seulement",
        "score": 1
      },
      {
        "label": "Aucun historique de consommation conservé",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ENER03",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & ressources",
    "title": "Mesure des principaux postes de consommation",
    "critical": false,
    "question": "Mesurez-vous la part respective de chaque gros poste dans votre consommation globale (chauffage, eau chaude, cuisine, prises) ?",
    "why": "Savoir exactement ce que consomme chaque équipement évite les fausses suppositions et cible les vraies sources d'économies.",
    "options": [
      {
        "label": "Oui, répartition détaillée couvrant la quasi-totalité des postes de consommation du logement",
        "score": 4
      },
      {
        "label": "Suivi individualisé des 3 ou 4 plus gros consommateurs d'énergie",
        "score": 3
      },
      {
        "label": "Mesure sur 1 ou 2 appareils seulement",
        "score": 2
      },
      {
        "label": "Estimations théoriques sans mesure physique réelle",
        "score": 1
      },
      {
        "label": "Aucune décomposition des postes de consommation",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ENER04",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & ressources",
    "title": "Production solaire / production locale",
    "critical": false,
    "question": "Si vous disposez de panneaux solaires, votre production d'électricité est-elle mesurée en temps réel dans Home Assistant ?",
    "why": "Connaître votre production instantanée est indispensable pour programmer l'allumage des appareils pendant les heures d'ensoleillement.",
    "options": [
      {
        "label": "Oui, production solaire mesurée en direct avec historique détaillé et prévisions de production",
        "score": 4
      },
      {
        "label": "Production solaire suivie en temps réel dans Home Assistant",
        "score": 3
      },
      {
        "label": "Relevé global journalier sans données en temps réel",
        "score": 2
      },
      {
        "label": "Production consultable uniquement sur l'application du fabricant de l'onduleur",
        "score": 1
      },
      {
        "label": "Panneaux solaires non raccordés à Home Assistant",
        "score": 0
      }
    ],
    "has_not_applicable": true,
    "not_applicable_label": "Non applicable (pas de panneaux solaires)"
  },
  {
    "id": "ENER05",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & ressources",
    "title": "Prise en compte des tarifs électriques",
    "critical": false,
    "question": "Vos tarifs d'électricité (Heures Creuses, Tempo, tarifs dynamiques) sont-ils intégrés dans Home Assistant ?",
    "why": "Connaître le prix exact de l'électricité à chaque instant permet d'automatiser les lancements d'appareils aux moments les plus avantageux.",
    "options": [
      {
        "label": "Oui, tarifs exacts intégrés en temps réel avec calcul automatique du coût de chaque appareil",
        "score": 4
      },
      {
        "label": "Grille tarifaire Heures Pleines / Heures Creuses configurée dans le tableau Énergie",
        "score": 3
      },
      {
        "label": "Tarif moyen fixe configuré pour estimer le coût global",
        "score": 2
      },
      {
        "label": "Tarifs connus mais non renseignés dans Home Assistant",
        "score": 1
      },
      {
        "label": "Aucune intégration des tarifs électriques",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ENER06",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & ressources",
    "title": "Optimisation énergétique automatique",
    "critical": false,
    "question": "Home Assistant déclenche-t-il automatiquement certains appareils aux heures où l'électricité est la moins chère ?",
    "why": "Automatiser les lancements sur les heures creuses ou jours avantageux fait baisser directement votre facture annuelle d'électricité.",
    "options": [
      {
        "label": "Pilotage dynamique multi-critères (surplus solaire en temps réel, tarifs dynamiques Tempo/Spot, consigne de température)",
        "score": 4
      },
      {
        "label": "Pilotage automatisé par Home Assistant selon les plages horaires tarifaires (Heures Creuses)",
        "score": 3
      },
      {
        "label": "Contacteur jour/nuit classique (ou horloge mécanique) sans pilotage domotique",
        "score": 2
      },
      {
        "label": "Chauffe-eau en marche continue 24h/24 ou programmation manuelle occasionnelle",
        "score": 1
      },
      {
        "label": "Aucun pilotage, consommation continue non régulée",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ENER07",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & ressources",
    "title": "Optimisation de l’autoconsommation",
    "critical": false,
    "question": "Votre surplus d'électricité solaire est-il automatiquement utilisé sur place plutôt que d'être réinjecté gratuitement sur le réseau ?",
    "why": "Autoconsommer son surplus maximise la rentabilité de votre installation solaire photovoltaïque.",
    "options": [
      {
        "label": "Oui, gestionnaire d'énergie dynamique modulant la recharge, l'eau chaude et les appareils selon le surplus",
        "score": 4
      },
      {
        "label": "Appareils et chauffe-eau enclenchés automatiquement lors des périodes de surplus solaire",
        "score": 3
      },
      {
        "label": "Nous allumons manuellement certains appareils quand il y a du soleil",
        "score": 2
      },
      {
        "label": "Surplus solaire réinjecté sur le réseau sans utilisation locale",
        "score": 1
      },
      {
        "label": "Aucune optimisation d'autoconsommation",
        "score": 0
      }
    ],
    "has_not_applicable": true,
    "not_applicable_label": "Non applicable (pas de panneaux solaires)"
  },
  {
    "id": "ENER08",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & ressources",
    "title": "Suivi de la consommation d’eau",
    "critical": false,
    "question": "Suivez-vous votre consommation d'eau quotidienne ou en temps réel dans Home Assistant ?",
    "why": "Suivre l'eau permet de détecter immédiatement un robinet qui goutte ou une chasse d'eau qui fuit continuellement.",
    "options": [
      {
        "label": "Oui, suivi en direct au litre près avec alertes de surconsommation et intégration au tableau Énergie",
        "score": 4
      },
      {
        "label": "Suivi régulier journalier de la consommation d'eau",
        "score": 3
      },
      {
        "label": "Relevé périodique mensuel ou manuel du compteur",
        "score": 2
      },
      {
        "label": "Relevé occasionnel sur la facture d'eau uniquement",
        "score": 1
      },
      {
        "label": "Aucun suivi de la consommation d'eau",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "ENER09",
    "domain": "ENER",
    "domain_name": "☀️ Énergie & ressources",
    "title": "Détection des anomalies de consommation",
    "critical": false,
    "question": "Home Assistant vous prévient-il en cas de consommation anormale (appareil oublié, fuite d'eau, talon électrique anormal) ?",
    "why": "Être alerté dès la première heure d'une dérive permet d'intervenir avant que la facture ou les dégâts ne s'envolent.",
    "options": [
      {
        "label": "Oui, alertes automatiques en direct sur détection de fuite, surconsommation inhabituelle ou talon nocturne élevé",
        "score": 4
      },
      {
        "label": "Alertes configurées sur certains seuils de consommation spécifiques",
        "score": 3
      },
      {
        "label": "Détection visuelle manuelle lors de la consultation des graphiques",
        "score": 2
      },
      {
        "label": "Anomalies constatées uniquement à la réception de la facture",
        "score": 1
      },
      {
        "label": "Aucune détection d'anomalie de consommation",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "INTER01",
    "domain": "INTER",
    "domain_name": "🔌 Interopérabilité & fonctionnement local",
    "title": "Utilisation de protocoles locaux",
    "critical": false,
    "question": "Vos équipements domotiques communiquent-ils via des protocoles locaux et ouverts (Zigbee, Z-Wave, Matter, Thread, Ethernet) ?",
    "why": "Les protocoles locaux ouverts garantissent que votre maison reste fonctionnelle et réparable pendant des décennies.",
    "options": [
      {
        "label": "Oui, la quasi-totalité du parc repose sur des protocoles locaux et ouverts sans cloud",
        "score": 4
      },
      {
        "label": "La majorité de mes appareils communique via des protocoles locaux",
        "score": 3
      },
      {
        "label": "Équilibre entre protocoles locaux et quelques équipements Wi-Fi fermés",
        "score": 2
      },
      {
        "label": "Majorité d'équipements en protocoles propriétaires ou fermés",
        "score": 1
      },
      {
        "label": "Parc entièrement constitué d'appareils fermés dépendants du cloud",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "INTER02",
    "domain": "INTER",
    "domain_name": "🔌 Interopérabilité & fonctionnement local",
    "title": "Dépendance au Cloud",
    "critical": false,
    "question": "Dans quelle mesure votre installation domotique peut-elle fonctionner si tous les serveurs cloud extérieurs deviennent indisponibles ?",
    "why": "L'autonomie locale garantit que votre maison reste pilotable même si un fabricant tiers fait faillite ou coupe ses serveurs.",
    "options": [
      {
        "label": "Indépendance totale : 100 % des fonctions vitales fonctionnent en circuit fermé local",
        "score": 4
      },
      {
        "label": "Plus de 90 % des fonctions sont locales, seuls quelques services d'information utilisent le cloud",
        "score": 3
      },
      {
        "label": "Fonctions principales locales mais plusieurs équipements clés dépendent du cloud",
        "score": 2
      },
      {
        "label": "Dépendance forte : de nombreux appareils s'arrêtent sans accès aux serveurs des fabricants",
        "score": 1
      },
      {
        "label": "Dépendance totale : la maison s'arrête si les serveurs distants sont coupés",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "INTER03",
    "domain": "INTER",
    "domain_name": "🔌 Interopérabilité & fonctionnement local",
    "title": "Remplaçabilité des équipements",
    "critical": false,
    "question": "Si un fabricant d'ampoules ou de prises disparaît, pouvez-vous remplacer facilement ses modules par une autre marque sans tout reconstruire ?",
    "why": "Choisir des appareils interchangeables protège votre investissement contre l'obsolescence programmée.",
    "options": [
      {
        "label": "Oui, utilisation exclusive de standards universels interchangeables sans friction",
        "score": 4
      },
      {
        "label": "La plupart des équipements sont remplaçables sans impacter le reste du système",
        "score": 3
      },
      {
        "label": "Quelques équipements propriétaires difficiles à remplacer par une autre marque",
        "score": 2
      },
      {
        "label": "Remplacement complexe nécessitant de revoir les scénarios",
        "score": 1
      },
      {
        "label": "Équipements totalement verrouillés à un écosystème fermé",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "INTER04",
    "domain": "INTER",
    "domain_name": "🔌 Interopérabilité & fonctionnement local",
    "title": "Organisation de Home Assistant",
    "critical": false,
    "question": "Votre configuration Home Assistant est-elle bien ordonnée (appareils assignés à des pièces, entités triées, zones définies) ?",
    "why": "Un système bien rangé par pièce simplifie la création d'automatisations et rend les tableaux de bord clairs.",
    "options": [
      {
        "label": "Organisation exemplaire : 100 % des appareils assignés à leur pièce, zones et catégories rigoureusement renseignées",
        "score": 4
      },
      {
        "label": "Bonne organisation générale avec la majorité des appareils rangés par pièce",
        "score": 3
      },
      {
        "label": "Organisation partielle : plusieurs appareils restent non assignés à une pièce",
        "score": 2
      },
      {
        "label": "Configuration en vrac avec peu de classement",
        "score": 1
      },
      {
        "label": "Aucun rangement : toutes les entités sont mélangées sans structure",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "INTER05",
    "domain": "INTER",
    "domain_name": "🔌 Interopérabilité & fonctionnement local",
    "title": "Standardisation de l’installation",
    "critical": false,
    "question": "Utilisez-vous des standards de communication homogènes et reconnus (formats d'échange structurés, MQTT, Matter) ?",
    "why": "Standardiser la communication rend le système plus rapide, plus léger et facile à faire évoluer au fil des ans.",
    "options": [
      {
        "label": "Oui, architecture locale homogène et standardisée facilitant les évolutions futures",
        "score": 4
      },
      {
        "label": "Standards ouverts appliqués sur la majorité des intégrations",
        "score": 3
      },
      {
        "label": "Mélange de plusieurs méthodes sans homogénéité stricte",
        "score": 2
      },
      {
        "label": "Peu de standardisation, solutions disparates",
        "score": 1
      },
      {
        "label": "Aucun standard : empilement de technologies hétérogènes non coordonnées",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "INTER06",
    "domain": "INTER",
    "domain_name": "🔌 Interopérabilité & fonctionnement local",
    "title": "Centralisation des intégrations dans Home Assistant",
    "critical": false,
    "question": "L'ensemble de vos objets et passerelles domotiques est-il centralisé sous Home Assistant sans devoir ouvrir plusieurs applications tierces ?",
    "why": "Centraliser tous les appareils dans un seul système permet de faire dialoguer des marques différentes qui ne se parlent pas habituellement.",
    "options": [
      {
        "label": "Oui, 100 % des équipements sont pilotables et automatisables depuis Home Assistant",
        "score": 4
      },
      {
        "label": "La quasi-totalité des appareils est centralisée, avec une seule application tierce résiduelle",
        "score": 3
      },
      {
        "label": "La majorité est centralisée mais nous utilisons encore 2 ou 3 applications de fabricants",
        "score": 2
      },
      {
        "label": "Moins de la moitié des objets est regroupée dans Home Assistant",
        "score": 1
      },
      {
        "label": "Pas de centralisation : chaque famille d'objets s'utilise dans sa propre application",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "UX01",
    "domain": "UX",
    "domain_name": "📱 Confort & expérience utilisateur",
    "title": "Commandes physiques simples et accessibles",
    "critical": false,
    "question": "Les personnes vivant avec vous ou vos invités peuvent-ils utiliser les éclairages et volets naturellement sans explication technique ?",
    "why": "La meilleure domotique est celle qui se fait oublier et qui ne complique jamais les gestes du quotidien pour vos proches.",
    "options": [
      {
        "label": "Oui, boutons muraux clairs avec retour visuel, télécommandes d'ambiance et aucune friction",
        "score": 4
      },
      {
        "label": "Utilisation simple et naturelle pour la famille et les invités réguliers",
        "score": 3
      },
      {
        "label": "Globalement accessible avec parfois quelques confusions sur les doubles appuis",
        "score": 2
      },
      {
        "label": "Utilisation complexe nécessitant des explications pour les invités",
        "score": 1
      },
      {
        "label": "Inutilisable sans formation préalable ou sans l'application sur smartphone",
        "score": 0
      }
    ],
    "has_not_applicable": true,
    "not_applicable_label": "Non applicable (je vis seul)"
  },
  {
    "id": "UX02",
    "domain": "UX",
    "domain_name": "📱 Confort & expérience utilisateur",
    "title": "Dashboard familial",
    "critical": false,
    "question": "Avez-vous mis en place un tableau de bord simplifié et épuré regroupant uniquement les commandes indispensables du quotidien ?",
    "why": "Une interface claire et sans jargon donne confiance aux membres du foyer sans risque de dérégler l'installation.",
    "options": [
      {
        "label": "Oui, interface d'excellence épurée, adaptée aux enfants et conjoints (vue tablette murale / kiosk)",
        "score": 4
      },
      {
        "label": "Tableau de bord famille clair avec accès direct aux 10 actions indispensables",
        "score": 3
      },
      {
        "label": "Tableau de bord simplifié existant mais encore un peu encombré d'éléments techniques",
        "score": 2
      },
      {
        "label": "Tableau de bord personnalisé mais trop complexe pour les personnes non initiées",
        "score": 1
      },
      {
        "label": "Seulement la vue brute par défaut avec des centaines d'entités techniques en vrac",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "UX03",
    "domain": "UX",
    "domain_name": "📱 Confort & expérience utilisateur",
    "title": "Adaptation aux différents écrans",
    "critical": false,
    "question": "Vos tableaux de bord sont-ils confortables et adaptés à la taille de chaque écran (smartphone, tablette, PC) ?",
    "why": "Adapter les boutons et l'affichage à l'écran utilisé rend le pilotage rapide et agréable dans toutes les situations.",
    "options": [
      {
        "label": "Vues dédiées parfaitement optimisées pour smartphone, tablette murale et grand écran",
        "score": 4
      },
      {
        "label": "Navigation fluide sur smartphone et disposition claire sur tablette et PC",
        "score": 3
      },
      {
        "label": "Lisible sur smartphone mais non optimisé pour tablette (grands espaces vides)",
        "score": 2
      },
      {
        "label": "Conçu pour grand écran uniquement, navigation difficile sur smartphone",
        "score": 1
      },
      {
        "label": "Illisible sur mobile (éléments coupés, colonnes trop étroites)",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "UX04",
    "domain": "UX",
    "domain_name": "📱 Confort & expérience utilisateur",
    "title": "Notifications pertinentes",
    "critical": false,
    "question": "Les notifications reçues sur smartphone sont-elles réservées aux alertes utiles et urgentes (sans spam nocturne) ?",
    "why": "Recevoir trop de notifications inutiles conduit à ignorer les alertes, y compris celles qui signalent une fuite ou un problème de sécurité.",
    "options": [
      {
        "label": "Système exemplaire : alertes hiérarchisées, sons personnalisés et boutons d'action directs",
        "score": 4
      },
      {
        "label": "Notifications ciblées : alertes critiques prioritaires et filtrage des alertes nocturnes",
        "score": 3
      },
      {
        "label": "Notifications utiles mais sans distinction d'urgence entre sécurité et météo",
        "score": 2
      },
      {
        "label": "Nombreuses notifications reçues à toute heure y compris la nuit",
        "score": 1
      },
      {
        "label": "Spam quotidien de notifications futiles ou aucune alerte configurée",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "UX05",
    "domain": "UX",
    "domain_name": "📱 Confort & expérience utilisateur",
    "title": "Automatisations discrètes",
    "critical": false,
    "question": "Vos automatisations se font-elles discrètes sans surprendre ni agacer les membres du foyer (lumière qui s'éteint inopportunément) ?",
    "why": "Une automatisation bien calibrée doit anticiper les besoins sans forcer les occupants à adapter leurs habitudes à la machine.",
    "options": [
      {
        "label": "Discrétion totale : la maison réagit naturellement, satisfaction unanime du foyer et des invités",
        "score": 4
      },
      {
        "label": "Domotique fluide et discrète qui anticipe les besoins sans rien imposer",
        "score": 3
      },
      {
        "label": "Automatisations acceptées mais quelques frictions lors de changements d'habitudes",
        "score": 2
      },
      {
        "label": "Frustrations régulières exprimées par les proches sur des automatismes imprévisibles",
        "score": 1
      },
      {
        "label": "Domotique intrusive et agaçante (lumières qui s'éteignent sur des personnes immobiles)",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "UX06",
    "domain": "UX",
    "domain_name": "📱 Confort & expérience utilisateur",
    "title": "Priorité donnée à l’utilisateur / override manuel",
    "critical": false,
    "question": "Si vous éteignez manuellement une lumière ou forcez un volet, l'automatisme s'arrête-t-il pour respecter votre choix ?",
    "why": "L'humain doit toujours avoir le dernier mot sur la machine en un seul clic sans lutter contre le système.",
    "options": [
      {
        "label": "Gestion exemplaire : priorité manuelle immédiatement respectée avec reprise automatique transparente",
        "score": 4
      },
      {
        "label": "Tout appui manuel sur un bouton suspend l'automatisme pendant une durée définie",
        "score": 3
      },
      {
        "label": "Priorité manuelle gérée mais temporaire sans possibilité de forçage prolongé",
        "score": 2
      },
      {
        "label": "Reprise en main manuelle difficile nécessitant de désactiver le scénario dans les paramètres",
        "score": 1
      },
      {
        "label": "L'automatisme lutte contre l'utilisateur (rallume la lumière 5 secondes après l'extinction)",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "UX07",
    "domain": "UX",
    "domain_name": "📱 Confort & expérience utilisateur",
    "title": "Réactivité du système",
    "critical": false,
    "question": "Lorsque vous appuyez sur un interrupteur ou déclenchez une action, la réaction de l'appareil est-elle instantanée ?",
    "why": "Une latence perceptible donne l'impression que le système n'a pas compris la commande et pousse à réappuyer plusieurs fois inutilement.",
    "options": [
      {
        "label": "Instantanée et imperceptible (< 150 ms), identique à un câblage électrique traditionnel",
        "score": 4
      },
      {
        "label": "Réponse rapide et fluide (< 300 ms) sur la totalité des commandes locales",
        "score": 3
      },
      {
        "label": "Temps de réponse correct (500 ms à 1s) mais variable selon la charge de la box",
        "score": 2
      },
      {
        "label": "Latences perceptibles (1 à 2 secondes) dues à des allers-retours vers des serveurs distants",
        "score": 1
      },
      {
        "label": "Latences très lentes et imprévisibles (> 2 secondes) à chaque appui bouton",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "MAINT01",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & documentation",
    "title": "Convention de nommage",
    "critical": false,
    "question": "Vos appareils et entités sont-ils tous nommés de façon claire et ordonnée (ex: Lumière Salon, Température Chambre) ?",
    "why": "Un nommage clair par pièce évite les erreurs lors de la création d'automatisations et simplifie grandement la maintenance.",
    "options": [
      {
        "label": "Nomenclature exemplaire sur 100 % des entités par pièce sans aucun identifiant brut d'usine",
        "score": 4
      },
      {
        "label": "Convention de nommage appliquée sur plus de 80 % du parc domotique",
        "score": 3
      },
      {
        "label": "La plupart des entités ont un nom compréhensible mais sans convention homogène",
        "score": 2
      },
      {
        "label": "Moins de 50 % des entités sont proprement renommées",
        "score": 1
      },
      {
        "label": "Majorité d'entités avec des noms génériques d'usine ou codes hexadécimaux bruts",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "MAINT02",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & documentation",
    "title": "Documentation de l’installation",
    "critical": false,
    "question": "Avez-vous consigné sur un document simple (papier ou numérique) les informations essentielles de votre installation (adresses IP, accès de secours, matériel) ?",
    "why": "Si vous êtes absent ou indisponible, une documentation minimale permet à un proche ou à un technicien de comprendre l'installation et de dépanner.",
    "options": [
      {
        "label": "Documentation complète et à jour : schéma, plan réseau, guide pour les proches et inventaire",
        "score": 4
      },
      {
        "label": "Dossier technique clair récapitulant les adresses IP, accès de secours et liste des modules",
        "score": 3
      },
      {
        "label": "Tableau des adresses IP et liste du matériel existant mais non tenus à jour",
        "score": 2
      },
      {
        "label": "Quelques notes éparses ou fichiers textes non structurés",
        "score": 1
      },
      {
        "label": "Aucune documentation écrite, toute la connaissance est uniquement dans ma tête",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "MAINT03",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & documentation",
    "title": "Documentation des automatisations",
    "critical": false,
    "question": "Vos automatisations et scénarios comportent-ils des titres explicites et une description de leur rôle ?",
    "why": "Après plusieurs mois, il devient difficile de se souvenir de la logique exacte d'un scénario complexe sans une description courte.",
    "options": [
      {
        "label": "100 % des automatisations et scripts possèdent une description complète et des commentaires clairs",
        "score": 4
      },
      {
        "label": "Plus de 80 % des automatisations possèdent un titre explicite et une description détaillée",
        "score": 3
      },
      {
        "label": "Description renseignée uniquement sur les quelques automatisations complexes",
        "score": 2
      },
      {
        "label": "Noms compréhensibles mais champ description vide sur la quasi-totalité des scénarios",
        "score": 1
      },
      {
        "label": "Aucune description avec des noms par défaut obscurs (ex: Nouvelle automatisation 3)",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "MAINT04",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & documentation",
    "title": "Nettoyage des entités inutilisées",
    "critical": false,
    "question": "Supprimez-vous régulièrement les anciens appareils hors d'usage ou remplacés de votre registre Home Assistant ?",
    "why": "Conserver des entités fantômes alourdit la base de données et peut générer des erreurs dans vos journaux système.",
    "options": [
      {
        "label": "Registre d'entités rigoureusement purgé, aucune entité fantôme, base de données optimisée",
        "score": 4
      },
      {
        "label": "Les entités orphelines sont supprimées au fur et à mesure du remplacement du matériel",
        "score": 3
      },
      {
        "label": "Nettoyage occasionnel des appareils retirés",
        "score": 2
      },
      {
        "label": "Nettoyage très rare, nombreuses entités orphelines visibles dans les outils de développement",
        "score": 1
      },
      {
        "label": "Des dizaines d'anciennes entités supprimées ou hors d'usage encombrent le registre",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "MAINT05",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & documentation",
    "title": "Tableau de santé technique",
    "critical": false,
    "question": "Disposez-vous d'une vue d'ensemble ou d'une alerte automatique dès qu'une pile de capteur devient faible ou qu'un appareil ne répond plus ?",
    "why": "Être prévenu avant l'extinction complète d'un capteur évite les pannes surprises de détection ou de chauffage en plein hiver.",
    "options": [
      {
        "label": "Vue santé complète + alerte automatique dès qu'une pile passe sous 15 % avec modèle de pile précisé",
        "score": 4
      },
      {
        "label": "Dashboard technique complet regroupant l'état des piles, les métriques système et appareils hors ligne",
        "score": 3
      },
      {
        "label": "Présence d'une carte basique listant les piles faibles sur un tableau de bord",
        "score": 2
      },
      {
        "label": "Niveau des piles consultable uniquement appareil par appareil dans les paramètres",
        "score": 1
      },
      {
        "label": "Aucun suivi de l'état technique : une pile vide est découverte quand l'appareil ne répond plus",
        "score": 0
      }
    ],
    "has_not_applicable": true,
    "not_applicable_label": "Non applicable (aucun appareil à pile)"
  },
  {
    "id": "MAINT06",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & documentation",
    "title": "Procédure de reprise / récupération",
    "critical": false,
    "question": "En cas de panne matérielle de votre serveur domotique, avez-vous une procédure ou un support prêt pour réinstaller rapidement ?",
    "why": "Un plan de reprise clair permet de remettre en service la maison en moins d'une heure en cas de défaillance matérielle.",
    "options": [
      {
        "label": "Plan de reprise complet : document accessible hors ligne, clé USB de secours prête et procédure claire",
        "score": 4
      },
      {
        "label": "Procédure de reprise formalisée étape par étape (support d'installation, méthode de restauration)",
        "score": 3
      },
      {
        "label": "Je sais réinstaller et restaurer le système de mémoire, mais je n'ai pas de procédure écrite formalisée (ou procédure incomplète sans mots de passe)",
        "score": 2
      },
      {
        "label": "Connaissance orale très sommaire des étapes sans document ni support prêt",
        "score": 1
      },
      {
        "label": "Aucune procédure : en cas de crash du serveur, je ne saurais pas par où commencer",
        "score": 0
      }
    ],
    "has_not_applicable": false
  },
  {
    "id": "MAINT07",
    "domain": "MAINT",
    "domain_name": "🛠️ Maintenance & documentation",
    "title": "Historique des modifications importantes",
    "critical": false,
    "question": "Gardez-vous une trace ou faites-vous une sauvegarde étiquetée avant d'effectuer des modifications importantes sur votre système ?",
    "why": "Garder une trace des modifications permet d'identifier immédiatement l'origine d'un dysfonctionnement apparu récemment.",
    "options": [
      {
        "label": "Traçabilité exemplaire : configuration versionnée sous Git ou journal des révisions exhaustif",
        "score": 4
      },
      {
        "label": "Historique régulier et daté avec sauvegardes étiquetées avant chaque gros changement",
        "score": 3
      },
      {
        "label": "Journal de bord textuel tenu à jour lors des modifications majeures",
        "score": 2
      },
      {
        "label": "Notes sporadiques sans date ni suivi structuré",
        "score": 1
      },
      {
        "label": "Aucun historique des modifications",
        "score": 0
      }
    ],
    "has_not_applicable": false
  }
];

class SmartHomeScoreCard extends HTMLElement {
  constructor() {
    super();
    this._config = {};
    this._hass = null;
    this._view = 'welcome'; // 'welcome' | 'scanning' | 'discovery' | 'audit' | 'cockpit'
    this._activeTab = 'overview';
    this._currentQuestionIndex = 0;
    this._showWhy = false;
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

  _getGlobalScoreEntity() {
    if (!this._hass || !this._hass.states) return null;
    // 1. Attribute signature match (100% language agnostic)
    for (const [entityId, stateObj] of Object.entries(this._hass.states)) {
      if (stateObj && stateObj.attributes && (stateObj.attributes.criteria_states || stateObj.attributes.maturity_level !== undefined)) {
        return stateObj;
      }
    }
    // 2. Direct names
    const candidates = [
      'sensor.smart_home_score_global_score',
      'sensor.smart_home_score_score_global',
      'sensor.global_score',
      'sensor.score_global'
    ];
    for (const cand of candidates) {
      if (this._hass.states[cand]) return this._hass.states[cand];
    }
    // 3. Substring match
    for (const [entityId, stateObj] of Object.entries(this._hass.states)) {
      if (typeof entityId === 'string' && (entityId.includes('smart_home_score') || entityId.includes('score_global') || entityId.includes('global_score'))) {
        return stateObj;
      }
    }
    return null;
  }

  _getCriteriaStates() {
    const globalSensor = this._getGlobalScoreEntity();
    return (globalSensor && globalSensor.attributes && globalSensor.attributes.criteria_states) ? globalSensor.attributes.criteria_states : {};
  }

  _getScanBreakdown() {
    const states = this._getCriteriaStates();
    let autoCount = 0;
    let capabilityCount = 0;
    let pendingList = [];

    for (const c of SHS_CRITERIA) {
      const st = states[c.id];
      if (st && st.status === 'auto_evaluated' && st.confidence >= 90 && st.effective_score !== null) {
        autoCount++;
      } else if (st && st.evidence && st.auto_score !== null && st.auto_score !== undefined) {
        capabilityCount++;
        pendingList.push(c);
      } else {
        pendingList.push(c);
      }
    }

    const questionOnlyCount = Math.max(0, SHS_CRITERIA.length - autoCount - capabilityCount);

    return { autoCount, capabilityCount, questionOnlyCount, pendingList };
  }

  _getPendingCriteria() {
    return this._getScanBreakdown().pendingList;
  }

  _render() {
    if (!this.shadowRoot) return;

    try {
      const globalScoreSensor = this._getGlobalScoreEntity();
      const attrs = globalScoreSensor?.attributes || {};

      const hasData = globalScoreSensor && globalScoreSensor.state !== 'unknown' && globalScoreSensor.state !== 'unavailable';
      const scoreVal = hasData ? parseFloat(globalScoreSensor.state) : 0.0;
      const completenessVal = attrs.completeness !== undefined ? parseFloat(attrs.completeness) : (hasData ? 100.0 : 0.0);
      const maturityText = attrs.maturity_level || 'Non évalué';
      const criticalCount = attrs.critical_count !== undefined ? parseInt(attrs.critical_count, 10) : 0;
      const potentialGain = attrs.potential_gain !== undefined ? parseFloat(attrs.potential_gain) : 0.0;

      const isProvisional = attrs.is_provisional ?? (completenessVal < 100);

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
          .shs-btn-success {
            background: #059669;
          }
          .shs-btn-success:hover {
            background: #047857;
          }
          /* Scanning & Discovery Styles */
          .shs-scan-box {
            background: rgba(59, 130, 246, 0.08);
            border: 1px solid rgba(59, 130, 246, 0.25);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            margin: 12px 0;
          }
          .shs-spinner {
            display: inline-block;
            width: 36px;
            height: 36px;
            border: 3px solid rgba(255, 255, 255, 0.15);
            border-radius: 50%;
            border-top-color: #60a5fa;
            animation: spin 1s ease-in-out infinite;
            margin-bottom: 12px;
          }
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
          .shs-discovery-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin: 16px 0;
          }
          .shs-discovery-item {
            background: rgba(0, 0, 0, 0.25);
            border-radius: 8px;
            padding: 12px 8px;
            text-align: center;
          }
          .shs-discovery-count {
            font-size: 1.35rem;
            font-weight: 800;
            color: #60a5fa;
          }
          .shs-discovery-label {
            font-size: 0.75rem;
            color: var(--shs-muted);
            margin-top: 4px;
            line-height: 1.25;
          }
          /* Questionnaire Styles */
          .shs-audit-box {
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 16px;
          }
          .shs-domain-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
          }
          .shs-meta-sub {
            font-size: 0.78rem;
            color: #94a3b8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }
          .shs-question-main {
            font-size: 1.15rem;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 12px;
            line-height: 1.45;
          }
          .shs-evidence-box {
            background: rgba(59, 130, 246, 0.12);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 14px;
          }
          .shs-evidence-header {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.82rem;
            font-weight: 700;
            color: #93c5fd;
            margin-bottom: 4px;
          }
          .shs-evidence-text {
            font-size: 0.85rem;
            color: #cbd5e1;
            line-height: 1.35;
            margin-bottom: 10px;
          }
          .shs-why-btn {
            background: transparent;
            border: none;
            color: #60a5fa;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            padding: 0;
            margin-bottom: 14px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
          }
          .shs-why-content {
            background: rgba(59, 130, 246, 0.08);
            border-left: 3px solid #3b82f6;
            border-radius: 4px;
            padding: 10px 12px;
            font-size: 0.85rem;
            color: #cbd5e1;
            line-height: 1.45;
            margin-bottom: 16px;
          }
          .shs-answers-grid {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 16px;
          }
          .shs-ans-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: var(--shs-text);
            padding: 12px 14px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 500;
            text-align: left;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 10px;
            line-height: 1.35;
          }
          .shs-ans-btn:hover {
            background: rgba(59, 130, 246, 0.18);
            border-color: #3b82f6;
            color: #93c5fd;
          }
          .shs-ans-btn-na {
            background: rgba(255, 255, 255, 0.02);
            border: 1px dashed rgba(255, 255, 255, 0.15);
            color: var(--shs-muted);
          }
          .shs-ans-btn-na:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.3);
            color: var(--shs-text);
          }
          .shs-nav-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-top: 14px;
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
            <span class="shs-badge-beta">Bêta v0.7.0-beta.16</span>
          </div>

          ${this._renderCurrentView(scoreVal, completenessVal, maturityText, criticalCount, potentialGain, isProvisional)}
        </div>
      `;

      this._bindEvents();
    } catch (err) {
      console.error('[SmartHomeScoreCard] Error in render:', err);
    }
  }

  _renderCurrentView(scoreVal, completenessVal, maturityText, criticalCount, potentialGain, isProvisional) {
    const globalScoreEntity = this._getGlobalScoreEntity();
    const stats = globalScoreEntity?.attributes?.installation_stats || {};
    if (this._view === 'welcome') {
      return `
        <div class="shs-welcome-box">
          <div class="shs-welcome-title">Bienvenue dans Smart Home Score</div>
          <div class="shs-welcome-desc">
            Analyse hybride intelligente : scan automatique de vos intégrations et entretien ciblé sur vos installations réelles (100 % local, 0 cloud).
          </div>
          <button class="shs-btn" id="btn-start-first-audit">
            🚀 Lancer mon premier audit
          </button>
        </div>
      `;
    }

    if (this._view === 'scanning') {
      return `
        <div class="shs-scan-box">
          <div class="shs-spinner"></div>
          <div style="font-size:1.1rem; font-weight:700; color:#f8fafc; margin-bottom:6px;">
            🔍 Scan automatique en cours...
          </div>
          <div style="font-size:0.85rem; color:var(--shs-muted); line-height:1.4;">
            Analyse des entités, intégrations, sauvegardes, réseaux locaux et énergie...
          </div>
        </div>
      `;
    }

    if (this._view === 'discovery') {
      const { autoCount, capabilityCount, questionOnlyCount, pendingList } = this._getScanBreakdown();
      const globalSensor = this._getGlobalScoreEntity();
      const stats = globalSensor?.attributes?.installation_stats || {};

      const devCount = stats.devices_count ?? '—';
      const entCount = stats.entities_count ?? '—';
      const intCount = stats.integrations_count ?? '—';
      const autoCountStat = stats.automations_count ?? '—';
      const scriptCount = stats.scripts_count ?? '—';
      const areaCount = stats.areas_count ?? '—';

      return `
        <div class="shs-audit-box">
          <div style="text-align:center; margin-bottom:14px;">
            <div style="font-size:1.2rem; font-weight:800; color:#60a5fa;">✨ Scan de votre système terminé !</div>
            <div style="font-size:0.85rem; color:var(--shs-muted); margin-top:4px;">
              Découverte automatique de votre environnement Home Assistant
            </div>
          </div>

          <div class="shs-discovery-grid">
            <div class="shs-discovery-item" style="border-top: 3px solid #10b981; border:1px solid rgba(16, 185, 129, 0.25);">
              <div class="shs-discovery-count" style="color:#34d399;">${autoCount}</div>
              <div class="shs-discovery-label">Critères validés automatiquement</div>
            </div>
            <div class="shs-discovery-item" style="border-top: 3px solid #3b82f6; border:1px solid rgba(59, 130, 246, 0.25);">
              <div class="shs-discovery-count" style="color:#60a5fa;">${capabilityCount}</div>
              <div class="shs-discovery-label">Réponses déjà suggérées</div>
            </div>
            <div class="shs-discovery-item" style="border-top: 3px solid #a855f7; border:1px solid rgba(168, 85, 247, 0.25);">
              <div class="shs-discovery-count" style="color:#c084fc;">${questionOnlyCount}</div>
              <div class="shs-discovery-label">Questions sans réponse détectable</div>
            </div>
          </div>

          <div style="font-size:0.78rem; color:var(--shs-muted); text-align:center; margin:-6px 0 14px 0;">
            59 critères au total · Vous validerez les critères pendant l'entretien.
          </div>

          <div style="background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:12px 14px; margin-bottom:16px;">
            <div style="font-size:0.85rem; font-weight:700; color:#93c5fd; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
              🔍 Votre installation analysée
            </div>
            <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:6px; font-size:0.8rem; color:#cbd5e1;">
              <div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:6px 8px;">📱 <strong>${devCount}</strong> appareils détectés</div>
              <div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:6px 8px;">⚡ <strong>${entCount}</strong> entités analysées</div>
              <div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:6px 8px;">🔌 <strong>${intCount}</strong> intégrations</div>
              <div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:6px 8px;">⚙️ <strong>${autoCountStat}</strong> automatisations</div>
              <div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:6px 8px;">📜 <strong>${scriptCount}</strong> scripts</div>
              <div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:6px 8px;">🏠 <strong>${areaCount}</strong> zones / pièces</div>
              ${stats.has_zigbee && stats.zigbee_devices_count ? `<div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:6px 8px;">📡 <strong>${stats.zigbee_devices_count}</strong> appareils Zigbee</div>` : ''}
              ${stats.has_matter ? `<div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:6px 8px;">🌐 Réseau Matter actif</div>` : ''}
              ${stats.has_zwave ? `<div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:6px 8px;">📶 Réseau Z-Wave actif</div>` : ''}
            </div>
          </div>

          <button class="shs-btn" id="btn-start-targeted-audit">
            🚀 Démarrer l'entretien ciblé (${pendingList.length} critères)
          </button>
        </div>
      `;
    }

    if (this._view === 'audit') {
      const pending = this._getPendingCriteria();
      const total = pending.length;
      if (total === 0) {
        return `
          <div class="shs-welcome-box">
            <div class="shs-welcome-title">🎉 Tous les critères ont été traités !</div>
            <div class="shs-welcome-desc">Votre audit est 100 % complet.</div>
            <button class="shs-btn" id="btn-view-summary">📊 Voir mon bilan complet</button>
          </div>
        `;
      }

      const curIdx = Math.min(this._currentQuestionIndex, total - 1);
      const crit = pending[curIdx] || pending[0];
      const st = this._getCriteriaStates()[crit.id];
      const hasEvidence = st && st.evidence;
      const proposedScore = st?.auto_score ?? null;

      let proposedOption = null;
      if (proposedScore !== null) {
        proposedOption = crit.options.find(o => o.score === proposedScore);
      }

      return `
        <div class="shs-audit-box">
          <div class="shs-domain-row">
            <span class="shs-meta-sub">${crit.id} · ${crit.domain_name}</span>
            <span style="font-size:0.8rem; color:var(--shs-muted); font-weight:600;">Question ${curIdx + 1} / ${total}</span>
          </div>

          <div class="shs-progress-bar" style="margin-bottom:14px;">
            <div class="shs-progress-fill" style="width: ${((curIdx + 1) / total) * 100}%;"></div>
          </div>

          <div class="shs-question-main">${crit.question}</div>

          ${hasEvidence ? `
            <div class="shs-evidence-box">
              <div class="shs-evidence-header">
                <span>💡</span> <span>Observation du scan Home Assistant :</span>
              </div>
              <div class="shs-evidence-text">${st.evidence}</div>
              ${proposedOption ? `
                <button class="shs-btn shs-btn-success" data-action="score" data-score="${proposedOption.score}" style="font-size:0.88rem; padding:10px 14px;">
                  ✅ Confirmer la proposition : « ${proposedOption.label} »
                </button>
              ` : ''}
            </div>
          ` : ''}

          <button class="shs-why-btn" id="btn-toggle-why">
            ℹ️ ${this._showWhy ? 'Masquer les explications' : 'Pourquoi cette question ?'}
          </button>

          ${this._showWhy ? `
            <div class="shs-why-content">
              <strong>${crit.title} :</strong> ${crit.why}
            </div>
          ` : ''}

          <div class="shs-answers-grid">
            ${crit.options.map(opt => `
              <button class="shs-ans-btn" data-action="score" data-score="${opt.score}">
                <span>🔹</span> <span>${opt.label}</span>
              </button>
            `).join('')}

            ${crit.has_not_applicable ? `
              <button class="shs-ans-btn shs-ans-btn-na" data-action="na">
                <span>⚪</span> <span>${crit.not_applicable_label || 'Non applicable à mon logement'}</span>
              </button>
            ` : ''}

            <button class="shs-ans-btn shs-ans-btn-na" data-action="skip">
              <span>❔</span> <span>Je ne sais pas / Plus tard</span>
            </button>
          </div>

          <div class="shs-nav-row">
            ${curIdx > 0 ? `
              <button class="shs-btn shs-btn-sec" id="btn-prev-q" style="width:auto; padding:8px 14px; font-size:0.85rem;">
                ◀️ Question précédente
              </button>
            ` : '<div></div>'}
            <button class="shs-btn shs-btn-sec" id="btn-view-summary" style="width:auto; padding:8px 14px; font-size:0.85rem;">
              📊 Voir mon bilan
            </button>
          </div>
        </div>
      `;
    }

    return `
      ${stats.devices_count ? `
        <div style="font-size:0.78rem; color:#93c5fd; background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.2); border-radius:8px; padding:7px 12px; margin-bottom:12px; display:flex; align-items:center; gap:6px;">
          <span>🔎</span>
          <span><strong>Analyse :</strong> ${stats.devices_count} appareils • ${stats.entities_count} entités • ${stats.automations_count} automatisations • ${stats.integrations_count} intégrations</span>
        </div>
      ` : ''}

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
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.78rem; color:var(--shs-muted);">
          <span>Éléments traités : <strong>${completenessVal.toFixed(0)} %</strong></span>
          <button id="btn-click-potential" style="background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); color:#34d399; padding:3px 8px; border-radius:6px; font-weight:700; font-size:0.78rem; cursor:pointer; display:inline-flex; align-items:center; gap:4px; transition:all 0.2s;" title="Cliquez pour afficher les actions d'amélioration">
            <span>⚡ Potentiel : +${potentialGain.toFixed(1)} pts</span>
            <span style="font-size:0.7rem;">👉</span>
          </button>
        </div>
      </div>

      <div class="shs-nav-tabs">
        <button class="shs-tab-btn ${this._activeTab === 'overview' ? 'active' : ''}" id="tab-overview">📊 Synthèse</button>
        <button class="shs-tab-btn ${this._activeTab === 'domains' ? 'active' : ''}" id="tab-domains">🏛️ Domaines</button>
        <button class="shs-tab-btn ${this._activeTab === 'actions' ? 'active' : ''}" id="tab-actions">⚡ Actions</button>
        <button class="shs-tab-btn ${this._activeTab === 'evolution' ? 'active' : ''}" id="tab-evolution">📈 Évolution</button>
      </div>

      <div id="shs-tab-body">
        ${this._renderTabBody(isProvisional)}
      </div>

      <div style="display:flex; gap:8px; margin-top:14px;">
        <button class="shs-btn" id="btn-resume-audit" style="font-size:0.85rem;">
          📝 Reprendre / Modifier l'entretien
        </button>
        <button class="shs-btn shs-btn-sec" id="btn-scan" style="font-size:0.85rem; width:auto;">
          🔄 Rescan
        </button>
      </div>

      <div style="text-align:center; margin-top:10px;">
        <button id="btn-open-restart-modal" style="background:transparent; border:none; color:var(--shs-muted); font-size:0.78rem; text-decoration:underline; cursor:pointer; padding:4px 8px; transition:color 0.2s;">
          Faire un nouvel audit (recommencer depuis zéro)
        </button>
      </div>

      <div style="margin-top:14px; padding-top:10px; border-top:1px solid rgba(255,255,255,0.06); display:flex; justify-content:space-between; align-items:center; font-size:0.72rem; color:var(--shs-muted);">
        <div>
          <span>Smart Home Score <strong>v0.7.0-beta.16</strong></span> • <span>Modèle <strong>v1.0</strong></span>
        </div>
        <div>
          <button id="btn-download-diag" style="background:transparent; border:none; color:#38bdf8; font-size:0.72rem; text-decoration:underline; cursor:pointer; padding:2px 4px;">
            📥 Télécharger les diagnostics
          </button>
        </div>
      </div>
    `;
  }



  _downloadDiagnostics() {
    const globalSensor = this._getGlobalScoreEntity();
    const attrs = globalSensor?.attributes || {};
    const diagData = {
      integration_version: "0.7.0-beta.16",
      is_beta: true,
      model_version: "1.0",
      author: "Cyrille LEFRANC",
      exported_at: new Date().toISOString(),
      installation_stats: attrs.installation_stats || {},
      audit_summary: {
        global_score: globalSensor ? Number(globalSensor.state) : 0,
        completeness: attrs.completeness || 0,
        maturity_level: attrs.maturity_level || "Non évalué",
        is_provisional: attrs.is_provisional !== undefined ? attrs.is_provisional : true,
        critical_count: attrs.critical_count || 0,
        potential_gain: attrs.potential_gain || 0,
      },
      domain_scores: attrs.domain_scores || {},
      evolution_summary: attrs.evolution || {},
      criteria_states: attrs.criteria_states || {},
    };

    const blob = new Blob([JSON.stringify(diagData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `smart_home_score_diagnostics_${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  _renderHistoryList(entries) {
    if (!this._expandedAudits) {
      this._expandedAudits = {};
    }
    return `
      <div style="background:var(--shs-card-bg); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px;">
        <div style="font-size:0.8rem; font-weight:700; color:#cbd5e1; margin-bottom:8px;">📜 Historique chronologique (${entries.length} audit${entries.length > 1 ? 's' : ''})</div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          ${entries.slice().reverse().map((e, idx) => {
            const isExp = !!this._expandedAudits[e.audit_id];
            return `
              <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <div>
                    <span style="font-weight:700; font-size:0.85rem; color:#f8fafc;">${e.completed_at || e.date}</span>
                    <div style="font-size:0.75rem; color:var(--shs-muted); margin-top:2px;">
                      Risques critiques : <strong>${e.critical_count || e.critical_risks || 0}</strong> • Modèle : <strong>v${e.model_version || '1.0'}</strong>
                    </div>
                  </div>
                  <div style="text-align:right;">
                    <div style="font-size:1.1rem; font-weight:800; color:#38bdf8;">${e.global_score.toFixed(1)} <span style="font-size:0.75rem; color:var(--shs-muted);">/100</span></div>
                    <button class="shs-why-btn" data-toggle-audit="${e.audit_id}" style="margin:4px 0 0 0; font-size:0.75rem; padding:2px 6px;">
                      ${isExp ? '▲ Masquer' : '▼ Voir le détail'}
                    </button>
                  </div>
                </div>

                ${isExp ? `
                  <div style="margin-top:10px; border-top:1px solid rgba(255,255,255,0.08); padding-top:8px; display:grid; grid-template-columns:repeat(auto-fit, minmax(110px, 1fr)); gap:6px;">
                    ${Object.entries(e.domain_scores || {}).map(([dCode, dScore]) => `
                      <div style="background:rgba(15,23,42,0.4); padding:4px 6px; border-radius:4px; font-size:0.72rem; display:flex; justify-content:space-between;">
                        <span>${dCode}</span>
                        <strong style="color:#93c5fd;">${Number(dScore).toFixed(1)}</strong>
                      </div>
                    `).join('')}
                  </div>
                ` : ''}
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  _renderTabBody(isProvisional) {
    
    if (this._activeTab === 'evolution') {
      const globalSensor = this._getGlobalScoreEntity();
      const evo = globalSensor?.attributes?.evolution || {};
      const entries = evo.history_entries || [];

      if (!entries || entries.length === 0) {
        return `
          <div style="background:rgba(59,130,246,0.08); border-left:3px solid #3b82f6; border-radius:8px; padding:18px; text-align:center; color:#93c5fd; line-height:1.5;">
            <div style="font-size:1.1rem; font-weight:700; margin-bottom:6px;">📈 Historique d'évolution</div>
            Aucun audit complet n'a encore été finalisé.<br/>
            <span style="font-size:0.83rem; color:var(--shs-muted);">Terminez votre premier audit (100 % des critères) pour initier votre courbe d'évolution.</span>
          </div>
        `;
      }

      if (entries.length === 1) {
        const e = entries[0];
        return `
          <div style="display:flex; flex-direction:column; gap:12px;">
            <div style="background:rgba(16,185,129,0.1); border-left:3px solid #10b981; border-radius:8px; padding:14px; color:#a7f3d0;">
              <div style="font-weight:700; font-size:0.95rem; margin-bottom:4px;">Premier audit de référence finalisé</div>
              <div style="font-size:0.85rem; color:#cbd5e1;">
                Score enregistré : <strong>${e.global_score.toFixed(1)} / 100</strong> le ${e.completed_at || e.date}.
              </div>
              <div style="font-size:0.8rem; color:#94a3b8; margin-top:6px;">
                📍 Votre premier audit servira de point de référence pour mesurer votre progression au fil de vos améliorations.
              </div>
            </div>

            ${this._renderHistoryList(entries)}
          </div>
        `;
      }

      // 2 or more completed audits
      const domProg = evo.domain_progressions || {};
      
      // SVG Chart calculation
      const chartPoints = entries.map((en, idx) => {
        const x = entries.length === 1 ? 150 : 25 + (idx * (250 / (entries.length - 1)));
        const y = 65 - ((en.global_score / 100) * 50);
        return { x, y, score: en.global_score, date: en.completed_at || en.date };
      });
      const polylinePoints = chartPoints.map(p => `${p.x},${p.y}`).join(' ');

      return `
        <div style="display:flex; flex-direction:column; gap:12px;">
          <!-- 1. En-tête résumé -->
          <div style="background:var(--shs-card-bg); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:14px;">
            <div style="font-size:0.8rem; color:var(--shs-muted); font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">Évolution du Smart Home Score</div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
              <div style="font-size:1.35rem; font-weight:800; color:#f8fafc;">
                ${evo.first_audit_score.toFixed(1)} <span style="color:#94a3b8; font-size:1rem;">➔</span> <span style="color:#38bdf8;">${evo.latest_audit_score.toFixed(1)}</span>
                <span style="font-size:0.85rem; color:var(--shs-muted); font-weight:500;">/ 100</span>
              </div>
              <div style="font-size:0.85rem; font-weight:700; padding:4px 10px; border-radius:20px; ${evo.total_progression >= 0 ? 'background:rgba(16,185,129,0.15); color:#34d399;' : 'background:rgba(239,68,68,0.15); color:#f87171;'}">
                ${evo.total_progression >= 0 ? '+' : ''}${evo.total_progression.toFixed(1)} pts depuis le premier audit
              </div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--shs-muted); margin-top:8px; border-top:1px solid rgba(255,255,255,0.06); padding-top:6px;">
              <span>Premier audit : ${evo.first_completed_at}</span>
              <span>Dernier audit : ${evo.latest_completed_at}</span>
            </div>
            ${evo.has_model_version_mismatch ? `
              <div style="margin-top:8px; font-size:0.75rem; color:#f59e0b; background:rgba(245,158,11,0.1); padding:6px 10px; border-radius:6px;">
                ⚠️ Le référentiel a évolué entre ces deux audits. La comparaison est indicative.
              </div>
            ` : ''}
          </div>

          <!-- 2. Courbe SVG du score global -->
          <div style="background:var(--shs-card-bg); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px;">
            <div style="font-size:0.8rem; font-weight:700; color:#cbd5e1; margin-bottom:6px;">📈 Trajectoire du Score Global</div>
            <svg viewBox="0 0 300 80" style="width:100%; height:auto; overflow:visible;">
              <line x1="20" y1="65" x2="280" y2="65" stroke="rgba(255,255,255,0.1)" stroke-dasharray="2" />
              <line x1="20" y1="40" x2="280" y2="40" stroke="rgba(255,255,255,0.1)" stroke-dasharray="2" />
              <line x1="20" y1="15" x2="280" y2="15" stroke="rgba(255,255,255,0.1)" stroke-dasharray="2" />
              
              <polyline fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" points="${polylinePoints}" />
              
              ${chartPoints.map(p => `
                <circle cx="${p.x}" cy="${p.y}" r="4" fill="#0284c7" stroke="#ffffff" stroke-width="1.5" />
                <text x="${p.x}" y="${p.y - 7}" font-size="7" font-weight="700" fill="#38bdf8" text-anchor="middle">${p.score.toFixed(1)}</text>
              `).join('')}
            </svg>
          </div>

          <!-- 3. Vos plus belles progressions -->
          ${evo.top_progressions && evo.top_progressions.length > 0 ? `
            <div style="background:linear-gradient(135deg, rgba(245,158,11,0.12), rgba(59,130,246,0.08)); border:1px solid rgba(245,158,11,0.25); border-radius:10px; padding:12px 14px;">
              <div style="font-weight:700; font-size:0.85rem; color:#fbbf24; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                <span>🏆</span> <span>Vos plus belles progressions</span>
              </div>
              <div style="display:flex; flex-wrap:wrap; gap:8px;">
                ${evo.top_progressions.map(tp => `
                  <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(255,255,255,0.1); border-radius:6px; padding:6px 10px; font-size:0.8rem; display:flex; align-items:center; gap:6px;">
                    <span>${tp.domain_name}</span>
                    <strong style="color:#34d399;">+${tp.delta.toFixed(1)} pts</strong>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}

          <!-- 4. Progression des 8 domaines -->
          <div style="background:var(--shs-card-bg); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px;">
            <div style="font-size:0.8rem; font-weight:700; color:#cbd5e1; margin-bottom:10px;">🏛️ Progression par domaine</div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:8px;">
              ${Object.keys(domProg).map(k => {
                const dp = domProg[k];
                const isPos = dp.delta > 0;
                const isNeg = dp.delta < 0;
                const deltaColor = isPos ? '#34d399' : (isNeg ? '#f87171' : 'var(--shs-muted)');
                const deltaSign = isPos ? '+' : '';
                return `
                  <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:8px 10px;">
                    <div style="font-size:0.75rem; font-weight:600; color:var(--shs-text); margin-bottom:3px;">${dp.name}</div>
                    <div style="font-size:0.78rem; color:var(--shs-muted);">
                      ${dp.first.toFixed(1)} ➔ <strong>${dp.latest.toFixed(1)}</strong>
                    </div>
                    <div style="font-size:0.75rem; font-weight:700; color:${deltaColor}; margin-top:2px;">
                      ${deltaSign}${dp.delta.toFixed(1)} pts
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- 5. Historique des audits -->
          ${this._renderHistoryList(entries)}
        </div>
      `;
    }

    if (this._activeTab === 'domains') {
      const globalSensor = this._getGlobalScoreEntity();
      const domScores = globalSensor?.attributes?.domain_scores || {};
      const getDom = (domCode) => {
        if (domScores[domCode] !== undefined && domScores[domCode] !== null) {
          return Number(domScores[domCode]).toFixed(1);
        }
        return '—';
      };
      return `
        <div class="shs-domain-grid">
          <div class="shs-domain-card"><div class="shs-domain-title">⚡ Sécurité électrique</div><div class="shs-domain-score">${getDom('ELEC')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🔒 Cybersécurité</div><div class="shs-domain-score">${getDom('CYBER')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🛡️ Résilience</div><div class="shs-domain-score">${getDom('RES')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">⚙️ Automatisations</div><div class="shs-domain-score">${getDom('AUTO')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">☀️ Énergie</div><div class="shs-domain-score">${getDom('ENER')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🔌 Interopérabilité</div><div class="shs-domain-score">${getDom('INTER')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">📱 Expérience / UX</div><div class="shs-domain-score">${getDom('UX')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🛠️ Maintenance</div><div class="shs-domain-score">${getDom('MAINT')} / 100</div></div>
        </div>
      `;
    }

    if (this._activeTab === 'actions') {
      const globalSensor = this._getGlobalScoreEntity();
      const recs = globalSensor?.attributes?.recommendations || [];

      if (!recs || recs.length === 0) {
        return `
          <div style="background:rgba(16,185,129,0.12); border-left:3px solid #10b981; border-radius:8px; padding:14px; text-align:center; color:#a7f3d0;">
            🎉 <strong>Félicitations !</strong> Votre installation a atteint l'excellence maximale (100 / 100). Aucun critère perfectible restant.
          </div>
        `;
      }

      // Show top prioritized actions
      return `
        <div style="display:flex; flex-direction:column; gap:10px;">
          <div style="font-size:0.82rem; color:var(--shs-muted); display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
            <span><strong>${recs.length}</strong> actions d'amélioration identifiées</span>
            <span>Triées par pertinence & impact</span>
          </div>

          ${recs.map((r, idx) => {
            const prioClass = r.priority === 1 ? 'color:#f87171; background:rgba(239,68,68,0.18);' : (r.priority === 2 ? 'color:#fbbf24; background:rgba(245,158,11,0.18);' : (r.is_quick_win ? 'color:#34d399; background:rgba(16,185,129,0.18);' : 'color:#93c5fd; background:rgba(59,130,246,0.18);'));
            const effortLabel = r.difficulty === 'FACILE' ? 'Facile · <15 min' : (r.difficulty === 'MOYENNE' ? 'Effort Moyen' : 'Avancé');
            const targetScore = r.target_score || 4;
            const curScore = r.current_score || 0;
            const isExpanded = this._expandedActions && this._expandedActions[r.criterion_id];

            return `
              <div style="background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:14px;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px; margin-bottom:8px;">
                  <div>
                    <div style="font-size:0.75rem; color:#94a3b8; font-weight:600; text-transform:uppercase; margin-bottom:2px;">
                      ${r.criterion_id} · ${r.domain_name}
                    </div>
                    <div style="font-weight:700; font-size:0.95rem; color:#f8fafc; line-height:1.3;">
                      ${r.criterion_name}
                    </div>
                  </div>
                  <div style="background:rgba(16,185,129,0.18); color:#34d399; font-weight:700; font-size:0.82rem; padding:3px 8px; border-radius:6px; white-space:nowrap;">
                    +${r.exact_gain.toFixed(1)} pt
                  </div>
                </div>

                <div style="font-size:0.83rem; color:#cbd5e1; margin-bottom:8px; line-height:1.4;">
                  <strong>Pourquoi ?</strong> ${r.why_it_matters || r.recommendation_text}
                </div>

                <div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:8px 10px; font-size:0.8rem; margin-bottom:8px;">
                  <div style="color:#94a3b8; margin-bottom:4px;">
                    📍 <strong>Situation actuelle :</strong> ${r.current_level_desc || `Niveau ${curScore}/4`}
                  </div>
                  <div style="color:#60a5fa; font-weight:600;">
                    🎯 <strong>Objectif suivant :</strong> ${r.target_level_desc || `Niveau ${targetScore}/4`}
                  </div>
                </div>

                <div style="display:flex; gap:6px; flex-wrap:wrap; align-items:center; margin-bottom:8px;">
                  <span style="font-size:0.72rem; padding:2px 7px; border-radius:4px; font-weight:700; ${prioClass}">
                    ${r.priority_label}
                  </span>
                  <span style="font-size:0.72rem; padding:2px 7px; border-radius:4px; font-weight:600; background:rgba(255,255,255,0.08); color:#e2e8f0;">
                    ⏱️ ${effortLabel}
                  </span>
                  <span style="font-size:0.72rem; padding:2px 7px; border-radius:4px; font-weight:600; background:rgba(168,85,247,0.18); color:#d8b4fe;">
                    🏷️ ${r.action_type}
                  </span>
                </div>

                <button class="shs-why-btn" data-toggle-action="${r.criterion_id}" style="margin-bottom:0; font-size:0.8rem;">
                  ${isExpanded ? '▲ Masquer les conseils' : '▼ Voir comment améliorer'}
                </button>

                ${isExpanded ? `
                  <div style="background:rgba(59,130,246,0.08); border-left:3px solid #3b82f6; border-radius:4px; padding:10px 12px; font-size:0.83rem; color:#cbd5e1; line-height:1.45; margin-top:8px;">
                    <strong>💡 Conseil d'amélioration :</strong><br/>
                    ${r.recommendation_text}
                  </div>
                ` : ''}
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    return `
      <div style="font-size:0.85rem; color:var(--shs-muted); line-height:1.5;">
        ${isProvisional ? `
          <div style="background:rgba(245,158,11,0.1); border-left:3px solid #f59e0b; padding:8px 12px; border-radius:4px; margin-bottom:8px;">
            Entretien partiel : répondez aux questions restantes pour finaliser votre bilan complet.
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
      this._view = 'scanning';
      this._render();
      this._hass?.callService('smart_home_score', 'run_analysis', {});
      setTimeout(() => {
        this._view = 'discovery';
        this._render();
      }, 1200);
    });

    this.shadowRoot.getElementById('btn-start-targeted-audit')?.addEventListener('click', () => {
      this._view = 'audit';
      this._currentQuestionIndex = 0;
      this._showWhy = false;
      this._render();
    });

    this.shadowRoot.getElementById('btn-toggle-why')?.addEventListener('click', () => {
      this._showWhy = !this._showWhy;
      this._render();
    });

    this.shadowRoot.querySelectorAll('[data-toggle-action]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const cid = e.currentTarget.getAttribute('data-toggle-action');
        this._expandedActions = this._expandedActions || {};
        this._expandedActions[cid] = !this._expandedActions[cid];
        this._render();
      });
    });

    this.shadowRoot.getElementById('btn-click-potential')?.addEventListener('click', () => {
      this._activeTab = 'actions';
      this._render();
    });

    this.shadowRoot.querySelectorAll('[data-action]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        this._isBusy = true;
        this._render();
        setTimeout(() => {
          this._isBusy = false;
          this._render();
        }, 500);
        const action = e.currentTarget.getAttribute('data-action');
        const pending = this._getPendingCriteria();
        const crit = pending[this._currentQuestionIndex];
        if (crit) {
          if (action === 'skip') {
            this._hass?.callService('smart_home_score', 'skip_question', { criterion_id: crit.id });
          } else if (action === 'na') {
            this._hass?.callService('smart_home_score', 'submit_answer', { criterion_id: crit.id, answer_key: 'not_applicable' });
          } else if (action === 'score') {
            const score = parseInt(e.currentTarget.getAttribute('data-score'), 10);
            this._hass?.callService('smart_home_score', 'submit_answer', { criterion_id: crit.id, answer_key: String(score) });
          }
        }
        if (this._currentQuestionIndex < pending.length - 1) {
          this._currentQuestionIndex++;
          this._showWhy = false;
        } else {
          this._view = 'cockpit';
        }
        this._render();
      });
    });

    this.shadowRoot.getElementById('btn-prev-q')?.addEventListener('click', () => {
      if (this._currentQuestionIndex > 0) {
        this._currentQuestionIndex--;
        this._showWhy = false;
        this._render();
      }
    });

    this.shadowRoot.getElementById('btn-view-summary')?.addEventListener('click', () => {
      this._view = 'cockpit';
      this._render();
    });

    this.shadowRoot.getElementById('btn-resume-audit')?.addEventListener('click', () => {
      this._view = 'discovery';
      this._showWhy = false;
      this._render();
    });

    this.shadowRoot.getElementById('btn-scan')?.addEventListener('click', () => {
      this._view = 'scanning';
      this._render();
      this._hass?.callService('smart_home_score', 'run_analysis', {});
      setTimeout(() => {
        this._view = 'discovery';
        this._render();
      }, 1200);
    });

    this.shadowRoot.getElementById('btn-open-restart-modal')?.addEventListener('click', () => {
      this._showRestartModal = true;
      this._render();
    });

    this.shadowRoot.getElementById('btn-cancel-restart')?.addEventListener('click', () => {
      this._showRestartModal = false;
      this._render();
    });

    this.shadowRoot.getElementById('btn-confirm-restart')?.addEventListener('click', async () => {
      this._showRestartModal = false;
      this._isBusy = true;
      this._render();
      try {
        await this._hass?.callService('smart_home_score', 'restart_audit', {});
      } catch (err) {
        console.warn('Service restart_audit notice:', err);
      }
      this._currentQuestionIndex = 0;
      this._view = 'discovery';
      this._isBusy = false;
      this._render();
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
  description: "Scanner automatique et entretien d'audit de votre maison connectée",
  documentationURL: 'https://github.com/nano2sillery/smart_home_score'
};

if (existingCardIdx >= 0) {
  window.customCards[existingCardIdx] = cardEntry;
} else {
  window.customCards.push(cardEntry);
}
