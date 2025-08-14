import copy
from random import shuffle

from .Color import Color
from .Direction import Direction
from .Player import Player
from .Board import Board

class AIPlayer(Player):
    def __init__(self, color: Color, name="", engine="alpha-beta", max_depth=2):
        super().__init__(color, name)

        self._ref_board: Board
        if engine == "minimax":
            self._engine = self._get_best_move_minimax
        elif engine == "alpha-beta":
            self._engine = self._get_best_move_alphabeta
        self._max_depth = max_depth
        self._possible_move: list[tuple[int,int]] | list[list[int]]= []


    def set_ref_board(self, board: Board):
        """Set the reference board for AI to use.

        Args:
            board (Board): the board.
        """
        self._ref_board = board

    def _get_possible_moves(self, board: Board, color: Color):
        """Get possible moves from the board for `color`.

        Args:
            board (Board): the board.
            color (Color): the color

        Returns:
            list[tuple[int,int]]: a list of possible move for `color`.
        """
        possible_moves = [
            (i, j)
            for i in range(8)
            for j in range(8)
            if not board[i, j].pawn and self._legal_moves(board, (i, j), color)
        ]
        self._possible_move = possible_moves
        return possible_moves

    def _legal_moves(self, board: Board, requested_move, color: Color):
        """Check if the current move is valid.

        Args:
            board (Board): the board.
            requested_move (tuple[int,int]): the position in (row, col).
            color (Color): the color

        Returns:
            bool: True if the current position is valid, False otherwise.
        """
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
        """Calculate the score different between AI and another player.

        Args:
            board (Board): the board

        Returns:
            int: the score difference.
        """
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
        """The minimax algorithm to get the best move from the current board.

        Args:
            board (Board): the board.
            move (tuple[int,int]): the movement in (row, col).
            color (Color): the color of the corrent movement.
            depth (int): current depth of the algorithm
            maximizing (bool): should the current step maximizing or minimizing
            the value.

        Returns:
            int: _description_
        """
        r, c = move
        board.place_pawn(r, c, color)
        board.update_board(r, c, color)
        if depth <= 0:
            return self._calculate_score(board)
        possible_moves = self._get_possible_moves(board, color.switch())
        if not possible_moves:
            return self._calculate_score(board)
        shuffle(possible_moves)

        score = -64 if maximizing else 64
        for (r, c) in possible_moves:
            if maximizing:
                board_copy = copy.deepcopy(board)
                score = max(score, self._minimax(board_copy, (r, c), color.switch(), depth-1, False))
            else:
                board_copy = copy.deepcopy(board)
                score = min(score, self._minimax(board_copy, (r, c), color.switch(), depth-1, True))
        return score

    def _get_best_move_minimax(self, max_depth=3):
        """Return the best move.

        Args:
            max_depth (int, optional): the maximum depth to explore. Defaults
            to 3.

        Returns:
            tuple[int,int]: a movement in (row, col).
        """
        if not self._ref_board:
            print("The reference board is not set in AIPlayer.")
            exit(1)

        board = Board()
        board.board = copy.deepcopy(self._ref_board.board)

        score_self = -64
        next_move = (-1, -1)
        possible_moves = self._get_possible_moves(board, self.color)
        shuffle(possible_moves)
        for (r, c) in possible_moves:
            board_copy = copy.deepcopy(board)
            score = self._minimax(board_copy, (r, c), self.color, max_depth, False)
            if score_self <= score:
                score_self = score
                next_move = (r, c)
        return next_move

    def _alphabeta(self, board: Board, move, color: Color, depth, maximizing, alpha, beta) -> int:
        """The minimax algorithm to get the best move from the current board.

        Args:
            board (Board): the board.
            move (tuple[int,int]): the movement in (row, col).
            color (Color): the color of the corrent movement.
            depth (int): current depth of the algorithm
            maximizing (bool): should the current step maximizing or minimizing
            the value.
            alpha (int): alpha
            beta (int): beta

        Returns:
            int: _description_
        """
        r, c = move
        board.place_pawn(r, c, color)
        board.update_board(r, c, color)
        if depth <= 0:
            return self._calculate_score(board)
        possible_moves = self._get_possible_moves(board, color.switch())
        if not possible_moves:
            return self._calculate_score(board)
        shuffle(possible_moves)

        score = -64 if maximizing else 64
        for (r, c) in possible_moves:
            if maximizing:
                board_copy = copy.deepcopy(board)
                score = max(score, self._minimax(board_copy, (r, c), color.switch(), depth-1, False))
                if score >= beta:
                    break
                alpha = max(alpha, score)
            else:
                board_copy = copy.deepcopy(board)
                score = min(score, self._minimax(board_copy, (r, c), color.switch(), depth-1, True))
                if score <= alpha:
                    break
                beta = min(beta, score)
        return score

    def _get_best_move_alphabeta(self, max_depth=5):
        """Return the best move.

        Args:
            max_depth (int, optional): the maximum depth to explore. Defaults
            to 5.

        Returns:
            tuple[int,int]: a movement in (row, col).
        """
        if not self._ref_board:
            print("The reference board is not set in AIPlayer.")
            exit(1)

        board = Board()
        board.board = copy.deepcopy(self._ref_board.board)

        alpha, beta = -64, 64
        score_self = -64
        next_move = (-1, -1)
        possible_moves = self._get_possible_moves(board, self.color)
        shuffle(possible_moves)

        for (r, c) in possible_moves:
            board_copy = copy.deepcopy(board)
            score = self._alphabeta(board_copy, (r, c), self.color, max_depth, False, alpha, beta)
            alpha = max(alpha, score)
            if score_self <= score:
                if score >= beta:
                    break
                score_self = score
                next_move = (r, c)
        return next_move

    def make_move(self, fig=None):
        print(f"AI ({self.color}) is thinking.")
        return self._engine(max_depth=3)
