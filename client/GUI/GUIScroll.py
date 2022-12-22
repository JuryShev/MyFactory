
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QFileDialog, qApp, QWidget


class GUIListPersonal(QtWidgets.QWidget):
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



class GUIScrollPersonal():
    def __init__(self, frame_loadList, base_size):
        super(GUIScrollPersonal, self).__init__()
        self.scrollArea_AListPersonal = QtWidgets.QScrollArea(frame_loadList)
        self.scrollArea_AListPersonal.setBaseSize(QtCore.QSize(base_size[0], base_size[1]))
        self.scrollArea_AListPersonal.setWidgetResizable(True)
        self.scrollArea_AListPersonal.setObjectName("scrollArea_AListPersonal_")
        self.scrollArea_AListPersonal_ = QtWidgets.QWidget()
        self.scrollArea_AListPersonal_.setGeometry(QtCore.QRect(0, 0, 650, 464))
        self.scrollArea_AListPersonal_.setObjectName("scrollArea_AListPersonal")
        self.scrollArea_AListPersonal.setWidget(self.scrollArea_AListPersonal_)
        self.scrollArea_AListPersonal.raise_()
        self.Label_NumCurrentList = QtWidgets.QLabel(frame_loadList)
        self.Label_NumCurrentList.raise_()
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.Label_NumCurrentList.setFont(font)
        self.Label_NumCurrentList.setStyleSheet("color: rgb(255, 255, 255);")
        self.Label_NumCurrentList.setObjectName("Label_NumCurrentList")
        self.Label_NumLastList = QtWidgets.QLabel(frame_loadList)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.Label_NumLastList.setFont(font)
        self.Label_NumLastList.setStyleSheet("color: rgb(255, 255, 255);")
        self.Label_NumLastList.setObjectName("Label_NumLastList")
        self.TB_Left_APers = QtWidgets.QToolButton(frame_loadList)
        self.TB_Left_APers.setStyleSheet("")
        self.TB_Left_APers.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "./GUI/icon/arrow_left [#336].png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TB_Left_APers.setIcon(icon)
        self.TB_Left_APers.setObjectName("TB_Left_APers")
        self.TB_Right_APers = QtWidgets.QToolButton(frame_loadList)
        self.TB_Right_APers.setStyleSheet("\n"
                                          "border:none\\n")
        self.TB_Right_APers.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(
            "./GUI/icon/arrow_right [#336].png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TB_Right_APers.setIcon(icon1)
        self.TB_Right_APers.setObjectName("TB_Right_APers")
        self.Label_AllPersonal = QtWidgets.QLabel(frame_loadList)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.Label_AllPersonal.setFont(font)
        self.Label_AllPersonal.setStyleSheet("color: rgb(255, 255, 255);")
        self.Label_AllPersonal.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_AllPersonal.setObjectName("Label_AllPersonal")

        # self.PB_Save_APers = QtWidgets.QPushButton(frame_loadList)
        # font = QtGui.QFont()
        # font.setFamily("Roboto")
        # font.setPointSize(10)
        # font.setBold(False)
        # font.setItalic(False)
        # font.setUnderline(False)
        # font.setWeight(50)
        # font.setStrikeOut(False)
        # self.PB_Save_APers.setFont(font)
        # self.PB_Save_APers.setStyleSheet("\n"
        #                                  "background-color: rgb(209, 209, 209);")
        # self.PB_Save_APers.setObjectName("PB_Save_APers")

        self.Label_NumLastList.raise_()
        self.TB_Left_APers.raise_()
        self.TB_Right_APers.raise_()
        self.Label_AllPersonal.raise_()

