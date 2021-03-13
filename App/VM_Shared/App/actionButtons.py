from PyQt5 import QtWidgets, Qt, QtCore

class ActionButtons(QtWidgets.QHBoxLayout):

	def __init__(self, window):
		super().__init__()
		self.window = window
		self.setAlignment(QtCore.Qt.AlignRight)

		self.btn_minimise = QtWidgets.QPushButton('-')
		self.btn_minimise.setFixedWidth(40)
		self.btn_minimise.setStyleSheet('QPushButton { background-color: #0054DC; border: 1px solid #0054DC; border-radius: 5px; }')
		self.btn_minimise.clicked.connect(lambda: self.window.swap_screen("dock"))

		self.btn_close = QtWidgets.QPushButton('X')
		self.btn_close.setStyleSheet('QPushButton { background-color: #d14848; border: 1px solid #d14848; border-radius: 5px; margin-left: 5px; }')
		self.btn_close.setFixedWidth(40)
		self.btn_close.clicked.connect(self.window.close)

		self.addWidget(self.btn_minimise)
		self.addWidget(self.btn_close)