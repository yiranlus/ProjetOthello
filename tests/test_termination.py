from othello.Color import Color
from othello import AIPlayer
board_arr = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  1,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  1,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  1,  0,  0],
    [None, None,  0,  1,  0,  1,  1,  1],
    [ 1,  1,  1,  1,  1,  1,  1,  1],
    [None,  1,  1,  1,  1,  1,  1,  1],
    
]

from othello.Othello import Othello
from othello.HumanPlayer import HumanPlayer
from othello.Board import Board
from othello.Pawn import Pawn
from othello.AIPlayer import AIPlayer

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
#player2 = AIPlayer(Color.WHITE,"Blue")

game = Othello(player1, player2,display_choice = 'matplotlib')
#player2.set_ref_board(game.board)
#game.board = board
# game.players_turn = 0
game.start_game()

#game.board.display()
