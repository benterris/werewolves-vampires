from constraint_programming import constraint_program
from action import Action
from scipy.special import binom


class PossiblePlays:
    """Classe qui permet de déterminer les coups possibles depuis un état donné"""

    @staticmethod
    def get_possible_plays(state, m, n, player=0):
        """player : 0 pour V, 1 pour W
        m et n sont la taille de la grille
        (m coordonnée en x et n en y)"""

        j = "V" if player==0 else "W"
        var = {}
        for entity in state:
            if entity["type"] == j:
                available_cases = []
                for k in[-1, 0, 1]:
                    for l in [-1, 0, 1]:
                        if (0 <= entity['x'] + k < m) and (0<= entity['y'] + l <= n):
                            available_cases.append((entity['x'] + k, entity['y'] + l))
                for individual in range(entity["number"]):
                    var[(entity["type"], individual, entity["x"], entity["y"])] = list(available_cases)

        P = constraint_program(var)
        P.set_arc_consistency()
        solutions = P.solve_all()


        for solution in solutions:
            movements = {}
            for (_, _, x_init, y_init), (x_end, y_end) in solution.items():

                if x_init != x_end or y_init != y_end:
                    if (x_init, y_init, x_end, y_end) not in movements:
                        movements[((x_init, y_init, x_end, y_end))] = 1
                    else:
                        movements[((x_init, y_init, x_end, y_end))] += 1
            if len(movements) > 0:
                action = Action()
                for (x_init, y_init, x_end, y_end), number in movements.items():
                    action.add_deplacement((j, number, (x_init, y_init), (x_end, y_end)))
                yield action

    @staticmethod
    def get_next_states(state, action):
        """Calculates the possible next states given a previous state and an action"""
        # On cherche les batailles aléatoires
        movements = action.get_deplacements()
        states_pile = [(state, 1, 0)] #Etat, proba, étape
        next_states = []
        while len(states_pile) > 0:
            current_state, proba, step = states_pile.pop()
            if step == len(movements):
                next_states.append((current_state, proba))
            else:
                _, number, (x_init, y_init), (x_end, y_end) = movements[step]
                entity1 = PossiblePlays.what_in_that_case(current_state, x_init, y_init)
                entity2 = PossiblePlays.what_in_that_case(current_state, x_end, y_end)
                if entity2 is None:
                    if entity1["number"] > number:
                        current_state = PossiblePlays.set_case(current_state, x_init, y_init, {"type":entity1["type"], "number":entity1["number"] - number, "x":x_init, "y":y_init})
                        current_state = PossiblePlays.set_case(current_state, x_end, y_end, {"type":entity1["type"], "number":number, "x":x_end, "y":y_end})
                    else:
                        current_state = PossiblePlays.remove_case(current_state, x_init, y_init)
                        current_state = PossiblePlays.set_case(current_state, x_end, y_end,
                                                               {"type": entity1["type"], "number": number, "x": x_end,
                                                                "y": y_end})
                    states_pile.append((current_state, proba, step+1))

                elif entity2["type"] == entity1["type"]:
                    if entity1["number"] > number:
                        current_state = PossiblePlays.set_case(current_state, x_init, y_init, {"type":entity1["type"], "number":entity1["number"] - number, "x":x_init, "y":y_init})
                        current_state = PossiblePlays.set_case(current_state, x_end, y_end, {"type":entity1["type"], "number":number + entity2["number"], "x":x_end, "y":y_end})
                    else:
                        current_state = PossiblePlays.remove_case(current_state, x_init, y_init)
                        current_state = PossiblePlays.set_case(current_state, x_end, y_end,
                                                               {"type": entity1["type"], "number": number + entity2["number"], "x": x_end,
                                                                "y": y_end})
                    states_pile.append((current_state, proba, step + 1))

                elif entity2["type"] == "H" and number >= entity2["number"]:
                    if entity1["number"] > number:
                        current_state = PossiblePlays.set_case(current_state, x_init, y_init, {"type":entity1["type"], "number":entity1["number"] - number, "x":x_init, "y":y_init})
                        current_state = PossiblePlays.set_case(current_state, x_end, y_end, {"type":entity1["type"], "number":number + entity2["number"], "x":x_end, "y":y_end})
                    else:
                        current_state = PossiblePlays.remove_case(current_state, x_init, y_init)
                        current_state = PossiblePlays.set_case(current_state, x_end, y_end,
                                                               {"type": entity1["type"], "number": number + entity2["number"], "x": x_end,
                                                                "y": y_end})
                    states_pile.append((current_state, proba, step + 1))

                elif entity2["type"] == "H":
                    #Il y a bataille joueur-humain
                    #on commence par vider la case de départ
                    if entity1["number"] > number:
                        current_state = PossiblePlays.set_case(current_state, x_init, y_init, {"type":entity1["type"], "number":entity1["number"] - number, "x":x_init, "y":y_init})
                    else:
                        current_state = PossiblePlays.remove_case(current_state, x_init, y_init)
                    P_victory = number / (2*entity2["number"])
                    #Ensemble des issues possibles
                    #On perd et tout le monde meurt ou on gagne et tt le monde meurt
                    new_proba = (1-P_victory) * P_victory**entity2["number"] + P_victory * (1-P_victory)**number
                    current_state = PossiblePlays.remove_case(current_state, x_end, y_end)
                    states_pile.append((current_state, proba * new_proba, step + 1))
                    #On perd mais des humains survivent
                    for possibility in range(1, entity2["number"]+1):
                        current_state = PossiblePlays.set_case(current_state, x_end, y_end, {"type": entity2["type"],
                                                                                             "number": possibility, "x": x_end,
                                                                                             "y": y_end})
                        new_proba = (1-P_victory)**(possibility+1) * P_victory**(entity2["number"] - possibility) * binom(entity2["number"], possibility)
                        states_pile.append((current_state, proba * new_proba, step + 1))
                    #On gagne
                    for possibility in range(1, number + entity2["number"]+1):
                        current_state = PossiblePlays.set_case(current_state, x_end, y_end, {"type": entity1["type"],
                                                                                             "number": possibility, "x": x_end,
                                                                                             "y": y_end})
                        new_proba = P_victory**(possibility+1) * (1-P_victory)**(entity2["number"] + number - possibility) * binom(entity2["number"] + number, possibility)
                        states_pile.append((current_state, proba * new_proba, step + 1))

                elif number >= 1.5 * entity2["number"]:
                    # On arrive sur des ennemis et on les défonce
                    if entity1["number"] > number:
                        current_state = PossiblePlays.set_case(current_state, x_init, y_init, {"type":entity1["type"], "number":entity1["number"] - number, "x":x_init, "y":y_init})
                    else:
                        current_state = PossiblePlays.remove_case(current_state, x_init, y_init)
                    current_state = PossiblePlays.set_case(current_state, x_end, y_end, {"type": entity1["type"],
                                                                                         "number": number,
                                                                                         "x": x_end,
                                                                                         "y": y_end})
                    states_pile.append((current_state, proba, step + 1))

                elif 1.5 * number <= entity2["number"]:
                    # On arrive sur des ennemis et on se fait défoncer
                    if entity1["number"] > number:
                        current_state = PossiblePlays.set_case(current_state, x_init, y_init, {"type":entity1["type"], "number":entity1["number"] - number, "x":x_init, "y":y_init})
                    else:
                        current_state = PossiblePlays.remove_case(current_state, x_init, y_init)
                    states_pile.append((current_state, proba, step + 1))
                else:
                    #Bataille contre ennemis
                    if entity1["number"] > number:
                        current_state = PossiblePlays.set_case(current_state, x_init, y_init, {"type":entity1["type"], "number":entity1["number"] - number, "x":x_init, "y":y_init})
                    else:
                        current_state = PossiblePlays.remove_case(current_state, x_init, y_init)
                    if number >=  entity2["number"]:
                        P_victory = (number/entity2["number"] - 0.5)
                    else:
                        P_victory = number/(2*entity2["number"])
                        # Ensemble des issues possibles
                    #On perd et tout le monde meurt ou on gagne et tt le monde meurt
                    new_proba = (1-P_victory) * P_victory**entity2["number"] + P_victory * (1-P_victory)**number
                    current_state = PossiblePlays.remove_case(current_state, x_end, y_end)
                    states_pile.append((current_state, proba * new_proba, step + 1))
                    #On perd
                    for possibility in range(1, entity2["number"]+1):
                        current_state = PossiblePlays.set_case(current_state, x_end, y_end, {"type": entity2["type"],
                                                                                             "number": possibility, "x": x_end,
                                                                                             "y": y_end})
                        new_proba = (1-P_victory)**(possibility+1) * P_victory**(entity2["number"] - possibility) * binom(entity2["number"], possibility)
                        states_pile.append((current_state, proba * new_proba, step + 1))

                    for possibility in range(1, number+1):
                        current_state = PossiblePlays.set_case(current_state, x_end, y_end, {"type": entity1["type"],
                                                                                             "number": possibility,
                                                                                             "x": x_end,
                                                                                             "y": y_end})
                        new_proba = P_victory ** (possibility + 1) * (1 - P_victory) ** (
                                number - possibility) * binom(number,
                                                                                      possibility)
                        states_pile.append((current_state, proba * new_proba, step + 1))
        #On renvoie les états possibles dans l'ordre de leur proba
        return sorted(next_states, key=lambda t: 1-t[1])






    @staticmethod
    def what_in_that_case(state, x, y):
        for entity in state:
            if entity["x"] == x and entity["y"] == y:
                return entity
        return None

    @staticmethod
    def remove_case(state, x, y):
        state = [entity for entity in state if not (entity["x"] == x and entity["y"] == y)]
        return state

    @staticmethod
    def set_case(state, x, y, new_case):
        state = [entity for entity in state if not (entity["x"]== x and entity["y"]== y)]
        state.append(new_case)
        return state





