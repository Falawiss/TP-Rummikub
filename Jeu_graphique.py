from Interface.csts import *
from Interface.Pioche import *
from Interface.Tuile import *
from Interface.Set import *
from Interface.Joueur import *
from Interface.Table import *
from Interface.InputDialog import *

from Interface.Partie import *

import Interface.csts as csts
import numpy as np
from PyQt5.QtWidgets import *


def main():
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

def open_dialog(Lancer_partie_bouton, global_layout):
    global_layout.removeWidget(Lancer_partie_bouton)
    Lancer_partie_bouton.hide()  # Masquer le bouton
    dialog = InputDialog()
    if dialog.exec_() == QDialog.Accepted:  # Si "OK" est cliqué
        noms = dialog.get_entries()  # Récupérer les entrées
        print("Noms ajoutées :", noms)  # Afficher les entrées dans la console
        global_layout, table_layout, main_layout, selec_layout = gen_affichage(global_layout)
        partie = Partie(noms, global_layout, table_layout, main_layout, selec_layout)

def gen_affichage(global_layout) :
    # Créer un QFrame pour entourer la Table de jeu avec un contour
    table_frame = QFrame()
    table_frame.setFrameShape(QFrame.Box)  # Dessiner un contour
    table_frame.setLineWidth(2)  # Épaisseur du contour
    table_layout = QGridLayout()
    table_frame.setLayout(table_layout)  # Associer le layout au QFrame

    # Créer un QFrame pour entourer la sélection de tuiles avec un contour
    selec_frame = QFrame()
    selec_frame.setFrameShape(QFrame.Box) 
    selec_frame.setLineWidth(2)  
    selec_layout = QGridLayout()
    selec_frame.setLayout(selec_layout) 

    # Créer un QFrame pour entourer la main du joueur avec un contour
    main_frame = QFrame()
    main_frame.setFrameShape(QFrame.Box) 
    main_frame.setLineWidth(2) 
    main_layout = QGridLayout()
    main_frame.setLayout(main_layout)  
    
    # Ajout des layouts au global layout
    global_layout.addWidget(table_frame,1,1,2,1)
    global_layout.addWidget(selec_frame,3,1)
    global_layout.addWidget(main_frame,4,1)

    return global_layout, table_layout, main_layout, selec_layout

if __name__ == "__main__":
    main()
    


    

