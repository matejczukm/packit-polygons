from hexagon_action_space import *
import numpy as np


def numpy_board_to_list(board_np):
    board = []
    board_np = board_np.astype(int)
    n = board_np.shape[0]
    offset = int(
        np.floor(n / 2)
    )
    for i in range(offset + 1):
        board.append(board_np[i].tolist()[:n - offset + i])
    for i in range(offset):
        board.append(board_np[offset + 1 + i].tolist()[1 + i:])
    return board


def start_game(board_side):
    board_np = generate_board(board_side)  # np.ndarray


def perform_move():
    pass


def print_board(board):
    for row in board:
        print(row)


if __name__ == '__main__':
    pass
    # np_board = generate_board(5)
    # print(np_board)
    # board = numpy_board_to_list(np_board)
    # print_board(board)
