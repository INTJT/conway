from core.project import Project
from core.tools.tool import Tool

from collections import deque


class Editor:

    _instance = None

    @staticmethod
    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

            editor = cls._instance

            editor._undo = deque()
            editor._redo = deque()

            editor._project = None
            editor._tool = None

            editor._extensions = dict()

        return cls._instance

    def execute(self, command):
        command.execute()
        if command.need_save():
            self._undo.append(command)
        if len(self._redo) != 0:
            self._redo.clear()

    def undo(self):
        if len(self._undo) != 0:
            command = self._undo.pop()
            command.revoke()
            self._redo.append(command)

    def redo(self):
        if len(self._redo) != 0:
            command = self._redo.pop()
            command.execute()
            self._undo.append(command)

    @property
    def history_length(self): return len(self._undo), len(self._redo)

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, project):
        if project is not None and not isinstance(project, Project):
            raise ValueError("Value must be an instance of class \"Project\"")
        self._project = project
        self._undo.clear()
        self._redo.clear()
        self._tool = None
        self["iterations"] = 0
        self["pre-pencil"] = None
        self["pre-selection"] = None
        self["pre-rectangle"] = None
        self["pre-rectangle-fill"] = None
        self["pre-move"] = (0, 0)
        self["pre-move-fill"] = None
        if project:
            self["selection"] = project.board.full_selection
        else:
            self["selection"] = None

    @property
    def tool(self):
        return self._tool

    @tool.setter
    def tool(self, tool):
        if tool is not None and not issubclass(tool, Tool):
            raise ValueError("Value must be an instance of class \"Tool\"")
        self._tool = tool

    def __getitem__(self, key): return self._extensions[key]
    def __setitem__(self, key, value): self._extensions[key] = value


editor = Editor()

editor["radius"] = 1
editor["selection"] = None
editor["random"] = 0.5
editor["iterations"] = 0

editor["pre-pencil"] = None
editor["pre-selection"] = None

editor["pre-rectangle"] = None
editor["pre-rectangle-fill"] = None

editor["pre-move"] = (0, 0)
editor["pre-move-fill"] = None
