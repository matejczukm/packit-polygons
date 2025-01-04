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
# from our_packit.triangular_mode import frontend_interface as tri_fi
# from our_packit.hexagonal_mode import frontend_interface as hex_fi
# from our_packit.triangular_mode import data_conversions as tri_dc
# from our_packit.hexagonal_mode import data_conversions as hex_dc
#
# sys.path.insert(0, './alpha-zero-general')
# from PackitAIPlayer import AIPlayer
#
# # ai = AIPlayer(4, 'triangular')
# ai_players = {}

from our_packit import frontend_interface as packit_fi


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
        return JsonResponse(
            packit_fi.start_new_game(data['board_size'], data['game_mode'], data['ai_mode'], data['ai_starts'])
        )


@csrf_exempt
def confirm_move(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse(
            packit_fi.confirm_move(data['board'], data['move'], data['turn'], data['game_mode'], data['ai_mode'])
        )
