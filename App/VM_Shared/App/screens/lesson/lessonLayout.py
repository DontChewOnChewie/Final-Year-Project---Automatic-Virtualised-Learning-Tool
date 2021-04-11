from PyQt5 import QtWidgets, Qt, QtCore
from PyQt5.QtGui import QCursor, QPixmap
from actionButtons import ActionButtons

class LessonLayout(QtWidgets.QVBoxLayout): 

	def __init__(self, window, parent, lesson_data):
		super().__init__(parent)
		self.window = window
		self.lesson_data = lesson_data
		self.setSpacing(0)
		self.setAlignment(QtCore.Qt.AlignCenter)

		self.lbl_title = QtWidgets.QLabel("Lesson Screen")
		self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
		self.lbl_title.setStyleSheet('QLabel { font-size: 30px; color: #4f4e59; }')

		self.lbl_lesson_name = QtWidgets.QLabel(self.lesson_data['name'])
		self.lbl_lesson_name.setAlignment(QtCore.Qt.AlignCenter)
		self.lbl_lesson_name.setStyleSheet('QLabel { font-size: 16px; color: #4f4e59; }')

		self.addLayout(ActionButtons(self.window))
		self.addWidget(self.lbl_title)
		self.addWidget(self.lbl_lesson_name)

