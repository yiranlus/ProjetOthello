import click

from .Color import Color
from .AIPlayer import AIPlayer
from .HumanPlayer import HumanPlayer
from .Othello import Othello

def parse_engine(s: str):
    """Parse the string to engine name and maximum depth

    Args:
        s (str): the string to parse.

    Returns:
        (str, int): the engine name and the maximum depth.
    """
    engine = "alpha-beta"
    max_depth = 3
    if s.startswith("mm"):
        engine = "minimax"
        max_depth_s = s[2:]
        max_depth = 3 if max_depth_s == "" else int(max_depth_s)
    elif s.startswith("ab"):
        engine = "alpha-beta"
        max_depth_s = s[2:]
        max_depth = 3 if max_depth_s == "" else int(max_depth_s)
    return engine, max_depth

@click.command()
@click.option("--black-ai", type=str, is_flag=False, flag_value="ab3",
              help="AI will playing the black, default to ab3. Use \"ab\" for "
              "alpha-beta algorithm or \"mm\" for minimax algorithm. A number "
              "can be appended to specify the maximum depth the algorithm will"
              "explore.")
@click.option("--white-ai", type=str, is_flag=False, flag_value="ab3",
              help="The same as for --black-ai.")
@click.option("-b", "--black", type=str, is_flag=False, flag_value="Player",
              help="The name of the player who play the black.")
@click.option("-w", "--white", type=str, is_flag=False, flag_value="Player",
              help="The name of the player who play the white.")
@click.option("-d", "--display", type=str, default="console",
              help="Where to display the board, either \"console\" or using" \
              "\"matplotlib\". Defaults to \"console\".")
def main(black_ai, white_ai, black, white, display):
    player_black, player_white = None, None
    print(black_ai, white_ai, black, white)

    n_human_player = 0

    if black_ai:
        player_black = AIPlayer(Color.BLACK, "AI", parse_engine(black_ai))
    if white_ai:
        player_white = AIPlayer(Color.WHITE, "AI", parse_engine(white_ai))

    if black:
        n_human_player += 1
        player_black = HumanPlayer(Color.BLACK, black)
    if white:
        n_human_player += 1
        player_white = HumanPlayer(Color.WHITE, white)

    if not player_black:
        n_human_player += 1
        player_black = HumanPlayer(Color.BLACK, f"Player {n_human_player}")
    if not player_white:
        n_human_player += 1
        player_white = HumanPlayer(Color.WHITE, f"Player {n_human_player}")

    game = Othello(player_black, player_white, display)
    if isinstance(player_black, AIPlayer):
        player_black.set_ref_board(game.board)
    if isinstance(player_white, AIPlayer):
        player_white.set_ref_board(game.board)

    try:
        game.start_game()
    except KeyboardInterrupt:
        print("quitting the game")

if __name__ == "__main__":
    main()