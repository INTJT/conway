from core.project import Project
from core.board import Board
from core.rule import Rule

import re
from PyQt5 import QtWidgets
from ui.ui_project_modal import Ui_Dialog


class ProjectModal(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):

        super(ProjectModal, self).__init__(*args, **kwargs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.project = None
        self.ui.name_edit.textChanged.connect(self.validate)
        self.ui.rule_edit.textChanged.connect(self.validate)
        self.ui.rule_edit.setText("B3/S23")
        self.ui.ok.clicked.connect(lambda: self.close_modal(True))
        self.ui.cancel.clicked.connect(lambda: self.close_modal(False))
        self.validate()

    def validate(self):
        self.ui.ok.setEnabled(self.ui.name_edit.text() != ""
                              and bool(re.match(r"^[bB][0-8]+/[sS][0-8]+$", self.ui.rule_edit.text())))

    def close_modal(self, ok):
        if ok:
            self.project = Project(
                self.ui.name_edit.text(),
                Board.randomized(
                    self.ui.width_box.value(),
                    self.ui.height_box.value(),
                    self.ui.random.value() / 100,
                    Rule.from_bs_notation(self.ui.rule_edit.text())
                ),
                {"life": "#ffffff", "dead": "#000000"}
            )
        super().close()

    @staticmethod
    def open_modal():
        modal = ProjectModal()
        modal.exec()
        return modal.project
