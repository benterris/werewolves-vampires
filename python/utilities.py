import pydash as _


def other_player(player):
    """
    Given a player ('A' or 'B'), return its opponent
    """
    return 'B' if player == 'A' else 'A'


def next_states(state, player):
    """
    Takes a state and return a list of states after `player` played
    """
    # TODO: implement
    # Match game example:
    _next = []
    for i in range(3):
        for j in range(state[i]):
            new_state = _.clone_deep(state)
            new_state[i] = j
            _next.append(new_state)
    return _next


def is_terminal(state):
    # TODO: implement
    # Match game example:
    return True if state == [0, 0, 0] else False


def heuristic(state, player):
    """
    A score of the given state, with `player` the next player to play
    """
    # TODO: implement
    # Match game example:
    # To win you must NOT take the last match
    if state == [0, 0, 0]:
        if player == 'A':
            return 1
        else:
            return -1
    return 0
