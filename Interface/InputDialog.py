from PyQt5.QtWidgets import *

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entrée de texte")
        
        # Initialiser une liste pour stocker les noms
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