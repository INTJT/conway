from core.editor import Editor
from core.tools.tool import Tool


class Move(Tool):

    def __init__(self, button, board):
        super(Move, self).__init__(button, board)
        Editor()["pre-move-fill"] = not button
        self._fill = not button
        self._start = None
        self._calculated = False
        self._changed = set()
        self._moved_selection = None

    def move(self, x, y):

        if self._start is None:
            self._start = (x, y)

        Editor()["pre-move"] = (x - self._start[0], y - self._start[1])

    def _move(self):

        editor = Editor()

        selection = editor["selection"]
        move = editor["pre-move"]

        for x in selection[0]:
            for y in selection[1]:
                if self._board[(x, y)] != self._fill:
                    self._changed.add((x, y))

        for x in selection[0]:
            for y in selection[1]:

                move_point = ((x + move[0]), (y + move[1]))

                if move_point[0] not in range(self._board.width) or \
                        move_point[1] not in range(self._board.height):
                    continue

                if self._board[move_point] != self._board[(x, y)]:
                    self._changed.add(move_point)
                elif move_point in self._changed:
                    self._changed.remove(move_point)

        if selection[0] != range(self._board.width) or \
                selection[1] != range(self._board.height):

            self._moved_selection = (
                range(
                    max((min(selection[0]) + move[0]), 0),
                    min((max(selection[0]) + move[0]) + 1, self._board.width)
                ),
                range(
                    max((min(selection[1]) + move[1]), 0),
                    min((max(selection[1]) + move[1]) + 1, self._board.height)
                )
            )

            if len(self._moved_selection[0]) == 0 or len(self._moved_selection[1]) == 0:
                self._moved_selection = self._board.full_selection

        else:
            self._moved_selection = self._board.full_selection

        self._prev_selection = editor["selection"]

        self._calculated = True

    def execute(self):

        if not self._calculated:
            self._move()

        editor = Editor()

        for point in self._changed:
            self._board[point] = not self._board[point]

        self._moved_selection, editor["selection"] = editor["selection"], self._moved_selection

        editor["pre-move"] = (0, 0)
        editor["pre-move-fill"] = None

    def revoke(self):
        self.execute()

    def need_save(self):
        if not self._calculated:
            self._move()
        return self._moved_selection != Editor()["selection"] or len(self._changed) != 0
