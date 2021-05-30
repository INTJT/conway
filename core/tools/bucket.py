from core.tools.tool import Tool
from core.editor import Editor

from collections import deque


class Bucket(Tool):

    def __init__(self, button, board):
        super(Bucket, self).__init__(button, board)
        self._changed = set()
        self._fill = button
        self._point = None
        self._calculated = False

    def move(self, x, y):
        self._point = (x, y)

    def _bucket(self):

        selection = Editor()["selection"]

        points = deque()
        if (self._point[0] in selection[0] and self._point[1] in selection[1]) and \
                self._board[self._point] != self._fill:
            points.append(self._point)
            self._changed.add(self._point)
            self._board[self._point] = self._fill

        while len(points) != 0:

            x, y = points.pop()

            for j, i in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                if (x + j in selection[0] and y + i in selection[1]) and \
                        self._board[x + j, y + i] != self._fill:
                    points.append((x + j, y + i))
                    self._changed.add((x + j, y + i))
                    self._board[x + j, y + i] = self._fill

        self._calculated = True

    def execute(self):

        if not self._calculated:
            self._bucket()

        else:
            for point in self._changed:
                self._board[point] = not self._board[point]

    def revoke(self):
        self.execute()

    def need_save(self):
        if self._calculated:
            return len(self._changed) != 0
        else:
            return self._board[self._point] != self._fill
