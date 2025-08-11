class Case:
    def __init__(self, pawn=None):
        self._pawn = pawn

    @property
    def pawn(self):
        return self._pawn

    @pawn.setter
    def pawn(self, value):
        self._pawn = value

    @property
    def is_empty(self):
        return self._pawn is None