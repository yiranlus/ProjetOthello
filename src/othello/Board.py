import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .Direction import Direction
from .Color import Color
from .Pawn import Pawn
from .Case import Case

class Board:
    def __init__(self):
        self.rows = 8
        self.cols = 8
        self.number_pawns = 60

        # initialize empty board
        self.board = np.empty((self.rows, self.cols), dtype=Case)
        for row in range(8):
            for col in range(8):
                self.board[row, col] = Case()

        # initialize 4 center squares
        self.board[3,3].pawn = Pawn(Color.WHITE)
        self.board[3,4].pawn = Pawn(Color.BLACK)
        self.board[4,3].pawn = Pawn(Color.BLACK)
        self.board[4,4].pawn = Pawn(Color.WHITE)

        f = lambda x: x.pawn.color.value if x.pawn else -1
        self.f_vec = np.vectorize(f)


    def place_pawn(self, r, c, color: Color):
        """Place a pawn on the board.

        Args:
            r (int): the row position of the pawn
            c (int): the column position of the pawn
            color (Color): The color of the pawn
        """
        self.board[r, c].pawn = Pawn(color)
        self.number_pawns -= 1


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

            if self.board[r + dr, c + dc].pawn is None:
                continue
            elif self.board[r + dr, c + dc].pawn.color != color:
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
        color_c = self.board[r + dr, c + dc].pawn.color
        count = 0

        idx_ls = []
        while color_c != color:
            count += 1

            if ((r + dr * count < 0) | (r + dr * count >= self.rows) |
                (c + dc * count < 0) | (c + dc * count >= self.cols)):
                color_c = color
                continue

            if self.board[r + dr * count, c + dc * count].pawn is None:
                color_c = color
                continue

            if self.board[r + dr * count, c + dc * count].pawn.color != color:
                idx_ls.append((r + dr * count, c + dc * count))

            elif self.board[r + dr * count, c + dc * count].pawn.color == color:
                for idx in idx_ls:
                    r_idx = idx[0]
                    c_idx = idx[1]
                    self.board[r_idx, c_idx].pawn.flip()
                color_c = color
            else:
                color_c = color


    def __getitem__(self, index) -> Case:
        """Return the `Case` in the board with index `index`.

        Args:
            index (tuple[int, int]): the index to access the board.

        Returns:
            Case: The case at the `index` in the board.
        """
        return self.board[index]


    def display(self, display_choice='console', 
                extra=None, player = 'Color.BLACK'):
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
                    if not self.board[i,j].pawn:
                        if extra and (i,j) in extra:
                            print("*", end=" ")
                        else:
                            print(" ", end=" ")
                    elif self.board[i,j].pawn.color == Color.BLACK:
                        print("\u2b24", end=" ")
                    elif self.board[i,j].pawn.color == Color.WHITE:
                        print("\u25ef", end=" ")
                print()

        elif display_choice == 'matplotlib':
            x_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            locs = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]

            vec_board = self.f_vec(self.board)
            vec_board = vec_board.astype(float)
            vec_board[vec_board < 0] = np.nan
            
            possible_moves = np.empty((self.rows, self.cols))

            if extra:
                for extra_val in extra:
                    r = extra_val[0]
                    c = extra_val[1]
                    possible_moves[r, c] = player
            
            # create 8 x 8 grid of all the indices
            nx, ny = (7, 7)
            x = np.linspace(0,nx,nx+1, dtype=int)
            y = np.linspace(0,ny,ny+1, dtype=int)
            rows, cols = np.meshgrid(x, y, indexing='ij')

            # if not plt.fignum_exists(1):
            plt.ion()
      
            fig, ax = plt.subplots(num=1)
            ax.cla()  
            
            
            ax.scatter(cols + 0.5, rows + 0.5,
                    s=250,
                    c = possible_moves[rows,cols],
                    cmap=mpl.cm.Greys_r,
                    marker = 'x')
                    #edgecolors='black')

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

            plt.gca().set_aspect(1.0)
            plt.show(block=False)

        else:
            raise ValueError("Use 'console' for console display or 'matplotlib' for graphic display.")


if __name__ == "__main__":
    board = Board()
    board.place_pawn(3, 5, Color.WHITE)
    board.update_board(3, 5, Color.WHITE)
    board.place_pawn(3, 6, Color.WHITE)
    extra = [(1,1),(2,4)]
    #board.display()
    #board.display('matplotlib', extra)
    board.place_pawn(2, 5, Color.BLACK)
    board.update_board(2, 5, Color.BLACK)
    board.place_pawn(4, 5, Color.BLACK)
    board.update_board(4, 5, Color.BLACK)
    board.display()
    board.display('matplotlib', extra)

