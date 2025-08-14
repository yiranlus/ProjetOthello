from .Color import Color

class Pawn:
    def __init__(self, color: Color):
        """Create a pawn of `color`.

        Args:
            color (Color)
        """
        self._color: Color = color

    @property
    def color(self):
        return self._color

    def flip(self):
        """Flip the color of the pawn.
        """
        self._color = self._color.switch()

if __name__ == "__main__":
    p = Pawn(Color.BLACK)
    print("color of pawn:", p.color)
    p.flip()
    print("color of pawn:", p.color)