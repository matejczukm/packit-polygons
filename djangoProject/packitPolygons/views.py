import datetime

import numpy as np
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os
from .models import Game
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
from PackitAIPlayer import AIPlayer

# ai = AIPlayer(4, 'triangular')
ai_players = {}


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
    return render(request, 'packitPolygons/hexagonal_board.html')


def index(request):
    return render(request, 'packitPolygons/index.html')


@csrf_exempt
def save_game(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        game = Game(
            size=data['board_size'],
            board=data['board'],
            turns=data['turns'],
            triangular_mode=data['game_mode'] == 'triangular',
            ai_mode=data['ai_mode'],
            ai_starts=data['ai_starts'] if data['ai_mode'] else None
        )
        game.save()
        return HttpResponse(status=204)

@csrf_exempt
def start_new_game(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        board_size = data['board_size']
        mode = data['game_mode']
        if not data['ai_mode'] or not data['ai_starts']:
            if mode == 'triangular':
                return JsonResponse(tri_fi.start_game(int(board_size)))
            return JsonResponse(hex_fi.start_game(int(board_size)))

        model_name = mode + str(board_size)
        if model_name not in ai_players:
            ai_players[model_name] = AIPlayer(board_size, mode)
        ai_player = ai_players[model_name]
        if mode == 'triangular':
            board = tri_fi.get_board(board_size)
            move = ai_player.mcts_get_action(board, 1)
            board = tri_dc.convert_numpy_array_to_triangle(board)
            move = tri_dc.convert_numpy_array_to_triangle(move)
            return JsonResponse(tri_fi.perform_move(
                board=board,
                move=move,
                turn=2
            ))
        board = hex_fi.generate_board(board_size)
        move = ai_player.mcts_get_action(board, 1)
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
        # print(data)
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
        board_size = len(board[-1]) if mode == 'hexagonal' else len(board)

        model_name = mode + str(board_size)
        if model_name not in ai_players:
            ai_players[model_name] = AIPlayer(board_size, mode)
        ai_player = ai_players[model_name]
        if mode == 'triangular':
            board_np = tri_dc.convert_triangle_to_numpy_array(board).astype(bool).astype(int)
            move_np = tri_dc.convert_triangle_to_numpy_array(move).astype(bool).astype(int)
            board_np = board_np + move_np
            # print(board_np)
            next_move = ai_player.mcts_get_action(board_np, turn)
            board = tri_dc.convert_numpy_array_to_triangle(board_np)
            next_move = tri_dc.convert_numpy_array_to_triangle(next_move)
            return JsonResponse(tri_fi.perform_move(
                board=board,
                move=next_move,
                turn=turn + 1
            ))

        board_np = hex_fi.list_board_to_numpy(board, 1).astype(bool).astype(int)
        move_np = hex_fi.list_board_to_numpy(move).astype(bool).astype(int)
        board_np = board_np + move_np
        next_move = ai_player.mcts_get_action(board_np, turn)
        board = hex_fi.numpy_board_to_list(board_np)
        next_move = hex_fi.numpy_board_to_list(next_move)
        return JsonResponse(hex_fi.perform_move(
            board=board,
            move=next_move,
            turn=turn + 1
        ))
