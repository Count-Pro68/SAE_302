from key import RSA
from action_key import Action
from routeur import routeur

if __name__ == "__main__":
    print("Test n°0: test du fonctionnement du fichier Key ;")
    print("Test n°1: test du fonctionnement du fichier action_key et routeur;")
    print("Test n°2: test du fonctionnement du fichier action_key et routeur (Db)")
    print()
    try:
        nb = int(input("Choisir un test, (uniquement la valeur numérique)"))
    except TypeError:
        print("Il faut saisir une valeur numérique ex:0 ou 1")
    if nb == 0:
        print(RSA().demande_cles())
    elif nb == 1:
        # Test 1 : Chiffrement et déchiffrement d'un texte
        db = routeur()
        #il est nécessaire de crée un objet db pour éviter de recharger des clé et d'avoir une incompatibilité de la clé privée avec la clé publique
        texte = "test RSA"
        print("texte original :", texte)

        texte_chiffre = Action(texte,db).chiffrement()
        print("texte chiffré :", texte_chiffre)

        texte_dechiffre = Action(texte_chiffre,db).dechiffrement()
        print("texte déchiffré :", texte_dechiffre)
    elif nb == 2:
        #Test 2: Chiffrement et dechiffrement d'un text trop long (doit générer une erreur)
        db = routeur()
        texte = "test RSA pour un message trop long: Le chiffrement RSA est un algorithme de cryptographie asymétrique, très utilisé dans le commerce électronique, et plus généralement pour échanger des données confidentielles sur Internet. Cet algorithme a été décrit en 1977 par Ronald Rivest, Adi Shamir et Leonard Adleman. RSA a été breveté par le Massachusetts Institute of Technology en 1983 aux États-Unis. Le brevet a expiré le 21 septembre 2000. "
        print("texte original :", texte)

        texte_chiffre = Action(texte, db).chiffrement()
        print("texte chiffré :", texte_chiffre)

        texte_dechiffre = Action(texte_chiffre, db).dechiffrement()
        print("texte déchiffré :", texte_dechiffre)
    else:
        print(f"il n'y a pas de test correspondant au nombre {nb}")