from .Color import Color

class Player:
    def __init__(self, color: Color, name: str=""):
        self._color: Color = color
        self._name: str = name

    @property
    def color(self):
        return self._color

    @property
    def name(self):
        return self._name

    def make_move(self):
        """Ask the player to make a move. Return a tuple of (row, column).
        """
        pass