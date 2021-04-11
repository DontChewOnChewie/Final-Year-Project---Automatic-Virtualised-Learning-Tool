from PyQt5 import QtWidgets, Qt, QtCore
from PyQt5.QtGui import QCursor, QPixmap
import math
from actionButtons import ActionButtons

class HomeLayout(QtWidgets.QVBoxLayout): 

	def __init__(self, window, parent, title, ips):
		super().__init__(parent)
		self.window = window
		self.ips = ips
		self.ip_labels = []
		self.setSpacing(10)
		self.setAlignment(QtCore.Qt.AlignTop)

		self.lbl_title = QtWidgets.QLabel(title)
		self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
		self.lbl_title.setStyleSheet('QLabel { font-size: 30px; color: #4f4e59; margin-bottom: 30px; }')

		self.create_ip_labels()

		self.btn_start_lesson = QtWidgets.QPushButton("Start Lesson")
		self.btn_start_lesson.setFixedWidth(math.floor(window.width() / 2))
		self.btn_start_lesson.setStyleSheet('QPushButton { background-color: #f98d58; color: white; border: 1px solid #f98d58; border-radius: 5px; padding: 5px 10px; }')
		self.btn_start_lesson.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.btn_start_lesson.clicked.connect(lambda: self.window.swap_screen("lesson"))

		self.addLayout(ActionButtons(self.window))
		self.addWidget(self.lbl_title)
		for lbl in self.ip_labels:
			self.addLayout(lbl)
		self.addWidget(self.btn_start_lesson, alignment=QtCore.Qt.AlignCenter)

	def create_ip_labels(self):
		for ip in self.ips:
			image = QtWidgets.QLabel()
			if ip.split(":")[0].strip() == "Docker":
				pm = QPixmap("../docker.svg").scaled(30, 30)
				image.setPixmap(pm)
			else:
				pm = QPixmap("../virtualbox.svg").scaled(30, 30)
				image.setPixmap(pm)

			lbl = QtWidgets.QLabel(":".join(ip.split(":")[1:]))
			lbl.setAlignment(QtCore.Qt.AlignCenter)
			lbl.setFixedWidth(150)
			lbl.setStyleSheet('QLabel { color: #4f4e59; } ')

			layout = QtWidgets.QHBoxLayout()
			layout.setAlignment(QtCore.Qt.AlignCenter)
			layout.setSpacing(5)
			layout.addWidget(image)
			layout.addWidget(lbl)
			self.ip_labels.append(layout)


