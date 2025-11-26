from sympy import randprime, mod_inverse
import random

class RSA:
    """
    class qui regroupe l'ensemble des fonction qui crée les clé publique et privée.
    """
    def __init__(self):
        self.p = self.generation_nb_premier()
        self.q = self.generation_nb_premier()
        while self.q == self.p:  # Assure que p et q sont distincts
            self.q = self.generation_nb_premier()
        self.e = 65537 # exposant de chiffrement (ici il s'agit de la valeur publique our le RSA)
        self.n = self.p * self.q #modulo de p et q
        self.phi_n = (self.p - 1) * (self.q - 1)
        self.d = mod_inverse(self.e, self.phi_n) #modulo inversé
        self.cle_publique = (self.n, self.e)
        self.cle_privee = (self.n, self.d)

    def generation_nb_premier(self):
        """
        génération de quatre nombres premier compris entre les valeur a et b, ici 2^200 et 2^201
        :return: un des 4 nombre sélectionné
        """
        nbr = {randprime(2**200, 2**201) for _ in range(4)}
        return random.choice(tuple(nbr))

    def demande_cles(self):
        """
        pour répondre à une demande de clés
        :return: renvoie les clés publique et privée dans une même liste
        """
        cles = (self.cle_publique, self.cle_privee)
        return cles

class DB:
    """
    Création d'une class DB pour 'simmuler' al base de donnée à ajouter plsu tard
    """
    def __init__(self):
        self.cle = RSA().demande_cles()
        self.cle_publique = self.cle[0]
        self.cle_privee = self.cle[1]

class Action:
    """
    class qui permet le chiffrage et le dechiffrage, les actions basé sur les clés
    """
    def __init__(self,texte:str,db):
        self.cle_publique = db.cle_publique
        self.cle_privee = db.cle_privee
        if not isinstance(texte, (str, int)):
            raise TypeError("La valeur de 'texte' doit être une chaîne de caractères ou une suite numerique")
        self.texte = texte

    def chiffrement(self):
        """
        cle_publique récupére le tuple qui contient n et e
        :param texte: texte à crypter
        :return: texte crypté
        """
        m = int.from_bytes(self.texte.encode(), byteorder='big')# Conversion en entier
        n = self.cle_publique[0]
        if m > n:
            raise ValueError(f"Le texte est trop long pour être chiffré avec cette clé (taille max : {n}).")
        return pow(m, self.cle_publique[1], self.cle_publique[0])# RSA : c = m^e mod n

    def dechiffrement(self):
        """
        cle_privee récupére le tuple qui contient n et d
        :param message: message à decripter
        :return: message décripté
        """
        m = pow(self.texte, self.cle_privee[1], self.cle_privee[0]) # RSA : m = c^d mod n
        length = (self.cle_privee[0].bit_length() + 7) // 8 # Convertir l'entier en texte // peut être dans la ligne en dessous mais trop long
        return m.to_bytes(length, byteorder='big').decode()

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
