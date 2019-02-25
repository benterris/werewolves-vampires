class Heuristic:

    @staticmethod
    def distance(x1, y1, x2, y2):
        """Nombre de déplacements pour aller de (x1, y1) à (x2, y2)"""
        return max(abs(x1 - x2), abs(y1 - y2))

    @staticmethod
    def heuristic(state, positive_player=0, current_player=0):
        """Calsul de l'heuristique d'une situation
            paramètres
             positive_player : joueur pour lequel on veut calculer l'heuristique (0 pour V, 1 pour LG)
             current_player : joueur qui doit jouer, 0 so c'est aux vampires, 1 s c'est aux LG"""

        heur = 0

        # On calcule l'heuristique comme positive si les vampires sont avantagés, on inversera à la fin si nécessaire

        # Paramètres ajustables
        M1 = 100
        M2 = 20
        M3 = 10
        M4 = 1

        # On compte vampires et LG
        for entite in state:
            if entite['type'] == "V":
                heur += M1 * entite['number']
            elif entite['type'] == "W":
                heur -= M1 * entite['number']
        #print("Etape 1 : ", heur)

        for entite in state:
            if entite["type"] == "H":
                for entite2 in state:
                    if entite2['type'] == "V" and entite2['number'] >= entite["number"]:
                        ntour = 2 * \
                            Heuristic.distance(
                                entite["x"], entite["y"], entite2["x"], entite2["y"])
                        if current_player == 0:
                            ntour -= 1
                        else:
                            ntour += 1
                        heur += M2 * (1/ntour) * entite["number"]
                    elif entite2['type'] == "W" and entite2['number'] >= entite["number"]:
                        ntour = 2 * \
                            Heuristic.distance(
                                entite["x"], entite["y"], entite2["x"], entite2["y"])
                        if current_player == 1:
                            ntour -= 1
                        else:
                            ntour += 1
                        heur -= M2 * (1/ntour) * entite["number"]
       # print("Etape 2 : ", heur)

        for entite in state:
            if entite["type"] == "V":
                for entite2 in state:
                    if entite2["type"] == "W":
                        n1, n2 = entite['number'], entite2["number"]
                        if n1 >= 1.5 * n2:
                            ntour = 2 * \
                                Heuristic.distance(
                                    entite["x"], entite["y"], entite2["x"], entite2["y"])
                            if current_player == 0:
                                ntour -= 1
                            else:
                                ntour += 1
                            heur += M3 * (1/ntour**2) * n2
                        elif n2 >= 1.5 * n1:
                            ntour = 2 * \
                                Heuristic.distance(
                                    entite["x"], entite["y"], entite2["x"], entite2["y"])
                            if current_player == 1:
                                ntour -= 1
                            else:
                                ntour += 1
                            heur -= M3 * (1 / ntour**2) * n1
                        elif n1 > n2:
                            ntour = 2 * \
                                Heuristic.distance(
                                    entite["x"], entite["y"], entite2["x"], entite2["y"])
                            if current_player == 1:
                                ntour -= 1
                            else:
                                ntour += 1
                            P_victoire = 0
                            if n1 == n2:
                                P_victoire = 0.5
                            elif n1 > n2 and current_player == 0:
                                P_victoire = n1/n2 - 0.5
                            elif n1 > n2 and current_player == 1:
                                P_victoire = 1 - n2/(2*n1)
                            elif n1 < n2 and current_player == 0:
                                P_victoire = n1/(2*n2)
                            elif n1 > n2 and current_player == 1:
                                P_victoire = 1 - (n2/n1 - 0.5)
                            heur += M3 * (1/ntour**2) * n1 * P_victoire
                            heur -= M3 * (1/ntour**2) * n2 * (1-P_victoire)

       # print("Etape 3 : ", heur)

        if positive_player == 1:
            return -heur
        else:
            return heur
