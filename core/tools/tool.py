from core.command import Command


class Tool(Command):

    def __init__(self, button, board):
        self._board = board

    def move(self, x, y):
        pass
