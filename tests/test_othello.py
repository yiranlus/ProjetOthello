from othello.HumanPlayer import HumanPlayer
from othello.Othello import Othello
from othello.Color import Color

player1 = HumanPlayer(Color.BLACK, "Alexis")
player2 = HumanPlayer(Color.WHITE, "Alicia")
game = Othello(player1, player2)
game.start_game()