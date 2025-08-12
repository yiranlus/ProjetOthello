import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .Pawn import Pawn
from .Case import Case

class Board:
    def __init__(self):
        self.rows = 8
        self.cols = 8

        # initialize empty board
        self.board = np.empty((self.rows, self.cols), dtype=Case)
        for row in range(8):
            for col in range(8):
                self.board[row, col] = Case()

        # initialize 4 center squares
        self.board[3,3].pawn = Pawn(0)
        self.board[3,4].pawn = Pawn(1)
        self.board[4,3].pawn = Pawn(1)
        self.board[4,4].pawn = Pawn(0)


    def place_pawn(self, r, c, color):
        self.board[r, c].pawn = Pawn(color)

    
    def display(self):
        f = lambda x: x.pawn.color if x.pawn else (-1)
        f_vec = np.vectorize(f)

        print(f_vec(self.board))
    

    def display_graphic(self):
        x_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        locs = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]
        
        # create 8 x 8 grid of all the indices
        nx, ny = (7, 7)
        x = np.linspace(0,nxts(),nx+1, dtype=int)
        y = np.linspace(0,ny,ny+1, dtype=int)
        rows, cols = np.meshgrid(x, y, indexing='ij')

        ax.scatter(rows + 0.5, cols + 0.5,
                   s=500,
                   c = self.board[rows,cols],
                   cmap=mpl.cm.Greys_r,
                   edgecolors='black')

        # plot on the figure and adjust the axis labels
        fig, ax = plt.subplots()
        ax.scatter(rows + 0.5, cols + 0.5,
                   s=500,
                   c = self.board[rows,cols],
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
        #ax.set_facecolor('#E1F8DC')
        ax.set_facecolor('#117950')
        ax.yaxis.set_inverted(True)
        
        plt.show()


if __name__ == "__main__":
    board = Board()
    board.place_pawn(3, 2, 1)
    board.place_pawn(1,1,1)
    print(board.display_console())
    #print(board.display())
    