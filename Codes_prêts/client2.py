#!/usr/bin/env python3                     # Indique au système quel interpréteur Python utiliser
# -*- coding: utf-8 -*-                     # Encodage UTF-8 pour gérer les caractères accentués

"""
Code identique au premier client
"""

import socket                               # Module pour la communication réseau
import threading                            # Module pour gérer le multithreading


class TerminalClient:                      # Définition de la classe du client
    def __init__(self, nom, ip, port, master_ip, master_port, sauts_defaut):  # Constructeur
        self.nom = nom                     # Nom du client (ex: A ou B)
        self.ip = ip                       # Adresse IP du client
        self.port = port                   # Port d’écoute du client
        self.master_ip = master_ip         # Adresse IP du master
        self.master_port = master_port     # Port du master
        self.sauts_defaut = sauts_defaut   # Nombre de routeurs par défaut

        self.socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Création du socket TCP
        self.socket_ecoute.bind((self.ip, self.port))                            # Association IP/port
        self.socket_ecoute.listen(1)                                              # Mise en écoute du socket

    # --------------------------------------------------
    # Outils pour les sockets
    # --------------------------------------------------

    def envoyer_ligne(self, s, contenu):    # Fonction pour envoyer une ligne texte
        data = contenu if contenu.endswith("\n") else contenu + "\n"  # Ajoute \n si absent
        s.sendall(data.encode())            # Envoi des données encodées en UTF-8

    def lire_ligne(self, s):                # Fonction pour lire une ligne complète
        resultat = ""                       # Chaîne de caractères reçue
        fini = False                        # Indicateur de fin de ligne
        while not fini:                     # Boucle jusqu'à réception complète
            octet = s.recv(1)               # Lecture d’un octet depuis le socket
            if octet == b"":                # Si la connexion est fermée
                break                       # Sort de la boucle
            if octet == b"\n":              # Si fin de ligne détectée
                fini = True                 # On marque la fin
            else:
                resultat += octet.decode()  # Ajoute l’octet décodé à la chaîne
        return resultat if resultat else None  # Retourne le message ou None

    # --------------------------------------------------
    # Partie Serveur - Client
    # --------------------------------------------------

    def attendre_messages(self):            # Serveur local du client
        print(f"[{self.nom}] Client actif sur {self.ip}:{self.port}")  # Message d’état

        actif = True                        # Variable de contrôle
        while actif:                        # Boucle d’écoute permanente
            connexion, adresse = self.socket_ecoute.accept()  # Acceptation d’une connexion
            t = threading.Thread(           # Création d’un thread
                target=self.traiter_connexion,  # Fonction exécutée par le thread
                args=(connexion, adresse)       # Arguments transmis
            )
            t.daemon = True                # Thread en mode daemon
            t.start()                      # Démarrage du thread

    def traiter_connexion(self, s, origine):  # Traitement d’un message entrant
        contenu = None                     # Variable pour stocker le message
        try:
            contenu = self.lire_ligne(s)   # Lecture du message reçu
        except:
            pass                           # Ignore les erreurs
        finally:
            s.close()                      # Fermeture du socket

        if contenu:                        # Si un message valide est reçu
            print(f"[{self.nom}] Message reçu : {contenu}")  # Affichage


    # --------------------------------------------------
    # Contact Master
    # --------------------------------------------------

    def demander_chemin(self, sauts):       # Demande d’un chemin au master
        socket_tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket temporaire

        try:
            socket_tmp.connect((self.master_ip, self.master_port))      # Connexion au master
            self.envoyer_ligne(socket_tmp, f"CLIENT_GET_PATH;{sauts}")  # Envoi de la requête

            reponse = self.lire_ligne(socket_tmp)  # Lecture de la réponse
        finally:
            socket_tmp.close()              # Fermeture du socket

        if not reponse or "PATH;" not in reponse:  # Vérification de la réponse
            return []                       # Retourne une liste vide si erreur

        chaine = reponse.split("PATH;", 1)[1]  # Extraction du contenu utile
        blocs = chaine.split("|")              # Séparation des routeurs

        chemin = []                        # Liste finale du chemin
        index = 0                          # Index manuel
        while index < len(blocs):          # Boucle de traitement
            elements = blocs[index].split(",")  # Découpage des infos routeur
            chemin.append((elements[0], elements[1], int(elements[2])))  # Ajout au chemin
            index += 1                     # Incrémentation de l’index

        return chemin                      # Retourne le chemin complet


    # --------------------------------------------------
    # Construction du message
    # --------------------------------------------------

    def fabriquer_message(self, chemin, ip_final, port_final, texte):  # Construction du message
        enveloppe = f"DELIVER;{ip_final};{port_final};{texte}"          # Message final de base

        chemin_inverse = chemin[:]          # Copie du chemin
        chemin_inverse.reverse()            # Inversion du chemin

        for info in chemin_inverse[:-1]:    # Parcours sauf le premier routeur
            enveloppe = f"NEXT;{info[1]};{info[2]};{enveloppe}"  # Encapsulation

        return enveloppe                    # Retourne le message final


    # --------------------------------------------------
    # Envoi final
    # --------------------------------------------------

    def envoyer(self, ip_dest, port_dest, texte, sauts=None):  # Fonction d’envoi
        if sauts is None:                 # Si aucun nombre de sauts fourni
            sauts = self.sauts_defaut     # Utilise la valeur par défaut

        route = self.demander_chemin(sauts)  # Demande du chemin
        if len(route) == 0:               # Si aucun routeur disponible
            print("[CLIENT] Aucun routeur disponible")  # Message d’erreur
            return                         # Arrêt de la fonction

        paquet = self.fabriquer_message(route, ip_dest, port_dest, texte)  # Création du message

        premier = route[0]                # Sélection du premier routeur
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Nouveau socket
            s.connect((premier[1], premier[2]))                    # Connexion au routeur
            self.envoyer_ligne(s, paquet)                           # Envoi du message
        except Exception as e:
            print("[CLIENT] Erreur envoi", e)  # Gestion des erreurs
        finally:
            s.close()                      # Fermeture du socket


    # --------------------------------------------------
    # Lancement
    # --------------------------------------------------

    def lancer(self):                      # Démarrage global du client
        th = threading.Thread(target=self.attendre_messages)  # Thread serveur
        th.daemon = True                   # Mode daemon
        th.start()                         # Lancement du thread

        print(f"[{self.nom}] Prêt à envoyer")  # Message prêt

        actif = True                       # Boucle principale
        while actif:
            print("\nNouvelle transmission")  # Interface utilisateur
            ip = input("IP cible : ").strip()  # Saisie IP
            p = int(input("Port cible : ").strip())  # Saisie port
            texte = input("Message : ")  # Saisie message

            s = input("Sauts (vide = défaut) : ").strip()  # Saisie sauts
            sauts = int(s) if s.isdigit() else self.sauts_defaut  # Validation sauts

            self.envoyer(ip, p, texte, sauts)  # Envoi du message


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":                 # Point d’entrée du programme
    client = TerminalClient(               # Création du client
        nom="B",                           # Nom du client
        ip="127.0.0.1",                    # IP locale
        port=6001,                         # Port local (obligatoirement différent pour chaque client)
        master_ip="127.0.0.1",             # IP du master
        master_port=5000,                  # Port du master
        sauts_defaut=2                     # Nombre de routeurs par défaut
    )

    client.lancer()                        # Lancement du client "python3 clientX.py"

#python3 clientX.py = permet de lancer un client en fonction du choix du programme
