from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .trianglesActionSpace.frontend_interface import start_game, perform_move
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
        return JsonResponse(perform_move(board, move, turn))


@csrf_exempt
def start_new_game(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        board_size = data['board_size']
        return JsonResponse(start_game(int(board_size)))


@csrf_exempt
def confirm_move(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # print(data)
        board = data['board']
        move = data['move']
        turn = data['turn']
        return JsonResponse(perform_move(
            board=board,
            move=move,
            turn=int(turn)
        ))
