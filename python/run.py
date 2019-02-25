import map_printer
import random


SIZE = (5, 5)

N = SIZE[0]
M = SIZE[1]


state = [
    {"type": "W", "number": 1, "x": 0, "y": 2},
    {"type": "H", "number": 1, "x": 2, "y": 0},
    {"type": "H", "number": 1, "x": 2, "y": 2},
    {"type": "H", "number": 1, "x": 2, "y": 3},
    {"type": "H", "number": 1, "x": 2, "y": 4},
    {"type": "V", "number": 1, "x": 4, "y": 2},
]


def game_loop(state):
    """
    Run this to start a game
    """
    # Initial player
    player = "V"

    while True:
        map_printer.print_state(state, N, M)
        input()
        player = "W" if player == "V" else "V"
        next_move_example_random(player, state)


def fight(attacker, defender, state):
    # TODO: implement real fighting rules

    winner = attacker if attacker['number'] >= defender['number'] else defender
    survivors = abs(attacker['number'] - defender['number'])
    return winner, survivors


def next_move_example_random(player, state):
    """
    Example of a choice of a next move
    Here the player moves all his pawns randomly
    """
    i = 0
    while i < len(state):
        el = state[i]
        if el['type'] == player:
            moveTo = [randomContiguous1D(
                el['x'], N), randomContiguous1D(el['y'], M)]
            objectAtLocation = findObjectAtLocation(
                moveTo[0], moveTo[1], state, el)
            if objectAtLocation:
                if objectAtLocation['type'] == 'H':
                    el['number'] += objectAtLocation['number']
                    el['x'], el['y'] = moveTo[0], moveTo[1]
                    state.remove(objectAtLocation)
                    continue
                elif objectAtLocation['type'] == player:
                    objectAtLocation['number'] += el['number']
                    state.remove(el)
                    continue
                else:
                    # case enemy
                    el['x'], el['y'] = moveTo[0], moveTo[1]
                    winner, survivors = fight(el, objectAtLocation, state)
                    state.remove(
                        objectAtLocation) if winner == el else state.remove(el)
                    winner['number'] = survivors
                    continue
            else:
                el['x'], el['y'] = moveTo[0], moveTo[1]

        i += 1

# UTILITIES
# =========


def findObjectAtLocation(x, y, state, movingObject):
    """
    Finds in the state if there is an object at location (x, y)
    """
    for el in state:
        if el['x'] == x and el['y'] == y:
            if el != movingObject:
                return el
    return None


def randomContiguous1D(x, size):
    """
    Return a random number in {x-1, x, x+1}, contained in the limit [0, size - 1]
    Used for the example of random moves
    """
    return min(max(x + random.randint(-1, 1), 0), size - 1)


game_loop(state)
