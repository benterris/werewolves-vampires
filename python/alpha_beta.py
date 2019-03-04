import pydash as _
import utilities
import config
from state import State
from possible_plays_improved import PossiblePlays
from Heuristic import Heuristic


class AlphaBeta:
    """
    Class to perform the alpha-beta algorithm
    """

    def __init__(self):
        self.nodes = config.MAX_NODES

    def __reset_nodes(self):
        self.nodes = config.MAX_NODES

    def get_best_next_action(self, state: State, player: str):
        """
        Return the best move for the player according to alpha-beta

        state: a State object
        player: 'V' or 'W'
        """
        self.__reset_nodes()

        _value, best_action_path = self.__max_value(
            state, -float('inf'), float('inf'), player, config.MAX_DEPTH)
        return best_action_path[0]

    def __max_value(self, state: State, alpha: float, beta: float, player: str, depth: int):
        """
        Computes the best possible value obtainable for the player maximising the heuristic
        Returns: the alpha value of the node and the action path to get this value
        """
        player_number = AlphaBeta.__convert_player_string_to_number(
            player)
        if depth == 0 or self.nodes <= 0 or Heuristic.is_terminal_state(state):
            return Heuristic.heuristic(state, player_number, player_number), []

        successors_with_action = AlphaBeta.__get_successors_with_actions(
            state, player_number)
        value = alpha
        best_action_path = []
        for s in successors_with_action:
            value, action_path = self.__min_value(
                State(state.x_max, state.y_max, s[0]), alpha, beta, utilities.other_player(player), depth - 1)
            if value > alpha:
                alpha = value
                best_action_path = [s[1]] + action_path
            if alpha >= beta:
                break
        self.nodes -= 1
        return alpha, best_action_path

    def __min_value(self, state, alpha, beta, player, depth):
        player_number = AlphaBeta.__convert_player_string_to_number(
            player)
        if depth == 0 or self.nodes <= 0 or Heuristic.is_terminal_state(state):
            return Heuristic.heuristic(state, 1 - player_number, player_number), []

        successors_with_action = AlphaBeta.__get_successors_with_actions(
            state, player_number)
        value = beta
        best_action_path = []
        for s in successors_with_action:
            value, action_path = self.__max_value(
                State(state.x_max, state.y_max, s[0]), alpha, beta, utilities.other_player(player), depth - 1)
            if value < beta:
                beta = value
                best_action_path = [s[1]] + action_path
            if alpha >= beta:
                break
        self.nodes -= 1
        return beta, best_action_path

    @staticmethod
    def __get_successors_with_actions(state: State, current_player: int):
        """
        Computes the next possibles states and actions from a given state

        returns: list of pairs (next_state, action)
        """
        possible_actions_generator = PossiblePlays.get_possible_plays(
            state, state.x_max, state.y_max, current_player)
        possible_actions = AlphaBeta.__first_items(
            possible_actions_generator, config.MAX_ACTIONS)
        successors_with_action = [(PossiblePlays.get_next_states(
            state, action)[0][0], action) for action in possible_actions]
        return successors_with_action

    @staticmethod
    def __first_items(generator, n_items):
        """
        Get the first n_items items of a generator
        """
        items = []
        for _ in range(n_items):
            try:
                items.append(next(generator))
            except StopIteration:
                break
        return items

    @staticmethod
    def __convert_player_string_to_number(player: str):
        """
        (In the heuristic code we have 0 for V's and 1 for W's)
        Translate the player string to the corresponding number
        """
        return 0 if player == 'V' else 1

    # TODO: add random nodes (WIP)
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
