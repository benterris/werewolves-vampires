from possible_plays_improved import PossiblePlays
from action import Action
from state import State


state = [
    {"type": "V", "number": 2, "x": 6, "y": 0},
    {"type": "V", "number": 6, "x": 6, "y": 1},
    {"type": "H", "number": 1, "x": 9, "y": 2},
    {"type": "W", "number": 4, "x": 8, "y": 2},
    {"type": "W", "number": 2, "x": 9, "y": 3},
    {"type": "W", "number": 2, "x": 8, "y": 4},
]
state_ = [
    {"type": "H", "number": 2, "x": 0, "y": 0},
    {"type": "V", "number": 2, "x": 0, "y": 1},
]

actions = PossiblePlays.get_possible_plays(state, 10, 5, 0)
#for action in actions:
#    for movement in action.get_deplacements():
#        print(movement)
#    print()

def print_state(state, m, n):
    print(state)
    mat = [["      " for x in range(m)] for y in range(n)]
    for entity in state:
        mat[entity["y"]][entity["x"]] = "({}, {})".format(entity["type"], entity["number"])

    for line in mat:
        for case in line:
            print(case, " | ", end="")
        print()

print("Etat original : ")

print_state(state, 10, 5)
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
print_state(state, 10, 5)
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
state = State(5, 5)
state.states = [{'number': 4, 'type': 'W', 'x': 2, 'y': 3},
                {'number': 4, 'type': 'V', 'x': 2, 'y': 2}]

action = Action()
action.add_deplacement(('V', 3, (2, 2), (2, 3)))
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


