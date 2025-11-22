from sympy import randprime
import secrets
def generation_nb_premier():
    """
    la fonction permet de générer quatre nombres premier au hasard compris entre 1.000 et 100.000,
    ils sont rangés dans une liste ""liste"("(ligne 1). Puis est choisie au hasard l'élement de la liste.
    :return: nombre premier tiré au hasard
    """
    liste = [randprime(1000, 100000) for _ in range(4)]
    return secrets.choice(liste)

