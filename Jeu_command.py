from Interface.csts import * # Constantes du jeu
from Interface.Pioche import * # Pile de tuiles de départ
from Interface.Tuile import * # Défintion d'une tuile
from Interface.Set import * # Un groupe de tuile respectant des règles particulières
from Interface.Joueur import * # Un joueur de la partie
from Interface.Table import * # Support des Sets posés par les joueurs

from Interface.Partie_command import * # Module qui gère la partie et les interactions

import Interface.csts as csts
import numpy as np

def main():
    """
    Initialisation d'une partie
    """
    noms = []
    nom = input("Entrez le nom du premier joueur : ")
    noms = [nom]
    while nom != '' :
        nom = input("Entrez le nom du joueur suivant : ")
        noms.append(nom)

    partie = Partie(noms, 2)

if __name__ == "__main__":
    main()

    

