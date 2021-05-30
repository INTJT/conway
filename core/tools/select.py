from core.editor import Editor
from core.tools.tool import Tool


class Select(Tool):

    def __init__(self, button, board):

        super(Select, self).__init__(button, board)

        self._board = board
        self._start = None
        self._end = None

        editor = Editor()
        self._backup = editor["selection"]
        self._pre_selection = self._backup
        editor["pre-selection"] = self._pre_selection

    def move(self, x, y):

        if self._start is None:
            self._start = (x, y)

        self._end = (x, y)

        pre_selection = (
            range(
                max(0, min(self._start[0], self._end[0])),
                min(self._board.width, max(self._start[0], self._end[0]) + 1)
            ),
            range(
                max(0, min(self._start[1], self._end[1])),
                min(self._board.height, max(self._start[1], self._end[1]) + 1)
            )
        )

        if len(pre_selection[0]) == 0 or len(pre_selection[1]) == 0:
            pre_selection = self._board.full_selection

        self._pre_selection = pre_selection
        Editor()["pre-selection"] = self._pre_selection

    def execute(self):
        editor = Editor()
        editor["selection"] = self._pre_selection
        editor["pre-selection"] = None

    def revoke(self):
        Editor()["selection"] = self._backup

    def need_save(self):
        return self._backup != self._pre_selection
