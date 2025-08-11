import Player
import Board
import Pawn
class Othello:

    def __init__(self):
        self.number_pawns = 60
        self.board = Board()
        self.players = [Player(0),Player(1)]

    def is_terminated(self):       
        if self.number_pawns>0:
            if legal_moves(self.board,0) == False:
                if legal_moves(self.board,0) == True:
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
                 
