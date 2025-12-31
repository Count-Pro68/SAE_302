#!/usr/bin/env python3                 # Interpréteur Python
# -*- coding: utf-8 -*-                 # Encodage UTF-8

import socket                           # Module pour la communication réseau
import threading                        # Module pour le multithreading
from key import RSA                     # Module pour le chiffrement
from action_key import Action           # ''

class DB:
    """
    Class pour stocker les informations comme les clés et éviter par erreur d'en régénérer
    """
    def __init__(self):
        #création des clés
        self.cle_publique, self.cle_privee = RSA().demande_cles()


class NoeudIntermediaire(DB):               # Routeur renommé
    def __init__(self, nom, ip_locale, port_locale, ip_master, port_master):
        #héritage
        super().__init__()
        self.nom = nom                   # Nom ou ID du routeur
        self.ip = ip_locale              # IP du routeur
        self.port = port_locale          # Port du routeur
        self.master_ip = ip_master       # IP du serveur master
        self.master_port = port_master   # Port du master

        self.sock_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Création socket TCP
        self.sock_serveur.bind((self.ip, self.port))  # Bind IP et port
        self.sock_serveur.listen(5)                     # Mise en écoute

    # --------------------------------------------------
    # outils pour les sockets
    # --------------------------------------------------
    def ecrire_ligne(self, s, texte):
        if not texte.endswith("\n"):            # Ajoute \n si nécessaire
            texte += "\n"
        s.sendall(texte.encode("utf-8"))        # Envoi du texte encodé

    def lire_ligne(self, s):
        buffer = []                             # Liste pour accumuler les octets
        while True:                             # Boucle jusqu’à \n ou fermeture
            octet = s.recv(1)                   # Lecture octet par octet
            if not octet:                        # Si socket fermé
                return None if not buffer else "".join(buffer)  # Retourne None ou le message
            if octet == b"\n":                  # Fin de ligne détectée
                break
            buffer.append(octet.decode())       # Ajoute l’octet décodé
        return "".join(buffer)                  # Retourne la ligne complète

    # --------------------------------------------------
    # Enregistrements  au master
    # --------------------------------------------------
    def inscription_master(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket temporaire
            s.connect((self.master_ip, self.master_port))          # Connexion au master

            message = f"ROUTER_REGISTER;{self.nom};{self.ip};{self.port}"  # Message d’enregistrement
            self.ecrire_ligne(s, message)                             # Envoi du message

            resp = self.lire_ligne(s)                                 # Lecture de la réponse
            print(f"[{self.nom}] Master a répondu : {resp}")          # Affichage

            s.close()                                                 # Fermeture du socket
        except Exception as e:
            print(f"[{self.nom}] Erreur inscription : {e}")           # Gestion erreur

    # --------------------------------------------------
    # Boucle d'écoute
    # --------------------------------------------------
    def boucle_ecoute(self):
        print(f"[{self.nom}] Routeur actif sur {self.ip}:{self.port}")  # Message état
        continuer = True
        while continuer:                                # Boucle principale
            connexion, origine = self.sock_serveur.accept()  # Accepte nouvelle connexion
            t = threading.Thread(
                target=self.traiter_connexion,          # Fonction de traitement
                args=(connexion, origine)              # Arguments
            )
            t.daemon = True                             # Thread daemon
            t.start()                                   # Démarrage thread

    def traiter_connexion(self, sock, origine):
        try:
            msg = self.lire_ligne(sock)                # Lecture message
            if not msg:                                # Si vide
                return
            print(f"[{self.nom}] Message reçu : {msg}")  # Affichage

            elements = msg.split(";", 3)               # Découpe max 4 parties
            cmd = elements[0].upper()                  # Commande en majuscules

            if cmd == "NEXT":                           # Commande intermédiaire
                if len(elements) != 4:                 # Vérification format
                    print(f"[{self.nom}] NEXT mal formé")
                    return

                _, ip_suivant, port_suivant, data = elements  # Extraction info

                if ip_suivant.upper() == "NONE":       # Dernier routeur logique
                    print(f"[{self.nom}] Dernier routeur → DATA = {data}")
                    return

                print(f"[{self.nom}] Transfert vers {ip_suivant}:{port_suivant}")
                self.transmettre(ip_suivant, int(port_suivant), data)  # Renvoi

            elif cmd == "DELIVER":                      # Commande finale
                if len(elements) != 4:                 # Vérification format
                    print(f"[{self.nom}] DELIVER mal formé")
                    return
                _, ip_client, port_client, data_final = elements  # Extraction infos
                print(f"[{self.nom}] Livraison finale au client {ip_client}:{port_client}")
                self.transmettre(ip_client, int(port_client), data_final)  # Envoi

            else:                                       # Commande inconnue
                print(f"[{self.nom}] Commande inconnue : {cmd}")

        except Exception as e:
            print(f"[{self.nom}] Erreur traitement message : {e}")   # Gestion erreur
        finally:
            sock.close()                                       # Fermeture socket

    # --------------------------------------------------
    # Transmission
    # --------------------------------------------------
    def transmettre(self, ip, port, data):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Nouveau socket
            s.connect((ip, port))                                   # Connexion
            if not data.endswith("\n"):                              # Ajout \n si absent
                data += "\n"
            s.sendall(data.encode("utf-8"))                          # Envoi du message
            s.close()                                                # Fermeture socket
        except Exception as e:
            print(f"[{self.nom}] Impossible de joindre {ip}:{port} → {e}")  # Erreur

    # --------------------------------------------------
    # Démarrage
    # --------------------------------------------------
    def demarrer(self):
        self.inscription_master()             # Inscription au master
        th = threading.Thread(target=self.boucle_ecoute, daemon=True)  # Thread écoute
        th.start()                            # Lancement du thread
        print(f"[{self.nom}] Routeur prêt.")  # Message
        threading.Event().wait()              # Maintient le programme actif


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    ROUTEUR_ID = "R1"                  # Nom du routeur
    ROUTEUR_IP = "127.0.0.1"           # IP locale
    ROUTEUR_PORT = 5001                # Port d’écoute (différent entre chaque routeurs)
    MASTER_IP = "127.0.0.1"            # IP master
    MASTER_PORT = 5000                 # Port master

    routeur = NoeudIntermediaire(      # Création instance routeur
        nom=ROUTEUR_ID,
        ip_locale=ROUTEUR_IP,
        port_locale=ROUTEUR_PORT,
        ip_master=MASTER_IP,
        port_master=MASTER_PORT
    )

    routeur.demarrer()                  # Lancement du routeur

#python3 routeurX.py = permet de lancer un routeur en fonction du choix du programme
