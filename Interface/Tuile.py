import numpy as np
import Interface.csts as csts

class Tuile :
    """
    Classe Tuile :
    Attributs :
        - color : 0-5
        - value : 0-13
    Methodes :
        - __init__() : création de la tuile
        - color_name() : nom de la couleur
        - __str__() : affichage de la valeur avec la couleur associée
    """
    def __init__(self, value:int, color:int) :
        """
        Création d'une tuile
        """
        # Vérification des valeurs
        if (color in np.arange(0,5) and value in np.arange(0,14)) and ((color == 0 and value == 0) or (color != 0 and value != 0)) :
            self.color = color
            self.value = value
        else :
            self.color = None
            self.value = None
    
    def color_name(self) :
        """
        Donne le nom de la couleur d'une tuile à partir de csts et de son index de couleur
        """
        return csts.colors_name[self.color]
    
    def __str__(self) :
        """
        Permet d'afficher une tuile dans la console
        """
        ajout = (len(str(self.value))%2)*" "
        return f"{csts.colors_code[self.color_name()]} {ajout}{self.value}{csts.colors_code['reset']}"

    