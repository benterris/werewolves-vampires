import sys
from config import *

def main(args):
    """Let's go"""
    # 0. Lire les arguments
    if len(args) >= 3:
        server_ip = args[-2]
        server_port = args[-1]



    # 2. Etablir la connexion avec le serveur

    # 3. Envoyer les infos au serveur

    # 4. Recevoir les infos de map du serveur

    # 5. Si pas notre tour, attendre le coup de l'autre

    fini = True
    while not fini:

        # Lancer la recherche de meilleur coup

        # Envoyer notre coup au serveur

        # Attendre l'information du serveur avec le tour de l'adversaire

        pass

    print("Fini !")
    return


if __name__ == "__main__":
    main(sys.argv)
