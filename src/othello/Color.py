from __future__ import annotations
from enum import Enum

class Color(Enum):
    WHITE = 1
    BLACK = 0

    def __str__(self):
        circle = "\u2b24" if self == Color.BLACK else "\u25ef"
        return f"{self.name.lower()} {circle}"

    def switch(self) -> Color:
        """return the other color.

        Returns:
            Color: the other color.
        """
        if self == Color.BLACK:
            return Color.WHITE
        return Color.BLACK

if __name__ == "__main__":
    c = Color.BLACK

    print(c)
    print(c.switch())