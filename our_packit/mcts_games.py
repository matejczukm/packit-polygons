from typing import Any
from mcts_simple import Game
import numpy as np

from our_packit.triangular_mode.display import print_board
import our_packit.triangular_mode.game_logic as tgc


class TriangularPackit(Game):
    def __init__(self, board_size):
        self.board = tgc.get_board(board_size)
        self.players = [0, 1]
        self.turn = 1
        self._update_actions()

    def _update_actions(self):
        self.possible_actions_list = tgc.get_possible_moves(self.board, self.turn)

    def render(self):
        print_board(self.board)

    def get_state(self):
        return np.copy(self.board)

    def number_of_players(self):
        return len(self.players)

    def current_player(self):
        return (self.turn + 1) % 2

    def possible_actions(self):
        return list(range(len(self.possible_actions_list)))

    def take_action(self, action: int):
        self.board = tgc.place_polygon(self.board, self.possible_actions_list[action])
        self.turn += 1
        self._update_actions()

    def has_outcome(self):
        return len(self.possible_actions_list) == 0

    def winner(self):
        return [self.players[self.turn % 2]]

