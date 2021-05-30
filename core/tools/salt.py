from core.editor import Editor
from core.tools.pencil import Pencil
from random import random


class Salt(Pencil):

    def __init__(self, button, board):
        super(Salt, self).__init__(button, board)

    def _need_change(self, value):
        if self._fill == value:
            return False
        else:
            return random() ** 0.5 < Editor()["random"]
