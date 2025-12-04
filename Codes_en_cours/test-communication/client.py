# serveur.py
import socket                # fournit les fonctions de communication réseau
import threading             # permet de gérer chaque client dans un thread séparé
import sys                   # pour pouvoir quitter proprement

HOST = "127.0.0.1"           # adresse d'écoute (localhost pour tests)
PORT = 5000                  # port d'écoute (doit être >1023 sauf si root)

def handle_client(conn, addr):
    """
    Fonction exécutée dans un thread pour gérer un client unique.
    Reçoit un message, affiche, répond, puis ferme la connexion.
    """
    try:
        print(f"[+] Connexion depuis {addr}")
        # Attendre un message du client (bloquant)
        data = conn.recv(1024)        # lit jusqu'à 1024 octets
        if not data:
            print(f"[!] Connexion fermée par le client {addr}")
            return
        message = data.decode()       # décoder les octets en chaîne
        print(f"[Client {addr}] {message}")

        # Préparer et envoyer la réponse
        reply = "Message bien reçu"
        conn.sendall(reply.encode())  # envoyer la réponse encodée en octets

    except Exception as e:
        print(f"[Erreur] client {addr} : {e}")
    finally:
        conn.close()                  # fermer la connexion du client
        print(f"[-] Déconnexion {addr}")

def main():
    # Création du socket TCP (IPv4)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Autoriser la réutilisation de l'adresse si le serveur redémarre rapidement
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))   # attacher le socket à l'adresse et port
        server.listen()             # passer en mode écoute (backlog par défaut)
        print(f"[Serveur] En écoute sur {HOST}:{PORT}")
    except Exception as e:
        print(f"[Erreur] impossible de démarrer le serveur : {e}")
        server.close()
        sys.exit(1)

    try:
        while True:
            conn, addr = server.accept()   # accepte une connexion entrante
            # Créer et démarrer un thread pour traiter ce client
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n[Serveur] Arrêt demandé par l'utilisateur")
    finally:
        server.close()
        print("[Serveur] Fermé")

if __name__ == "__main__":
    main()
