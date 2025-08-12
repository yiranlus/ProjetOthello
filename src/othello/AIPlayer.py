from .Player import Player

class AIPlayer(Player):
    def __init__(self, color, name=""):
        super().__init__(color, name)

    def make_move(self):
        raise NotImplemented()