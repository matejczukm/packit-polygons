import datetime

import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os
# from mcts_simple import UCT, MCTS
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)
from our_packit.triangular_mode import frontend_interface as tri_fi
from our_packit.hexagonal_mode import frontend_interface as hex_fi
from our_packit.triangular_mode import data_convertions as tri_dc
sys.path.insert(0, './alpha-zero-general')
from HexGame import HexGame


def model_move(board, turn, game_mode):
    if game_mode == 'triangular':
        moves = tri_fi.get_possible_moves(board, turn)
    else:
        moves = hex_fi.get_possible_placements_for_turn(board, turn)
    # updated_board = board + random.choice(moves)
    # return updated_board
    if moves:
        return random.choice(moves)
    return np.zeros_like(board)


def hexagon(request):
    # current_turn = 1
    # context = {
    #     'current_turn': current_turn,
    # }
    return render(request, 'packitPolygons/hexagonal_board.html')


def index(request):
    # current_turn = 1
    # context = {
    #     'current_turn': current_turn,
    # }
    return render(request, 'packitPolygons/index.html')


# def apply_move(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         board = data['board']
#         move = data['move']
#         turn = data['turn']
#         return JsonResponse(tri_fi.perform_move(board, move, turn))


@csrf_exempt
def start_new_game(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data['ai_mode'])
        print(data['ai_starts'])
        board_size = data['board_size']
        mode = data['game_mode']
        if not data['ai_mode'] or not data['ai_starts']:
            if mode == 'triangular':
                return JsonResponse(tri_fi.start_game(int(board_size)))
            return JsonResponse(hex_fi.start_game(int(board_size)))

        # TODO: choose model and game based on the mode and board size

        if mode == 'triangular':
            board = tri_fi.get_board(board_size)
            move = model_move(board, 1, mode)
            board = tri_dc.convert_numpy_array_to_triangle(board)
            move = tri_dc.convert_numpy_array_to_triangle(move)
            return JsonResponse(tri_fi.perform_move(
                board=board,
                move=move,
                turn=2
            ))
        board = hex_fi.generate_board(board_size)
        move = model_move(board, 1, mode)
        board = hex_fi.numpy_board_to_list(board)
        move = hex_fi.numpy_board_to_list(move)
        return JsonResponse(hex_fi.perform_move(
            board=board,
            move=move,
            turn=2
        ))


@csrf_exempt
def confirm_move(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        board = data['board']
        move = data['move']
        turn = int(data['turn'])
        mode = data['game_mode']
        print(data)
        if not data['ai_mode']:
            if mode == 'triangular':
                return JsonResponse(tri_fi.perform_move(
                    board=board,
                    move=move,
                    turn=turn
                ))
            return JsonResponse(hex_fi.perform_move(
                board=board,
                move=move,
                turn=turn
            ))

        if mode == 'triangular':
            board_np = tri_dc.convert_triangle_to_numpy_array(board).astype(bool).astype(int)
            move_np = tri_dc.convert_triangle_to_numpy_array(move).astype(bool).astype(int)
            board_np = board_np + move_np
            next_move = model_move(board_np, turn, mode)
            board = tri_dc.convert_numpy_array_to_triangle(board_np)
            next_move = tri_dc.convert_numpy_array_to_triangle(next_move)
            return JsonResponse(tri_fi.perform_move(
                board=board,
                move=next_move,
                turn=turn+1
            ))

        board_np = hex_fi.list_board_to_numpy(board, 1).astype(bool).astype(int)
        move_np = hex_fi.list_board_to_numpy(move).astype(bool).astype(int)
        board_np = board_np + move_np
        next_move = model_move(board_np, turn, mode)
        board = hex_fi.numpy_board_to_list(board_np)
        next_move = hex_fi.numpy_board_to_list(next_move)
        return JsonResponse(hex_fi.perform_move(
            board=board,
            move=next_move,
            turn=turn + 1
        ))

