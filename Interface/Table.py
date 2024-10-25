class Table :
    """
    Classe Table :
    Attributs :
        - table : liste de Sets
    Methodes :
        - __init__() : création de la Table
        - __str__() : affichage de la table
        - poser() : ajoute un set à la table
        - copy() : renvoie une copie de l'objet
    """
    def __init__(self) :
        self.table = []
        self.table_creation = []

    def __str__(self) :
        txt = f"------------------------\nTable :\n"
        for s in self.table :
            txt += str(s) + '\n'
        return txt + "------------------------"
    
    def poser(self, set) :
        self.table.append(set)

    def copy(self) :
        new_table = Table()
        new_table.table = self.table.copy()
        return new_table