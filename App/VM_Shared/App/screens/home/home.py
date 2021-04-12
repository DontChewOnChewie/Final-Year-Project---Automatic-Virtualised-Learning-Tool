from PyQt5.QtCore  import Qt, QSize, QTimer
from PyQt5 import QtWidgets
import json
import os
from screens.home.homeLayout import HomeLayout
from screens.home.PingSweeper import PingSweeper


class HomeWindow(QtWidgets.QDialog):

    def __init__(self, app, parent_widget):
        super(QtWidgets.QDialog, self).__init__()
        self.app = app
        self.parent_widget = parent_widget
        self.ips = []
        self.setObjectName('Custom_Dialog')
        self.setStyleSheet(Stylesheet)

        self.lesson_data = self.get_lesson_data('../lesson.json')
        self.get_docker_ip_file("../ips.txt")
        sweeper = PingSweeper()
        vm_ip = sweeper.mass_sweep("10.10.10.4")
        self.ips.append(vm_ip)
        self.setup_widgets()

    def setup_widgets(self):
        self.widget = QtWidgets.QWidget(self)
        self.widget.setObjectName('rounded-window')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.widget)
        widgetLayout = HomeLayout(self.parent_widget, self.widget, self.lesson_data['name'], self.ips)


    def get_lesson_data(self, lesson_file):
        if os.path.isfile(lesson_file):
        	with open(lesson_file, 'r') as lesson:
        		return json.load(lesson)
        else:
            return { "name":"Un-Named Lesson" } 

    def get_docker_ip_file(self, docker_ip_file):
        if os.path.isfile(docker_ip_file):
            with open(docker_ip_file, 'r', encoding='utf-16') as _docker_ip_file:
                self.ips.append(_docker_ip_file.read())
                return _docker_ip_file.read()
        return False


Stylesheet = """
#rounded-window {
    background: #e4efe9;
    border-radius: 10px;
    opacity: 100;
}
"""