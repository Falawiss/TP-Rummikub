from csts import *

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
    def __init__(self, value, color) :
        # Vérification des valeurs
        if (color in np.arange(0,5) and value in np.arange(0,14)) and ((color == 0 and value == 0) or (color != 0 and value != 0)) :
            self.color = color
            self.value = value
        else :
            self.color = None
            self.value = None
    
    def color_name(self) :
        return colors_name[self.color]
    
    def __str__(self) :
        return f"{colors_code[self.color_name()]} {self.value} {colors_code['reset']}"
    
tuile = Tuile(1,2)
print(tuile)
print(tuile.color_name())
tuile = Tuile(0,2)
print(tuile)
print(tuile.color_name())
tuile = Tuile(0,0)
print(tuile)
print(tuile.color_name())
tuile = Tuile(1,15)
print(tuile)
print(tuile.color_name())
tuile = Tuile(17,7)
print(tuile)
print(tuile.color_name())
tuile = Tuile(0,18)
print(tuile)
print(tuile.color_name())

