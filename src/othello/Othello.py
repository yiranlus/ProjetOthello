import Player
import Board

class Othello:

    def __init__(self):
        self.players_turn = 0
        self.number_pawns = 60
        self.board = Board()
        self.players = [Player(0),Player(1)]

    def is_terminated(self):       
        if self.number_pawns>0:
            if self.legal_moves(0) == False:
                if self.legal_moves(1) == True:
                    return True
        return False
    
    def get_winner(self):
        count = [0,0]
        board = self.board 
        for row in range(8):
            for col in range(8):
                if ~board[row,col].is_empty:
                    count[board[row,col].pawn.color] += 1
        id_winner = count.index(max(count))
        name_winner = self.players[id_winner].name
        color_winner = self.players[id_winner].color
        return "The winner of the game is:"+name_winner+"("+color_winner+")"
                 

    def ask_players(self):
        self.board.print()
        requested_move = self.players[self.players_turn].make_move()
        valid_move = self.legal_move(requested_move)
        while not(valid_move):
            print("Illegal move, choose again")
            requested_move = self.players[self.players_turn].make_move()
            valid_move = self.legal_move(requested_move)
        self.board.place_pawn(requested_move)
        self.number_pawns -= 1
        self.players_turn = (self.players_turn +1)%2

    def start_game(self):
        self.ask_players()
        while not(self.is_terminated()):
            self.ask_players()
        self.get_winner()



    def legal_moves(self,requested_move,check_start=True): # Recurssive approach
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]
        potential_move = []
        if check_start:
            check_start=False
            row,col = requested_move[0], requested_move[1]
            board , id_player = self.board , self.players_turn
            id_opponent = (id_player+1)%2
            for r,c in direction: # This loop determines all the possible moves to explore for 1st neighbors
                neighbor_r = row + r
                neighbor_c = col + r
                if neighbor_r>0 and neighbor_c >0 and neighbor_r<7 and neighbor_c<7:
                    if not(self.board[neighbor_r,neighbor_c].is_empty):
                        if self.board[neighbor_r,neighbor_c].pawn.color == id_opponent:
                            potential_move.append([(neighbor_r,neighbor_c),(r,c)])
        else:
            if not(potential_move):
                return False
            else:
                for neighbor_r,neighbor_c,r,c in requested_move:
                    if neighbor_r>0 and neighbor_c >0 and neighbor_r<7 and neighbor_c<7:
                        if not(self.board[neighbor_r,neighbor_c].is_empty):
                            if self.board[neighbor_r,neighbor_c].pawn.color == id_player:
                                return True
                            else:
                                potential_move.append([(neighbor_r,neighbor_c),(r,c)])  
        return self.legal_moves(potential_move,check_start)



    