from core.tools.tool import Tool
from core.editor import Editor


class Pencil(Tool):

    def __init__(self, button, board):
        super(Pencil, self).__init__(button, board)
        self._changed = set()
        Editor()["pre-pencil"] = board.copy()
        self._fill = button

    def _need_change(self, value):
        return value != self._fill

    def move(self, x, y):

        editor = Editor()

        radius = editor["radius"]
        selection = editor["selection"]
        pre_board = editor["pre-pencil"]

        for i in range(-radius + 1, radius):

            if y + i not in selection[1]:
                continue

            for j in range(-radius + 1, radius):

                if x + j not in selection[0]:
                    continue

                if self._need_change(pre_board[y + i, x + j]) and not (x + j, y + i) in self._changed:
                    self._changed.add((x + j, y + i))
                    pre_board[y + i, x + j] = not pre_board[y + i, x + j]

    def execute(self):

        Editor()["pre-pencil"] = None

        for point in self._changed:
            self._board[point] = not self._board[point]

    def revoke(self):
        self.execute()

    def need_save(self):
        return len(self._changed) != 0
