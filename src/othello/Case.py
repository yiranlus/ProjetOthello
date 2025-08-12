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

if __name__ == "__main__":
    import numpy as np
    from othello.Pawn import Pawn

    f = lambda x: x.pawn.color if x.pawn else (-1)
    f_vec = np.vectorize(f)

    board = np.empty((8,8), dtype=Case)
    for i in range(8):
        for j in range(8):
            board[i,j] = Case()
    board[3,3].pawn = Pawn(1)
    board[3,4].pawn = Pawn(0)
    board[4,3].pawn = Pawn(0)
    board[4,4].pawn = Pawn(1)

    print(f_vec(board))