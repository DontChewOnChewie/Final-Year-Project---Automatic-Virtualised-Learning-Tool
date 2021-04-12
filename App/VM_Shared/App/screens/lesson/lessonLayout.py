from PyQt5 import QtWidgets, Qt, QtCore
from PyQt5.QtGui import QCursor, QPixmap
from actionButtons import ActionButtons
from screens.lesson.Objective import Objective

class LessonLayout(QtWidgets.QVBoxLayout): 

	def __init__(self, window, parent, lesson_data):
		super().__init__(parent)
		self.window = window
		self.lesson_data = lesson_data
		self.current_obj = 0
		self.setSpacing(0)
		self.setAlignment(QtCore.Qt.AlignCenter)

		self.lbl_title = QtWidgets.QLabel("Lesson Screen")
		self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
		self.lbl_title.setStyleSheet('QLabel { font-size: 30px; color: #4f4e59; font-weight: bold; }')

		self.lbl_lesson_name = QtWidgets.QLabel(self.lesson_data['name'])
		self.lbl_lesson_name.setAlignment(QtCore.Qt.AlignCenter)
		self.lbl_lesson_name.setStyleSheet('QLabel { font-size: 16px; color: #4f4e59; margin-bottom: 15px; }')

		self.addLayout(ActionButtons(self.window))
		self.addWidget(self.lbl_title)
		self.addWidget(self.lbl_lesson_name)

		if "objectives" in self.lesson_data.keys():
			self.objectives = self.lesson_data['objectives']
			self.objective = Objective(self, self.objectives[self.current_obj])
			self.addLayout(self.objective)

	def swap_challenge(self, incr):
		if self.current_obj + incr == len(self.objectives):
			self.objective.show_start_screen()
			return

		if self.current_obj + incr > -1 and self.current_obj < len(self.objectives) - 1:
			self.current_obj += incr
			self.objective.update_widget(self.objectives[self.current_obj])
