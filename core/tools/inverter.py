from core.tools.pencil import Pencil


class Inverter(Pencil):

    def __init__(self, button, board):
        super(Inverter, self).__init__(button, board)

    def _need_change(self, value):
        return True
