from PyQt5 import QtWidgets, Qt, QtCore
from screens.dock.dockLayout import DockLayout

class DockWindow(QtWidgets.QDialog):

	def __init__(self, app , parent_widget):
		super(QtWidgets.QDialog, self).__init__()
		self.app = app
		self.parent_widget = parent_widget
		self.setup_widgets()


	def setup_widgets(self):
		self.widget = QtWidgets.QWidget(self)

		layout = QtWidgets.QVBoxLayout(self)
		layout.addWidget(self.widget)
		widgetLayout = DockLayout(self.parent_widget, self.widget)
