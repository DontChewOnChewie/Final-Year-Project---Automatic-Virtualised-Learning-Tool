from PyQt5 import QtWidgets, Qt, QtCore
from PyQt5.QtGui import QCursor
from actionButtons import ActionButtons

class NoteLayout(QtWidgets.QVBoxLayout): 

	def __init__(self, window, parent):
		super().__init__(parent)
		self.window = window
		self.parent = parent

		self.lbl_title = QtWidgets.QLabel("Notes")
		self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
		self.lbl_title.setStyleSheet('QLabel { font-size: 30px; color: #4f4e59; font-weight: bold; }')

		self.inp_notes = QtWidgets.QPlainTextEdit()
		self.inp_notes.setStyleSheet('QPlainTextEdit { border-radius: 10px; }')

		self.addLayout(ActionButtons(self.window))
		self.addWidget(self.lbl_title)
		self.addWidget(self.inp_notes)

