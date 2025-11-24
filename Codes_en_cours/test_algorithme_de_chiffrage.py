from sympy import randprime, mod_inverse
import random
def generation_nb_premier():
    """
    La fonction permet de générer quatre nombres premiers au hasard compris entre 1.000 et 100.000,
    ils sont rangés dans un set "nbr"(ligne 1). Puis est choisie au hasard l'élément de la liste.
    La fonction secrets.choice permet une meilleure protection que random.
    Il faut néanmoins traduire le set en tuple pour pouvoir le lire.
    :retourn : nombre premier tiré au hasard
    """
    nbr = {randprime(1000, 100000) for _ in range(4)}
    return random.choice(tuple(nbr))

def création_clés(p = generation_nb_premier(), q = generation_nb_premier()):
    """
    Algorithme de création des clés de chiffrement publique et privée (RSA).
    Utilisation de la valeur 65537 en exposant de chiffrement publique
    :return: clé_publique et clé_privée sous forme de set (dans l'odre {n,e} et {n,d})
    """
    e = 65537 #exposant de chiffrement publique

    n = p*q # modulo de p et q
    phi_n = (p-1)*(q-1) #calcul de phi(n)

    d = mod_inverse(e, phi_n)
    clé_publique = {n,e}
    clé_privée = {n,d}
    return clé_publique, clé_privée

def chiffrement()

print(création_clés())

