"""Lab 1 : Client de paiement avec timeout, réessais et identifiant unique."""
import socket
import time
import uuid

SERVEUR_IP = "127.0.0.1"
PORT = 5000
TIMEOUT = 2
MAX_ESSAIS = 2

# Génération d'une clé d'idempotence unique pour ce paiement
id_transaction = uuid.uuid4().hex[:8]
message = f"payer 5000 id={id_transaction}"

print(f"Tentative de paiement: {message}")
t0 = time.time()
succes = False

for essai in range(MAX_ESSAIS):
    try:
        print(f"Essai {essai + 1}/{MAX_ESSAIS}...")
        c = socket.create_connection((SERVEUR_IP, PORT), timeout=TIMEOUT)
        c.sendall(message.encode())
        reponse = c.recv(1024).decode()
        print(f"Réponse reçue du serveur: {reponse}")
        succes = True
        c.close()
        break
    except OSError as e:
        print(f"Échec de l'essai {essai + 1} : {e}")

duree_ms = (time.time() - t0) * 1000
if succes:
    print(f"Paiement confirmé avec succès en {duree_ms:.1f} ms.")
else:
    print(f"Échec définitif du paiement après {MAX_ESSAIS} essais ({duree_ms:.1f} ms).")
