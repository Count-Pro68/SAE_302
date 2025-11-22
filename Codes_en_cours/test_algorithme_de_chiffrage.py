from sympy import randprime
import secrets
def generation_nb_premier():
    """
    La fonction permet de générer quatre nombres premiers au hasard compris entre 1.000 et 100.000,
    ils sont rangés dans un set "nbr"(ligne 1). Puis est choisie au hasard l'élément de la liste.
    La fonction secrets.choice permet une meilleure protection que random.
    Il faut néanmoins traduire le set en tuple pour pouvoir le lire.
    :retourn : nombre premier tiré au hasard
    """
    nbr = {randprime(1000, 100000) for _ in range(4)}
    return secrets.choice(tuple(nbr))
print(generation_nb_premier())

def création_clé():
    p=generation_nb_premier()
    q=generation_nb_premier()
    e=65537

