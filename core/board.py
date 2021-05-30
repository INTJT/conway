from core.rule import Rule

from random import random
from numpy import full
from numba import njit, prange


@njit(parallel=True)
def life_iteration(universe, born, survive):

    height, width = universe.shape
    copied = universe.copy()

    for x in prange(width):
        for y in prange(height):

            x_left = width - 1 if x == 0 else x - 1
            x_right = 0 if x == width - 1 else x + 1
            y_top = height - 1 if y == 0 else y - 1
            y_bottom = 0 if y == height - 1 else y + 1

            count = copied[y_top, x_left] + copied[y_top, x] + copied[y_top, x_right] \
                + copied[y, x_left] + copied[y, x_right] \
                + copied[y_bottom, x_left] + copied[y_bottom, x] + copied[y_bottom, x_right]

            if copied[y, x]:
                if count not in survive:
                    universe[y, x] = False
            else:
                if count in born:
                    universe[y, x] = True


class Board:

    def __init__(self, width, height, rule, fill=True):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")
        self._board = full((height, width), bool(fill))
        self._rule = None
        self.rule = rule

    def __getitem__(self, key): return self._board[key[1], key[0]]
    def __setitem__(self, key, value): self._board[key[1], key[0]] = bool(value)

    @property
    def width(self): return self._board.shape[1]

    @property
    def height(self): return self._board.shape[0]

    @property
    def view(self):
        view = self._board.view()
        view.setflags(write=False)
        return view

    @property
    def rule(self): return self._rule

    @rule.setter
    def rule(self, rule):
        if rule is None or not isinstance(rule, Rule):
            raise ValueError("value must be the instance of class \"Rule\"")
        self._rule = rule

    @property
    def full_selection(self):
        return (
            range(self.width),
            range(self.height)
        )

    def save(self):
        return BoardMemento(self._board.copy())

    def restore(self, memento):
        self._board = memento.board_backup.copy()

    def copy(self): return self._board.copy()

    def iteration(self):
        life_iteration(self._board, self._rule.born, self._rule.survive)

    @staticmethod
    def randomized(width, height, probability, rule):

        randomized_board = Board(width, height, rule)

        for i in range(randomized_board.height):
            for j in range(randomized_board.width):
                randomized_board[j, i] = random() < probability

        return randomized_board


class BoardMemento:

    @property
    def board_backup(self):
        return self._backup

    def __init__(self, board):
        self._backup = board.copy()
