from PyQt5 import QtWidgets, QtCore, QtGui


class TabContainer(QtWidgets.QTabWidget):
    def __init__(self, style):
        super(TabContainer, self).__init__()
        self.setGeometry(QtCore.QRect(90, 60, 1181, 731))
        self.setObjectName("tabWidget")
        self.dict_widget = {}
        self.setStyleSheet(style)

    def fill_tab(self):
        for i in self.dict_widget:
            self.addTab(self.dict_widget[i], i)













