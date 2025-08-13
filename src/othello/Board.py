import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from typing import Optional

from .Direction import Direction
from .Color import Color
from .Pawn import Pawn
from .Case import Case

class Board:
    def __init__(self, board_arr: Optional[np.ndarray]=None):
        self.rows = 8
        self.cols = 8

        # initialize empty board
        if board_arr is not None:
            self._board = board_arr
        else:
            self._board = np.full((self.rows, self.cols), Case.EMPTY, dtype=int)

            # initialize 4 center squares
            self._board[3,3] = Color.WHITE.value
            self._board[3,4] = Color.BLACK.value
            self._board[4,3] = Color.BLACK.value
            self._board[4,4] = Color.WHITE.value

        f = lambda x: x.pawn.color.value if x.pawn else Case.EMPTY
        self.f_vec = np.vectorize(f)


    def place_pawn(self, r, c, color: Color):
        """Place a pawn on the board.

        Args:
            r (int): the row position of the pawn
            c (int): the column position of the pawn
            color (Color): The color of the pawn
        """
        self._board[r, c] = color.value

    def update_board(self, r, c, color: Color):
        """Update the pawn after placing a pawn

        Args:
            r (int): the row position of the pawn
            c (int): the column position of the pawn
            color (Color): the color of the pawn
        """
        for direction in Direction:
            dr, dc = direction.value

            if ((r + dr < 0) | (r + dr >= self.rows) |
                (c + dc < 0) | (c + dc >= self.cols)):
                continue

            if self._board[r + dr, c + dc] == Case.EMPTY:
                continue
            elif self._board[r + dr, c + dc] != color.value:
                self.flip_sandwiches(r, c, color, dr, dc)


    def flip_sandwiches(self, r, c, color, dr, dc):
        """Flip the pawn based on the position and the direction.

        Args:
            r (int): the row position of the pawn
            c (int): the column position of the pawn
            color (Color): the color of the pawn
            dr (int): the direction along the row axis
            dc (int): the direction along the column axis
        """
        color_c = self._board[r + dr, c + dc]
        count = 0

        idx_ls = []
        while color_c != color.value:
            count += 1

            if ((r + dr * count < 0) | (r + dr * count >= self.rows) |
                (c + dc * count < 0) | (c + dc * count >= self.cols)):
                color_c = color.value
                continue

            if self._board[r + dr * count, c + dc * count] == Case.EMPTY:
                color_c = color.value
                continue

            if self._board[r + dr * count, c + dc * count] != color.value:
                idx_ls.append((r + dr * count, c + dc * count))

            elif self._board[r + dr * count, c + dc * count] == color.value:
                for idx in idx_ls:
                    r_idx = idx[0]
                    c_idx = idx[1]
                    self._board[r_idx, c_idx] = (self._board[r_idx, c_idx] + 1) % 2
                color_c = color.value
            else:
                color_c = color.value

    @property
    def board_arr(self) -> np.ndarray:
        return self._board

    def __getitem__(self, index) -> Case:
        """Return the `Case` in the board with index `index`.

        Args:
            index (tuple[int, int]): the index to access the board.

        Returns:
            Case: The case at the `index` in the board.
        """
        if self._board[index] == Case.EMPTY:
            return Case()
        else:
            return Case(pawn=Pawn(Color(self._board[index])))


    def display(self, display_choice='console', extra=None):
        """Display the board on the screen.

        Args:
            display_choice (str, optional): where to display the board, either
            "console" or "matplotlib". Defaults to 'console'.
            extra (list[tuple[int,int]], optional): additional points to be
            displayed on the screen. This can be used to show the player the
            possible positions of the next pawn. Defaults to None.
        """
        if display_choice == 'console':
            print("  A B C D E F G H")
            for i in range(8):
                print(i+1, end=" ")
                for j in range(8):
                    if self._board[i,j] == Case.EMPTY:
                        if extra and (i,j) in extra:
                            print("*", end=" ")
                        else:
                            print(" ", end=" ")
                    elif self._board[i,j] == Color.BLACK.value:
                        print("\u2b24", end=" ")
                    elif self._board[i,j] == Color.WHITE.value:
                        print("\u25ef", end=" ")
                print()

        elif display_choice == 'matplotlib':
            x_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            locs = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]

            # vec_board = self.f_vec(self.board)
            vec_board = self._board
            if extra:
                for extra_val in extra:
                    r = extra_val[0]
                    c = extra_val[1]
                    vec_board[r, c] = 0.25

            # create 8 x 8 grid of all the indices
            nx, ny = (7, 7)
            x = np.linspace(0,nx,nx+1, dtype=int)
            y = np.linspace(0,ny,ny+1, dtype=int)
            rows, cols = np.meshgrid(x, y, indexing='ij')

            # plot on the figure and adjust the axis labels
            fig, ax = plt.subplots()
            ax.scatter(cols + 0.5, rows + 0.5,
                       s=500,
                       c = vec_board[rows,cols],
                       cmap=mpl.cm.Greys_r,
                       edgecolors='black')

            ax.set_xlim([0,8])
            ax.set_ylim([0,8])

            # remove the major ticks and their corresponding labels in x-dir
            ax.tick_params(
                axis='x',          # changes apply to the x-axis
                which='major',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labelbottom=False) # labels along the bottom edge are off

            # remove the minor ticks but keep their corresponding labels in x-dir
            ax.tick_params(
                axis='x',          # changes apply to the x-axis
                which='minor',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labeltop=True,
                labelbottom=False) # labels along the bottom edge are off

            # remove the major ticks and their corresponding labels in y-dir
            ax.tick_params(
                axis='y',          # changes apply to the x-axis
                which='major',      # both major and minor ticks are affected
                left=False,      # ticks along the bottom edge are off
                right=False,         # ticks along the top edge are off
                labelleft=False) # labels along the bottom edge are off

            # remove the minor ticks but keep their corresponding labels in y-dir
            ax.tick_params(
                axis='y',          # changes apply to the x-axis
                which='minor',      # both major and minor ticks are affected
                left=False,      # ticks along the bottom edge are off
                right=False,         # ticks along the top edge are off
                labelleft=True) # labels along the bottom edge are off

            ax.set_xticks(ticks=locs, labels=x_labels, minor=True)
            ax.set_yticks(ticks=locs, labels=range(1,9), minor=True)

            ax.grid(color='black', linestyle='-', linewidth=1)
            ax.set_facecolor('#117950')
            ax.yaxis.set_inverted(True)

            plt.show()

        else:
            return ValueError("Use 'console' for console display or 'matplotlib' for graphic display.")


if __name__ == "__main__":
    board = Board()
    board.place_pawn(3, 5, Color.WHITE)
    board.update_board(3, 5, Color.WHITE)
    board.place_pawn(3, 6, Color.WHITE)
    extra = [(1,1),(2,4)]
    #board.display()
    #board.display('matplotlib', extra)
    # board.place_pawn(2, 5, Color.BLACK)
    # board.update_board(2, 5, Color.BLACK)
    # board.place_pawn(4, 5, Color.BLACK)
    # board.update_board(4, 5, Color.BLACK)
    board.display(extra=extra)
    # board.display('matplotlib', extra)

