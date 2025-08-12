import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

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

        f = lambda x: x.pawn.color.value if x.pawn else None
        self.f_vec = np.vectorize(f)


    def place_pawn(self, r, c, color: Color):
        self.board[r, c].pawn = Pawn(color)
        self.number_pawns -= 1


    def update_board(self, r, c, color: Color):
        rows = [-1, 0, 1]
        cols = [-1, 0, 1]

        for row in rows:
            for col in cols:
                if (row == 0) & (col == 0):
                    continue

                if ((r + row < 0) | (r + row >= self.rows) |
                    (c + col < 0) | (c + col >= self.cols)):
                    continue

                #print(self.board[r + row, c + col].__dict__)
                #print(r+row)
                if self.board[r + row, c + col].pawn is None:
                    continue
                elif self.board[r + row, c + col].pawn.color != color:
                    self.flip_sandwiches(r, c, color, row, col)


    def flip_sandwiches(self, r, c, color, row, col):
        color_c = self.board[r + row, c + col].pawn.color
        count = 0

        idx_ls = []
        while color_c != color:
            count += 1

            if ((r + row * count < 0) | (r + row * count >= self.rows) |
                (c + col * count < 0) | (c + col * count >= self.cols)):
                color_c = color
                continue

            if self.board[r + row * count, c + col * count].pawn is None:
                color_c = color
                continue

            if self.board[r + row * count, c + col * count].pawn.color != color:
                idx_ls.append((r + row * count, c + col * count))

            elif self.board[r + row * count, c + col * count].pawn.color == color:
                for idx in idx_ls:
                    r_idx = idx[0]
                    c_idx = idx[1]
                    self.board[r_idx, c_idx].pawn.flip()
                color_c = color
            else:
                color_c = color


    def __getitem__(self, index):
        return self.board[index]


    def display(self, display_choice = 'console', extra=None):
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
    board.place_pawn(2, 5, Color.BLACK)
    board.update_board(2, 5, Color.BLACK)
    board.place_pawn(4, 5, Color.BLACK)
    board.update_board(4, 5, Color.BLACK)
    board.display()
    board.display('matplotlib', extra)

