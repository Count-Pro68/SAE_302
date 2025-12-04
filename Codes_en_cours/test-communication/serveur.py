# client.py
import socket

HOST = "127.0.0.1"    # adresse du serveur
PORT = 5000           # port du serveur

def main():
    # Création du socket client TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))              # se connecter au serveur
            message = "Bonjour serveur !"       # message à envoyer
            s.sendall(message.encode())         # envoyer encodé en octets

            data = s.recv(1024)                 # recevoir jusqu'à 1024 octets
            if data:
                print(f"[Serveur] {data.decode()}")  # décoder et afficher
            else:
                print("[Client] Pas de réponse du serveur")
        except ConnectionRefusedError:
            print("[Client] Connexion refusée : le serveur n'est pas démarré ?")
        except Exception as e:
            print(f"[Client] Erreur : {e}")

if __name__ == "__main__":
    main()
