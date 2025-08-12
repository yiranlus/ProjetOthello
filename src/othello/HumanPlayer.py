from Player import Player

class HumanPlayer(Player):
    def __init__(self, color, name=""):
        super().__init__(color, name)

    def make_move(self):
        color_name = "black" if self.color == 0 else "white"
        circle = "\u2b24" if self.color == 0 else "\u25ef"
        coord = input(f"Your movement ({self.name}, {color_name} {circle}): ")
        if ord("A") <= ord(coord[0]) <= ord("H"):
            c = ord(coord[0]) - ord("A")
        if ord("1") <= ord(coord[1]) <= ord("8"):
            r = ord(coord[1]) - ord("1")

        return (r, c)


if __name__ == "__main__":
    h = HumanPlayer(1, "Alexis")
    x = h.make_move()
    print(x)