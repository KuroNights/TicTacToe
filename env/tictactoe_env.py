import numpy as np


class TicTacToeEnv:
    def __init__(self, board_size=6, win_length=4):
        self.board_size = board_size
        self.win_length = win_length
        self.n_actions = board_size * board_size
        self.reset()

    def reset(self):
        self.board = np.zeros(self.n_actions, dtype=int)
        self.done = False
        self.winner = None
        return self.board.copy()

    def available_actions(self):
        return [i for i in range(self.n_actions) if self.board[i] == 0]

    def step(self, action, player):
        if self.done:
            return self.board.copy(), 0, True

        if self.board[action] != 0:
            return self.board.copy(), -1, False

        self.board[action] = player
        r, c = divmod(action, self.board_size)

        if self._check_win(r, c, player):
            self.done = True
            self.winner = player
            return self.board.copy(), 1, True

        if not (self.board == 0).any():
            self.done = True
            self.winner = 0
            return self.board.copy(), 0, True

        return self.board.copy(), 0, False

    def _check_win(self, r, c, player):

        def count(dr, dc):
            total = 1

            i, j = r + dr, c + dc
            while self._in_bounds(i, j) and self._get(i, j) == player:
                total += 1
                i += dr
                j += dc

            i, j = r - dr, c - dc
            while self._in_bounds(i, j) and self._get(i, j) == player:
                total += 1
                i -= dr
                j -= dc

            return total

        return (
            count(0, 1) >= self.win_length or
            count(1, 0) >= self.win_length or
            count(1, 1) >= self.win_length or
            count(1, -1) >= self.win_length
        )

    def _in_bounds(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def _get(self, r, c):
        return self.board[r * self.board_size + c]
