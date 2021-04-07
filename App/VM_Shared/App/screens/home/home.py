from PyQt5.QtCore  import Qt, QSize, QTimer
from PyQt5 import QtWidgets
import sys
import math
import json
from screens.home.homeLayout import HomeLayout


class HomeWindow(QtWidgets.QDialog):

    def __init__(self, app, parent_widget):
        super(QtWidgets.QDialog, self).__init__()
        self.app = app
        self.parent_widget = parent_widget
        self.setObjectName('Custom_Dialog')
        self.setStyleSheet(Stylesheet)

        self.get_lesson_data('../lesson.json')
        self.setup_widgets()

    def setup_widgets(self):
        self.widget = QtWidgets.QWidget(self)
        self.widget.setObjectName('rounded-window')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.widget)
        widgetLayout = HomeLayout(self.parent_widget, self.widget, self.lesson_data['name'])


    def get_lesson_data(self, lesson_file):
    	with open(lesson_file, 'r') as lesson:
    		self.lesson_data = json.load(lesson)    


Stylesheet = """
#rounded-window {
    background: #002025;
    border-radius: 10px;
    opacity: 100;
}
"""