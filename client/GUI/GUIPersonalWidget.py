from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import  pyqtSignal

from PyQt5.QtWidgets import QDialog, QFileDialog, qApp, QWidget

class GUIPersonalWidget (QtWidgets.QWidget):
    def __init__(self, id_widget, path_icon_edit, parent=None):

        super(GUIPersonalWidget, self).__init__(parent)
        self.id = id_widget
        ##################################
        self.comment_icon = "C:\\Users\\Yura\\PycharmProjects\\pythonProject\\my_project\\furniture_factory\\GUI_designer\\icon/comment 4.png"
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.comment_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.GLay_LPers = QtWidgets.QFrame(self)
        self.GLay_LPers.setGeometry(QtCore.QRect(310, 240, 512, 93))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GLay_LPers.sizePolicy().hasHeightForWidth())
        self.GLay_LPers.setSizePolicy(sizePolicy)
        self.GLay_LPers.setMinimumSize(QtCore.QSize(0, 90))
        self.GLay_LPers.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.GLay_LPers.setObjectName("GLay_LPers_2")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.GLay_LPers)
        self.gridLayout_8.setContentsMargins(12, -1, 12, 5)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.SP_Lastval = QtWidgets.QSplitter(self.GLay_LPers)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SP_Lastval.sizePolicy().hasHeightForWidth())
        self.SP_Lastval.setSizePolicy(sizePolicy)
        self.SP_Lastval.setOrientation(QtCore.Qt.Vertical)
        self.SP_Lastval.setObjectName("SP_Lastval_2")
        self.label_name_Lastval = QtWidgets.QLabel(self.SP_Lastval)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(9)
        self.label_name_Lastval.setFont(font)
        self.label_name_Lastval.setObjectName("label_name_Lastval_2")
        self.label_Lastval = QtWidgets.QLabel(self.SP_Lastval)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_Lastval.setFont(font)
        self.label_Lastval.setObjectName("label_Lastval_2")
        self.gridLayout_8.addWidget(self.SP_Lastval, 0, 6, 2, 1)
        self.SP_Meanval = QtWidgets.QSplitter(self.GLay_LPers)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SP_Meanval.sizePolicy().hasHeightForWidth())
        self.SP_Meanval.setSizePolicy(sizePolicy)
        self.SP_Meanval.setOrientation(QtCore.Qt.Vertical)
        self.SP_Meanval.setObjectName("SP_Meanval_2")
        self.label_name_Meanval = QtWidgets.QLabel(self.SP_Meanval)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(9)
        self.label_name_Meanval.setFont(font)
        self.label_name_Meanval.setObjectName("label_name_Meanval_2")
        self.label_Meanval = QtWidgets.QLabel(self.SP_Meanval)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_Meanval.setFont(font)
        self.label_Meanval.setObjectName("label_Meanval_2")
        self.gridLayout_8.addWidget(self.SP_Meanval, 0, 5, 2, 1)
        spacerItem9 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem9, 0, 3, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(7, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem10, 0, 1, 1, 1)
        self.TB_LPersCommentAssessment = QtWidgets.QToolButton(self.GLay_LPers)
        self.TB_LPersCommentAssessment.setMinimumSize(QtCore.QSize(30, 30))
        self.TB_LPersCommentAssessment.setStyleSheet("\n"
                                                           "border:none\\n")
        self.TB_LPersCommentAssessment.setIcon(icon4)
        self.TB_LPersCommentAssessment.setIconSize(QtCore.QSize(35, 35))
        self.TB_LPersCommentAssessment.setCheckable(False)
        self.TB_LPersCommentAssessment.setObjectName("label_LPersCommentAssessment_14")
        self.gridLayout_8.addWidget(self.TB_LPersCommentAssessment, 2, 5, 3, 1)
        self.label_LPersPhoto = QtWidgets.QLabel(self.GLay_LPers)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_LPersPhoto.sizePolicy().hasHeightForWidth())
        self.label_LPersPhoto.setSizePolicy(sizePolicy)
        self.label_LPersPhoto.setMinimumSize(QtCore.QSize(64, 64))
        self.label_LPersPhoto.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_LPersPhoto.setText("")
        self.label_LPersPhoto.setObjectName("label_LPersPhoto_2")
        self.gridLayout_8.addWidget(self.label_LPersPhoto, 0, 0, 4, 1)
        self.label_LPersCheckAssessment = QtWidgets.QLabel(self.GLay_LPers)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_LPersCheckAssessment.sizePolicy().hasHeightForWidth())
        self.label_LPersCheckAssessment.setSizePolicy(sizePolicy)
        self.label_LPersCheckAssessment.setMinimumSize(QtCore.QSize(20, 20))
        self.label_LPersCheckAssessment.setStyleSheet("border-image: url(:/newPrefix/icon/tick-mark.png);")
        self.label_LPersCheckAssessment.setText("")
        self.label_LPersCheckAssessment.setObjectName("label_LPersCheckAssessment_2")
        self.gridLayout_8.addWidget(self.label_LPersCheckAssessment, 0, 4, 1, 1)
        self.VLay_Name_LPers = QtWidgets.QFrame(self.GLay_LPers)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VLay_Name_LPers.sizePolicy().hasHeightForWidth())
        self.VLay_Name_LPers.setSizePolicy(sizePolicy)
        self.VLay_Name_LPers.setObjectName("VLay_Name_LPers_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.VLay_Name_LPers)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.Label_LPersLastName = QtWidgets.QLabel(self.VLay_Name_LPers)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.Label_LPersLastName.setFont(font)
        self.Label_LPersLastName.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_LPersLastName.setObjectName("Label_LPersLastName_2")
        self.verticalLayout_9.addWidget(self.Label_LPersLastName)
        self.Label_LPersName = QtWidgets.QLabel(self.VLay_Name_LPers)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_LPersName.sizePolicy().hasHeightForWidth())
        self.Label_LPersName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.Label_LPersName.setFont(font)
        self.Label_LPersName.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_LPersName.setObjectName("Label_LPersName_2")
        self.verticalLayout_9.addWidget(self.Label_LPersName)
        self.gridLayout_8.addWidget(self.VLay_Name_LPers, 0, 2, 5, 1)
        self.verticalLayout_3.addWidget(self.GLay_LPers)

class GUIPersonalWidgetScroll (QtWidgets.QWidget):


    def __init__(self, id_widget: int, path_icon_edit, parent=None):
        super(GUIPersonalWidgetScroll, self).__init__(parent)
        self.id=id_widget
        self.path_icon_edit=path_icon_edit
        self.flag_edit=0
        self.comment=''
        self._translate = QtCore.QCoreApplication.translate
        self.Pers_new = QtWidgets.QFrame()  # self.WorkWindow.scrollArea_AListPersonal
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.config_pers_frame()
        self.Label_APersPhoto_new = QtWidgets.QLabel(self.Pers_new)
        self.Label_APersPhoto_new=self.config_label(self.Label_APersPhoto_new,
                                                    QtCore.QRect(10, 10, 64, 64),
                                                    stylesheet="background-color: rgb(255, 255, 255);",
                                                    name="Label_APersPhoto_3")


        self.TB_APersCommentAssessment_new = QtWidgets.QToolButton(self.Pers_new)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:\\Users\\Yura\\PycharmProjects\\pythonProject\\my_project\\furniture_factory\\GUI_designer\\icon/comment 4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TB_APersCommentAssessment_new=self.config_button(self.TB_APersCommentAssessment_new,
                                                              QtCore.QRect(530, 40, 51, 41), stylesheet="\n""border:none\\n",
                                                              icon=icon1, icon_size=QtCore.QSize(35, 35), name="Label_APersCommentAssessment_3"
                                                              )


        self.ComboBox_SelectAssessment_new = QtWidgets.QComboBox(self.Pers_new)
        self.ComboBox_SelectAssessment_new.addItem("")
        self.ComboBox_SelectAssessment_new.setItemText(0, self._translate("MainWindow", 'не оценен'))
        self.ComboBox_SelectAssessment_new.setGeometry(QtCore.QRect(530, 10, 80, 22))
        self.ComboBox_SelectAssessment_new.setObjectName("ComboBox_SelectAssessment_3")
        self.ComboBox_SelectAssessment_new.currentTextChanged.connect(self.combobox_select_assessment_emit)

        self.Label_APersName_new = QtWidgets.QLabel(self.Pers_new)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)

        self.Label_APersLastName_new = QtWidgets.QLabel(self.Pers_new)
        self.Label_APersLastName_new=self.config_label(self.Label_APersLastName_new,
                                                       rect=QtCore.QRect(80, 20, 391, 20),
                                                       font=font, name="Label_APersLastName_3")
        self.Label_APersLastName_new.setAlignment(QtCore.Qt.AlignCenter)

        self.Label_APersName_new=self.config_label(self.Label_APersName_new,rect=QtCore.QRect(80, 50, 391, 20),
                                                   font=font, name="Label_APersName_3")
        self.Label_APersName_new.setAlignment(QtCore.Qt.AlignCenter)



        self.TB_APersCheckEdit_new = QtWidgets.QToolButton(self.Pers_new)
        self.icon_APersCheckEdit_new = QtGui.QIcon()
        self.icon_APersCheckEdit_new.addPixmap(QtGui.QPixmap(self.path_icon_edit
            ),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TB_APersCheckEdit_new=self.config_button(self.TB_APersCheckEdit_new,
                                                      QtCore.QRect(503, 4, 21, 31), stylesheet="\n""border:none\\n",
                                                      icon=self.icon_APersCheckEdit_new, icon_size=QtCore.QSize(17, 17), name="Label_APersCheckEdit_3"
                                                      )
        self.TB_APersCheckEdit_new.setCheckable(False)
        self.TB_APersCheckEdit_new.clicked.connect(self.edit_assessment)

        self.Label_APersCheckAssessment_new = QtWidgets.QLabel(self.Pers_new)
        self.Label_APersCheckAssessment_new=self.config_label(self.Label_APersCheckAssessment_new,
                                                              rect=QtCore.QRect(479, 10, 21, 21),
                                                              stylesheet="border-image: url(C:\\Users\\Yura\\PycharmProjects\\pythonProject\\my_project\\furniture_factory\\GUI_designer\\icon/comment 4.png);",
                                                              name="Label_APersCheckAssessment_3")

    def config_pers_frame(self):
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.Pers_new.setSizePolicy(self.sizePolicy)
        self.Pers_new.setMinimumSize(QtCore.QSize(100, 90))
        self.Pers_new.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.Pers_new.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Pers_new.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Pers_new.setObjectName("Pers_new")
    def config_label(self, label_config,rect, text="", stylesheet="", font=None, name=""):
        label_config.setGeometry(rect)
        label_config.setStyleSheet(stylesheet)#
        if font!=None:
            label_config.setFont(font)
        label_config.setText(text)
        label_config.setObjectName(name)#""
        return label_config
    def config_button(self, button_conf, rect, stylesheet="", icon=None, icon_size=None, name=""  ):
        button_conf.setGeometry(rect)#
        button_conf.setStyleSheet(stylesheet)
        if icon!=None:
            button_conf.setIcon(icon)
            button_conf.setIconSize(icon_size)#
        button_conf.setObjectName(name)
        return button_conf
    def config_combobox(self):

        self.ComboBox_SelectAssessment_new.setGeometry(QtCore.QRect(530, 10, 80, 22))
        self.ComboBox_SelectAssessment_new.setObjectName("ComboBox_SelectAssessment_3")
        self.ComboBox_SelectAssessment_new.addItem("")

