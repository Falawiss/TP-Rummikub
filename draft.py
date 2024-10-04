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
    def __init__(self, lst_noms:list, nb_manches:int) :
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
    def __init__(self, nom:str) :
        self.nom = nom
        self.main = []
        self.score = 0

    def tirer(self, nb_tuiles:int, pioche) :
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

class Set :
    def __init__(self, lst_tuiles:list) :
        self.nature = 'not a set'
        self.colors = []
        self.extrems = [None, None]
        values = [t.value for t in lst_tuiles]
        colors = [t.color for t in lst_tuiles]
        np.sort(values)
        self.set = []
        if len(lst_tuiles) > 2 :
            """
            if np.max(values) - np.min(values) == len(values)-1 and len(np.unique(colors)) == 1:
                self.set = [Tuile(values[t],colors[t]) for t in range(len(lst_tuiles))]
                self.nature = 'suite'
                self.extrems = [np.max(values)+1, np.min(values)-1]
            elif len(np.unique(colors)) == len(lst_tuiles) and np.unique(values) == 1 :
                self.nature = 'serie'
                self.color = np.unique(colors)
                self.set = [Tuile(values[t],colors[t]) for t in range(len(lst_tuiles))]
            """
            self.set = [Tuile(values[t],colors[t]) for t in range(len(lst_tuiles))]
            self.nature = 'suite'
            

    def valeur_set(self) :
        somme = 0
        for t in self.set :
            somme += t.value
        return somme
    
    def __str__(self) :
        txt = ''
        for t in self.set :
            txt += t.__str__()
        return txt
    
    def ajoute_tuile(self, tuile, idx) :
        if (tuile.color not in self.color and "serie" in self.nature)  or (tuile.value in self.extrems and "suite" in self.nature) :
            new_set = []
            for i in range(len(self.set)) :
                if i == idx :
                    new_set.append(tuile)
                else :
                    new_set.append(self.set[i])
            self.set = new_set

    def supprime_tuile(self, idx) :
        if len(self.set) > 3 :
            new_set = []
            for i in range(len(self.set)) :
                if i != idx :
                    new_set.append(self.set[i])
            self.set = new_set