from sympy import randprime, mod_inverse
import random

class RSA:
    """
    class qui regroupe l'ensemble des fonctions qui crée les clés publique et privée.
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
        génération de quatre nombres premiers compris entre les valeurs a et b, ici 2^200 et 2^201
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