#!/usr/bin/env python3                         # Indique l'utilisation de Python 3
# coding: utf-8                                # Encodage UTF-8 pour les caractères français

import socket                                  # Module pour la communication réseau (TCP)
import threading                               # Module pour gérer plusieurs connexions en parallèle
import random                                  # Module pour la sélection aléatoire

ADRESSE_SERVEUR = "127.0.0.1"                  # Adresse IP du serveur master
PORT_SERVEUR = 5000                            # Port d'écoute du serveur master

"""
***********************
Classe Routeur
***********************
"""

class Routeur:                                 # Classe représentant un routeur enregistré
    """Représente un routeur connu par le serveur master"""

    def __init__(self, identifiant: str, ip: str, port: int):  # Constructeur du routeur
        self.identifiant = identifiant          # Identifiant unique du routeur
        self.ip = ip                            # Adresse IP du routeur
        self.port = port                        # Port utilisé par le routeur

    def vers_texte(self) -> str:                # Convertit le routeur en chaîne de caractères
        return f"{self.identifiant},{self.ip},{self.port}"  # Format texte du routeur

"""
***********************
Classe Serveur/Master
***********************
"""

class ServeurMaster:                            # Classe principale du serveur master
    def __init__(self, adresse=ADRESSE_SERVEUR, port=PORT_SERVEUR):  # Constructeur
        self.adresse = adresse                  # Adresse IP du serveur
        self.port = port                        # Port du serveur

        self.routeurs = []                      # Liste des routeurs enregistrés
        self.verrou_routeurs = threading.Lock() # Verrou pour protéger l'accès concurrent

        self.socket_serveur = socket.socket(    # Création du socket serveur
            socket.AF_INET,                     # Utilisation d'IPv4
            socket.SOCK_STREAM                  # Utilisation du protocole TCP
        )

    def demarrer(self):                         # Démarre le serveur master
        self.socket_serveur.bind((self.adresse, self.port))  # Association IP / port
        self.socket_serveur.listen(10)           # Autorise jusqu'à 10 connexions simultanées
        print(f"[MASTER] Serveur démarré sur {self.adresse}:{self.port}")  # Message d'état

        try:
            while True:                          # Boucle infinie d'attente de connexions
                socket_client, adresse_client = self.socket_serveur.accept()  # Accepte un client
                print(f"[MASTER] Connexion reçue depuis {adresse_client}")     # Log connexion

                threading.Thread(                # Création d'un thread pour ce client
                    target=self.gestion_client,  # Fonction exécutée dans le thread
                    args=(socket_client, adresse_client),  # Paramètres
                    daemon=True                  # Thread lié au programme principal
                ).start()                        # Démarrage du thread

        finally:
            self.socket_serveur.close()           # Fermeture du socket serveur

    def gestion_client(self, socket_client: socket.socket, adresse_client):  # Gère un client
        try:
            message = self.lire_ligne(socket_client)  # Lecture du message du client

            if not message:                     # Si aucun message reçu
                return                          # Fin de la session

            print(f"[MASTER] Message reçu ({adresse_client}) : {message}")  # Affichage

            reponse = self.traiter_commande(message)  # Analyse de la commande

            if reponse:                         # Si une réponse existe
                self.envoyer_ligne(socket_client, reponse)  # Envoi au client

        except Exception as erreur:              # Gestion des erreurs
            print(f"[MASTER][ERREUR] {adresse_client} -> {erreur}")  # Log erreur

        finally:
            socket_client.close()                # Fermeture de la connexion
            print(f"[MASTER] Connexion fermée avec {adresse_client}")  # Log fermeture

    def lire_ligne(self, sock: socket.socket) -> str | None:  # Lecture ligne par ligne
        tampon = bytearray()                     # Tampon de réception

        while True:
            octet = sock.recv(1)                 # Lecture d'un octet

            if not octet:                        # Si la connexion est fermée
                return None if not tampon else tampon.decode()  # Retour des données

            if octet == b'\n':                   # Fin de ligne détectée
                break                            # Sortie de la boucle

            tampon.extend(octet)                 # Ajout de l'octet au tampon

        return tampon.decode()                   # Conversion en chaîne UTF-8

    def envoyer_ligne(self, sock: socket.socket, texte: str):  # Envoi d'une ligne
        sock.sendall((texte + "\n").encode())    # Envoi du message avec saut de ligne

    def traiter_commande(self, ligne: str) -> str:  # Analyse de la commande reçue
        morceaux = ligne.strip().split(";")      # Découpage selon le protocole

        if not morceaux:                         # Message vide
            return "ERROR;MESSAGE_VIDE"          # Erreur

        commande = morceaux[0].upper()           # Commande principale

        match commande:                          # Analyse de la commande
            case "ROUTER_REGISTER":              # Enregistrement d'un routeur
                return self.enregistrer_routeur(morceaux)

            case "CLIENT_GET_PATH":              # Demande de chemin
                return self.generer_chemin(morceaux)

            case _:                              # Commande inconnue
                return "ERROR;COMMANDE_INCONNUE"

    def enregistrer_routeur(self, donnees: list[str]) -> str:  # Ajout / mise à jour routeur
        if len(donnees) != 4:                    # Vérification du format
            return "ERROR;FORMAT_ROUTEUR"

        _, identifiant, ip, port_texte = donnees # Extraction des champs

        try:
            port = int(port_texte)               # Conversion du port
        except ValueError:
            return "ERROR;PORT_INVALIDE"         # Erreur si conversion impossible

        with self.verrou_routeurs:               # Accès sécurisé à la liste
            for routeur in self.routeurs:        # Recherche d'un routeur existant
                if routeur.identifiant == identifiant:
                    routeur.ip = ip              # Mise à jour IP
                    routeur.port = port          # Mise à jour port
                    return f"OK;REGISTERED;{identifiant}"

            self.routeurs.append(Routeur(identifiant, ip, port))  # Ajout nouveau routeur

        return f"OK;REGISTERED;{identifiant}"    # Confirmation

    def generer_chemin(self, donnees: list[str]) -> str:  # Génération du chemin
        if len(donnees) != 2:                    # Vérification du format
            return "ERROR;FORMAT_CHEMIN"

        try:
            nombre_sauts = int(donnees[1])       # Nombre de routeurs demandés
            if nombre_sauts <= 0:
                raise ValueError
        except ValueError:
            return "ERROR;NB_SAUTS_INVALIDE"     # Valeur incorrecte

        with self.verrou_routeurs:               # Accès sécurisé
            if len(self.routeurs) < nombre_sauts:
                return "ERROR;PAS_ASSEZ_DE_ROUTEURS"

            selection = random.sample(self.routeurs, nombre_sauts)  # Sélection aléatoire

        chemin = "|".join(r.vers_texte() for r in selection)  # Construction du chemin
        return f"PATH;{chemin}"                 # Retour au client

"""
***********************
Lancement programmes
***********************
"""

if __name__ == "__main__":                      # Point d'entrée du programme
    serveur = ServeurMaster()                  # Création du serveur master
    serveur.demarrer()                         # Démarrage du serveur

#python3 masterX.py = permet de lancer le master en fonction du choix du programme