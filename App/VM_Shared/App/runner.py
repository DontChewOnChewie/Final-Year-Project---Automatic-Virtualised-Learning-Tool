from PyQt5.QtCore  import Qt, QSize, QTimer
from PyQt5 import QtWidgets
import sys
import math
import os
from screens.home.home import HomeWindow
from screens.dock.dock import DockWindow
from screens.lesson.lesson import LessonWindow
from screens.notes.notes import NotesWindow

class ApplicationRunner(QtWidgets.QStackedWidget):

	def __init__(self, app):
		super(QtWidgets.QStackedWidget, self).__init__()
		self.app = app
		self.routes = { "home": self.standard_screen, "dock": self.dock_screen, "lesson": self.lesson_screen, "notes":self.notes_screen }

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.start = HomeWindow(self.app, self)
		self.dock = DockWindow(self.app, self)
		self.lesson = LessonWindow(self.app, self)
		self.notes = NotesWindow(self.app, self)
		self.addWidget(self.start)
		self.addWidget(self.dock)
		self.addWidget(self.lesson)
		self.addWidget(self.notes)
		self.screen_dimensions = self.app.primaryScreen().availableGeometry()
		self.set_screen_geometry()

	def swap_screen(self, screen):
		try:
			self.routes[screen]()
			return True
		except KeyError:
			return False

	def standard_screen(self):
		self.set_screen_geometry()
		self.setCurrentIndex(0)

	def set_screen_geometry(self):
		self.window_size = [math.floor(self.screen_dimensions.width() * 0.3), math.floor(self.screen_dimensions.height() * 0.5)]
		self.setFixedSize(self.window_size[0], self.window_size[1])
		self.window_position = [math.floor(self.screen_dimensions.width() * 0.35), math.floor(self.screen_dimensions.height() * 0.25)]
		self.move(self.window_position[0], self.window_position[1])

	def dock_screen(self):
		self.set_dock_screen_geometry()
		self.setCurrentIndex(1)

	def set_dock_screen_geometry(self):
		self.window_size = [math.floor(self.screen_dimensions.width() * 0.05), math.floor(self.screen_dimensions.height() * 0.4)]
		self.setFixedSize(self.window_size[0], self.window_size[1])
		self.window_position = [math.floor(self.screen_dimensions.width() * 0.95), math.floor(self.screen_dimensions.height() * 0.3)]
		self.move(self.window_position[0], self.window_position[1])

	def lesson_screen(self):
		self.set_lesson_screen_geometry()
		self.setCurrentIndex(2)

	def set_lesson_screen_geometry(self):
		self.window_size = [math.floor(self.screen_dimensions.width() * 0.3), math.floor(self.screen_dimensions.height() * 0.5)]
		self.setFixedSize(self.window_size[0], self.window_size[1])
		self.window_position = [math.floor(self.screen_dimensions.width() * 0.35), math.floor(self.screen_dimensions.height() * 0.25)]
		self.move(self.window_position[0], self.window_position[1])

	def notes_screen(self):
		self.set_notes_screen_geometry()
		self.setCurrentIndex(3)

	def set_notes_screen_geometry(self):
		self.window_size = [math.floor(self.screen_dimensions.width() * 0.3), math.floor(self.screen_dimensions.height() * 0.5)]
		self.setFixedSize(self.window_size[0], self.window_size[1])
		self.window_position = [math.floor(self.screen_dimensions.width() * 0.35), math.floor(self.screen_dimensions.height() * 0.25)]
		self.move(self.window_position[0], self.window_position[1])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    stacked_widget = ApplicationRunner(app)
    stacked_widget.show()
    sys.exit(app.exec_())
