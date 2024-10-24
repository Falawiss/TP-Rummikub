from Classes.csts import *
from Classes.Pioche import *
from Classes.Tuile import *
from Classes.Set import *
from Classes.Joueur import *
from Classes.Table import *

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
        self.joueurs = []

        for i in range(len(lst_noms)) :
            nom = lst_noms[i]
            self.joueurs.append(Joueur(nom))

        self.nb_manches = nb_manches
        self.pioche = Pioche()
        self.time = 0.   
        self.table = Table()

        for m in range(nb_manches) :
            self.manche = m
            self.start_manche()


    def start_manche(self) :
        self.distribuer()
        gagnant = False
        while not gagnant :
            for j in self.joueurs :
                print(j)

                j_virtuel = j.copy()
                table_virtuel = self.table.copy()
                choice = []
                

                set_choice = input("Tuiles à sélectionner dans la Main : ")
                if set_choice != '' :
                    for i in set_choice.split('-') :
                        choice.append(j_virtuel.main[int(i)-1])
                        j_virtuel.main[int(i)-1] = None
                    j_virtuel.nettoyer_main()


                if j.num_tour != 0 :
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
                    
                    return_choice = input("Compléter des sets de la table ? o/n : ")
                    while return_choice not in ['', 'n', 'N'] :
                        return_choice = input("Tuile de la main à reposer dans un autre set : ")
                        return_set_destination = input('Set de la table à compléter : ')
                        if return_choice != '' and return_set_destination != '' :
                            table_virtuel[int(return_set_destination-1)].ajoute_tuile(j_virtuel.main[int(return_choice)])
                
                final_choice = Set(choice)
                print("FINAL CHOICE : ",final_choice)
                validity = True
                if final_choice.nature != 'not a set' :
                    for table_set in table_virtuel :
                        table_set.check_set()
                        if table_set.nature == 'not a set' :
                            validity = False
                else :
                    validity = False

                if final_choice.valeur_set() < 3 and j.num_tour == 0 :
                    validity = False

                if validity :
                    j.main = j_virtuel.main
                    self.table.table = table_virtuel
                    self.table.table.append(final_choice)
                    j.num_tour += 1
                else :
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
        for j in self.joueur :
            j.maj_score()
        self.pioche = Pioche()
        self.time = 0.
        self.table = Table()

        continuer = input("Voulez-vous refaire une manche ? o/n : ")
        if continuer in ['o','O'] :
            self.start_manche()

    def distribuer(self) :
        for t in range(14) :
            for j in self.joueurs :
                j.tirer(1, self.pioche)

    def piocher(self, joueur) :
        joueur.tirer(1, self.pioche)
    
    def poser(self, set) :
        self.table.poser(set)