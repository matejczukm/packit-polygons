from .game_logic import get_possible_placements, get_board
import numpy as np


def get_max_turns(n):
    return int((np.sqrt(1+8*n**2) - 1) / 2)


def get_whole_action_space(n):
    actions = []
    board = get_board(n)
    for i in range(1, get_max_turns(n)+1):
        actions.extend(get_possible_placements(board, i, as_list=True))

    return np.array(actions)


if __name__ == '__main__':
    print(get_whole_action_space(4))
