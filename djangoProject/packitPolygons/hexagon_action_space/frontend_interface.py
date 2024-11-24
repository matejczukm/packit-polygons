import json

from .hexagons_game_logic import *
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


def list_board_to_numpy(board, value=0):
    n = len(board)
    offset = int(
        np.floor(n / 2)
    )
    for i in range(offset):
        board[i].extend([value] * (offset - i))
    for i in range(offset):
        board[offset + 1 + i] = [value] * (i + 1) + board[offset + 1 + i]

    return np.array(board)


def start_game(board_side):
    board_np = generate_board(board_side)  # np.ndarray
    possible_moves = get_possible_placements_for_turn(board_np, 1)
    # possible_moves = [
    #     numpy_board_to_list(placement) for placement in get_possible_placements_for_turn(board_np, 1)
    # ]
    return {
        'board': numpy_board_to_list(board_np),
        'moves': [
            json.dumps(numpy_board_to_list(move), separators=(',', ': ')) for move in possible_moves
        ]
    }


def perform_move(board, move, turn):
    print(board)
    board_np = list_board_to_numpy(board, 1)
    board_np = board_np.astype(bool).astype(int)
    print(board_np)
    move_np = list_board_to_numpy(move)

    board_np = place_polygon(board_np, move_np)
    possible_moves = get_possible_placements_for_turn(board_np, turn)

    return {
        'board': numpy_board_to_list(board_np),
        'moves': [
            json.dumps(numpy_board_to_list(move * turn), separators=(',', ': ')) for move in
            possible_moves
        ]
    }


def print_board(board):
    for row in board:
        print(row)


if __name__ == '__main__':
    pass
    # np_board = generate_board(5)
    # print(np_board)
    # board = numpy_board_to_list(np_board)
    # print_board(board)
    # print(list_board_to_numpy(board))
