from PyQt5 import QtWidgets, Qt, QtCore, QtGui

class DockLayout(QtWidgets.QVBoxLayout):

	def __init__(self, window, parent):
		super().__init__(parent)
		self.window = window
		self.setSpacing(10)
		self.setAlignment(QtCore.Qt.AlignCenter)

		self.home_button= QtWidgets.QPushButton()
		self.home_image = QtGui.QPixmap('../home.svg').scaled(40, 40)
		self.home_button.setIcon(QtGui.QIcon(self.home_image))
		self.home_button.setFixedSize(40, 40)
		self.home_button.clicked.connect(lambda: self.window.swap_screen("home"))

		self.lesson_button= QtWidgets.QPushButton()
		self.lesson_image = QtGui.QPixmap('../lesson.svg').scaled(40, 40)
		self.lesson_button.setIcon(QtGui.QIcon(self.lesson_image))
		self.lesson_button.setFixedSize(40, 40)
		self.lesson_button.clicked.connect(lambda: self.window.swap_screen("home"))

		self.ip_button= QtWidgets.QPushButton()
		self.ip_image = QtGui.QPixmap('../ip.svg').scaled(40, 40)
		self.ip_button.setIcon(QtGui.QIcon(self.ip_image))
		self.ip_button.setFixedSize(40, 40)
		self.ip_button.clicked.connect(lambda: self.window.swap_screen("home"))

		self.addWidget(self.home_button, alignment=QtCore.Qt.AlignCenter)
		self.addWidget(self.lesson_button, alignment=QtCore.Qt.AlignCenter)
		self.addWidget(self.ip_button, alignment=QtCore.Qt.AlignCenter)
