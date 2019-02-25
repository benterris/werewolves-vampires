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
        for state_line in self.states:
            if state_line['x'] == x and state_line['y'] == y:
                self.states.remove(state_line)
            break

    def update(self, changes):
        """
        Updates State using changes given in server communication format
        :param changes: list of lists [(x,y),humans,vampires,werewolves]
        :return: None
        """
        TYPES = ['H', 'V', 'W']
        for change in changes:
            state_line = dict()
            state_line['x'] = change[0][0]
            state_line['y'] = change[0][1]
            pos_number = next((item for item in enumerate(change[1:]) if item[1] is not 0),
                              False)  # Finds the first non null value and returns False if all null
            if pos_number:  # If a non null value is found
                state_line['type'] = TYPES[pos_number[0]]
                state_line['number'] = pos_number[1]
                self.states.append(state_line)
            else:  # If empty cell
                self.remove_by_pos(state_line['x'], state_line['y'])


if __name__ == '__main__':
    s = State(5, 10)
    s.update([[(9, 0), 2, 0, 0], [(4, 1), 0, 0, 4], [(2, 2), 4, 0, 0], [(9, 2), 1, 0, 0], [(4, 3), 0, 4, 0],
              [(9, 4), 2, 0, 0]])
    print(s)
    print('-------------------------')
    s.update([[(9, 0), 0, 0, 0]])
    print(s)

    pass
