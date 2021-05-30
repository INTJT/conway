from core.editor import Editor
from core.launcher import Launcher

from PIL.ImageQt import ImageQt
from PIL.Image import fromarray

from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor, QBitmap, QPen


class BoardView:

    def __init__(self, widget):

        self.widget = widget

        self.command = None
        self.stop_auto = None

        self.position = (0, 0)
        self.previous_position = None
        self._button = None
        self.zoom = 5

        self.widget.setMouseTracking(True)

        self.widget.paintEvent = lambda _: self.render()

        self.widget.mousePressEvent = self.mouse_press
        self.widget.mouseMoveEvent = self.mouse_move
        self.widget.mouseReleaseEvent = self.mouse_release
        self.widget.wheelEvent = self.wheel
        self.widget.setMouseTracking(True)

    def get_position(self, x, y):
    
        board = Editor().project.board

        center = (self.widget.width() / 2, self.widget.height() / 2)
        start = (center[0] + self.position[0] - self.zoom * board.width / 2,
                 center[1] + self.position[1] - self.zoom * board.height / 2)

        return int((x - start[0]) / self.zoom), int((y - start[1]) / self.zoom)
    
    def move(self, dx, dy):
        self.position = (self.position[0] + dx, self.position[0] + dy)
        self.render()

    def render(self):

        editor = Editor()
        project = editor.project

        if project:

            board = project.board
            view = board.view if editor["pre-pencil"] is None else editor["pre-pencil"]

            center = (self.widget.width() / 2, self.widget.height() / 2)
            start = (center[0] + self.position[0] - self.zoom * board.width / 2,
                     center[1] + self.position[1] - self.zoom * board.height / 2)

            qp = QPainter()
            qp.begin(self.widget)

            qp.setBackgroundMode(QtCore.Qt.OpaqueMode)

            live, dead = QColor(project.colors["life"]), QColor(project.colors["dead"])

            qp.setPen(live)
            qp.setBackground(dead)

            image = ImageQt(fromarray(view))
            pixmap = QBitmap.fromImage(image)

            qp.drawPixmap(
                QtCore.QRectF(start[0], start[1], self.zoom * board.width, self.zoom * board.height),
                pixmap,
                QtCore.QRectF(0, 0, board.width, board.height)
            )

            x_selection, y_selection = editor["selection"] \
                if editor["pre-selection"] is None else editor["pre-selection"]

            selection_rect = QtCore.QRectF(
                start[0] + min(x_selection) * self.zoom,
                start[1] + min(y_selection) * self.zoom,
                (max(x_selection) - min(x_selection) + 1) * self.zoom,
                (max(y_selection) - min(y_selection) + 1) * self.zoom
            )

            qp.fillRect(
                selection_rect,
                live if editor["pre-move-fill"] else dead
            )

            move = editor["pre-move"]
            selection_rect.adjust(move[0] * self.zoom, move[1] * self.zoom, move[0] * self.zoom, move[1] * self.zoom)

            qp.drawPixmap(
                selection_rect,
                pixmap,
                QtCore.QRectF(
                    min(x_selection),
                    min(y_selection),
                    max(x_selection) - min(x_selection) + 1,
                    max(y_selection) - min(y_selection) + 1
                )
            )

            if x_selection != range(board.width) or y_selection != range(board.height):

                qp.setPen(QPen(QColor.fromRgb(
                    255 - live.red(),
                    255 - live.green(),
                    255 - live.blue()), 2.5))

                qp.drawRect(selection_rect)

            pre_rectangle = editor["pre-rectangle"]
            if pre_rectangle and len(pre_rectangle[0]) != 0 and len(pre_rectangle[1]) != 0:
                qp.fillRect(
                    QtCore.QRectF(
                        start[0] + min(pre_rectangle[0]) * self.zoom,
                        start[1] + min(pre_rectangle[1]) * self.zoom,
                        (max(pre_rectangle[0]) - min(pre_rectangle[0]) + 1) * self.zoom,
                        (max(pre_rectangle[1]) - min(pre_rectangle[1]) + 1) * self.zoom
                    ),
                    live if editor["pre-rectangle-fill"] else dead
                )

            qp.end()

    def mouse_press(self, event):

        if not self._button:

            self.previous_position = event

            button = event.button()

            if button == QtCore.Qt.LeftButton or \
                    button == QtCore.Qt.RightButton:

                self._button = QtCore.Qt.LeftButton if button == QtCore.Qt.LeftButton else QtCore.Qt.RightButton

                editor = Editor()
                if editor.tool:

                    launcher = Launcher()
                    if launcher.auto:
                        launcher.auto = False
                        self.stop_auto = True

                    self.command = Editor().tool(button == QtCore.Qt.LeftButton, Editor().project.board)
                    self.mouse_move(event)

    def mouse_move(self, event):

        if Editor().project:

            if event.buttons() == QtCore.Qt.NoButton:
                pass

            elif self.command:
                self.command.move(*self.get_position(event.x(), event.y()))
                self.widget.update()

            else:
                position = event.pos()
                self.position = (self.position[0] + position.x() - self.previous_position.x(),
                                 self.position[1] + position.y() - self.previous_position.y())
                self.previous_position = position
                self.widget.update()

    def mouse_release(self, event):

        button = event.button()

        if button == self._button:

            self.previous_position = None

            if self.command:

                launcher = Launcher()
                enabled = False

                if self.command.need_save():
                    if launcher.enabled:
                        enabled = True
                        launcher.stop()

                Editor().execute(self.command)
                self.command = None

                if enabled:
                    launcher.start()
                    if self.stop_auto:
                        launcher.auto = True
                        self.stop_auto = None

            self._button = None

        self.widget.update()

    def wheel(self, event):

        d = -event.angleDelta().y()
        scale = 0.5 if d > 0 else 2

        if self.zoom * scale > 0.01:

            c = (self.widget.width() / 2, self.widget.height() / 2)
            e = (event.x() - c[0], event.y() - c[1])
            v = (self.position[0] - e[0], self.position[1] - e[1])

            self.position = (e[0] + scale * v[0], e[1] + scale * v[1])

            self.zoom *= scale
            self.widget.update()
