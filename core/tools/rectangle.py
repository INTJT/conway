from core.editor import Editor
from core.tools.select import Select


class Rectangle(Select):

    def __init__(self, button, board):
        super(Rectangle, self).__init__(button, board)
        self._fill = button
        self._changed = set()
        self._calculated = False
        Editor()["pre-rectangle-fill"] = button

    def move(self, x, y):

        if self._start is None:
            self._start = (x, y)

        self._end = (x, y)

        editor = Editor()
        selection = editor["selection"]
        editor["pre-rectangle"] = (
            range(
                max(min(selection[0]), min(self._start[0], self._end[0])),
                min(max(selection[0]), max(self._start[0], self._end[0])) + 1
            ),
            range(
                max(min(selection[1]), min(self._start[1], self._end[1])),
                min(max(selection[1]), max(self._start[1], self._end[1])) + 1
            )
        )

    def _rectangle(self):

        editor = Editor()
        rectangle, editor["pre-rectangle"], editor["pre-rectangle-fill"] = editor["pre-rectangle"], None, None

        for x in rectangle[0]:
            for y in rectangle[1]:
                if self._board[(x, y)] != self._fill:
                    self._changed.add((x, y))

        self._calculated = True

    def execute(self):

        if not self._calculated:
            self._rectangle()

        for point in self._changed:
            self._board[point] = not self._board[point]

    def revoke(self):
        self.execute()

    def need_save(self):
        if not self._calculated:
            self._rectangle()
        return super(Rectangle, self).need_save() or len(self._changed) != 0
