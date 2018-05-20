# coding=utf-8

"""
Implementation of HillClimbing algorithm to solve below problem


1091/5000
One company desire to build an internal computer network, installing machines in several rooms (12 machines in all).
Each computer will be connected to two others, except the first and last (which are connected to only one other
computer). Not all combinations of connections between computers are possible. Table 3 below shows the connection
possibilities (the dash (-) indicates that there is no possible connection between the indicated computers). The
company wants to make these connections in order to save the cable (in meters). We are facing an optimization problem.

The operator considered to generate the successors of the current state is only the permutation of the current order of
connections between computers two by two, without testing all combinations in the same iteration. For example, given
the initial state:
E1 (C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12)

The permutations in an iteration would be:
E1 (C2, C1, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12)
E2 (C1, C3, C2, C4, C5, C6, C7, C8, C9, C10, C11, C12)
E3 (C1, C2, C4, C3, C5, C6, C7, C8, C9, C10, C11, C12) etc ...

"""
import random
import sys

COMPUTER_DISTANCES = {
    'C1,C2': 30, 'C1,C3': 84, 'C1,C4': 56, 'C1,C6': 70, 'C1,C8': 75, 'C1,C10': 40, 'C1,C12': 10, 'C2,C3': 65,
    'C2,C7': 70, 'C2,C10': 40, 'C3,C4': 60, 'C3,C5': 52, 'C3,C6': 55, 'C3,C8': 135, 'C3,C9': 143, 'C3,C10': 48,
    'C3,C11': 25, 'C4,C5': 135, 'C4,C8': 20, 'C4,C11': 58, 'C5,C6': 70, 'C5,C8': 122, 'C5,C9': 98, 'C5,C10': 80,
    'C6,C7': 68, 'C6,C9': 82, 'C6,C10': 35, 'C6,C12': 130, 'C7,C8': 40, 'C7,C9': 120, 'C7,C10': 57, 'C8,C9': 89,
    'C8,C11': 45, 'C9,C10': 23, 'C9,C12': 68, 'C10,C11': 10, 'C11,C12': 14
}


class Entry(object):
    """
    Default entry with representation (positions sequence) and its value.
    """

    def __init__(self, positions_sequence):
        self.positions_sequence = positions_sequence
        self.value = sys.maxsize

    def __eq__(self, other):
        return other.positions_sequence == self.positions_sequence

    def __str__(self):
        return str(self.positions_sequence)

    def evaluate_function(self):
        """
        Evaluate entry. In the problem, it is the distance between sequence of Computers
        :param entry: Entry
        :return: value of entry
        """
        value = 0
        for pos in range(len(self.positions_sequence)-1):
            a = self.positions_sequence[pos]
            b = self.positions_sequence[pos+1]
            if a and b and '{},{}'.format(a, b) in COMPUTER_DISTANCES:
                value += COMPUTER_DISTANCES.get('{},{}'.format(a, b))
            elif a and b and '{},{}'.format(b, a) in COMPUTER_DISTANCES:
                value += COMPUTER_DISTANCES.get('{},{}'.format(b, a))
            else:
                # print('It was not possible to find possible connection between {} and {} in {}'.format(a, b, self))
                value = -1
                return
        # print('{} has value {}'.format(self, value))
        self.value = value


def get_random_init(position_set):
    """
    Get random initial position
    :param position_set: list of positions
    :return: random position of set
    """
    random.shuffle(position_set)
    entry = Entry(position_set)
    entry.evaluate_function()
    while entry.value == sys.maxsize:
        random.shuffle(position_set)
        entry = Entry(position_set)
        entry.evaluate_function()
    return entry


def permute_positions(entry):
    """
    Permute positions of entry
    :param entry: Entry
    :return:
    """
    permuted_positions_entries = []
    for pos in range(len(entry.positions_sequence) - 1):
        new_entry = Entry(entry.positions_sequence[:])
        swap_item = new_entry.positions_sequence[pos]
        new_entry.positions_sequence[pos] = new_entry.positions_sequence[pos + 1]
        new_entry.positions_sequence[pos + 1] = swap_item
        permuted_positions_entries.append(new_entry)

    return permuted_positions_entries


def get_best_neighbor(position):
    """
    Get best neighbor from position
    :param position:
    :return:
    """
    neighboors = permute_positions(position)
    best_neighbor = None
    for entry in neighboors:
        entry.evaluate_function()
        best_neighbor = best_neighbor if (best_neighbor and best_neighbor.value <= entry.value) else entry

    return best_neighbor


def hill_climbing(init, valid_set):
    """
    Hill Climbing function

    function HILL-CLIMBING(problem) returns a state that is a local maximum
    current ← MAKE-NODE(problem.INITIAL-STATE)
    loop do
        neighbor ← a highest-valued successor of current
        if neighbor.VALUE ≤ current.VALUE then return current.STATE
            current ← neighbor

    :param init: initial position
    :param valid_set: set of valid positions
    :return: optimum local or optimum global
    """
    climbing = True
    current = init or get_random_init(valid_set)
    current.evaluate_function()
    while True:
        best_neighbor = get_best_neighbor(current)
        if (best_neighbor and current) and best_neighbor.value >= current.value:
            return current
        elif not best_neighbor:
            return current
        current = best_neighbor
        print('==== {} - {} ===='.format(
            current, current.value)
        )


def main():
    """
    Main method to algorithm
    :return:
    """
    initial_position = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12'] # 604
    # initial_position = ['C8', 'C5', 'C4', 'C1', 'C12', 'C11', 'C3', 'C6', 'C9', 'C7', 'C10', 'C2'] # 716
    # initial_position = ['C5', 'C6', 'C10', 'C7', 'C9', 'C12', 'C11', 'C8', 'C4', 'C3', 'C2', 'C1'] # 584
    # initial_position = ['C4', 'C8', 'C7', 'C2', 'C1', 'C12', 'C11', 'C3', 'C5', 'C6', 'C10', 'C9'] # 389

    # initial_entry = Entry(initial_position)
    # initial_entry.evaluate_function()
    max = None
    while not max or max.value > 389: # best value registered
        max = hill_climbing(None, initial_position)

    # max = hill_climbing(initial_entry, None)

    print('\nThe best option is {} with value equals to {}'.format(max, max.value))


if __name__ == '__main__':
    main()
