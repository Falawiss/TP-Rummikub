import numpy as np
from Interface.Tuile import *       
class Set :
    """
    Classe Set :
    Attributs :
        - nature : string (serie, suite, serie_suite, not a set)
        - set : liste de Tuiles
        - vc : valeurs et couleurs de chaque tuile
    Methodes :
        - __init__() : création du set
        - check_set() : vérifie la nature d'un set
        - ajoute_tuile(tuile) : ajoute une tuile à la liste
        - enleve_tuile(idx) : enlève une tuile à la liste à partir de son index
        - sort() : range le set par ordre croissant (et couleur aussi)
        - reset_vc() : remet à jour les attributs vc et set à partir d'une liste de set
        - valeur_set() : retourne la somme des valeurs du set
        - __str__() : affiche le set
    """
    def __init__(self, lst_tuiles) :
        self.set = lst_tuiles
        values = np.array([t.value for t in lst_tuiles])
        colors = np.array([t.color for t in lst_tuiles])
        self.vc = np.vstack((values, colors))
        self.nature = 'not a set'
        self.check_set()

    def check_set(self) :
        if len(self.set) >= 3 :
            if 0 not in self.vc[0] :
                if len(self.vc[0]) == len(np.arange(np.min(self.vc[0]), np.max(self.vc[0])+1)) and len(np.unique(self.vc[1])) == 1 :
                    self.nature = 'suite'
                elif len(np.unique(self.vc[1])) == len(self.set) and len(np.unique(self.vc[0])) == 1 :
                    self.nature = 'serie'
                else :
                    self.nature = 'not a set'
            else :
                set_no_joker = self.vc[:,self.vc[0]!=0]
                if len(np.unique(self.vc[1])) == len(self.set) and len(np.unique(set_no_joker[0])) == 1 :
                    self.nature = 'serie'
                if len(np.unique(set_no_joker[1])) == 1 :
                    if np.max(set_no_joker[0]) - np.min(set_no_joker[0]) == len(self.vc[0]) and np.unique(set_no_joker[0]) == len(set_no_joker[0]) :
                        self.nature = 'suite'
                    else :
                        self.nature = 'serie'
        else :
            self.nature = 'not a set'
        #self.sort()

    def ajoute_tuile(self, tuile) :
        self.set.append(tuile)
        self.reset_vc(self.set)
        self.check_set()

    def enleve_tuile(self, idx) :
        n_set = []
        for i in range(len(self.set)) :
            if i != idx -1 :
                n_set.append(self.set[i])
        self.reset_vc(n_set)
        self.check_set()

    #def sort(self) : 
        


    def reset_vc(self, lst_tuiles) :
        self.set = lst_tuiles
        self.vc = np.zeros((2,len(self.set)), dtype=int)
        self.vc[0] = np.array([t.value for t in lst_tuiles])
        self.vc[1] = np.array([t.color for t in lst_tuiles])
    
    def valeur_set(self) :
        somme = 0
        for t in self.set :
            somme += t.value
        return somme

    def __str__(self) :
        txt = ''
        for t in self.set :
            txt += t.__str__()
        return txt + " | " + self.nature