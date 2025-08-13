class Case:
    EMPTY = -1

    def __init__(self, pawn=None):
        self._pawn = pawn

    @property
    def pawn(self):
        return self._pawn

    @pawn.setter
    def pawn(self, value):
        self._pawn = value

    def __int__(self):
        if self._pawn:
            return self._pawn.color.value
        return -1

    @property
    def is_empty(self):
        return self._pawn is None

if __name__ == "__main__":
    import numpy as np

    a = np.zeros((2,2), dtype=int)
    a[0,0] = Case()
    print(a)