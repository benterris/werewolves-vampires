

class Action():
    """Représente l'ensemble des déplacements lors d'un tour"""

    def __init__(self):
        self.__deplacements = []

    def __repr__(self):
        return ' | '.join([str(move) for move in self.__deplacements])

    def add_deplacement(self, deplacement):
        """deplacement est un 4-uplet (type, nombre, (xdepart, ydepart), (xarrivee, yarrivee))"""
        self.__deplacements.append(deplacement)

    def get_deplacements(self):
        return self.__deplacements

    def is_valid(self):
        """Vérifie que les cases d'arrivée ne sont pas des cases de départ"""
        arrival = set()
        for dep in self.__deplacements:
            arrival.add(dep[3])
        for dep in self.__deplacements:
            if dep[2] in arrival:
                return False
        return True
