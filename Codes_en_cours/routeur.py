"""
"
Socket, Thread, QT et MariaDB
Déchiffrement d'une seul couche
"
"
envoiyer son @ip
envoi le port d'écoute
envoie la clé publique

le routeur doit écouter sur un port fixe
chaque message reçu = thread dédié
(voir aide chat-gpt)


Ecouter les port et accpter les connexions

importer le système de cryptage comme une librairie
"

# [id de l'action][CLE_PUBLIQUE][PORT][@ip]
                            "
                            il faut crée plusieurs actions qui se suivent
                            "
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
"""
from key import RSA
from action_key import Action

class DB:
    """
    Class pour stocker les informations comme les clés et éviter par erreur d'en regénérer
    """
    def __init__(self):
        #création des clés
        self.cle = RSA().demande_cles()
        self.cle_publique = self.cle[0]
        self.cle_privee = self.cle[1]


class routeur(DB):
    def __init__(self,message:str):
        #héritage
        super().__init__()
        #message
        if not isinstance(message, str):
            raise TypeError("le message doit être une une chaîne de caractères")
        self.message = message
        self.liste = []

    def conteneurisation(self):
        """
        Cette fonction devra permettre de conteneuriser le message et de le crypter
        :return: le return sera en binaire (fonction b"")
        """

        self.liste = (Action(self.message, DB()).chiffrement()) #Action(self.message, DB()).chiffrement(), Action(self.cle_publique, DB()).chiffrement()
        print(Action(self.message, DB()).chiffrement(), )
        return self.liste

    def deconteneurisation(self, message):
        """
        Cette fonction devra permettre de déconteneuriser le message et de le déchiffrer
        :return: le return sera en clair (lecture humaine)
        """
        #réception d'un message
        m = Action(message,DB).dechiffrement()
        return

if __name__ == "__main__":
    # il est nécessaire de créer un objet db pour éviter de recharger des clés et d'avoir une incompatibilité de la clé privée avec la clé publique
    message = "test RSA"
    print("message original :", message)

    message_chiffre = routeur(message).conteneurisation()
    print("message chiffré :", message_chiffre)
    """
    message_dechiffre = routeur(message_chiffre).deconteneurisation()
    print("message déchiffré :", message_dechiffre)
    """
