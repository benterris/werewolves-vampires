import utilities

MAX_DEPTH = 100  # TODO: load this from a config file


class AlphaBeta:

    def get_best_next_state(self, state, player):
        """
        Return the best move for the player according to alpha-beta
        """
        value, state_path = self.max_value_ab(
            state, -float('inf'), float('inf'), player, MAX_DEPTH)
        return state_path[0]

    def max_value_ab(self, state, alpha, beta, player, depth):
        """
        Computes the best possible value obtainable for the player maximising the heuristic
        Returns the value and the path of states to get there
        """
        if depth == 0 or utilities.is_terminal(state):
            return utilities.heuristic(state, player), []
        successors = utilities.next_states(state, player)
        value = alpha
        best_state_path = []
        for s in successors:
            value, state_path = self.min_value_ab(
                s, alpha, beta, utilities.other_player(player), depth - 1)
            if value > alpha:
                alpha = value
                best_state_path = [s] + state_path
            if alpha >= beta:
                break
        return alpha, best_state_path

    def min_value_ab(self, state, alpha, beta, player, depth):
        if depth == 0 or utilities.is_terminal(state):
            return utilities.heuristic(state, player), []
        successors = utilities.next_states(state, player)
        value = beta
        best_state_path = []
        for s in successors:
            value, state_path = self.max_value_ab(
                s, alpha, beta, utilities.other_player(player), depth - 1)
            if value < beta:
                beta = value
                best_state_path = [s] + state_path
            if alpha >= beta:
                break
        return beta, best_state_path
