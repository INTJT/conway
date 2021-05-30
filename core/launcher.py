from core.editor import Editor
from core.command import Command
from core.observable import Observable

from PyQt5.QtCore import QTimer


class IterationCommand(Command):

    def __init__(self, board):
        self._board = board
        self._backup = board.save()
        self._backup_iterations = Editor()["iterations"]
        self._again = False

    def iteration(self):
        self._board.iteration()
        Editor()["iterations"] += 1

    def execute(self):
        if self._again:
            memento = self._board.save()
            self._board.restore(self._backup)
            self._backup = memento
            self._again = False
            Editor()["iterations"], self._backup_iterations = self._backup_iterations, Editor()["iterations"]

    def revoke(self):
        memento = self._board.save()
        self._board.restore(self._backup)
        self._backup = memento
        Editor()["iterations"], self._backup_iterations = self._backup_iterations, Editor()["iterations"]
        self._again = True

    def need_save(self):
        return self._backup_iterations != Editor()["iterations"]


class Launcher(Observable):

    _instance = None

    @staticmethod
    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            launcher = cls._instance
            super(Launcher, launcher).__init__()
            launcher._set_events(("launcher", "iterations"))

            launcher._timer = QTimer()
            launcher._timer.timeout.connect(launcher.iterations)

            launcher._command = None
            launcher.speed = 1
            launcher._steps = 1

        return cls._instance

    def start(self):
        if self._command is not None:
            raise Exception("It's already started")
        self._command = IterationCommand(Editor().project.board)
        self.notify("launcher")

    def iterations(self):
        for _ in range(self._steps):
            self._command.iteration()
        self.notify("iterations")

    def stop(self):
        if self._command is None:
            raise Exception("It's not started")
        self._timer.stop()
        Editor().execute(self._command)
        self._command = None
        self.notify("launcher")

    def cancel(self):
        if self._command is None:
            raise Exception("It's not started")
        self._timer.stop()
        self._command.revoke()
        self._command = None
        self.notify("launcher")

    @property
    def enabled(self):
        return bool(self._command)

    @property
    def auto(self):
        return self._timer.isActive()

    @auto.setter
    def auto(self, value):
        if not isinstance(value, bool):
            raise ValueError("Value must be a bool")
        elif self._command is None:
            raise Exception("Launcher must be started")
        if value:
            self._timer.start()
        else:
            self._timer.stop()
        self.notify("launcher")

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Value must be a positive integer")
        self._steps = value
        self.notify("launcher")

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Value must be a positive integer")
        self._speed = value
        self._timer.setInterval(1000 / self._speed)
        self.notify("launcher")


def launcher_stop_auto(function):

    def _inner(*args):

        launcher = Launcher()
        closed = False

        if launcher.auto:
            closed = True
            launcher.auto = False

        function(*args)

        if closed and launcher.enabled:
            launcher.auto = True

    return _inner
