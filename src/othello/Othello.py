from .Board import Board
from .Color import Color
from .Direction import Direction
from .Player import Player


class Othello:

    def __init__(self, player_black: Player, player_white: Player, display_choice='console'):
        """create the game master of Othello`.

        Args:

            Player (list of class Player): list containing the info of the 2 players
        """
        self.players_turn = 0 # Black (0) or White (1) to play
        self.board: Board = Board()

        self.players: list[Player] = [player_black, player_white]
        self._possible_move: list[tuple[int,int]] = []
        self.display_choice = display_choice


    def get_possible_moves(self, id_player: int) -> list[tuple[int, int]]:
        """Get all the possible positions where the current player can play on
        the board.

        Args:
            id_player (int): the ID of the player. Either 0 (the player who play
            black) or 1 (the player who play the white).

        Returns:
            list[tuple[int, int]]: a list of positions in (row, col).
        """
        possible_moves = [
            (i, j)
            for i in range(8)
            for j in range(8)
            if not self.board[i, j].pawn and self.legal_moves((i, j), id_player)
        ]
        self._possible_move = possible_moves
        return possible_moves


    def is_terminated(self) -> bool:
        """ Check if the game is done (no more pawns or legal moves for both players).

        Returns:
            bool: True if the game is done, False otherwise
        """
        # self.board.display()

        if self.get_possible_moves(self.players_turn):
            return False
        else:
            self.switch_player()
            if self.get_possible_moves(self.players_turn):
                return False
        return True

    def get_winner(self) -> Player:
        """ Once the game is done count the number of pawns of given colors to
            determine the winner.

        Returns:
            Player: Print the name of the winner
        """
        count = [0,0]
        for row in range(8):
            for col in range(8):
                if not(self.board[row,col].is_empty):
                    count[self.board[row,col].pawn.color.value] += 1
        id_winner = count.index(max(count))
        return self.players[id_winner]


    def switch_player(self):
        """Swith the player.
        """
        self.players_turn = (self.players_turn + 1) % 2


    def ask_players(self):
        """ Ask players alternatively to make a move, accept it if it is legal
        and print the board.
        """
        self.board.display(display_choice = self.display_choice,
                           extra=self._possible_move,
                           player = self.players_turn)
        current_player = self.players[self.players_turn]
        requested_move = current_player.make_move(self.board.fig)
        valid_move = self.legal_moves(requested_move)
        while not(valid_move): # If the requested move is not legal
            print("Illegal move, choose again")
            requested_move = current_player.make_move(self.board.fig)
            valid_move = self.legal_moves(requested_move)
        self.board.place_pawn(requested_move[0],requested_move[1],current_player.color) # Place the pawn
        self.board.update_board(requested_move[0],requested_move[1],current_player.color) # Place the pawn
        self.switch_player()


    def start_game(self):
        """Start the game.
        """
        while not(self.is_terminated()):
            self.ask_players()
        self.board.display(display_choice = self.display_choice, extra=self._possible_move)
        winner = self.get_winner()
        print(f"The winner of the game is: {winner.name} ({winner.color})")


    def legal_moves(self, requested_move: tuple[int, int], id_player=None):
        """Check if the `requested_move` is valid to play.

        Args:
            requested_move (tuple[int, int]): the move from the user.
            id_player (int, optional): The ID of the player, either 0 or 1.
            Defaults to None.

        Returns:
            bool: True if the `requested_move` is valid, otherwise False.
        """
        r, c = requested_move
        if self.board[r, c].pawn:
            return False

        if id_player == None:
            id_player =  self.players_turn # Get whose turn it is

        for direction in Direction:
            dr, dc = direction.value
            nr, nc = r+dr, c+dc
            if not (0 <= nr + dr <= 7 and 0 <= nc + dc <= 7):
                continue
            if not self.board[nr, nc].pawn:
                continue
            elif self.board[nr, nc].pawn.color == self.players[id_player].color:
                continue

            while 0 <= nr + dr <= 7 and 0 <= nc + dc <= 7:
                nr += dr
                nc += dc

                if not self.board[nr, nc].pawn:
                    break
                elif self.board[nr, nc].pawn.color == self.players[id_player].color:
                    return True

        return False


if __name__ == "__main__":
    pass
