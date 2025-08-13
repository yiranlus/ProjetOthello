from enum import Enum
class Color(Enum):
    WHITE = 1
    BLACK = 0

    def __str__(self):
        return self.name.lower()

    def switch(self):
        if self == Color.BLACK:
            return Color.WHITE
        return Color.BLACK

if __name__ == "__main__":
    c = Color.BLACK

    print(c)
    print(c.switch())