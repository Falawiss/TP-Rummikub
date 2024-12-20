from Interface.Tuile import *
import numpy as np

class Pioche :
    """
    Classe Pioche :
    Attributs :
        - pioche : liste de Tuiles
    Methodes :
        - __init__() : création de la pioche, et mélanger
        - tirer() : tirer une tuile de la pioche, et l'enlever de la liste
        - __str__() : permet d'afficher les tuiles de la pioche
    """
    def __init__(self) :
        """
        Création des 106 Tuiles de la pioche 
        """
        self.pioche = []
        for i in range(2) :
            for v in range(1,14) :
                for c in range(1,5) :
                    self.pioche.append(Tuile(v,c))
            self.pioche.append(Tuile(0,0))
        # Mélanger la pioche
        np.random.shuffle(self.pioche)

    def tirer(self) :
        """
        Tirer une tuile et la supprimer de la pioche
        """
        if len(self.pioche) > 1 :
            tirage = self.pioche[-1]
            self.pioche = self.pioche[:-1]
            return tirage
        
    def __str__(self) :
        """
        Afficher la Pioche dans la console
        """
        txt = ""
        for t in self.pioche :
            txt += str(t)
        return txt