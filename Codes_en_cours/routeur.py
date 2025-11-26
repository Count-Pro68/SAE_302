"""
Socket, Thread, QT et MariaDB
Déchiffrement d'une seul couche
"""
"""
envoiyer son @ip
envoi le port d'écoute
envoie la clé publique

le routeur doit écouter sur un port fixe
chaque message reçu = thread dédié
(voir aide chat-gpt)


Ecouter les port et accpter les connexions

importer le système de cryptage comme une librairie
"""

# [id de l'action][CLE_PUBLIQUE][PORT][@ip]
                            """
                            il faut crée plusieurs actions qui se suivent
                            """
# cRéation d'un socket routeur
routeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
routeur.bind(("0.0.0.0", ROUTEUR_PORT))
routeur.listen()

#quand un routeur ou un cleint contacte
conn, addr = routeur.accept()

#lancer un thread pour ne pas bloquer
threading.Thread(target=traiter_connexion, args=(conn,)).start()

# !!!! le message est en binaire faire les conversion avant et apprés pour respecter les condition.

#[TAILLE_DONNEES][DONNEES_CHIFFREES]

#décomposer dans une fonction le paquet receptionné

def conteneurisation

print (3.50+3.50+3.50+3.50+1.50+3.50+3.50+3.50+1.50+1.50+3.50+1.50+1.50+0.25+0.25+0.25+0.25+0.25)