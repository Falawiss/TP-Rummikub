import numpy as np

colors_name = ["joker", "jaune", "rouge", "bleu", "noir"]
colors_code = {
    'rouge': '\033[91m',
    'jaune': '\033[93m',
    'bleu': '\033[94m',
    'noir': '\033[30m',
    'joker': '\033[35m',
    'reset': '\033[0m'  
}

class Partie :
    def __init__(self, lst_noms, nb_manches) :
        self.joueurs = []

        for i in range(len(lst_noms)) :
            nom = lst_noms[i]
            self.joueurs.append(Joueur(nom))

        self.nb_manches = nb_manches
        self.manche = 0
        self.pioche = Pioche()
        self.time = 0
        self.table = Table(10)

    def distribuer(self) :
        for t in range(14) :
            for j in self.joueurs :
                j.tirer(1, self.pioche)

    def manche(self) :
        self.distribuer()

        

class Joueur :
    def __init__(self, nom) :
        self.nom = nom
        self.main = []
        self.score = 0

    def tirer(self, nb_tuiles, pioche) :
        for t in range(nb_tuiles) :
            self.main.append(pioche.tirer())

    def maj_score(self) :
        for t in self.main :
            if t.value == 0 :
                self.score += 30
            else :
                self.score += t.value



class Pioche :
    def __init__(self) :
        self.pioche = []
        for i in range(2) :
            for v in range(1,14) :
                for c in range(1,5) :
                    self.pioche.append(Tuile(v,c))
            self.pioche.append(Tuile(0,0))
        np.random.shuffle(self.pioche)

    def tirer(self) :
        tirage = self.pioche[-1]
        self.pioche = self.pioche[:-1]
        return tirage


class Table :
    def __init__(self, dim) :
        self.table = np.zeros((dim, dim))-1

class Tuile :
    def __init__(self, value, color) :
        self.color = color
        self.value = value
    
    def color_name(self) :
        return colors_name[self.color]
    
    def __str__(self) :
        return f"{colors_code[self.color_name()]} {self.value} {colors_code['reset']}"
    
class Set :
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