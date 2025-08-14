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
    # print(args)

    num_inputs_players = 0
    players_white = 0
    players_black = 0

    if args.white_ai:
        player_white = AIPlayer(Color.WHITE, "White")
        num_inputs_players += 1
        players_white += 1

    if args.black_ai:
        player_black = AIPlayer(Color.BLACK, "Black")
        num_inputs_players += 1
        players_black += 1

    if args.white is not None:
        player_white = HumanPlayer(Color.WHITE, args.white)
        num_inputs_players += 1
        players_white += 1

    if args.black is not None:
        player_black = HumanPlayer(Color.BLACK, args.black)
        num_inputs_players += 1
        players_black += 1

    if num_inputs_players == 0:
        parser.print_help()
        return 0

    if num_inputs_players != 2 | (players_white > 1) | (players_black > 1):
        print('Please choose both a black and a white player.')
        return 1

    game = Othello(player_black=player_black, player_white=player_white)
    if isinstance(player_black, AIPlayer):
        player_black.set_ref_board(game.board)
    if isinstance(player_white, AIPlayer):
        player_white.set_ref_board(game.board)

    game.start_game()
