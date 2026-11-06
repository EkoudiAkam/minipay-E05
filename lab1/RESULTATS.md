# Résultats et Observations - Lab 1 : Premier système distribué et double débit

## Équipe : E05
## Membre : Yvan Ekoudi (EkoudiAkam)

### Étape 2 : Simulation des pannes partielles
- **Serveur arrêté :** La tentative de connexion échoue immédiatement avec l'erreur `ConnectionRefusedError` (code d'erreur socket 10061 sous Windows). Le client sait instantanément que le serveur n'est pas joignable et qu'aucun traitement n'a commencé.
- **Serveur injoignable (IP fictive `10.255.255.1`) :** La tentative bloque pendant exactement la durée du timeout (2 secondes) avant de lever une exception `TimeoutError`. Deux pannes distinctes se manifestent donc par des délais et des comportements totalement différents, infirmant l'idée fausse que le réseau est instantané ou fiable.

### Étape 3 : Reproduction du double débit et Idempotence
- **Sans clé d'idempotence :** Avec un délai serveur (3 s) supérieur au timeout du client (2 s), le client réémet sa requête lors du 2e essai. Le serveur, qui a déjà exécuté le premier ordre dans son thread de traitement, reçoit et exécute le second ordre comme une nouvelle transaction. Résultat : 2 débits comptabilisés pour un seul ordre utilisateur (10 000 FCFA prélevés au lieu de 5 000 FCFA).
- **Avec clé d'idempotence (UUID) :** En associant un identifiant unique à chaque transaction et en mémorisant les identifiants déjà traités côté serveur, le réessai est reconnu comme un doublon. Le serveur renvoie l'accusé de réception sans réexécuter le débit. Le compteur reste exactement à 1 débit.
