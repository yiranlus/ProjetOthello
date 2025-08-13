import argparse

from .AIPlayer import AIPlayer
from .Color import Color
from .HumanPlayer import HumanPlayer
from .Othello import Othello

def main():
    parser = argparse.ArgumentParser(
                    prog='Othello',
                    description='Play the game Othello with two players.')
    
    parser.add_argument('-w_ai', '--white_ai', action='store_true') 
    parser.add_argument('-b_ai', '--black_ai', action='store_true')
    parser.add_argument('-w', '--white', type=str) 
    parser.add_argument('-b', '--black', type=str)
    #parser.add_argument('-init_b', '--initial_board')

    args = parser.parse_args()
    print(args)

    num_inputs_players = 0
    players_white = 0
    players_black = 0

    if args.white_ai:
        player2 = AIPlayer(Color.WHITE, "White")
        num_inputs_players += 1
        players_white += 1

    if args.black_ai:
        player1 = AIPlayer(Color.BLACK, "Black")
        num_inputs_players += 1
        players_black += 1

    if args.white is not None:
        player2 = HumanPlayer(Color.WHITE, args.white)
        num_inputs_players += 1
        players_white += 1

    if args.black is not None:
        player1 = HumanPlayer(Color.BLACK, args.black)
        num_inputs_players += 1
        players_black += 1

    if num_inputs_players != 2:
       raise Exception('Expected a flag for each player.' \
                       '\nEx: -w and -b or -w and -b_ai')
    
    if (players_white > 1) | (players_black > 1):
        raise Exception('Please choose both a black and a white player.')

    players = [player1,player2]
    game = Othello(player_black=player2, player_white=player1)
    while not game.is_terminated():
        game.ask_players()
