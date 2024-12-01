import json

from .game_logic import *
import numpy as np


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
    # print(board)
    board_np = list_board_to_numpy(board, 1)
    # Convert the board from turn numbers to binary (0s and 1s) for backend processing
    board_np = board_np.astype(bool).astype(int)
    # print(board_np)
    move_np = list_board_to_numpy(move)
    move_np = move_np.astype(bool).astype(int)

    board_np = place_polygon(board_np, move_np)
    possible_moves = get_possible_placements_for_turn(board_np, turn)
    # print(possible_moves)

    return {
        'board': numpy_board_to_list(board_np),
        'moves': [
            json.dumps(numpy_board_to_list(move * turn), separators=(',', ': ')) for move in
            possible_moves
        ]
    }


if __name__ == '__main__':
    pass
    # np_board = generate_board(5)
    # print(np_board)
    # board = numpy_board_to_list(np_board)
    # print_board(board)
    # print(list_board_to_numpy(board))
