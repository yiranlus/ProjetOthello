from .Player import Player
from .Board import Board
from .Direction import Direction
from .Color import Color
import numpy as np

class Othello:

    def __init__(self,Player):
        """create the game master of Othello`.

        Args:

            Player (list of class Player): list containing the info of the 2 players
        """
        self.players_turn = 0 # Black (0) or White (1) to play
        self.board = Board()

        self.players = [Player[0],Player[1]]


    def get_possible_moves(self,id_player):
        """ Return all the possible moves, defined by case which are empty and next to
        an opponent's pawn.
        Args:
            id_player (int): Player color Id, 0 if black, 1 if white.
        Output:
            list of list [x,y] with the coordinates of possible moves for the player
        """
        id_opponent= (id_player +1)%2
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]

        current_board = self.board.f_vec(self.board.board)
        opponent_pos = np.argwhere(current_board==id_opponent) # Get psoition of opponent's pawns
        possible_move = []
        for opps in opponent_pos: # Get all the neighbors of the opponent's pawns
            possible_move+=[[opps[0]+direct.value[0],opps[1]+direct.value[1]] for direct in Direction ]
        possible_move = [ [r,c] for r,c in possible_move if r>=0 and c>=0 and r<8 and c<8]
        possible_move = [move for move in possible_move if current_board[move[0],move[1]]==None] # Filter only the empty case
        return possible_move

    def is_terminated(self): 
        """ Check if the game is done (no more pawns or legal moves for both players).
        Output:
            True if the game is done, False otherwise
        """
        # self.board.display()
        if self.board.number_pawns >0: # If there are still pawns to be played
            possible_move_black = self.get_possible_moves(0)
            possible_move_white = self.get_possible_moves(1)
            legal_move_white = False
            for move in possible_move_white: # Check the legality of all white moves
                if self.legal_moves(move,id_player=1):
                    legal_move_white = True # If legal set True
                    break
            legal_move_black = False
            for move in possible_move_black: # Check the legality of all black moves
                if self.legal_moves(move,id_player=0):
                    legal_move_black = True # If legal set True and stop the loop
            if self.players_turn == 0:
                if legal_move_black == False:
                    self.players_turn = 1
            else:
                if legal_move_white == False:
                    self.players_turn = 0
            if legal_move_black + legal_move_white == False: #No legal move for both players
                return True
            else: # If there are legal moves to be played by at least one player
                return False
        else: # If there is no more pawns remaining off the board
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
                    count[board.board[row,col].pawn.color] += 1
        id_winner = count.index(max(count))
        name_winner = self.players[id_winner].name
        color_winner = self.players[id_winner].color
        colour = ["black","white"]
        return "The winner of the game is: "+name_winner+" ("+colour[color_winner]+")"


    def ask_players(self):
        """ Ask players alternatively to make a move, accept it if
            it is legal and print the board.
        """
        self.board.display()
        requested_move = self.players[self.players_turn].make_move()
        valid_move = self.legal_moves(requested_move)
        valid_move = self.legal_moves(requested_move)
        while not(valid_move): # If the requested move is not legal
            print("Illegal move, choose again")
            requested_move = self.players[self.players_turn].make_move()
            valid_move = self.legal_moves(requested_move)
            valid_move = self.legal_moves(requested_move)
        self.board.place_pawn(requested_move[0],requested_move[1],self.players_turn) # Place the pawn
        self.board.update_board(requested_move[0],requested_move[1],self.players_turn) # Place the pawn
        self.players_turn = (self.players_turn +1)%2 # Switch players turn


    def start_game(self):
        self.ask_players()
        while not(self.is_terminated()):
            self.ask_players()
        print(self.get_winner())


    def legal_moves(self,requested_move,check_start=True,id_player=None): # Recurssive approach
        r, c = requested_move
        if self.board[r, c].pawn:
            return False

        direction = [(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if id_player == None:
            id_player =  self.players_turn # Get whose turn it is

        for dr, dc in direction:
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
    from .HumanPlayer import HumanPlayer

    player1 = HumanPlayer(0, "Alexis")
    player2 = HumanPlayer(1, "Alicia")
    players = [player1,player2]
    game = Othello(players)
    while not game.is_terminated():
        game.ask_players()




