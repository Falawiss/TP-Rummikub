import csts
np = csts.np

# Alors alors, 
# Lorsque l'utilisateur choisi des tuiles, il peut renseigner 2 foix la même, pas bien
# Il faut mettre à jour la table lors d'une modification
# Ajouter toutes les vérifications de validité


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
        ajout = (len(str(self.value))%2)*" "
        return f"{csts.colors_code[self.color_name()]} {ajout}{self.value}{csts.colors_code['reset']}"
    
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
            self.nature = 'not a set'
        self.sort()

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

    def sort(self) : 
        self.vc = np.sort(self.vc)
        n_set = []
        for i in range(len(self.vc[0])) :
            n_set.append(Tuile(self.vc[0,i], self.vc[1,i]))
        self.set = n_set

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
        gagnant = False
        while not gagnant :
            for j in self.joueurs :
                print(j)
                if j.num_tour == 0:
                    set_choose = input("Tuiles à sélectionner dans la Main (2-5-12) : ")
                    if set_choose != '' :
                        set_sel = []
                        for s_c in set_choose.split('-') :
                            set_sel.append(j.main[int(s_c)-1])
                        Set_sel = Set(set_sel)
                        print(Set_sel)
                        if Set_sel.valeur_set() >= 3 and Set_sel.nature in ['serie', 'suite']: 
                            self.poser(Set_sel)
                            for s_c in set_choose.split('-') :
                                j.main[int(s_c)-1] = None
                            j.nettoyer_main()
                            j.num_tour += 1
                        else :
                            j.tirer(1, self.pioche)
                    else :
                        j.tirer(1, self.pioche)

                else :
                    sel_main = input("Tuiles à sélectionner dans la Main (2-5-12) : ")
                    if sel_main != '' :
                        sel_tuiles = []
                        for s in sel_main.split('-') :
                            sel_tuiles.append(j.main[int(s)-1])

                        for t in sel_tuiles :
                            print(t, end='')

                        sel_set = input("Sets à sélectionner sur la Table (1-3) : ")
                        sel_tuile_set = []
                        for s in sel_set.split('-') :
                            sel_Set = self.table.table[int(sel_set)-1]
                            print(sel_Set)

                            sel_tuile_set.append(input("Tuiles à sélectionner dans ce Set (1-2-4) :"))
                            for t in sel_tuile_set[-1].split('-') :
                                sel_tuiles.append(sel_Set.set[int(t)-1])

                        final_Set = Set(sel_tuiles)
                        print(final_Set)

                        print(sel_main, sel_set, sel_tuile_set)
                        #if final_Set.nature != "not a set" :
                        for n in range(len(sel_set.split('-'))) :
                            s = sel_set.split('-')[n]
                            left_Set = self.table.table[int(s)-1]
                            for idx in sel_tuile_set[n].split('-') :
                                left_Set.enleve_tuile(idx)
                            #if left_Set.nature == "not a set" :
                            print(left_Set, self.table.table[int(s)-1])

                print(j)
                print(self.table)
                if len(j.main) == 0 :
                    gagnant = False
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
        txt = f"------------------------\nTable :\n"
        for s in self.table :
            txt += f"{s.__str__()} \n"
        return txt + "------------------------"
    
    def poser(self, set) :
        self.table.append(set)


t1 = Tuile(1,2)
t2 = Tuile(2,2)
t3 = Tuile(3,2)
set1 = Set([t1, t2, t3])
print(set1)
set1.enleve_tuile(2)
print(set1)
set1.ajoute_tuile(t2)
print(set1)


partie = Partie(["Serge", "Jean"], 2)




    

