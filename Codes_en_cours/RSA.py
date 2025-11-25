from sympy import randprime, mod_inverse
import random

class RSA:
    def __init__(self):
        self.p = self.generation_nb_premier()
        self.q = self.generation_nb_premier()
        self.e = 65537
        self.n = self.p * self.q
        self.phi_n = (self.p - 1) * (self.q - 1)
        self.d = mod_inverse(self.e, self.phi_n)
        self.cle_publique = (self.n, self.e)
        self.cle_privee = (self.n, self.d)

    def generation_nb_premier(self):
        nbr = {randprime(1000, 100000) for _ in range(4)}
        return random.choice(tuple(nbr))

    def demande_cles(self, demande:str):
        if not isinstance(demande, str):
            raise TypeError("La valeur de 'demande' doit être une chaîne de caractères.")
        if demande not in ("publique", "privee"):
            raise ValueError("La valeur de 'demande' doit être 'publique' ou 'privee'.")
        else:
            if demande == "publique":
                return self.cle_publique
            elif demande == "privee":
                return self.cle_privee

class DB:
    def __init__(self):
        self.cle_publique = None
        self.cle_privee = None

    def enregistrement(self):
        self.cle_publique = RSA().demande_cles("publique")
        self.cle_privee = RSA().demande_cles("privee")

