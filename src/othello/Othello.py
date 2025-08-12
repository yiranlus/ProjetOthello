from Player import Player
from Board import Board
import numpy as np
from HumanPlayer import HumanPlayer
class Othello:

    def __init__(self,Player):
        """create the game master of Othello`.

        Args:

            Player (list of class Player): list containing the info of the 2 players
        """
        self.players_turn = 0 # Black (0) or White (1) to play
        self.number_pawns = 60 # Number of pawns remaining off the board
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
        current_board = np.zeros((8,8),int) -1
        for row in range(8):# Check all the case of the board
            for col in range(8):
                if not(self.board.board[row,col].is_empty): # if there is a pawn on the case
                    current_board[row,col] =  self.board.board[row,col].pawn.color # Assign color id to current_board
        opponent_pos = np.argwhere(current_board==id_opponent) # Get psoition of opponent's pawns
        possible_move = []
        for opps in opponent_pos: # Get all the neighbors of the opponent's pawns
            possible_move+=[[opps[0]+r,opps[1]+c] for r,c in direction ]
        possible_move = [move for move in possible_move if current_board[move[0],move[1]]==-1] # Filter only the empty case
        return possible_move
    
    def is_terminated(self):   # WIP
        """ Check if the game is done (no more pawns or legal moves for both players).
        Output:
            True if the game is done, False otherwise
        """     
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if self.number_pawns>0: # If there are still pawns to be played            
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
                    break
            if legal_move_black * legal_move_white == False: #No legal move for both players
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
        return "The winner of the game is:"+name_winner+"("+color_winner+")"
                 

    def ask_players(self):
        """ Ask players alternatively to make a move, accept it if 
            it is legal and print the board.
        """   
        self.board.display_console()
        requested_move = self.players[self.players_turn].make_move()
        valid_move = self.legal_move(requested_move)
        while not(valid_move): # If the requested move is not legal
            print("Illegal move, choose again")
            requested_move = self.players[self.players_turn].make_move()
            valid_move = self.legal_move(requested_move)
        self.board.place_pawn(requested_move[0],requested_move[1],self.players_turn) # Place the pawn
        self.number_pawns -= 1 # Update the number of pawns remaining off the board
        self.players_turn = (self.players_turn +1)%2 # Switch players turn

    def start_game(self):
        self.ask_players()
        while not(self.is_terminated()):
            self.ask_players()
        self.get_winner()



    def legal_moves(self,requested_move,check_start=True,id_player=None): # Recurssive approach
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]
        potential_move = []
        if id_player == None:
            id_player =  self.players_turn # Get whose turn it is
        if check_start: # if block for the first iteration 
            check_start=False # not going through this block in future runs
            row,col = requested_move[0], requested_move[1]
            id_opponent = (id_player+1)%2
            for r,c in direction: # This loop determines all the possible moves to explore for 1st neighbors
                neighbor_r = row + r
                neighbor_c = col + r
                if neighbor_r>=0 and neighbor_c >=0 and neighbor_r<=7 and neighbor_c<=7: # if case within the board
                    if not(self.board.board[neighbor_r,neighbor_c].is_empty): # if there is a pawn on the case
                        if self.board.board[neighbor_r,neighbor_c].pawn.color == id_opponent: # if the color of the pawn is the opponent's
                            potential_move.append([(neighbor_r,neighbor_c),(r,c)]) # Add to potential moves
        else: # For all runs that are not the first one
            if not(requested_move): # If there is no more direction to explore
                return False # Move is illegal
            else: # If requested_move is not empty
                for neighbor,direct in requested_move:
                    neighbor_r,neighbor_c = neighbor[0],neighbor[1]
                    r,c = direct[0],direct[1]
                    if neighbor_r>=0 and neighbor_c >=0 and neighbor_r<=7 and neighbor_c<=7: # if case within the board
                        if not(self.board.board[neighbor_r,neighbor_c].is_empty):  # if there is a pawn on the case
                            if self.board.board[neighbor_r,neighbor_c].pawn.color == id_player: # if the color of the pawn is the player's
                                return True # This move is legal
                            else:  # if the color of the pawn is the opponent's
                                new_r = neighbor_r + r # Update the row id
                                new_c = neighbor_c + c # Update the column id
                                potential_move.append([(new_r,new_c),(r,c)])  # Add it to potential_move
        return self.legal_moves(potential_move,check_start) # Recurssive call until True is returned or 
    # no more directions are to be investigated, then return False


if __name__ == "__main__":
    player1 = HumanPlayer(0, "Alexis")
    player2 = HumanPlayer(1, "Alicia")
    players = [player1,player2]
    game = Othello(players)
    print(game.is_terminated())
    



