import pydash as _
import utilities


def minimax(state, player):
    return max([min_value(next_state, utilities.other_player(player)) for next_state in next_states(state, player)])


def min_value(state, player):
    if utilities.is_terminal(state):
        return utilities.heuristic(state, utilities.other_player(player))
    successors = utilities.next_states(state, player)
    return min([max_value(next_state, utilities.other_player(player)) for next_state in successors])


def max_value(state, player):
    if utilities.is_terminal(state):
        return utilities.heuristic(state, utilities.other_player(player))
    successors = utilities.next_states(state, player)
    return max([min_value(next_state, utilities.other_player(player)) for next_state in successors])
