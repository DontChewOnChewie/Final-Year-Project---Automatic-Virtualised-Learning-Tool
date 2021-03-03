from PyQt5.QtCore  import Qt, QSize, QTimer
from PyQt5 import QtWidgets
import sys
import math
import json
from homeScreen import HomeScreen


class MainWindow(QtWidgets.QDialog):

    def __init__(self, app):
        super(QtWidgets.QDialog, self).__init__()
        self.app = app
        self.setObjectName('Custom_Dialog')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(Stylesheet)

        self.get_lesson_data('challenge.json')
        self.setup_start_window_geometry()
        self.setup_widgets()

    def setup_start_window_geometry(self):
        screenDimensions = self.app.primaryScreen().availableGeometry()
        self.windowSize = [math.floor(screenDimensions.width() * 0.3), math.floor(screenDimensions.height() * 0.8)]
        self.setFixedSize(self.windowSize[0], self.windowSize[1])
        self.windowPosition = [math.floor(screenDimensions.width() * 0.7), math.floor(screenDimensions.height() * 0.1)]
        self.move(self.windowPosition[0], self.windowPosition[1])

    def setup_lesson_window_geometry(self):
        screenDimensions = self.app.primaryScreen().availableGeometry()
        self.windowSize = [math.floor(screenDimensions.width() * 0.8), math.floor(screenDimensions.height() * 0.15)]
        self.setFixedSize(self.windowSize[0], self.windowSize[1])
        self.windowPosition = [math.floor(screenDimensions.width() * 0.1), math.floor(screenDimensions.height() * 0.95)]
        self.move(self.windowPosition[0], self.windowPosition[1])

    def setup_widgets(self):
        self.widget = QtWidgets.QWidget(self)
        self.widget.setObjectName('rounded-window')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.widget)

        widgetLayout = HomeScreen(self, self.widget, self.lesson_data['name'], self.lesson_data['description'])


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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(app)
    win.exec_()