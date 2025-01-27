class AIPlayerRegistry:
    _ai_players = {}

    @classmethod
    def add_player(cls, name, player):
        cls._ai_players[name] = player

    @classmethod
    def get_players(cls):
        return cls._ai_players

    @classmethod
    def get_player(cls, name):
        return cls._ai_players.get(name)