from othello.HumanPlayer import HumanPlayer
from othello.AIPlayer import AIPlayer
from othello.Othello import Othello
from othello.Color import Color

player1 = HumanPlayer(Color.BLACK, "Alexis")
player_ai = AIPlayer(Color.WHITE, "AI")
game = Othello(player1, player_ai)
player_ai.set_ref_board(game.board)
game.start_game()