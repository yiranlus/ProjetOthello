class Player:
    def __init__(self, color, name=""):
        self._color = color
        self._name = name

    @property
    def color(self):
        return self._color

    @property
    def name(self):
        return self._name

    def make_move(self):
        """Ask the player to make a move. Return a tuple of (row, column).
        """
        raise NotImplementedError()