import socket # Gère les communications UDP & TCP
import time # Utiliser pour faire des pauses entre chaque cycles

DISCOVER_PORT = 9000 # assignation du port
CLIENT_PORT = 9100

routers = {}  # Stockage en mémoire uniquement

def parse_router_message(msg):
    # Distribue des informations (ports, ID, clé n, clé e)
    parts = msg.split(";") # Coupe la chaîne en utilisant ";"
    if parts[0] != "ROUTER":    # si le message ne vient pas d'un routeur, il n'est pas analysé
        return None
    d = {} # Création d'un dictionnaire
    for p in parts[1:]:
        k, v = p.split("=") # pour chaque champ du message on sépare par "="
        d[k] = v
    return d # Retourne dictionnaire avec données

def broadcast_discover():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #création socket IPv4 en mode UDP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # permet l'envoie des messages broadcast
    s.sendto(b"DISCOVER", ("<broadcast>", DISCOVER_PORT)) # Envoie le message discover en UDP broadcast vers le port des routeurs
    s.close() # fermer le socket

def listen_for_routers(timeout=2): # Création d’un socket UDP pour écouter les routeurs sur port 9000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", DISCOVER_PORT))
    """
    ("" = écoute sur toutes les interfaces locales)
    (Master attend les réponses sur ce port)
    """
    s.settimeout(timeout) # permet d'éviter d'attendre indéfiniment (2 secondes avant l'arrêt de la communication)
    try:
        while True: # message UDP
            data, addr = s.recvfrom(4096) # data = octets reçus
            msg = data.decode() # décodage du msg en texte

            info = parse_router_message(msg) # On analyse avec parse_router_message
            if info: # si valide alors...
                info["IP"] = addr[0] #Ajoute adresse IP envoyé automatiquement par le socket
                routers[info["ID"]] = info #enregistrement dans "routers"
                print("MASTER: router reçu :", info) # Affiche message débug

    except socket.timeout: # Fin du timeout (après X secondes -> Sortie du timeout
        pass
    s.close() # fermeture socket

def listen_for_client(timeout=2): # écoute client sur port 9100
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", CLIENT_PORT))
    """
        ("" = écoute sur toutes les interfaces locales)
        (Master attend les réponses sur ce port)
    """
    s.settimeout(timeout) # permet d'éviter d'attendre indéfiniment (2 secondes avant l'arrêt de la communication)

    try:
        data, addr = s.recvfrom(4096)
        if data.decode().strip() == "GET_LIST": # Demande la liste des routeurs
            print("MASTER: client demande la liste") # Affiche une réponse texte
            # construire la réponse
            lst = "LIST;"
            first = True
            for r in routers.values(): # Génère une chaîne de style
                if not first: lst += "|" # Séparé par "|"
                lst += f"ID={r['ID']},IP={r['IP']},PORT={r['PORT']},N={r['N']},E={r['E']}"
                first = False
            s.sendto(lst.encode(), addr) # Renvoi la liste au client
    except socket.timeout: # Timeout = permet la sortie de la boucle si X de secondes dépassées
        pass
    s.close() # Ferme le socket


print("MASTER lancé.") # Message de démarrage du Master
while True: # boucle infinie pour faire tourner le service
    broadcast_discover() #chaque secondes le master envoie une requête d'identification
    listen_for_routers() # Ecoute les réponses des routeurs
    listen_for_client() # Ecoute les réponses et demandes du client
    time.sleep(1) # Fait une pose de 1 secondes pour libérer le réseau
