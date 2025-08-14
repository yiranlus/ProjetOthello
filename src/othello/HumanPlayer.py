from math import dist
from numpy import argmin
from matplotlib.pyplot import ginput

from .Color import Color
from .Player import Player
#from pynput.mouse import Listener

class HumanPlayer(Player):
    def __init__(self, color: Color, name: str=""):
        """Create a human player.

        Args:
            color (Color): the color the player play.
            name (str, optional): the name of the player. Defaults to "".
        """
        super().__init__(color, name)

    def make_move(self, fig=None):
        locs = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]
        x_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        centers = [(i,j) for i in locs for j in locs]

        is_good_coord = False

        r, c = 0, 0
        while not is_good_coord:
            try:
                if fig is None:
                    coord = input(f"Your movement ({self.name}, {self.color})(to quit, type q): ")
                else:
                    coord_click = ginput(1)
                    dist_center = [dist((coord_click[0][0], coord_click[0][1]),i) for i in centers]
                    ind_min = argmin(dist_center)
                    col = x_labels[ind_min // 8]
                    row = str(1+(ind_min %8))
                    coord = col+row
                if coord == "q":
                    print("Game terminated.")
                    exit(0)
                if len(coord) != 2:
                    raise ValueError()
                if ord("A") <= ord(coord[0]) <= ord("H"):
                    c = ord(coord[0]) - ord("A")
                elif ord("a") <= ord(coord[0]) <= ord("h"):
                    c = ord(coord[0]) - ord("a")
                else:
                    raise ValueError()
                if ord("1") <= ord(coord[1]) <= ord("8"):
                    r = ord(coord[1]) - ord("1")
                else:
                    raise ValueError()
            except ValueError:
                print("Not good move! Reenter, please!")
            else:
                is_good_coord = True

        return r, c


if __name__ == "__main__":
    h = HumanPlayer(Color.BLACK, "Alexis")
    x = h.make_move()
    print(x)