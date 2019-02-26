from possible_plays import PossiblePlays
from time import time


state = [
    {"type": "W", "number": 1, "x": 0, "y": 2},
    {"type": "H", "number": 1, "x": 2, "y": 0},
    {"type": "H", "number": 1, "x": 2, "y": 2},
    {"type": "H", "number": 1, "x": 2, "y": 3},
    {"type": "H", "number": 1, "x": 2, "y": 4},
    {"type": "V", "number": 1, "x": 4, "y": 2},
]

deb = time()
actions = PossiblePlays.get_possible_plays(state, 5, 5, 0)
fin = time()
for action in actions:
    for movement in action:
        print(movement)
    print()
print(fin - deb, "s")