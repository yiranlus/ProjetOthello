from othello.HumanPlayer import HumanPlayer
from othello.Othello import Othello

player1 = HumanPlayer(0, "Alexis")
player2 = HumanPlayer(1, "Alicia")
players = [player1,player2]
game = Othello(players)
while not game.is_terminated():
    game.ask_players()
