from PyQt5 import QtWidgets, Qt, QtCore
import math
from actionButtons import ActionButtons

class HomeScreen(QtWidgets.QVBoxLayout): 

	def __init__(self, window, parent, title, description):
		super().__init__(parent)
		self.window = window
		self.setSpacing(0)
		self.setAlignment(QtCore.Qt.AlignTop)

		self.lbl_title = QtWidgets.QLabel(title)
		self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
		self.lbl_title.setFixedWidth(window.width())
		self.lbl_title.setStyleSheet('font-size: 30;')

		self.lbl_description = QtWidgets.QLabel(description)
		self.lbl_description.setWordWrap(True)
		self.lbl_description.setAlignment(QtCore.Qt.AlignCenter)

		self.btn_start_lesson = QtWidgets.QPushButton("Start Lesson")
		self.btn_start_lesson.setFixedWidth(math.floor(window.width() / 2))
		self.btn_start_lesson.setStyleSheet('QPushButton { background-color: #f98d58; color: white; border: 1px solid #f98d58; border-radius: 5px; padding: 5px 10px; }')

		self.addLayout(ActionButtons(self.window))
		self.addWidget(self.lbl_title)
		self.addWidget(self.lbl_description)
		self.addWidget(self.btn_start_lesson, alignment=QtCore.Qt.AlignCenter)
