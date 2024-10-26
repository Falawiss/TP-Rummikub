from Interface.csts import * # Constantes du jeu
from Interface.Pioche import * # Pile de tuiles de départ
from Interface.Tuile import * # Défintion d'une tuile
from Interface.Set import * # Un groupe de tuile respectant des règles particulières
from Interface.Joueur import * # Un joueur de la partie
from Interface.Table import * # Support des Sets posés par les joueurs
from Interface.InputDialog import * # Fenêtre pour insérer les noms des joueurs

import numpy as np
from PyQt5.QtWidgets import *

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
        - start_manche() : Lance une manche, et prépre le premier tour
        - tour_suivant() : gère les actions à réaliser à chaque tour
        - end_manche() : fin de la manche
        - distribuer() : donne les tuiles à chaque joueur en début de partie
        - piocher() : appelle la fonction piocher d'un joueur
        - aff_tuiles() : affiche une liste de tuiles ou de sets dans un layout donné
        - maj_aff() : Mets à jour l'affichage de chaque zone (main, choix, table)
        - clear_layout() : efface tous les éléments d'un layout donné
        - move_tuile() : déplace une tuile d'un stockage vers un autre
        - validation_set() : valide le choix et l'ajoute à la table (si validé)
    """
    def __init__(self, lst_noms:list, global_layout, table_layout, main_layout, selec_layout) :
        self.joueurs = []

        for i in range(len(lst_noms)) :
            nom = lst_noms[i]
            self.joueurs.append(Joueur(nom))

        self.pioche = Pioche()
        self.time = 0.   
        self.table = Table()
        self.current_j = 0

        self.global_layout = global_layout
        self.table_layout = table_layout
        self.main_layout = main_layout
        self.selec_layout = selec_layout

        validation_button = QPushButton("Valider le Set")
        validation_button.clicked.connect(self.validation_set)
        global_layout.addWidget(validation_button,3,2)

        fintour_button = QPushButton("Fin du tour")
        fintour_button.clicked.connect(self.tour_suivant)
        global_layout.addWidget(fintour_button,4,2)

        self.aff_nom = QLabel("Joueur : ")
        self.global_layout.addWidget(self.aff_nom, 1,2)

        self.aff_score = QLabel("Score : ")
        self.global_layout.addWidget(self.aff_score, 2,2)

        self.manche = 0
        self.start_manche()



    def start_manche(self) :
        self.distribuer()
        joueur = self.joueurs[self.current_j]
        self.j_virtuel = joueur.copy()
        self.table_virtuel = self.table.copy()
        self.choice = []
        self.maj_aff()        
    
    def tour_suivant(self) :
        if self.table.table == self.table_virtuel.table :
            self.piocher(self.j_virtuel)
        self.joueurs[self.current_j] = self.j_virtuel.copy()
        self.table = self.table_virtuel.copy()
        self.choice = []
        if len(self.joueurs[self.current_j].main) == 0 :
            self.manche += 1
            self.end_manche()

        if self.current_j < len(self.joueurs) -1:
            self.current_j += 1
        else :
            self.current_j = 0
        joueur = self.joueurs[self.current_j]
        self.j_virtuel = joueur.copy()
        self.table_virtuel = self.table.copy()
        self.choice = []
        self.maj_aff()  
        


    def end_manche(self) :
        for j in self.joueurs :
            j.maj_score()
        self.pioche = Pioche()
        self.time = 0.
        self.table = Table()
        self.start_manche()


    def distribuer(self) :
        print(self.pioche)
        print(len(self.pioche.pioche))
        for t in range(14) :
            for j in self.joueurs :
                j.tirer(1, self.pioche)
        print(len(self.pioche.pioche))

    def piocher(self, joueur) :
        joueur.tirer(1, self.pioche)
        print(len(self.pioche.pioche))

    def aff_tuiles(self, lst_tuiles, layout, loc) :
        self.clear_layout(layout)
        if len(lst_tuiles) > 0 :
            if type(lst_tuiles[0]) == Tuile :
                lst_tuiles = [lst_tuiles]
        for s in range(len(lst_tuiles)) :
            if type(lst_tuiles[s]) == Set :
                lst_tuiles[s] = lst_tuiles[s].set
            for t in range(len(lst_tuiles[s])) :
                tuile = lst_tuiles[s][t]
                button = QPushButton(str(tuile.value))
                button.setFixedSize(30,50)
                button.tuile = tuile
                button.value = tuile.value
                button.color = tuile.color
                button.loc = loc
                button.idx = [s,t]
                button.clicked.connect(lambda checked, b=button: self.move_tuile(b, b.idx, loc))
                button.setStyleSheet("""
                                            QPushButton {
                                                background-color: %s;
                                                color: white;
                                                border-radius: 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: gray;
                                            }
                                            QPushButton:pressed {
                                                background-color: black;
                                            }
                                        """%csts.colors_name[tuile.color])
                layout.addWidget(button, s,t+1)
    def maj_aff(self) :
        self.aff_nom.setText(f"Joueur : {self.joueurs[self.current_j].nom}")
        self.aff_score.setText(f"Score : {self.joueurs[self.current_j].score}")
        self.aff_tuiles(self.table_virtuel.table, self.table_layout, loc=1)
        self.aff_tuiles(self.choice, self.selec_layout, loc=2)
        print(self.j_virtuel)
        self.aff_tuiles(self.j_virtuel.main, self.main_layout, loc=3)

    def clear_layout(self, layout) :
        while layout.count() > 0 :
            layout.itemAt(0).widget().hide()
            layout.removeItem(layout.itemAt(0))
            

    def move_tuile(self, b, idx, loc) : 
        if loc == 3 :
            self.choice.append(b.tuile)
            self.j_virtuel.main[idx[1]] = None
            self.j_virtuel.nettoyer_main()
        elif loc == 2 :
            self.j_virtuel.main.append(self.choice[idx[1]])
            self.choice = list(np.delete(self.choice, idx[1]))


        self.maj_aff()

    def validation_set(self) :
        set_test = Set(self.choice)
        if set_test.nature != 'not a set' :
            if self.j_virtuel.num_tour == 1 and set_test.valeur_set() < 3 :
                for t in range(len(self.choice)) :
                    tuile = self.choice[t]
                    self.j_virtuel.main.append(tuile)
            else :
                self.table_virtuel.table.append(set_test)
            self.choice = []
        else :
            for t in range(len(self.choice)) :
                tuile = self.choice[t]
                self.j_virtuel.main.append(tuile)
            self.choice = []
        self.maj_aff()


