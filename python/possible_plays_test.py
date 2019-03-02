from possible_plays import PossiblePlays
from action import Action


state_1 = [
    {"type": "W", "number": 1, "x": 0, "y": 2},
    {"type": "H", "number": 1, "x": 2, "y": 0},
    {"type": "H", "number": 1, "x": 2, "y": 2},
    {"type": "H", "number": 1, "x": 2, "y": 3},
    {"type": "H", "number": 1, "x": 2, "y": 4},
    {"type": "V", "number": 2, "x": 4, "y": 2},
]
state = [
    {"type": "H", "number": 2, "x": 0, "y": 0},
    {"type": "V", "number": 2, "x": 0, "y": 1},
]

actions = PossiblePlays.get_possible_plays(state, 5, 5, 0)
#for action in actions:
#    for movement in action.get_deplacements():
#        print(movement)
#    print()

def print_state(state, m, n):
    mat = [["      " for x in range(m)] for y in range(n)]
    for entity in state:
        mat[entity["x"]][entity["y"]] = "({}, {})".format(entity["type"], entity["number"])

    for line in mat:
        for case in line:
            print(case, " | ", end="")
        print()

print("Etat original : ")
print_state(state, 5, 5)
for action in actions:
    print("Avec l'action :")
    for movement in action.get_deplacements():
        print(movement)
    print("On obtient les états : ")
    final_states = PossiblePlays.get_next_states(state, action)
    for f_state, proba in final_states:
        print_state(f_state, 5, 5)
        print("Avec la proba", proba)

print("-----------------------------------------------------------------------------------------------")
print()
state = [{'number': 2, 'type': 'V', 'x': 2, 'y': 1}, {'number': 1, 'type': 'H', 'x': 2, 'y': 2}, {'number': 1, 'type': 'W', 'x': 2, 'y': 4}]
action = Action()
action.add_deplacement(('V', 1, (2,1), (2,2)))
action.add_deplacement(('V', 1, (2,1), (1,0)))
print("Etat original : ")
print_state(state, 5, 5)
print("Avec l'action :")
for movement in action.get_deplacements():
    print(movement)
print("On obtient les états : ")
final_states = PossiblePlays.get_next_states(state, action)
for f_state, proba in final_states:
    print_state(f_state, 5, 5)
    print("Avec la proba", proba)



