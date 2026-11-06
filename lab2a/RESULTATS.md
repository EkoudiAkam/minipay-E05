# Résultats et Mesures - Lab 2A : Du serveur unique au répartiteur de charge

## Équipe : E05
## Membre : Yvan Ekoudi (EkoudiAkam)

---

### 1.Mesures réelles obtenues

| Configuration | Débit (req/s) | Latence moyenne (ms) | Erreurs (sur 200) | Observation |
|---|---|---|---|---|

| **Étape 2 : Monolithe unique (5001)** | 11.3 | 734.1 | 7 / 200 | Mesure de référence sur instance seule |
| **Étape 2 (bis) : Panne du Monolithe** | 4.9 | 2044.6 | 200 / 200 | **SPOF confirmé** (indisponibilité totale 100%) |
| **Étape 3 : 2 instances + Répartiteur (8000)** | 15.9 | 553.9 | **0 / 200** | Gain de débit (+40%) et réduction de latence |
| **Étape 4 : Arrêt de l'instance 5002** | 7.1 | 1165.1 | **0 / 200** | **Haute disponibilité préservée** (reprise sur panne automatique du LB) |

---

### 2. Observation de l'incohérence des données (Étape 5)

Interrogation directe des soldes de l'utilisatrice `awa` sur chaque instance :
- **Instance 5001 :** `{"compte":"awa","instance":5001,"solde":999501}`
- **Instance 5002 :** `{"compte":"awa","instance":5002,"solde":999899}`

**Constat :**
Les soldes sont totalement divergents (999 501 FCFA vs 999 899 FCFA).
Chaque instance a exécuté les écritures dans son fichier local SQLite (`monolithe_5001.db` et `monolithe_5002.db`). Le répartiteur distribue bien la charge applicative (stateless), mais n'assure aucune synchronisation de l'état (stateful).

---

### 3. Réponses aux questions de compréhension (Support p. 52)

#### Q1 : Analyse des écarts de performance
Avec deux instances derrière le répartiteur, le débit passe de 11.3 req/s à 15.9 req/s et la latence moyenne chute de 734ms à 554ms : les requêtes sont parallélisées entre les processus. Lors de la coupure de l'instance 5002, le débit chute à 7.1 req/s et la latence grimpe à 1165 ms car le répartiteur subit un timeout sur 5002 avant de rebasculer sur 5001, mais **aucune requête n'est perdue (0 erreur)**.

#### Q2 : Pourquoi les soldes sont différents et quel risque en production ?
Les instances 5001 et 5002 possèdent chacune leur propre base de données SQLite locale isolée. Les débits effectués via l'instance 5001 ne sont jamais répercutés sur 5002. Dans un système bancaire réel, cela entraînerait des incohérences comptables critiques et le risque de dépense double (un client pourrait vider son compte sur deux nœuds différents).

#### Q4 : Calcul de disponibilité en chaîne (Passerelle -> Paiement -> Compte)
Pour 3 services en série avec une disponibilité de 99,9 % ($A = 0,999$) chacun :
$$A_{\text{chaîne}} = (0,999)^3 \approx 0,9970 \quad (99,70\%)$$
- **Temps d'arrêt annuel de la chaîne :** $(1 - 0,9970) \times 8760\text{ h} \approx 26,3\text{ heures/an}$.
- **Comparaison :** Un monolithe à 99,9 % ne s'arrête que $8,76\text{ heures/an}$. La composition synchrone de microservices sans mode dégradé multiplie le risque d'indisponibilité par 3.
