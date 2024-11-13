from game_logic import place_polygon, get_possible_moves, get_board
import json
import data_convertions as dc


def start_game(board_size):
    board = get_board(board_size)
    possible_moves = get_possible_moves(board, 1)
    return {
        'board' : dc.convert_numpy_array_to_triangle(board),
        'moves' : [str(dc.convert_numpy_array_to_triangle(move)) for move in possible_moves]
    }

def perfor_move(board, move, turn):
    board_np = dc.convert_triangle_to_numpy_array(board)
    move_np = dc.convert_triangle_to_numpy_array(move)

    board_np = place_polygon(board_np, move_np)
    possible_moves = get_possible_moves(board_np, turn)

    return {
        'board' : dc.convert_numpy_array_to_triangle(board_np),
        'moves' : [str(dc.convert_numpy_array_to_triangle(move)) for move in possible_moves]
    }


if __name__ == '__main__':
    print(start_game(3))