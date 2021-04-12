from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from screens.notes.noteLayout import NoteLayout


class NotesWindow(QtWidgets.QDialog):

    def __init__(self, app, parent_widget):
        super(QtWidgets.QDialog, self).__init__()
        self.app = app
        self.parent_widget = parent_widget
        self.setStyleSheet(Stylesheet)

        self.setup_widgets()

    def setup_widgets(self):
        self.widget = QtWidgets.QWidget(self)
        self.widget.setObjectName('rounded-window')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.widget)
        widgetLayout = NoteLayout(self.parent_widget, self.widget)


Stylesheet = """
#rounded-window {
    background: #e4efe9;
    border-radius: 10px;
    opacity: 100;
}
"""