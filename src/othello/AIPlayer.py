import copy
import numpy as np
from random import shuffle

from .Color import Color
from .Direction import Direction
from .Player import Player
from .Board import Board

class AIPlayer(Player):
    def __init__(self, color: Color, name="AI", engine="alphabeta"):
        super().__init__(color, name)

        self._ref_board: Board
        if engine == "minimax":
            self._engine = self._get_best_move_minimax
        else:
            self._engine = self._get_best_move_alphabeta

    def set_ref_board(self, board: Board):
        """Set the reference board for AI to use.

        Args:
            board (Board): the board.
        """
        self._ref_board = board

    def _get_possible_moves(self, board_arr: np.ndarray, color: Color):
        """Get possible moves from the board for `color`.

        Args:
            board (Board): the board.
            color (Color): the color

        Returns:
            list[tuple[int,int]]: a list of possible move for `color`.
        """
        # possible_moves = [
        #     (i, j)
        #     for i in range(8)
        #     for j in range(8)
        #     if board_arr[i, j] == -1 and self._legal_moves(board_arr, (i, j), color)
        # ]
        self._possible_move = list(
            filter(
                lambda pos: self._legal_moves(board_arr, tuple(pos), color),
                np.argwhere(board_arr == -1).tolist()
            )
        )
        return self._possible_move

    def _legal_moves(self, board_arr: np.ndarray, requested_move, color: Color):
        """Check if the current move is valid.

        Args:
            board (Board): the board.
            requested_move (tuple[int,int]): the position in (row, col).
            color (Color): the color

        Returns:
            bool: True if the current position is valid, False otherwise.
        """
        r, c = requested_move
        if board_arr[r, c] != -1:
            return False

        for direction in Direction:
            dr, dc = direction.value
            nr, nc = r+dr, c+dc
            if not (0 <= nr + dr <= 7 and 0 <= nc + dc <= 7):
                continue
            if board_arr[nr, nc] == -1:
                continue
            elif board_arr[nr, nc] == color.value:
                continue

            while 0 <= nr + dr <= 7 and 0 <= nc + dc <= 7:
                nr += dr
                nc += dc

                if board_arr[nr, nc] == -1:
                    break
                elif board_arr[nr, nc] == color.value:
                    return True

        return False

    def _calculate_score(self, board_arr: np.ndarray):
        """Calculate the score different between AI and another player.

        Args:
            board (Board): the board

        Returns:
            int: the score difference.
        """
        score_self, score_opp = 0, 0
        score_self = np.sum(board_arr == self.color.value)
        score_opp = np.sum(board_arr == self.color.switch().value)
        return score_self - score_opp

    def _minimax(self, board_arr: np.ndarray, move, color: Color, depth, maximizing) -> int:
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
        board = Board(board_arr)
        board.place_pawn(r, c, color)
        board.update_board(r, c, color)
        if depth <= 0:
            return self._calculate_score(board_arr)
        if np.sum(board_arr == -1) == 0:
            return self._calculate_score(board_arr)

        possible_moves = self._get_possible_moves(board_arr, color.switch())
        if not possible_moves:
            return self._calculate_score(board_arr)
        shuffle(possible_moves)

        score = -64 if maximizing else 64
        for (r, c) in self._get_possible_moves(board_arr, color.switch()):
            if maximizing:
                score = max(score, self._minimax(board_arr.copy(), (r, c), color.switch(), depth-1, False))
            else:
                score = min(score, self._minimax(board_arr.copy(), (r, c), color.switch(), depth-1, False))
        return score

    def _get_best_move_minimax(self, max_depth=10):
        """Return the best move.

        Args:
            max_depth (int, optional): the maximum depth to explore. Defaults
            to 10.

        Returns:
            tuple[int,int]: a movement in (row, col).
        """
        if not self._ref_board:
            print("The reference board is not set in AIPlayer.")
            exit(1)

        board_arr = self._ref_board.board_arr

        score_self = -64
        next_move = (-1, -1)
        possible_moves = self._get_possible_moves(board_arr, self.color)
        shuffle(possible_moves)
        for (r, c) in possible_moves:
            score = self._minimax(board_arr.copy(), (r, c), self.color, max_depth, False)
            if score_self <= score:
                score_self = score
                next_move = (r, c)
        return next_move

    def _alphabeta(self, board_arr: np.ndarray, move, color: Color, depth, maximizing, alpha, beta) -> int:
        """The minimax algorithm to get the best move from the current board.

        Args:
            board (Board): the board.
            move (tuple[int,int]): the movement in (row, col).
            color (Color): the color of the corrent movement.
            depth (int): current depth of the algorithm
            maximizing (bool): should the current step maximizing or minimizing
            the value.
            alpha(int): alpha
            beta(int): beta

        Returns:
            int: _description_
        """
        r, c = move
        board = Board(board_arr)
        board.place_pawn(r, c, color)
        board.update_board(r, c, color)
        if depth <= 0:
            return self._calculate_score(board_arr)
        if np.sum(board_arr == -1) == 0:
            return self._calculate_score(board_arr)

        possible_moves = self._get_possible_moves(board_arr, color.switch())
        if not possible_moves:
            return self._calculate_score(board_arr)
        shuffle(possible_moves)

        score = -64 if maximizing else 64
        for (r, c) in possible_moves:
            if maximizing:
                score = max(score, self._alphabeta(board_arr.copy(), (r, c), color.switch(), depth-1, False, alpha, beta))
                if score >= beta:
                    break
                alpha = max(alpha, score)
            else:
                score = min(score, self._alphabeta(board_arr.copy(), (r, c), color.switch(), depth-1, True, alpha, beta))
                if score <= alpha:
                    break
                beta = min(beta, score)
        return score

    def _get_best_move_alphabeta(self, max_depth=10):
        """Return the best move.

        Args:
            max_depth (int, optional): the maximum depth to explore. Defaults
            to 10.

        Returns:
            tuple[int,int]: a movement in (row, col).
        """
        if not self._ref_board:
            print("The reference board is not set in AIPlayer.")
            exit(1)

        board_arr = self._ref_board.board_arr

        score_self = -64
        next_move = (-1, -1)
        alpha, beta = -64, 64

        possible_moves = self._get_possible_moves(board_arr, self.color)
        shuffle(possible_moves)
        for (r, c) in possible_moves:
            score = self._alphabeta(board_arr.copy(), (r, c), self.color, max_depth, False, alpha, beta)
            alpha = max(alpha, score)
            if score_self <= score:
                if score >= beta:
                    break
                score_self = score
                next_move = (r, c)
        return next_move

    def make_move(self):
        circle = "\u2b24" if self.color == Color.BLACK else "\u25ef"
        print(f"AI ({self.color}) is thinking.")
        move = self._engine(max_depth=5)
        if move == (-1, -1):
            print(f"malfunction")
            exit(1)
        return move
