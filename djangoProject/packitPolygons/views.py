from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os
from mcts_simple import UCT, MCTS
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)
from our_packit.triangular_mode import frontend_interface as tri_fi
from our_packit.hexagonal_mode import frontend_interface as hex_fi
from our_packit.mcts_games import TriangularPackit

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
        if data['ai_mode'] is None:
            board_size = data['board_size']
            mode = data['game_mode']
            if mode == 'triangular':
                return JsonResponse(tri_fi.start_game(int(board_size)))
            return JsonResponse(hex_fi.start_game(int(board_size)))
        elif data['ai_mode'] == True:
            board_size = data['board_size']
            mode = data['game_mode']
            if board_size == 4:
                game = TriangularPackit(4)
                tree = MCTS(game, allow_transpositions=False, training=False)
                tree.load("ai_models/triangularPackit401.mcts")
                node = tree.root
                actions = game.possible_actions()
                if node is not None and len(node.children) > 0:
                    action = node.choose_best_action(tree.training)
                    node = node.children[action]
                else:
                    action = random.choice(actions)
                    node = None
                game.take_action(action)
        else:
            pass


@csrf_exempt
def confirm_move(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # print(data)
        board = data['board']
        # print(board)
        move = data['move']
        turn = data['turn']
        mode = data['game_mode']
        if mode == 'triangular':
            return JsonResponse(tri_fi.perform_move(
                board=board,
                move=move,
                turn=int(turn)
            ))
        return JsonResponse(hex_fi.perform_move(
            board=board,
            move=move,
            turn=int(turn)
        ))
