import numpy as np

board_arr = [
    [ 1, -1,  0,  0,  0,  0,  0,  0],
    [ 1,  1,  0,  0,  0,  0,  0,  0],
    [ 1,  1,  1,  0,  0,  0,  0,  0],
    [ 1,  1,  0,  1,  0,  0,  0,  0],
    [ 1,  1,  1,  0,  1,  0,  0,  0],
    [ 1,  1,  0,  1,  0,  1,  0,  0],
    [ 1,  1,  0,  0,  1,  0,  1,  0],
    [ 1,  1,  1,  1,  1,  1,  1,  1],
]

from Othello import Othello
from HumanPlayer import HumanPlayer
from Board import Board
from Pawn import Pawn

board = Board()
for i in range(8):
    for j in range(8):
        if board_arr[i][j] != -1:
            board[i,j].pawn = Pawn(board_arr[i][j])

board.display()

player1 = HumanPlayer(0, "Alexis")
player2 = HumanPlayer(1, "Alicia")
game = Othello([player1, player2])
game.board = board
print(game.board.board[2,2].is_empty)
print(game.is_terminated())