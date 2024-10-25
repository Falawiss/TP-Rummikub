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

### Ajouter un tri du jeu du joueur et des Sets

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

if __name__ == "__main__":
    main()
    


    

