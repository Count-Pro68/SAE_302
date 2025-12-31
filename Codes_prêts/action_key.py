from sympy import randprime, mod_inverse

class Action:
    """
    class qui permet le chiffrage et le dechiffrage, les actions basés sur les clés
    """
    def __init__(self,texte:str,db):
        self.cle_publique = db.cle_publique
        self.cle_privee = db.cle_privee
        if not isinstance(texte, (str, int)):
            raise TypeError("La valeur de 'texte' doit être une chaîne de caractères ou une suite numerique")
        self.texte = texte

    def chiffrement(self):
        """
        cle_publique récupérer le tuple qui contient n et e
        :return: texte crypter
        """
        m = int.from_bytes(self.texte.encode(), byteorder='big')# Conversion en entier
        n = self.cle_publique[0]
        if m > n:
            raise ValueError(f"Le texte est trop long pour être chiffré avec cette clé (taille max : {n}).")
        return pow(m, self.cle_publique[1], self.cle_publique[0])# RSA : c = m^e mod n

    def dechiffrement(self):
        """
        cle_privee récupérer le tuple qui contient n et d
        :return: message décripter
        """
        m = pow(self.texte, self.cle_privee[1], self.cle_privee[0]) # RSA : m = c^d mod n
        length = (self.cle_privee[0].bit_length() + 7) // 8 # Convertir l'entier en texte // peut être dans la ligne en dessous mais trop long
        return m.to_bytes(length, byteorder='big').decode()