import Player
import Board
import Pawn
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


    def legal_moves(self):
        pass

    