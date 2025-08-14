from othello.AIPlayer import AIPlayer
from othello.Othello import Othello
from othello.Color import Color
from othello.Board import Board

import numpy as np

player1 = AIPlayer(Color.BLACK, "")
player2 = AIPlayer(Color.WHITE, "")
game = Othello(player1, player2, "matplotlib")
player1.set_ref_board(game.board)
player2.set_ref_board(game.board)
game.start_game()

# board = Board()
# board.display('matplotlib')

