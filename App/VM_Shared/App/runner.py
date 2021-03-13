from PyQt5.QtCore  import Qt, QSize, QTimer
from PyQt5 import QtWidgets
import sys
import math
from screens.home.home import HomeWindow
from screens.dock.dock import DockWindow

class ApplicationRunner(QtWidgets.QStackedWidget):

	def __init__(self, app):
		super(QtWidgets.QStackedWidget, self).__init__()
		self.app = app
		self.routes = { "home": self.start_screen, "dock": self.dock_screen }

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.start_screen = HomeWindow(self.app, self)
		self.dock_screen = DockWindow(self.app, self)
		self.addWidget(self.start_screen)
		self.addWidget(self.dock_screen)
		self.screen_dimensions = self.app.primaryScreen().availableGeometry()
		self.set_start_screen_geometry()

	def swap_screen(self, screen):
		self.routes[screen]()

	def start_screen(self):
		self.set_start_screen_geometry()
		self.setCurrentIndex(0)

	def set_start_screen_geometry(self):
		self.window_size = [math.floor(self.screen_dimensions.width() * 0.3), math.floor(self.screen_dimensions.height() * 0.8)]
		self.setFixedSize(self.window_size[0], self.window_size[1])
		self.window_position = [math.floor(self.screen_dimensions.width() * 0.7), math.floor(self.screen_dimensions.height() * 0.1)]
		self.move(self.window_position[0], self.window_position[1])

	def dock_screen(self):
		self.set_dock_screen_geometry()
		self.setCurrentIndex(1)

	def set_dock_screen_geometry(self):
		self.window_size = [math.floor(self.screen_dimensions.width() * 0.05), math.floor(self.screen_dimensions.height() * 0.4)]
		self.setFixedSize(self.window_size[0], self.window_size[1])
		self.window_position = [math.floor(self.screen_dimensions.width() * 0.95), math.floor(self.screen_dimensions.height() * 0.3)]
		self.move(self.window_position[0], self.window_position[1])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    stacked_widget = ApplicationRunner(app)
    stacked_widget.show()
    sys.exit(app.exec_())
