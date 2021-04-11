from PyQt5.QtCore  import Qt, QSize, QTimer
from PyQt5 import QtWidgets
import os
import json
from screens.lesson.lessonLayout import LessonLayout


class LessonWindow(QtWidgets.QDialog):

    def __init__(self, app, parent_widget):
        super(QtWidgets.QDialog, self).__init__()
        self.app = app
        self.parent_widget = parent_widget
        self.setStyleSheet(Stylesheet)

        self.get_lesson_data('../lesson.json')
        self.setup_widgets()

    def setup_widgets(self):
        self.widget = QtWidgets.QWidget(self)
        self.widget.setObjectName('rounded-window')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.widget)
        widgetLayout = LessonLayout(self.parent_widget, self.widget, self.lesson_data)


    def get_lesson_data(self, lesson_file):
        if os.path.isfile(lesson_file):
        	with open(lesson_file, 'r') as lesson:
        		self.lesson_data = json.load(lesson)
        else:
            self.lesson_data = { "name":"No lesson file was uploaded for this task.\n You're on your own!" } 


Stylesheet = """
#rounded-window {
    background: #e4efe9;
    border-radius: 10px;
    opacity: 100;
}
"""