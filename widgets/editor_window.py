from core.editor import Editor
from core.project import Project

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QColorDialog, QFileDialog

from ui.ui_editor import Ui_Editor
from widgets.board_view import BoardView
from widgets.project_modal import ProjectModal

from core.tools.pencil import Pencil
from core.tools.inverter import Inverter
from core.tools.salt import Salt
from core.tools.bucket import Bucket
from core.tools.select import Select
from core.tools.rectangle import Rectangle
from core.tools.move import Move

from core.rule import Rule
from core.launcher import Launcher, launcher_stop_auto


class EditorWindow(QtWidgets.QMainWindow):

    def _style(self):

        button_size = QSize(25, 25)

        self.ui.undo.setIconSize(button_size)
        self.ui.redo.setIconSize(button_size)

        self.ui.undo.setIcon(QIcon("ui/icons/undo.svg"))
        self.ui.redo.setIcon(QIcon("ui/icons/redo.svg"))

        self.ui.play.setIconSize(button_size)
        self.ui.stop.setIconSize(button_size)
        self.ui.step.setIconSize(button_size)

        self.ui.play.setIcon(QIcon("ui/icons/launcher/play.svg"))
        self.ui.stop.setIcon(QIcon("ui/icons/launcher/stop.svg"))
        self.ui.step.setIcon(QIcon("ui/icons/launcher/step.svg"))

        self.ui.move.setIconSize(button_size)
        self.ui.pencil.setIconSize(button_size)
        self.ui.select.setIconSize(button_size)
        self.ui.salt.setIconSize(button_size)
        self.ui.bucket.setIconSize(button_size)
        self.ui.inverter.setIconSize(button_size)
        self.ui.rectangle.setIconSize(button_size)
        self.ui.hand.setIconSize(button_size)

        self.ui.move.setIcon(QIcon("ui/icons/tools/move.svg"))
        self.ui.pencil.setIcon(QIcon("ui/icons/tools/pencil.svg"))
        self.ui.select.setIcon(QIcon("ui/icons/tools/select.svg"))
        self.ui.salt.setIcon(QIcon("ui/icons/tools/salt.svg"))
        self.ui.bucket.setIcon(QIcon("ui/icons/tools/bucket.svg"))
        self.ui.inverter.setIcon(QIcon("ui/icons/tools/inverter.svg"))
        self.ui.rectangle.setIcon(QIcon("ui/icons/tools/rectangle.svg"))
        self.ui.hand.setIcon(QIcon("ui/icons/tools/hand.svg"))

    def _init_file_menu(self):

        def new_project():
            project_modal = ProjectModal.open_modal()
            if project_modal:
                launcher = Launcher()
                if launcher.enabled:
                    launcher.cancel()
                Editor().project = project_modal
                self.update_project_group()
                self.update_board()

        def save_project():
            filename, _ = QFileDialog.getSaveFileName(parent=self,
                                                      caption='Select save file',
                                                      directory='.',
                                                      filter='Game of life project (*.life)')
            Project.save(Editor().project, filename)

        def open_project():
            try:
                filename, _ = QFileDialog.getOpenFileName(parent=self,
                                                          caption='Select save file',
                                                          directory='.',
                                                          filter='Game of life project (*.life)')
                project = Project.open(filename)
                launcher = Launcher()
                if launcher.enabled:
                    launcher.cancel()
                Editor().project = project
                self.update_project_group()
                self.update_board()
            except:
                pass

        def close_project():
            launcher = Launcher()
            if launcher.enabled:
                launcher.cancel()
            Editor().project = None
            self.update_project_group()
            self.update_board()

        self.ui.action_new.triggered.connect(lambda _: new_project())
        self.ui.action_open.triggered.connect(lambda _: open_project())
        self.ui.action_save.triggered.connect(lambda _: save_project())
        self.ui.action_close.triggered.connect(lambda _: close_project())

    def _init_editor_group(self):

        @launcher_stop_auto
        def undo(_):

            editor = Editor()
            launcher = Launcher()

            if editor.history_length[0] != 0:

                if launcher.enabled:
                    launcher.cancel()
                else:
                    editor.undo()

                self.update_board()

        @launcher_stop_auto
        def redo(_):

            editor = Editor()
            launcher = Launcher()

            if editor.history_length[1] != 0:

                if launcher.enabled:
                    launcher.cancel()
                else:
                    editor.redo()

                self.update_board()

        self.ui.undo.clicked.connect(undo)
        self.ui.redo.clicked.connect(redo)

        def bind_property(prop, slider, f=lambda identity: identity):

            def _inner(_):
                Editor()[prop] = f(slider.value())

            slider.valueChanged.connect(_inner)

        self.ui.radius_slider.setMinimum(1)
        self.ui.radius_slider.setMaximum(100)
        self.ui.radius_slider.setSingleStep(1)
        bind_property("radius", self.ui.radius_slider)

        self.ui.random_slider.setMinimum(1)
        self.ui.random_slider.setMaximum(100)
        self.ui.random_slider.setSingleStep(1)
        self.ui.random_slider.setValue(50)
        bind_property("random", self.ui.random_slider, lambda p: p / 100)

    def _init_launcher_group(self):

        def change_steps(_):
            Launcher().steps = self.ui.steps_slider.value()

        def change_speed(_):
            Launcher().speed = self.ui.speed_slider.value()

        self.ui.steps_slider.setMinimum(1)
        self.ui.steps_slider.setMaximum(100)
        self.ui.steps_slider.setSingleStep(1)
        self.ui.steps_slider.valueChanged.connect(change_steps)

        self.ui.speed_slider.setMinimum(1)
        self.ui.speed_slider.setMaximum(100)
        self.ui.speed_slider.setSingleStep(1)
        self.ui.speed_slider.valueChanged.connect(change_speed)

        def play(_):
            launcher = Launcher()
            if not launcher.enabled:
                launcher.start()
            launcher.auto = not launcher.auto

        def stop(_):
            launcher = Launcher()
            launcher.stop()

        def step(_):
            launcher = Launcher()
            if not launcher.enabled:
                launcher.start()
            if launcher.auto:
                launcher.auto = False
            launcher.iterations()

        Launcher().add_observer("launcher", self.update_launcher)
        Launcher().add_observer("iterations", self.update_board)

        self.ui.play.clicked.connect(play)
        self.ui.step.clicked.connect(step)
        self.ui.stop.clicked.connect(stop)

    def _init_tools_group(self):

        def set_tool(tool):
            Editor().tool = tool

        self.ui.pencil.clicked.connect(lambda _: set_tool(Pencil))
        self.ui.inverter.clicked.connect(lambda _: set_tool(Inverter))
        self.ui.salt.clicked.connect(lambda _: set_tool(Salt))
        self.ui.bucket.clicked.connect(lambda _: set_tool(Bucket))
        self.ui.select.clicked.connect(lambda _: set_tool(Select))
        self.ui.rectangle.clicked.connect(lambda _: set_tool(Rectangle))
        self.ui.move.clicked.connect(lambda _: set_tool(Move))
        self.ui.hand.clicked.connect(lambda _: set_tool(None))

    def _init_project_group(self):

        def update_name():
            project = Editor().project
            if project:
                project.name = self.ui.project_name.text()
                self.update_project_group()

        def update_rule():
            project = Editor().project
            if project:
                try:
                    project.board.rule = Rule.from_bs_notation(self.ui.project_rule.text())
                except ValueError:
                    print("add error dialog here")
                finally:
                    self.update_project_group()

        @launcher_stop_auto
        def change_color(life):

            editor = Editor()

            if editor.project:
                project = editor.project

                dialog = QColorDialog(QColor(project.colors["life" if life else "dead"]))
                dialog.exec()
                project.colors["life" if life else "dead"] = dialog.currentColor().name()

                self.update_project_group()

        self.ui.project_name.editingFinished.connect(update_name)
        self.ui.project_rule.editingFinished.connect(update_rule)
        self.ui.life_button.mouseReleaseEvent = lambda _: change_color(True)
        self.ui.dead_button.mouseReleaseEvent = lambda _: change_color(False)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.ui = Ui_Editor()
        self.ui.setupUi(self)

        self.selection = None
        self.view = BoardView(self.ui.board)

        self._init_file_menu()
        self._init_editor_group()
        self._init_launcher_group()
        self._init_tools_group()
        self._init_project_group()

        self.update_project_group()
        self.update_launcher()
        self._style()

    def update_project_group(self):

        project = Editor().project

        if project:

            self.ui.project_name.setText(project.name)
            self.setWindowTitle(f"Game of Life: {project.name}")

            self.ui.project_rule.setText(project.board.rule.bs_notation)

            self.ui.life_button.setStyleSheet(f"background: {project.colors['life']};")
            self.ui.dead_button.setStyleSheet(f"background: {project.colors['dead']};")

            self.ui.editorPanel.setEnabled(True)
            self.ui.projectGroup.setEnabled(True)
            self.ui.toolsPanel.setEnabled(True)
            self.ui.iterationPanel.setEnabled(True)
            self.ui.groups.setVisible(True)

            self.ui.action_save.setEnabled(True)
            self.ui.action_close.setEnabled(True)

        else:

            self.setWindowTitle("Game of Life")
            self.ui.editorPanel.setEnabled(False)
            self.ui.projectGroup.setEnabled(False)
            self.ui.iterationPanel.setEnabled(False)
            self.ui.toolsPanel.setEnabled(False)
            self.ui.groups.setVisible(False)

            self.ui.action_save.setEnabled(False)
            self.ui.action_close.setEnabled(False)

    def update_launcher(self):
        launcher = Launcher()
        self.ui.stop.setEnabled(launcher.enabled)
        self.ui.play.setIcon(QIcon(f"ui/icons/launcher/{('play' if not launcher.auto else 'pause')}.svg"))

    def update_board(self):
        editor = Editor()
        self.ui.iterations_label.setText(f"Iterations: {editor['iterations']}" if editor['iterations'] != 0 else "")
        self.ui.board.update()
