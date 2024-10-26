from Interface.csts import *
from Interface.Pioche import *
from Interface.Tuile import *
from Interface.Set import *
from Interface.Joueur import *
from Interface.Table import *

import numpy as np

class Partie :
    """
    Classe Partie :
    Attributs :
        - joueurs : liste de Joueurs
        - nb_manches : int
        - manche : int
        - pioche : Pioche
        - time : float
    Methodes :
        - __init__() : création de la partie
        - start_manche() : Lance une manche et gère toutes les actions des joueurs
        - end_manche() : fin de la manche
        - distribuer() : donne les tuiles à chaque joueur en début de partie
        - piocher() : appelle la fonction piocher d'un joueur
        - poser() : appeller la fonction poser de la table de jeu
    """
    def __init__(self, lst_noms:list, nb_manches:int) :
        """
        Création de la partie
        """
        self.joueurs = []
        # création des joueurs
        for i in range(len(lst_noms)) :
            nom = lst_noms[i]
            self.joueurs.append(Joueur(nom))
        # initialisation des paramètres de jeu
        self.nb_manches = nb_manches
        self.pioche = Pioche()
        self.time = 0.   
        self.table = Table()
        # déroulement des manches
        for m in range(nb_manches) :
            self.manche = m
            self.start_manche()

    def start_manche(self) :
        """
        Gestion des actions au long d'une manche
        """
        self.distribuer()
        gagnant = False
        while not gagnant :
            for j in self.joueurs :
                print(j)
                # Copie des informtaions de jeu 
                j_virtuel = j.copy()
                table_virtuel = self.table.copy().table
                choice = []
                validity = True
                
                # choix dans la main du joueur
                set_choice = input("Tuiles à sélectionner dans la Main : ")
                if set_choice != '' :
                    for i in set_choice.split('-') :
                        choice.append(j_virtuel.main[int(i)-1])
                        j_virtuel.main[int(i)-1] = None
                    j_virtuel.nettoyer_main()

                # vérification du nombre tour  
                if j.num_tour != 0 :
                    # ajouter des tuiles provantn de la table
                    table_set_choice = input("Sets à sélectionner sur la Table : ")
                    if table_set_choice != '' :
                        for i in table_set_choice.split('-') :
                            table_set = table_virtuel[int(i)-1]
                            print(table_set)
                            table_choice = input("Tuiles à sélectionner dans le Set : ")
                            if table_choice != '' :
                                for x in table_choice.split('-') :
                                    choice.append(table_set.set[int(x)-1])
                                    table_set.enleve_tuile(int(x)-1)
                    # Compléter des sets de la table avec des tuiles de la main directement
                    return_choice = input("Compléter des sets de la table ? o/n : ")
                    while return_choice not in ['', 'n', 'N'] :
                        return_choice = input("Tuile de la main à reposer dans un autre set : ")
                        return_set_destination = input('Set de la table à compléter : ')
                        if return_choice != '' and return_set_destination != '' :
                            table_virtuel[int(return_set_destination)-1].ajoute_tuile(j_virtuel.main[int(return_choice)-1])
                            if table_virtuel[int(return_set_destination)-1].nature == 'not a set' : 
                                validity = False
                # vérification des actions
                final_choice = Set(choice)
                print("FINAL CHOICE : ",final_choice)
                if final_choice.nature != 'not a set' :
                    for table_set in table_virtuel :
                        table_set.check_set()
                        if table_set.nature == 'not a set' :
                            validity = False
                else :
                    validity = False

                if final_choice.valeur_set() < 30 and j.num_tour == 0 :
                    validity = False

                if validity : # si la validité est respectée, le jeu est mis à jour avec les modifications
                    j.main = j_virtuel.main
                    self.table.table = table_virtuel
                    self.table.table.append(final_choice)
                    j.num_tour += 1
                else : # sinon on fait simplement piocher le joueur
                    j.tirer(1, self.pioche)
                

                print("VALIDITY : ", validity)

                print(j)
                print(self.table)

                if len(j.main) == 0 :
                    gagnant = True
                    print(f"FIN DE LA MANCHE !! {j.nom} a gagné")
                    self.end_manche()

                else :
                    print("\n\n -- CHANGEMENT DE JOUEUR -- \n\n")

    def end_manche(self) :
        """
        Gestion de la fin de manche
        """
        # MAJ des scores des joueurs
        for j in self.joueurs :
            j.maj_score()
        # réinitialisation des éléments de jeu
        self.pioche = Pioche()
        self.time = 0.
        self.table = Table()

        # Continer sur une nouvelle manche
        continuer = input("Voulez-vous refaire une manche ? o/n : ")
        if continuer in ['o','O'] :
            self.start_manche()

    def distribuer(self) :
        """
        Distribution des tuiles aux joueurs
        """
        for t in range(14) :
            for j in self.joueurs :
                j.tirer(1, self.pioche)
        j.sort()

    def piocher(self, joueur) :
        """
        Fais piocher un joueur
        """
        joueur.tirer(1, self.pioche)
    
    def poser(self, set) :
        """
        Pose un set sur la table
        """
        self.table.poser(set)