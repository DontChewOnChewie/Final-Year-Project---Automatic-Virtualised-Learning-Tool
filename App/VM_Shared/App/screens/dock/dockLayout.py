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
		self.home_button.setStyleSheet('QPushButton { background-color: #f98d58; color: white; border: 2px solid #ffffff; border-radius: 5px; padding: 5px 10px; }')
		self.home_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.home_button.clicked.connect(lambda: self.window.swap_screen("home"))

		self.lesson_button= QtWidgets.QPushButton()
		self.lesson_image = QtGui.QPixmap('../lesson.svg').scaled(40, 40)
		self.lesson_button.setIcon(QtGui.QIcon(self.lesson_image))
		self.lesson_button.setFixedSize(40, 40)
		self.lesson_button.setStyleSheet('QPushButton { background-color: #f98d58; color: white; border: 2px solid #ffffff; border-radius: 5px; padding: 5px 10px; }')
		self.lesson_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.lesson_button.clicked.connect(lambda: self.window.swap_screen("lesson"))

		self.close_button= QtWidgets.QPushButton()
		self.close_image = QtGui.QPixmap('../close.svg').scaled(40, 40)
		self.close_button.setIcon(QtGui.QIcon(self.close_image))
		self.close_button.setFixedSize(40, 40)
		self.close_button.setStyleSheet('QPushButton { background-color: #f98d58; color: white; border: 2px solid #ffffff; border-radius: 5px; padding: 5px 10px; }')
		self.close_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.close_button.clicked.connect(self.window.close)

		self.addWidget(self.home_button, alignment=QtCore.Qt.AlignCenter)
		self.addWidget(self.lesson_button, alignment=QtCore.Qt.AlignCenter)
		self.addWidget(self.close_button, alignment=QtCore.Qt.AlignCenter)
