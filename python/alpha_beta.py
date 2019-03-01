import pydash as _
import utilities
import config
from possible_plays import PossiblePlays
from Heuristic import Heuristic


class AlphaBeta:
    """
    Class to perform the alpha-beta algorithm
    TODO: add a layer of randomness between alpha / beta nodes
    """

    def get_best_next_state(self, state, player):
        """
        Return the best move for the player according to alpha-beta
        """
        _value, _state_path, best_action = self.max_value(
            state, -float('inf'), float('inf'), player, config.MAX_DEPTH)
        return best_action

    def max_value(self, state, alpha, beta, player, depth):
        """
        Computes the best possible value obtainable for the player maximising the heuristic
        Returns the value and the path of states to get there
        """
        current_player = 0
        positive_player = 0
        if depth == 0 or Heuristic.winned(state):
            # return utilities.heuristic(state, player), []
            # TODO: unify player name
            return Heuristic.heuristic(state, positive_player, current_player), []
        possible_actions = PossiblePlays.get_possible_plays(
            state, state.x_max, state.y_max, current_player)
        successors_with_action = [(PossiblePlays.get_next_states(
            state, action)[0], action) for action in possible_actions]

        value = alpha
        best_state_path = []
        best_action = None
        for s in successors_with_action:
            value, state_path = self.min_value(
                s[0], alpha, beta, utilities.other_player(player), depth - 1)
            if value > alpha:
                alpha = value
                best_state_path = [s[0]] + state_path
                best_action = s[1]
            if alpha >= beta:
                break
        return alpha, best_state_path, best_action

    def min_value(self, state, alpha, beta, player, depth):
        current_player = 1
        positive_player = 0
        if depth == 0 or Heuristic.winned(state):
            return Heuristic.heuristic(state, positive_player, current_player), []
        possible_actions = PossiblePlays.get_possible_plays(
            state, state.x_max, state.y_max, current_player)
        successors_with_action = [(PossiblePlays.get_next_states(
            state, action)[0], action) for action in possible_actions]
        # successors = utilities.next_states(state, player)
        value = beta
        best_state_path = []
        best_action = None
        for s in successors_with_action:
            value, state_path = self.max_value(
                s[0], alpha, beta, utilities.other_player(player), depth - 1)
            if value < beta:
                beta = value
                best_state_path = [s[0]] + state_path
                best_action = s[1]
            if alpha >= beta:
                break
        return beta, best_state_path, best_action

    # def random_node(self, states_with_probability, alpha, beta, player, depth):
    #     """
    #     [{state: {...}, proba: .15}, ...]

    #     """
    #     if player == 'A':
    #         # return value, path (path useless...)
    #         min_results = [self.min_value(s.get('state'), alpha, beta, utilities.other_player(
    #             player), depth) for s in states_with_probability]
    #         value = sum([states_with_probability[i].get('proba') * min_results[i][0]
    #                      for i in range(len(states_with_probability))])

    #         # TODO: take the most likely (here only the first)
    #         # maybe useless
    #         most_likely_path = min_results[0][1]

    #         return value, most_likely_path
    #     # Otherwise player is 'B'
    #     # return value, path (path useless...)
    #     max_results = [self.max_value(s.get('state'), alpha, beta, utilities.other_player(
    #         player), depth) for s in states_with_probability]
    #     value = sum([states_with_probability[i].get('proba') * max_results[i][0]
    #                  for i in range(len(states_with_probability))])

    #     # TODO: take the most likely (here only the first)
    #     most_likely_path = max_results[0][1]

    #     return value, most_likely_path
