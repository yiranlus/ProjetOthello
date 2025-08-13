from .Color import Color
from .Direction import Direction
from .Player import Player
from .Board import Board
from .Direction import Direction
from .Color import Color
import numpy as np

class Othello:

    def __init__(self, player_black: Player, player_white: Player):
        """create the game master of Othello`.

        Args:

            Player (list of class Player): list containing the info of the 2 players
        """
        self.players_turn = 0 # Black (0) or White (1) to play
        self.board: Board = Board()

        self.players: list[Player] = [player_black, player_white]
        self._possible_move: list[tuple[int,int]] = []

    def get_possible_moves(self, id_player):
        possible_moves = [
            (i, j)
            for i in range(8)
            for j in range(8)
            if not self.board[i, j].pawn and self.legal_moves((i, j), id_player)
        ]
        self._possible_move = possible_moves
        return possible_moves


    def is_terminated(self):
        """ Check if the game is done (no more pawns or legal moves for both players).
        Output:
            True if the game is done, False otherwise
        """
        # self.board.display()

        if self.get_possible_moves(self.players_turn):
            return False
        else:
            self.switch_player()
            if self.get_possible_moves(self.players_turn):
                return False
        return True

    def get_winner(self):
        """ Once the game is done count the number of pawns of given colors to
            determine the winner.
        Output:
            Print the name of the winner
        """
        count = [0,0]
        board = self.board
        for row in range(8):
            for col in range(8):
                if not(board.board[row,col].is_empty):
                    count[board.board[row,col].pawn.color.value] += 1
        id_winner = count.index(max(count))
        name_winner = self.players[id_winner].name
        color_winner = self.players[id_winner].color
        return f"The winner of the game is: {name_winner} ({color_winner})"

    def switch_player(self):
        self.players_turn = (self.players_turn + 1) % 2

    def ask_players(self):
        """ Ask players alternatively to make a move, accept it if
            it is legal and print the board.
        """
        self.board.display(extra=self._possible_move)
        current_player = self.players[self.players_turn]
        requested_move = current_player.make_move()
        valid_move = self.legal_moves(requested_move)
        while not(valid_move): # If the requested move is not legal
            print("Illegal move, choose again")
            requested_move = current_player.make_move()
            valid_move = self.legal_moves(requested_move)
        self.board.place_pawn(requested_move[0],requested_move[1],current_player.color) # Place the pawn
        self.board.update_board(requested_move[0],requested_move[1],current_player.color) # Place the pawn
        self.switch_player()


    def start_game(self):
        self.get_possible_moves(self.players_turn)
        self.ask_players()
        while not(self.is_terminated()):
            self.ask_players()
        self.board.display(extra=self._possible_move)
        print(self.get_winner())


    def legal_moves(self, requested_move, id_player=None): # Recurssive approach
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
    from othello.HumanPlayer import HumanPlayer

    player1 = HumanPlayer(Color.BLACK, "Alexis")
    player2 = HumanPlayer(Color.WHITE, "Alicia")
    players = [player1,player2]
    game = Othello(player_black=player2, player_white=player1)
    while not game.is_terminated():
        game.ask_players()
