from .Player import Player

class HumanPlayer(Player):
    def __init__(self, color, name=""):
        super().__init__(color, name)

    def make_move(self):
        coord = input("Your movement: ")
        if ord("A") <= ord(coord[0]) <= ord("H"):
            c = ord(coord[0]) - ord("A")
        if ord("1") <= ord(coord[1]) <= ord("8"):
            r = ord(coord[1]) - ord("1")

        return (c, r)


if __name__ == "__main__":
    h = HumanPlayer(1, "Alexis")
    x = h.make_move()
    print(x)