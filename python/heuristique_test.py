from Heuristic import Heuristic
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
heur = Heuristic.heuristic(state)
fin = time()
print(heur)
print(fin - deb, "s")

print(Heuristic.winned(state))
