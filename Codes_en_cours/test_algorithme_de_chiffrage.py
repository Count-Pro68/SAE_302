from sympy import randprime
import secrets
def generation_nb_premier():
    """
    La fonction permet de générer quatre nombres premiers au hasard compris entre 1.000 et 100.000,
    Ils sont rangés dans une liste ""liste"("(ligne 1). Puis est choisie au hasard l'élément de la liste.
    La fonction secrets.choice permet une meilleure protection que random.
    :retourn : nombre premier tiré au hasard
    """
    liste = [randprime(1000, 100000) for _ in range(4)]
    return secrets.choice(liste)
print(generation_nb_premier())

