from django.shortcuts import render
import json
from django.http import JsonResponse
# from ...trianglesActionSpace.frontend_interface import start_game, perform_move
# from packit_polygons.trianglesActionSpace.frontend_interface import start_game, perform_move

# import importlib
# frontend_interface = importlib.import_module('trianglesActionSpace.frontend_interface')
# start_game = frontend_interface.start_game
# perform_move = frontend_interface.perform_move


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


# def apply_move(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         board = data['board']
#         move = data['move']
#         turn = data['turn']
#         return JsonResponse(perform_move(board, move, turn))


# def start_new_game(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         board_size = data['board_size']
#         return JsonResponse(start_game(int(board_size)))
