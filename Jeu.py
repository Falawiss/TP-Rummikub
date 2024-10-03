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
    
class Pioche :
    """
    Classe Pioche :
    Attributs :
        - pioche : liste de Tuiles
    Methodes :
        - __init__() : création de la pioche, et mélanger
        - tirer() : tirer une tuile de la pioche, et l'enlever de la liste
    """
    def __init__(self) :
        self.pioche = []
        for i in range(2) :
            for v in range(1,14) :
                for c in range(1,5) :
                    self.pioche.append(Tuile(v,c))
            self.pioche.append(Tuile(0,0))
        np.random.shuffle(self.pioche)

    def tirer(self) :
        if len(self.pioche) > 1 :
            tirage = self.pioche[-1]
            self.pioche = self.pioche[:-1]
            return tirage
        else :
            return None

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
    """
    def __init__(self, nom) :
        if type(nom) == str :
            self.nom = nom
        else :
            self.nom = chr(64 + np.random.randint(26))
        self.main = []
        self.score = 0
        self.num_tour = 0


    def tirer(self, nb_tuiles, pioche) :
        for t in range(nb_tuiles) :
            self.main.append(pioche.tirer())

    def maj_score(self) :
        for t in self.main :
            if t.value == 0 :
                self.score += 30
            else :
                self.score += t.value

    def __str__(self) :
        return f"{self.nom} \nscore : {self.score} \nmain : {[t.__str__() for t in self.main]}"
    
    def reset_num_tour(self) :
        self.num_tour = 0
    
class Set :
    """
    Classe Set :
    Attributs :
        - nature : string (serie, suite, serie_suite, not a set)
        - set : liste de Tuiles
    Methodes :
        - __init__() : création du set

    """
    def __init__(self, lst_tuiles) :
        self.nature = 'not a set'
        values = [t.value for t in lst_tuiles]
        colors = [t.color for t in lst_tuiles]
        np.sort(values)
        if len(lst_tuiles) > 2 :
            if np.max(values) - np.min(values) == len(values)-1 :
                self.set = [Tuile(values[t],colors[t]) for t in range(len(lst_tuiles))]
                self.nature = 'serie'
            elif len(np.unique(colors)) == 1 :
                if self.nature == 'serie' :
                    self.nature = 'serie_suite'
                else :
                    self.nature = 'suite'
                self.set = [Tuile(values[t],colors[t]) for t in range(len(lst_tuiles))]
        else :
            self.set = []

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
        - start_manche() : remplis les mains des joueurs
    """
    def __init__(self, lst_noms, nb_manches) :
        self.joueurs = []

        for i in range(len(lst_noms)) :
            nom = lst_noms[i]
            self.joueurs.append(Joueur(nom))

        self.nb_manches = nb_manches
        self.manche = 0
        self.pioche = Pioche()
        self.time = 0.   

        for m in range(nb_manches) :
            self.start_manche()

    def start_manche(self) :
        self.distribuer()


class Table :
    """
    Classe Table :
    Attributs :
        - table : liste de Sets
    Methodes :
        - __init__() : création de la Table
    """
    def __init__(self) :
        self.table = []
        
