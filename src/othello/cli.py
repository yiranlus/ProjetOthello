import argparse
import sys

from .AIPlayer import AIPlayer
from .Color import Color
from .HumanPlayer import HumanPlayer
from .Othello import Othello

def main():
    parser = argparse.ArgumentParser(
                    prog='Othello',
                    description='Play the game Othello with two players.')

    parser.add_argument('-wai', '--white-ai', type=str,
                        help="White AI player, use '' for default engine, or mm "
                             "for minimax or ab for alpha-beta engine. You can "
                             "append a max depth after the engine name.")
    parser.add_argument('-bai', '--black-ai', type=str, help="same as -wai")
    parser.add_argument('-w', '--white', type=str)
    parser.add_argument('-b', '--black', type=str)
    parser.add_argument('-m', '--matplotlib', action="store_true")
    #parser.add_argument('-init_b', '--initial_board')

    args = parser.parse_args()
    # print(args)

    num_inputs_players = 0
    players_white = 0
    players_black = 0

    if args.white_ai is not None:
        engine = "alpha-beta"
        max_depth = 5
        if args.white_ai.startswith("mm"):
            engine = "minimax"
            max_depth = args.white_ai[2:]
            max_depth = 3 if max_depth == "" else int(max_depth)
        elif args.white_ai.startswith("ab"):
            engine = "alpha-beta"
            max_depth = args.white_ai[2:]
            max_depth = 5 if max_depth == "" else int(max_depth)
        player_white = AIPlayer(Color.WHITE, "White", engine, max_depth)
        num_inputs_players += 1
        players_white += 1

    if args.black_ai is not None:
        if args.black_ai == "":
            engine = "alpha-beta"
            max_depth = 5
        else:
            if args.black_ai.startswith("mm"):
                engine = "minimax"
                max_depth = args.black_ai[2:]
                max_depth = 3 if max_depth == "" else int(max_depth)
            elif args.black_ai.startswith("ab"):
                engine = "alpha-beta"
                max_depth = args.black_ai[2:]
                max_depth = 5 if max_depth == "" else int(max_depth)
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

    if args.matplotlib:
        display = "matplotlib"
    else:
        display = "console"

    game = Othello(player_black=player_black, player_white=player_white, display_choice=display)
    if isinstance(player_black, AIPlayer):
        player_black.set_ref_board(game.board)
    if isinstance(player_white, AIPlayer):
        player_white.set_ref_board(game.board)

    try:
        game.start_game()
    except KeyboardInterrupt:
        print("quitting the game")
        sys.exit(0)
