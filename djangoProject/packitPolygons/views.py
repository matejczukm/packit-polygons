from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import json
import polygonal_packit.game_core.frontend_interface as packit
# from .ai_players_registry import AIPlayerRegistry


def hexagon(request):
    return render(request, 'packitPolygons/hexagonal_board.html')


def index(request):
    return render(request, 'packitPolygons/index.html')


def start_new_game(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse(
            packit.start_new_game(data['board_size'],
                                  data['game_mode'],
                                  data['ai_mode'],
                                  data['ai_starts'],
                                  # AIPlayerRegistry.get_players()
                                  )
        )


def confirm_move(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse(
            packit.confirm_move(data['board'], data['move'], data['turn'], data['game_mode'], data['ai_mode'])
        )
