
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QFileDialog, qApp, QWidget


class GUIListPersonal():
#########################################################################
    def __init__(self, frame_loadList, minimum_size, base_size, style):
        super(GUIListPersonal, self).__init__()
        ####__________________Настройка листа______________________________####
        self.scrollArea_ListPersonal = QtWidgets.QListWidget(frame_loadList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.scrollArea_ListPersonal.setGeometry(QtCore.QRect(0, 0, 530, 641))
        sizePolicy.setHeightForWidth(self.scrollArea_ListPersonal.sizePolicy().hasHeightForWidth())
        self.scrollArea_ListPersonal.setSizePolicy(sizePolicy)
        self.scrollArea_ListPersonal.setMinimumSize(QtCore.QSize(minimum_size[0], minimum_size[1]))  # 0,70
        self.scrollArea_ListPersonal.setBaseSize(QtCore.QSize(base_size[0], base_size[1]))  # 150,150
        self.scrollArea_ListPersonal.setObjectName("scrollArea_AListPersonal_")
        self.scrollArea_ListPersonal.setStyleSheet(style)




