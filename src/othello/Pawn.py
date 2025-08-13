from .Color import Color

class Pawn:
    def __init__(self, color: Color):
        """create a pawn of `color`.

        Args:
            color (Color)
        """
        self._color: Color = color

    @property
    def color(self):
        return self._color

    def flip(self):
        if self._color == Color.BLACK:
            self._color = Color.WHITE
        else:
            self._color = Color.BLACK

if __name__ == "__main__":
    p = Pawn(Color.BLACK)
    print("color of pawn:", p.color)
    p.flip()
    print("color of pawn:", p.color)