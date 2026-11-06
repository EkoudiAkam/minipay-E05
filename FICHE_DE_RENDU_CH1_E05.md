# FICHE DE RENDU - CHAPITRE 1 : INTRODUCTION AUX SYSTÈMES DISTRIBUÉS

## En-tête
- **Chapitre :** Chapitre 1
- **Équipe :** E05
- **Membres et rôles pour ce chapitre :**
  - **Coordinateur :** Yvan EKOUDI (Coordination, gestion du dépôt GitHub, suivi des étapes et soumission)
  - **Responsable technique :** KAMENI SUNDA Lilian Laslande (Conception et implémentation de `serveur.py` et `client.py`)
  - **Responsable tests :** RIEPOUO NZIE Raïmatou (Simulation des pannes réseau, observation des erreurs et timeouts)
  - **Rédacteur :** NDENGUE HOGBE Fred Martin (Rédaction des observations d'étapes et des réponses théoriques)
  - **Relectrice :** YANTCHOP Leatitia (Relecture, vérification des empreintes cryptographiques et cohérence du barème)
  - **Responsable environnement :** WAOUNSI Dylan (Validation de l'environnement d'exécution, suivi des versions et intégrité Git)
- **Lien du dépôt GitHub :** https://github.com/EkoudiAkam/minipay-E05
- **Date de dépôt :** 06/11/2026

---

### 1. Preuves d'exécution
| Membre | Fichier de preuve joint | Remarque |
|---|:---:|---|
| Yvan EKOUDI | **Oui** | `preuve_E05_YvanEkoudi.json` (Validé - SHA-256 OK) |
| KAMENI SUNDA Lilian Laslande | **Oui** | `preuve_E05_KAMENISUNDALILIANLASLANDE.json` (Validé - SHA-256 OK) |
| RIEPOUO NZIE Raïmatou | **Oui** | `preuve_E05_RIEPOUONZIERaïmatou.json` (Validé - SHA-256 OK) |
| NDENGUE HOGBE Fred Martin | **Oui** | `preuve_E05_NdengueHogbeFredMartin.json` (Validé - SHA-256 OK) |
| YANTCHOP Leatitia | **Oui** | `preuve_E05_YantchopLeatitia.json` (Validé - SHA-256 OK) |
| WAOUNSI Dylan | **Oui** | `preuve_E05_WaounsiDylan.json` (Validé - SHA-256 OK) |

---

### 2. Résultats de l'équipe E05 (Graine déterministe dérivée de l'identifiant E05)
| Paramètre / Mesure | Valeur de l'équipe E05 |
|---|:---:|
| **Timeout configuré pour le client** | **1 seconde** |
| **Délai de traitement simulé par le serveur** | **2 secondes** |
| **Montant du paiement testé** | **6 000 FCFA** |
| **Paiements exécutés SANS identifiant unique (Scénario A)** | **2** (Double débit : 12 000 FCFA prélevés) |
| **Paiements exécutés AVEC identifiant unique (Scénario B)** | **1** (Idempotence réussie : 6 000 FCFA prélevés) |
| **Latence moyenne de connexion locale mesurée** | **~0.83 ms** |

---

### 3. Questions de compréhension (Support de cours, page 148)

#### Question 1. Avec les paramètres de votre équipe, le serveur exécute plusieurs fois le paiement alors que le client n'obtient aucune confirmation. Expliquez, étape par étape, ce qui se passe. Combien d'argent aurait été débité au total ?
*Réponse :*
1. Le client transmet un premier ordre de paiement de 6 000 FCFA au serveur.
2. Le serveur reçoit la requête, incrémente son compteur de débit et démarre son traitement artificiellement ralenti à 2 secondes.
3. Le client attend la réponse mais son timeout expire au bout d'1 seconde. Le client en déduit prématurément que la connexion ou le service a échoué.
4. Le client effectue un second essai en renvoyant le même message.
5. Le serveur, n'ayant aucun moyen d'identifier que cette seconde requête est une répétition, la traite comme une nouvelle transaction distincte.
Au total, **12 000 FCFA** ont été prélevés pour une seule commande réelle de l'utilisateur, et le client n'a jamais reçu la confirmation à temps.

#### Question 2. Parmi les huit idées fausses sur les réseaux, lesquelles ce scénario met-il en défaut ? Justifiez en deux ou trois phrases.
*Réponse :*
Ce scénario contredit formellement l'**idée fausse n°1 (« Le réseau est fiable »)**, car le client a considéré l'absence de réponse immédiate comme un échec, alors que la requête avait bien été acheminée et traitée. Il met également en défaut l'**idée fausse n°2 (« La latence est nulle »)**, le délai réel de réponse (2 s) ayant surpassé le délai arbitraire d'attente imposé par l'application cliente (1 s).

#### Question 3. Proposez une correction du côté serveur (l'identifiant unique) et une autre du côté client (par exemple le message affiché à l'utilisateur). Quelle limite garde chacune ?
*Réponse :*
- **Côté serveur :** Rendre l'opération **idempotente** à l'aide d'un jeton d'idempotence unique (UUID) généré à chaque achat. Le serveur mémorise les identifiants déjà exécutés et ignore tout rejeu. *Limite :* Cela oblige le serveur à conserver un historique de clés (surcoût de stockage et de mémoire vive, nécessité de purger les anciennes clés).
- **Côté client :** En cas d'expiration du délai d'attente, ne pas renvoyer immédiatement une nouvelle requête de débit mais afficher un message du type : *« Paiement en cours de vérification, veuillez patienter »* accompagné d'une requête de consultation d'état (`GET /statut`). *Limite :* L'utilisateur reste dans l'attente sans confirmation immédiate si la panne réseau persiste.

---

### 4. Difficultés rencontrées et solutions
- **Difficulté :** Comprendre qu'un échec de connexion immédiat (`ConnectionRefusedError`) n'a pas la même signification qu'un blocage par timeout (`TimeoutError`), et constater qu'un silence réseau ne signifie jamais qu'une opération n'a pas eu lieu.
- **Solution :** La mise en œuvre d'un identifiant unique (UUID) côté client associé à un ensemble (`set`) de contrôle côté serveur garantit que même si le client s'impatiente et réessaie, le paiement n'est exécuté qu'une seule et unique fois.

---

### 5. Contribution de chaque membre (Une ligne par étudiant)
| Membre | Contribution individuelle effective |
|---|---|
| **Yvan EKOUDI** | Initialisation du projet, gestion du dépôt Git, rédaction des fichiers de validation et coordination d'équipe. |
| **KAMENI SUNDA Lilian Laslande** | Conception des sockets TCP, écriture du code de `serveur.py` et gestion du multithreading. |
| **RIEPOUO NZIE Raïmatou** | Mise en place des tests de charge, simulation des pannes partielles et vérification des délais de timeout. |
| **NDENGUE HOGBE Fred Martin** | Analyse des journaux d'exécution, formalisation des résultats d'étape et rédaction des questions théoriques. |
| **YANTCHOP Leatitia** | Relecture globale de la fiche, vérification des signatures d'intégrité SHA-256 et respect du barème Moodle. |
| **WAOUNSI Dylan** | Paramétrage des environnements locaux d'exécution, tests de compatibilité Windows/Linux et validation Git. |
