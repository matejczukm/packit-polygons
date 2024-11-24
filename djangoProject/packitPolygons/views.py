from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .triangle_action_space import frontend_interface as tri_fi
from .hexagon_action_space import frontend_interface as hex_fi
import json


def hexagon(request):
    current_turn = 1
    # context = {
    #     'current_turn': current_turn,
    # }
    return render(request, 'packitPolygons/hexagonal_board.html')


def index(request):
    current_turn = 1
    context = {
        'current_turn': current_turn,
    }
    return render(request, 'packitPolygons/index.html', context)


def apply_move(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        board = data['board']
        move = data['move']
        turn = data['turn']
        return JsonResponse(tri_fi.perform_move(board, move, turn))


@csrf_exempt
def start_new_game(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        board_size = data['board_size']
        mode = data['game_mode']
        if mode == 'triangular':
            return JsonResponse(tri_fi.start_game(int(board_size)))
        return JsonResponse(hex_fi.start_game(int(board_size)))


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

