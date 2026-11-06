"""Lab 1 : Serveur de paiement avec comptage et gestion d'idempotence."""
import socket
import time

PORT = 5000

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", PORT))
s.listen(16)
print(f"Serveur de paiement à l'écoute sur le port {PORT}...")

compteur = 0
vus = set()

while True:
    conn, addr = s.accept()
    try:
        data = conn.recv(1024).decode()
        ident = data.split("id=")[-1].strip() if "id=" in data else None
        
        if ident and ident in vus:
            print(f"[Doublon] Transaction {ident} déjà exécutée. Ignorée.")
        else:
            compteur += 1
            if ident:
                vus.add(ident)
            print(f"[Paiement] Ordre reçu: '{data}' | Total paiements exécutés: {compteur}")
            
        time.sleep(0.2)  # Simulation d'un traitement
        conn.sendall(f"OK {data}".encode())
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
    finally:
        conn.close()
