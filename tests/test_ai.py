import numpy as np

from othello.HumanPlayer import HumanPlayer
from othello.AIPlayer import AIPlayer
from othello.Othello import Othello
from othello.Color import Color

# board_arr = np.array([
#     [-1, -1, -1, -1, -1, -1, -1, -1],
#     [-1,  1, -1, -1, -1,  1, -1, -1],
#     [ 0,  0,  0,  0,  1, -1, -1, -1],
#     [ 1,  1,  0,  1,  1,  1,  1,  0],
#     [ 1,  1,  1,  1,  1,  1,  1,  1],
#     [ 1,  1,  1,  1,  1,  1,  1,  1],
#     [ 1,  1,  1,  1,  1,  1,  1,  1],
#     [ 1,  1,  1,  1,  1,  1,  1,  1],
# ])

board_arr = np.array([
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  1,  1,  1,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  1,  0,  1],
    [ 1,  1,  0,  1,  1,  1,  1,  1],
    [ 1,  1,  1,  1,  1,  1,  1,  1],
    [ 1,  1,  1,  1,  1,  1,  1,  1],
    [ 1,  1,  1,  1,  1,  1,  1,  1],
    [ 1,  1,  1,  1,  1,  1,  1,  1],
])

# player_white = AIPlayer(Color.WHITE)
# player_black = AIPlayer(Color.BLACK)
player_white = HumanPlayer(Color.WHITE, "A")
player_black = HumanPlayer(Color.BLACK, "B")
game = Othello(player_black, player_white)
game.board._board = board_arr
game.players_turn = 1
# player_black.set_ref_board(game.board)
# player_white.set_ref_board(game.board)
game.board.display()
game.start_game()