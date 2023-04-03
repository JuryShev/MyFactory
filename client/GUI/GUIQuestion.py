from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal


class ButtonConnect(QtWidgets.QPushButton):
    entered = pyqtSignal()
    leaved = pyqtSignal()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.entered.emit()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.leaved.emit()


class GUIQuestion(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("tab_question")
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.setGeometry(QtCore.QRect(50, 10, 1111, 671))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_google = QtWidgets.QWidget()
        self.page_google.setObjectName("page")
        self.stackedWidget.addWidget(self.page_google)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        QtCore.QMetaObject.connectSlotsByName(self)
        ###########float_menu###########################
        self.float_menu = QtWidgets.QFrame(self)
        self.float_menu.setObjectName("float_menu")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.float_menu)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.PB_connect = ButtonConnect(self.float_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PB_connect.sizePolicy().hasHeightForWidth())
        self.PB_connect.setSizePolicy(sizePolicy)
        # self.PB_connect.setMinimumSize(QtCore.QSize(0, 25))
        # self.PB_connect.setMaximumSize(QtCore.QSize(25, 10000))
        self.PB_connect.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PB_connect.setText("")
        self.PB_connect.setIconSize(QtCore.QSize(32, 32))
        self.PB_connect.setCheckable(False)
        self.PB_connect.setChecked(False)
        self.PB_connect.setAutoRepeat(False)
        self.PB_connect.setAutoExclusive(True)
        self.PB_connect.setObjectName("PB_connect")
        self.horizontalLayout_2.addWidget(self.PB_connect)





