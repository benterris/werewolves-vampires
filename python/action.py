

class Action():
    """Représente l'ensemble des déplacements lors d'un tour"""

    def __init__(self):
        self.__deplacements = []

    def add_deplacement(self, deplacement):
        """deplacement est un 4-uplet (type, nombre, (xdepart, ydepart), (xarrivee, yarrivee))_"""
        self.__deplacements.append(deplacement)

    def get_deplacements(self):
        return self.__deplacements