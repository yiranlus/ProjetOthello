class Pawn:
    def __init__(self, color: int):
        """create a pawn of `color`.

        Args:
            color (int): 0 for black pawn, 1 for white pawn
        """
        self._color = color

    @property
    def color(self):
        return self._color

    def flip(self):
        if self._color == 0:
            self._color = 1
        else:
            self._color = 0

if __name__ == "__main__":
    p = Pawn(1)
    print("color of pawn:", p.color)
    p.flip()
    print("color of pawn:", p.color)