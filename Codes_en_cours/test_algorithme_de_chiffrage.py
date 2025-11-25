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

def creation_cles(demande:str, p = generation_nb_premier(), q = generation_nb_premier()):
    """
    Algorithme de création des clés de chiffrement publique et privée (RSA).
    Utilisation de la valeur 65537 en exposant de chiffrement publique
    :return: clé_publique et clé_privée sous forme de tuple (dans l'odre (n,e) et (n,d))
    """
    if not isinstance(demande, str):
        raise TypeError("La valeur de 'demande' doit être une chaîne de caractères.")
    if demande not in ("publique", "privée"):
        raise ValueError("La valeur de 'demande' doit être 'publique' ou 'privee'.")
    else:
        e = 65537 #exposant de chiffrement publique
        n = p*q # modulo de p et q
        phi_n = (p-1)*(q-1) #calcul de phi(n)
        d = mod_inverse(e, phi_n)
        cle_publique = (n,e)
        cle_privee = (n,d)
        if demande == "publique":
            return cle_publique
        if demande == "privee":
            return cle_privee

def chiffrement(message):
    """
    cle_publique récupére le tuple qui contient n et e
    :param message: message à crypter
    :return: message crypté
    """
    cle_publique = creation_cles("publique")
    m = int.from_bytes(message.encode(), byteorder='big')# Conversion en entier
    return pow(m, cle_publique[0], cle_publique[1])# RSA : c = m^e mod n

def dechiffrement(message):
    """
    cle_privee récupére le tuple qui contient n et d
    :param message: message à decripter
    :return: message décripté
    """
    cle_privee = creation_cles("privee")
    m = pow(message, cle_privee[0], cle_privee[1]) # RSA : m = c^d mod n
    length = (m.bit_length() + 7) // 8 # Convertir l'entier en texte // peut être dans la ligne en dessous mais trop long
    return m.to_bytes(length, byteorder='big').decode()

print(chiffrement())

if __name__ == "main":
    print(chiffrement())
