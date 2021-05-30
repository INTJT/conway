if __name__ == "__main__":

    from core.editor import Editor
    from widgets.editor_window import EditorWindow
    from PyQt5 import QtWidgets

    editor = Editor()

    application = QtWidgets.QApplication([])
    window = EditorWindow()
    window.show()
    application.exec()
