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


def conteneurisation(message: list):
    return message


class DB:
    """
    Création d'une class DB pour 'simmuler' al base de donnée à ajouter plsu tard
    """
    def __init__(self):
        self.cle = RSA().demande_cles()
        self.cle_publique = self.cle[0]
        self.cle_privee = self.cle[1]


if __name__ == "__main__":
    nb = int(input("choisir entre test 1 et test 2"))
    if nb == 1:
        # Test 1 : Chiffrement et déchiffrement d'un texte
        db = DB()
        #il est nécessaire de crée un objet db pour éviter de recharger des clé et d'avoir une incompatibilité de la clé privée avec la clé publique
        texte = "test RSA"
        print("texte original :", texte)

        texte_chiffre = Action(texte,db).chiffrement()
        print("texte chiffré :", texte_chiffre)

        texte_dechiffre = Action(texte_chiffre,db).dechiffrement()
        print("texte déchiffré :", texte_dechiffre)
    elif nb == 2:
        #Test 2: Chiffrement et dechiffrement d'un text trop long (doit générer une erreur)
        db = DB()
        texte = "test RSA pour un message trop long: Le chiffrement RSA est un algorithme de cryptographie asymétrique, très utilisé dans le commerce électronique, et plus généralement pour échanger des données confidentielles sur Internet. Cet algorithme a été décrit en 1977 par Ronald Rivest, Adi Shamir et Leonard Adleman. RSA a été breveté par le Massachusetts Institute of Technology en 1983 aux États-Unis. Le brevet a expiré le 21 septembre 2000. "
        print("texte original :", texte)

        texte_chiffre = Action(texte, db).chiffrement()
        print("texte chiffré :", texte_chiffre)

        texte_dechiffre = Action(texte_chiffre, db).dechiffrement()
        print("texte déchiffré :", texte_dechiffre)
    else:
        print(f"il n'y a pas de test correspondant au nombre {nb}")