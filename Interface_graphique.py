from PyQt5.QtWidgets import *
import numpy as np

import csts

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entrée de texte")
        
        # Initialiser une liste pour stocker les entrées
        self.entries = []

        # Créer un layout vertical
        layout = QVBoxLayout()

        # Champ de texte pour l'entrée
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Entrez votre texte ici")
        layout.addWidget(self.line_edit)

        # Bouton pour valider l'entrée
        self.add_button = QPushButton("Ajouter", self)
        self.add_button.clicked.connect(self.add_entry)
        layout.addWidget(self.add_button)

        # Bouton "OK" pour fermer la boîte de dialogue
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)  # Fermer la boîte de dialogue
        layout.addWidget(self.ok_button)

        # Définir le layout de la boîte de dialogue
        self.setLayout(layout)

    def add_entry(self):
        # Récupérer le texte de la ligne d'entrée
        text = self.line_edit.text()
        if text:  # Vérifier que le champ n'est pas vide
            self.entries.append(text)  # Ajouter le texte à la liste
            self.line_edit.clear()  # Effacer le champ de texte
        else:
            QMessageBox.warning(self, "Avertissement", "Veuillez entrer un texte valide.")

    def get_entries(self):
        return self.entries  # Retourner la liste des entrées
    
def open_dialog(Lancer_partie_bouton, global_layout):
    global_layout.removeWidget(Lancer_partie_bouton)
    Lancer_partie_bouton.hide()  # Masquer le bouton
    dialog = InputDialog()
    if dialog.exec_() == QDialog.Accepted:  # Si "OK" est cliqué
        noms = dialog.get_entries()  # Récupérer les entrées
        print("Noms ajoutées :", noms)  # Afficher les entrées dans la console
        global_layout, table_layout, main_layout, selec_layout = gen_affichage()
        partie = Partie(noms, global_layout, table_layout, main_layout, selec_layout)


def gen_affichage() :
    # Créer un QFrame pour entourer le table_layout avec un contour
    table_frame = QFrame()
    table_frame.setFrameShape(QFrame.Box)  # Dessiner un contour
    table_frame.setLineWidth(2)  # Épaisseur du contour
    table_layout = QGridLayout()
    table_frame.setLayout(table_layout)  # Associer le layout au QFrame

    # Créer un QFrame pour entourer le main_layout avec un contour
    main_frame = QFrame()
    main_frame.setFrameShape(QFrame.Box)  # Dessiner un contour
    main_frame.setLineWidth(2)  # Épaisseur du contour
    main_layout = QGridLayout()
    main_frame.setLayout(main_layout)  # Associer le layout au QFrame

    # Créer un QFrame pour entourer le main_layout avec un contour
    selec_frame = QFrame()
    selec_frame.setFrameShape(QFrame.Box)  # Dessiner un contour
    selec_frame.setLineWidth(2)  # Épaisseur du contour
    selec_layout = QGridLayout()
    selec_frame.setLayout(selec_layout)  # Associer le layout au QFrame

    global_layout.addWidget(table_frame,1,1)
    global_layout.addWidget(selec_frame,2,1)
    global_layout.addWidget(main_frame,3,1)

    return global_layout, table_layout, main_layout, selec_layout

    


# Alors alors, 
# Lorsque l'utilisateur choisi des tuiles, il peut renseigner 2 foix la même, pas bien
# Ajouter toutes les vérifications de validité du joker





def select_table_set(button) :
    print(button)


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
            #self.pioche.append(Tuile(0,0)) à ajouter si on veut des Jokers 
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

    def copy(self) :
        n_j = Joueur(self.nom)
        n_j.main = self.main.copy()
        return n_j
        
          
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
    def __init__(self, lst_noms:list, global_layout, table_layout, main_layout, selec_layout) :
        self.joueurs = []

        for i in range(len(lst_noms)) :
            nom = lst_noms[i]
            self.joueurs.append(Joueur(nom))

        self.pioche = Pioche()
        self.time = 0.   
        self.table = Table()
        self.choice = []

        self.global_layout = global_layout
        self.table_layout = table_layout
        self.main_layout = main_layout
        self.selec_layout = selec_layout

        validation_button = QPushButton("Valider le Set")
        validation_button.clicked.connect(self.validation_set)
        global_layout.addWidget(validation_button,2,2)

        self.start_manche()


    def start_manche(self) :
        self.distribuer()
        gagnant = False
        while not gagnant :
            for j in self.joueurs :
                j_virtuel = j.copy()
                table_virtuel = self.table.copy()
                

                self.aff_main(j_virtuel.main)
                self.aff_table(table_virtuel.table)
                gagnant = True

        #self.end_manche()
                
    def end_manche(self) :
        for j in self.joueurs :
            j.maj_score()
        self.pioche = Pioche()
        self.time = 0.
        self.table = Table()
        self.choice = []

        continuer = input("Voulez-vous refaire une manche ? o/n : ")
        if continuer in ['o','O'] :
            self.start_manche()

    def distribuer(self) :
        for t in range(14) :
            for j in self.joueurs :
                j.tirer(1, self.pioche)

    def piocher(self, joueur) :
        joueur.tirer(1, self.pioche)
    
    def poser(self, set) :
        self.table.poser(set)

    def aff_main(self, main) :
        self.clear_layout(self.main_layout)
        for t in range(len(main)) :
            tuile = main[t]
            button = QPushButton(str(tuile.value))
            button.setStyleSheet("""
                                    QPushButton {
                                        background-color: %s;
                                        color: white;
                                        border-radius: 5px;
                                    }
                                    QPushButton:hover {
                                        background-color: gray;
                                    }
                                    QPushButton:pressed {
                                        background-color: black;
                                    }
                                """%csts.colors_name[tuile.color])
            button.setFixedSize(30,50)
            button.clicked.connect(lambda checked, b=button: self.move_button(b, self.main_layout, self.selec_layout))
            self.main_layout.addWidget(button, 1,t)

    def aff_table(self, table) :
        self.clear_layout(self.table_layout)
        for s in range(len(table)) :
            set = table[s]
            button_set = QPushButton(f"Set {s}")
            button_set.setFixedSize(30,50)
            button_set.clicked.connect(lambda checked, b=button: self.select_table_set(b))
            self.table_layout.addWidget(button_set,s,1)

            for t in range(len(set)) :
                tuile = set[t]
                button = QPushButton(str(tuile.value))
                button.setStyleSheet("""
                                        QPushButton {
                                            background-color: %s;
                                            color: white;
                                            border-radius: 5px;
                                        }
                                        QPushButton:hover {
                                            background-color: gray;
                                        }
                                        QPushButton:pressed {
                                            background-color: black;
                                        }
                                    """%csts.colors_name[tuile.color])
                button.setFixedSize(30,50)
                button.clicked.connect(lambda checked, b=button: self.move_button(b, self.main_layout, self.selec_layout))
                self.table_layout.addWidget(button, s,t+1)

    def clear_layout(self, layout) :
        print('clearing')
        while layout.count() > 0 :
            layout.removeItem(layout.itemAt(0))
        print('clean')

    def validation_set(self) :
        print('validation du set')
        print(self.selec_layout)

    def move_button(self, button, current_layout, new_layout) :
        # Retirer le bouton du layout actuel
        current_layout.removeWidget(button)
        button.hide()  # Masquer le bouton

        # Ajouter le bouton à un autre layout
        new_layout.addWidget(button, 1,new_layout.count()+1)  # new_layout est le layout cible
        button.clicked.connect(lambda checked, b=button: self.move_button(b, new_layout, current_layout))
        button.show()  # Afficher le bouton dans le nouveau layout


        print("Index du bouton cliqué :",new_layout.indexOf(button))
        print("nombre de widgets :",new_layout.count())



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

    def __str__(self) :
        txt = f"------------------------\nTable :\n"
        for s in self.table :
            txt += f"{s.__str__()} \n"
        return txt + "------------------------"
    
    def poser(self, set) :
        self.table.append(set)

    def copy(self) :
        new_Table = Table()
        new_Table.table = self.table
        return new_Table
    
    


#partie = Partie(["Serge", "Jean"], 2)


if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    global_layout = QGridLayout()

    # Bouton pour lancer la partie
    Lancer_partie_bouton = QPushButton("Lancer la partie")
    Lancer_partie_bouton.clicked.connect(lambda b=Lancer_partie_bouton: open_dialog(Lancer_partie_bouton, global_layout))
    global_layout.addWidget(Lancer_partie_bouton, 1, 1)

    window.setLayout(global_layout)
    window.show()
    app.exec()

    




