import random


class State:
    def __init__(self, x_max, y_max):
        """
        initiates State class and defines its states to empty list
        :param x_max: maximum x bound
        :param y_max: maximum y bound
        """
        self.x_max = x_max
        self.y_max = y_max
        self.states = []

    def __getitem__(self, pos):
        return self.states[pos]

    def __repr__(self):
        """
        represents State object by its states
        :return: State representation
        """
        text = ''
        for state in self.states:
            text += str(state) + '\n'
        return text

    def __str__(self):
        """
        represents State object by its states
        :return: State representation
        """
        return self.__repr__()

    def remove_by_pos(self, x, y):
        """
        clears a cell given its coordinates
        :param x: x coordinate of the new empty cell
        :param y: y coordinate of the new empty cell
        :return: None
        """
        try:
            self.states.remove(self.findObjectAtLocation(x, y))
        except ValueError:
            raise ValueError('Cannot clear cell ({},{})'.format(x, y))

    # =========
    # UTILITIES
    # =========

    def randomContiguous1D(self, pos):
        # TODO watchout, this may go out of the map boundaries
        """
        Return a random number in {x-1, x, x+1}, contained in the limit [0, size - 1]
        Used for the example of random moves
        """
        possible_add = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        while True:
            toAdd = possible_add[random.randint(0, len(possible_add) - 1)]
            if pos[0] + toAdd[0] <= self.x_max-1 and pos[1] + toAdd[1] <= self.y_max-1 and pos[0] + toAdd[0] >= 0 and pos[
                1] + toAdd[1] >= 0:
                print('move from', pos[0], pos[1], ' To', pos[0] + toAdd[0], pos[1] + toAdd[1],'-----', self.x_max-1, self.y_max-1)
                return pos[0] + toAdd[0], pos[1] + toAdd[1]

    def findObjectAtLocation(self, x, y):
        """
        Finds in the state if there is an object at location (x, y)
        """
        for el in self.states:
            if el['x'] == x and el['y'] == y:
                return el
        return None

    def next_move_example_random(self, player):
        """
        Example of a choice of a next move
        Here the player moves all his pawns randomly
        """
        i = 0
        mov_list = []
        while i < len(self.states):
            el = self[i]
            if el['type'] == player:
                moveTo = self.randomContiguous1D((el['x'], el['y']))
                mov_list.append((player, el['number'], (el['x'], el['y']), moveTo))
            i += 1
        return mov_list

    def update(self, changes):
        """
        Updates State using changes given in server communication format
        :param changes: list of lists [(x,y),humans,vampires,werewolves]
        :return: None
        """
        types = ['H', 'V', 'W']
        for change in changes:
            state_line = dict()
            state_line['x'] = change[0][0]
            state_line['y'] = change[0][1]
            pos_number = next((item for item in enumerate(change[1:]) if item[1] != 0),
                              False)  # Finds the first non null value and returns False if all null
            if pos_number:  # If a non null value is found
                state_line['type'] = types[pos_number[0]]
                state_line['number'] = pos_number[1]
                occupied_cell = self.findObjectAtLocation(state_line['x'], state_line['y'])
                if occupied_cell:  # If the cell is already in states, remove it
                    self.states.remove(occupied_cell)
                self.states.append(state_line)
            else:  # If empty cell
                self.remove_by_pos(state_line['x'], state_line['y'])


if __name__ == '__main__':
    s = State(5, 10)
    s.update([[(9, 0), 2, 0, 0], [(4, 1), 0, 0, 4], [(2, 2), 4, 0, 0], [(9, 2), 1, 0, 0], [(4, 3), 0, 4, 0],
              [(9, 4), 2, 0, 0]])
    print(s)
    print('-------------------------')
    print(s.next_move_example_random('V'))
    pass
