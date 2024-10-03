import csts
np = csts.np


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
        # Vérification des valeurs
        if (color in np.arange(0,5) and value in np.arange(0,14)) and ((color == 0 and value == 0) or (color != 0 and value != 0)) :
            self.color = color
            self.value = value
        else :
            self.color = None
            self.value = None
    
    def color_name(self) :
        return csts.colors_name[self.color]
    
    def __str__(self) :
        return f"{csts.colors_code[self.color_name()]} {self.value} {csts.colors_code['reset']}"
    
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


    def tirer(self, nb_tuiles:int, pioche) :
        for t in range(nb_tuiles) :
            self.main.append(pioche.tirer())
        self.nettoyer_main()

    def maj_score(self) :
        for t in self.main :
            if t.value == 0 :
                self.score += 30
            else :
                self.score += t.value
        self.main = []

    def __str__(self) :
        txt = f"{self.nom} \nscore : {self.score} \nmain : "
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
        
          
class Set :
    """
    Classe Set :
    Attributs :
        - nature : string (serie, suite, serie_suite, not a set)
        - set : liste de Tuiles
    Methodes :
        - __init__() : création du set

    """
    def __init__(self, lst_tuiles:list) :
        self.nature = 'not a set'
        self.colors = []
        self.extrems = [None, None]
        values = [t.value for t in lst_tuiles]
        colors = [t.color for t in lst_tuiles]
        np.sort(values)
        if len(lst_tuiles) > 2 :
            if np.max(values) - np.min(values) == len(values)-1 :
                self.set = [Tuile(values[t],colors[t]) for t in range(len(lst_tuiles))]
                self.nature = 'suite'
                self.extrems = [np.max(values)+1, np.min(values)-1]
            elif len(np.unique(colors)) == len(lst_tuiles) :
                if self.nature == 'suite' :
                    self.nature = 'serie_suite'
                else :
                    self.nature = 'serie'
                self.color = np.unique(colors)
                self.set = [Tuile(values[t],colors[t]) for t in range(len(lst_tuiles))]
        else :
            self.set = []

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
        tour = True
        while tour :
            for j in self.joueurs :
                print(j)
                if j.num_tour == 0:
                    choix = input("Un set de plus de 30 pts à poser ? o/n : ")
                    if choix == 'o' :
                        set_choose = input("Donnez l'index des tuiles à sélectionner (2-5-12) : ")
                        set_sel = []
                        for s_c in set_choose.split('-') :
                            set_sel.append(j.main[int(s_c)-1])
                        Set_sel = Set(set_sel)
                        if Set_sel.valeur_set() >= 30 :
                            self.poser(Set_sel)
                            for s_c in set_choose.split('-') :
                                j.main[int(s_c)-1] = None
                            j.nettoyer_main()
                        else :
                            j.tirer(1, self.pioche)
                    else :
                        j.tirer(1, self.pioche)

                else :
                    sel_tuiles = []
                    sel_main = input("Tuiles à sélectionner dans la Main (2-5-12) : ")
                    for s in sel_main.split('-') :
                        sel_tuiles.append(j.main[int(s)])

                    print(sel_tuiles)

                    sel_set = input("Set à sélectionner sur la Table (1) : ")
                    sel_set = []
                    for s in sel_set.split('-') :
                        sel_set.append(self.table.table[s])

                    print(sel_set)
                    
                    sel_tuile_set = input("Tuiles à sélectionner dans ce Set (2-5-12) :")
                    for s in sel_tuile_set.split('-') :
                        sel_tuiles.append(sel_set.set[s])

                    print(sel_tuiles)


                    
                    
                print(j)
                print(self.table)
                if len(j.main) == 0 :
                    tour = False
                    self.end_manche()

    def end_manche(self) :
        for j in self.joueur :
            j.maj_score()
        self.pioche = Pioche()
        self.time = 0.
        self.table = Table()

    def distribuer(self) :
        for t in range(14) :
            for j in self.joueurs :
                j.tirer(1, self.pioche)

    def piocher(self, joueur) :
        joueur.tirer(1, self.pioche)
    
    def poser(self, set) :
        self.table.poser(set)



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
        self.table_creation = []

    def __str__(self) :
        txt = f"------------------------\nTable : "
        for s in self.table :
            txt += s.__str__()
        return txt + "\n------------------------"
    
    def poser(self, set) :
        self.table.append(set)




partie = Partie(["Serge", "Jean"], 2)




    

