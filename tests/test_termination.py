import numpy as np
from othello.Color import Color

board_arr = np.array([
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  1,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  1,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  1,  0,  0],
    [-1, -1,  0,  1,  0,  1,  1,  1],
    [ 1,  1,  1,  1,  1,  1,  1,  1],
    [-1,  1,  1,  1,  1,  1,  1,  1],
])

from othello.Othello import Othello
from othello.HumanPlayer import HumanPlayer
from othello.Board import Board
from othello.Pawn import Pawn

board = Board()
for i in range(8):
    for j in range(8):
        if board_arr[i][j] != -1:
            if board_arr[i][j] == 0:
                board[i,j].pawn = Pawn(Color.BLACK)
            else:
                board[i,j].pawn = Pawn(Color.WHITE)

# board.display()

player1 = HumanPlayer(Color.BLACK, "Alexis")
player2 = HumanPlayer(Color.WHITE, "Alicia")
game = Othello(player1, player2)

game.board._board = board_arr
# game.players_turn = 0
game.start_game()

#game.board.display()