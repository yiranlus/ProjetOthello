import copy

from .Color import Color
from .Direction import Direction
from .Player import Player
from .Board import Board

class AIPlayer(Player):
    def __init__(self, color: Color, name=""):
        super().__init__(color, name)

        self._ref_board: Board

    def set_ref_board(self, board: Board):
        self._ref_board = board

    def _get_possible_moves(self, board: Board, color: Color):
        possible_moves = [
            (i, j)
            for i in range(8)
            for j in range(8)
            if not board[i, j].pawn and self._legal_moves(board, (i, j), color)
        ]
        self._possible_move = possible_moves
        return possible_moves

    def _legal_moves(self, board: Board, requested_move, color: Color): # Recurssive approach
        r, c = requested_move
        if board[r, c].pawn:
            return False

        for direction in Direction:
            dr, dc = direction.value
            nr, nc = r+dr, c+dc
            if not (0 <= nr + dr <= 7 and 0 <= nc + dc <= 7):
                continue
            if not board[nr, nc].pawn:
                continue
            elif board[nr, nc].pawn.color == color:
                continue

            while 0 <= nr + dr <= 7 and 0 <= nc + dc <= 7:
                nr += dr
                nc += dc

                if not board[nr, nc].pawn:
                    break
                elif board[nr, nc].pawn.color == color:
                    return True

        return False

    def _calculate_score(self, board: Board):
        score_self, score_opp = 0, 0
        for i in range(8):
            for j in range(8):
                if board[i, j].pawn:
                    if board[i, j].pawn.color == self.color:
                        score_self += 1
                    else:
                        score_opp += 1
        return score_self - score_opp

    def _minimax(self, board: Board, move, color: Color, depth, maximizing) -> int:
        r, c = move
        board.place_pawn(r, c, color)
        board.update_board(r, c, color)
        if depth <= 0:
            return self._calculate_score(board)

        score_max = 0
        for (r, c) in self._get_possible_moves(board, color.switch()):
            if maximizing:
                score = self._minimax(copy.deepcopy(board), (r, c), color.switch(), depth-1, False)
                if score_max <= score:
                    score_max = score
            else:
                score = self._minimax(copy.deepcopy(board), (r, c), color.switch(), depth-1, True)
                if score_max >= score:
                    score_max = score
        return score_max

    def _get_best_move(self, max_depth=10):
        if not self._ref_board:
            print("The reference board is not set in AIPlayer.")
            exit(1)

        board = copy.deepcopy(self._ref_board)

        score_self = 0
        next_move = (-1, -1)
        for (r, c) in self._get_possible_moves(board, self.color):
             score = self._minimax(copy.deepcopy(board), (r, c), self.color, max_depth, False)
             if score_self <= score:
                 score_self = score
                 next_move = (r, c)
        return next_move

    def make_move(self):
        print("AI is thinking.")
        return self._get_best_move(max_depth=3)
