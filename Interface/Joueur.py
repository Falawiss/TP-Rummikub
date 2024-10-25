import numpy as np

from Interface.Tuile import *
class Joueur :
    """
    Classe Joueur :
    Attributs :
        - nom : string
        - main : liste de Tuiles
        - score : int
        - num_tour : int
    Methodes :
        - __init__() : création du joueur
        - tirer() : tirer une tuile de la pioche, et l'ajouter à la main
        - maj_score() : compter le score de la main et l'ajouter au score 
        - __str__() : affichage des informations du joueur
        - reset_num_tour() : remise à zero du compteur de tour
        - nettoyer_main() : Nettoie la liste de tuiles des valeurs None
        - copy() :  Renvoie une copie de l'objet
    """
    def __init__(self, nom) :
        if type(nom) == str :
            self.nom = nom
        else :
            self.nom = chr(64 + np.random.randint(26))
        self.main = []
        self.score = 0
        self.num_tour = 0


    def tirer(self, nb_tuiles:int, pioche) :
        for t in range(nb_tuiles) :
            self.main.append(pioche.tirer())
        self.nettoyer_main()
        self.sort()

    def maj_score(self) :
        for t in self.main :
            if t.value == 0 :
                self.score += 30
            else :
                self.score += t.value
        self.main = []

    def __str__(self) :
        txt = f"{self.nom} | Tour n°{self.num_tour}\nscore : {self.score} \nmain : \n|"
        for i in range(1,len(self.main)+1) :
            ajout = (len(str(i))%2)*" "
            txt += f"{i}{ajout}|"
        txt += '\n'
        for t in self.main :
            txt += t.__str__()
        return txt
    
    def reset_num_tour(self) :
        self.num_tour = 0

    def nettoyer_main(self) :
        nouvelle_main = []
        for t in self.main :
            if t != None :
                nouvelle_main.append(t)
        self.main = nouvelle_main

    def copy(self) :
        n_j = Joueur(self.nom)
        n_j.main = self.main.copy()
        return n_j
    
    def sort(self) : 
        vc = []
        values = np.array([t.value for t in self.main])
        colors = np.array([t.color for t in self.main])
        vc = np.vstack((values, colors))
        vc = np.sort(vc)
        n_main = []
        for i in range(len(vc[0])) :
            n_main.append(Tuile(vc[0,i], vc[1,i]))
        self.main = n_main