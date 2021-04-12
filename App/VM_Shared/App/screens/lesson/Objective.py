from PyQt5 import QtWidgets, Qt, QtCore
from PyQt5.QtGui import QCursor

class Objective(QtWidgets.QVBoxLayout):

	OBJECTIVE_TYPE = {"0":"Info", "1":"Input", "2":"Checkbox"}

	def __init__(self, parent, objective_data):
		super().__init__()
		self.parent = parent
		self.update_widget(objective_data)

	def update_widget(self, objective_data):
		self.clear_layout()
		self.objective_data = objective_data
		self.lbl_obj_title = QtWidgets.QLabel(self.objective_data['title'])
		self.lbl_obj_title.setStyleSheet('QLabel { font-size: 18px; color: #4f4e59; font-weight: bold; }')

		self.lbl_obj_desc = QtWidgets.QLabel(self.objective_data['description'])
		self.lbl_obj_desc.setWordWrap(True)
		self.lbl_obj_desc.setStyleSheet('QLabel { font-size: 14px; color: #4f4e59;}')

		self.addWidget(self.lbl_obj_title)
		self.addWidget(self.lbl_obj_desc)

		self.btn_continue = QtWidgets.QPushButton("Continue")
		self.btn_continue.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.btn_continue.setDisabled(True)
		self.btn_continue.clicked.connect(lambda: self.parent.swap_challenge(1))

		self.setup_objective_for_type()

		self.addWidget(self.btn_continue)

	def setup_objective_for_type(self):
		if self.objective_data['type'] == "0":
			self.btn_continue.setDisabled(False)
			self.btn_continue.setStyleSheet('QPushButton { background-color: #f98d58; color: white; border: 1px solid #f98d58; border-radius: 5px; padding: 5px 10px; }')
		elif self.objective_data['type'] == "1":
			self.inp_answer = QtWidgets.QLineEdit()
			self.inp_answer.textChanged.connect(self.textinput_changed)
			self.btn_continue.setStyleSheet('QPushButton { background-color: #d14848; color: white; border: 1px solid #d14848; border-radius: 5px; padding: 5px 10px; }')
			self.addWidget(self.inp_answer)
		elif self.objective_data['type'] == "2":
			self.checkbox = QtWidgets.QCheckBox("Complete?")
			self.checkbox.stateChanged.connect(self.checkbox_changed)
			self.btn_continue.setStyleSheet('QPushButton { background-color: #d14848; color: white; border: 1px solid #d14848; border-radius: 5px; padding: 5px 10px; }')
			self.addWidget(self.checkbox)

	def textinput_changed(self):
		for answer in self.objective_data['answers']:
			ans = answer if self.objective_data['case-sensitive'] else answer.lower()
			if ans == str(self.inp_answer.text()):
				self.btn_continue.setDisabled(False)
				self.btn_continue.setStyleSheet('QPushButton { background-color: #6cb85d; color: white; border: 1px solid #6cb85d; border-radius: 5px; padding: 5px 10px; }')
				return

		self.btn_continue.setDisabled(True)
		self.btn_continue.setStyleSheet('QPushButton { background-color: #d14848; color: white; border: 1px solid #d14848; border-radius: 5px; padding: 5px 10px; }')

	def checkbox_changed(self, state):
		if QtCore.Qt.Checked == state:
			self.btn_continue.setDisabled(False)
			self.btn_continue.setStyleSheet('QPushButton { background-color: #6cb85d; color: white; border: 1px solid #6cb85d; border-radius: 5px; padding: 5px 10px; }')
		else:
			self.btn_continue.setDisabled(True)
			self.btn_continue.setStyleSheet('QPushButton { background-color: #d14848; color: white; border: 1px solid #d14848; border-radius: 5px; padding: 5px 10px; }')

	def clear_layout(self):
		for i in reversed(range(self.count())):
			self.itemAt(i).widget().setParent(None)

