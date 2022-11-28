from PyQt5 import QtCore, QtGui, QtWidgets

class LayRegistr:
    def set_registr(self, layoutWidget, maximum_size: tuple):
        self.registr_frame = QtWidgets.QFrame(layoutWidget)
        self.registr_frame.setMaximumSize(QtCore.QSize(maximum_size[0], maximum_size[1]))  # 16777215, 150
        self.registr_frame.setStyleSheet(" border-width: 1px;\n"
                                         " border-style: solid;\n"
                                         " border-color:  rgb(158, 158, 158);\n"
                                         "border-radius: 15px;")
        self.registr_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.registr_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.registr_frame.setObjectName("registr_frame")
        self.LE_Password = QtWidgets.QLineEdit(self.registr_frame)
        self.LE_Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LE_Password.setGeometry(QtCore.QRect(20, 80, 251, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.LE_Password.setFont(font)
        self.LE_Password.setStyleSheet("border:none;\n"
                                       "border-bottom: 1px solid rgb(16,240,207);\n"
                                       "padding_bottom: 7px;\n"
                                       "background-color: rgb(255, 255,255);\n"
                                       "border-radius: 5px;\n"
                                       "")
        self.LE_Password.setObjectName("LE_Password")
        self.QL_Headline_registr = QtWidgets.QLabel(self.registr_frame)
        self.QL_Headline_registr.setGeometry(QtCore.QRect(10, 10, 291, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.QL_Headline_registr.setFont(font)
        self.QL_Headline_registr.setStyleSheet("color: rgb(255, 255, 255);\n"
                                               " border-color:  rgb(74,80 ,106 );")
        self.QL_Headline_registr.setAlignment(QtCore.Qt.AlignCenter)
        self.QL_Headline_registr.setObjectName("QL_Headline_registr")
        self.LE_Name = QtWidgets.QLineEdit(self.registr_frame)

        self.LE_Name.setGeometry(QtCore.QRect(20, 40, 251, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.LE_Name.setFont(font)
        self.LE_Name.setStyleSheet("border:none;\n"
                                   "border-bottom: 1px solid rgb(16,240,207);\n"
                                   "padding_bottom: 7px;\n"
                                   "background-color: rgb(255, 255,255);\n"
                                   "border-radius: 5px;\n"
                                   "")
        self.LE_Name.setObjectName("LE_Name")
        self.QL_Error_name = QtWidgets.QLabel(self.registr_frame)
        self.QL_Error_name.setGeometry(QtCore.QRect(20, 60, 271, 16))
        self.QL_Error_name.setStyleSheet("border-color:  rgb(74,80 ,106 );\n"
                                         "color: rgb(255, 129, 112);")
        self.QL_Error_name.setObjectName("QL_Error_name")
        self.QL_Error_pass = QtWidgets.QLabel(self.registr_frame)
        self.QL_Error_pass.setGeometry(QtCore.QRect(20, 100, 271, 16))
        self.QL_Error_pass.setStyleSheet("border-color:  rgb(74,80 ,106 );\n"
                                         "color: rgb(255, 129, 112);")
        self.QL_Error_pass.setObjectName("QL_Error_pass")
        self.QL_Name_status = QtWidgets.QLabel(self.registr_frame)
        self.QL_Name_status.setEnabled(True)
        self.QL_Name_status.setGeometry(QtCore.QRect(280, 40, 17, 17))
        self.QL_Name_status.setStyleSheet("border-image: url(:/newPrefix/icon/asterisk.png);\n"
                                          "image: url(:/newPrefix/icon/asterisk.png);")
        self.QL_Name_status.setText("")
        self.QL_Name_status.setObjectName("QL_Name_status")
        self.QL_Password_status = QtWidgets.QLabel(self.registr_frame)
        self.QL_Password_status.setEnabled(True)
        self.QL_Password_status.setGeometry(QtCore.QRect(280, 80, 17, 17))
        self.QL_Password_status.setStyleSheet("border-image: url(:/newPrefix/icon/asterisk.png);")
        self.QL_Password_status.setText("")
        self.QL_Password_status.setObjectName("QL_Password_status")
        self.QL_Password_rep_status = QtWidgets.QLabel(self.registr_frame)
        self.QL_Password_rep_status.setEnabled(True)
        self.QL_Password_rep_status.setGeometry(QtCore.QRect(280, 120, 17, 17))
        self.QL_Password_rep_status.setStyleSheet("border-image: url(:/newPrefix/icon/asterisk.png);")
        self.QL_Password_rep_status.setText("")
        self.QL_Password_rep_status.setObjectName("QL_Password_rep_status")
        self.LE_Password_rep = QtWidgets.QLineEdit(self.registr_frame)
        self.LE_Password_rep.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LE_Password_rep.setGeometry(QtCore.QRect(20, 120, 251, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.LE_Password_rep.setFont(font)
        self.LE_Password_rep.setStyleSheet("border:none;\n"
                                           "border-bottom: 1px solid rgb(16,240,207);\n"
                                           "padding_bottom: 7px;\n"
                                           "background-color: rgb(255, 255,255);\n"
                                           "border-radius: 5px;\n"
                                           "")
        self.LE_Password_rep.setObjectName("LE_Password_rep")
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.LE_Password.setPlaceholderText(_translate("UserRule", "пароль"))
        self.QL_Headline_registr.setText(_translate("UserRule", "регистрация пользователя"))
        self.LE_Name.setPlaceholderText(_translate("UserRule", "имя"))
        self.QL_Error_name.setText(_translate("UserRule", "слишком короткое имя"))
        self.QL_Error_pass.setText(_translate("UserRule", "слишком короткий пароль"))
        self.LE_Password_rep.setPlaceholderText(_translate("UserRule", "повторите пароль"))

class LayRule:
    def set_rule(self, layoutWidget):
        self.rule_frame = QtWidgets.QFrame(layoutWidget)
        self.rule_frame.setStyleSheet(" border-width: 1px;\n"
                                      " border-style: solid;\n"
                                      " border-color:  rgb(158, 158, 158);\n"
                                      "border-radius: 20px;")
        self.rule_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.rule_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rule_frame.setObjectName("rule_frame")
        self.frame_analytics = QtWidgets.QFrame(self.rule_frame)
        self.frame_analytics.setGeometry(QtCore.QRect(10, 100, 291, 35))
        self.frame_analytics.setStyleSheet(" border-color:  rgb(74,80 ,106 );\n"
                                           "border-bottom: 1px solid rgb(160, 241, 235);\n"
                                           "padding_bottom: 7px;")
        self.frame_analytics.setObjectName("frame_analytics")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_analytics)
        self.horizontalLayout_4.setObjectName("horizontalLayout_5")
        self.checkBox_analytics = QtWidgets.QCheckBox(self.frame_analytics)
        self.checkBox_analytics.setStyleSheet(" border-color:  rgb(74,80 ,106 );\n"
                                              "color: rgb(255, 255, 255);\n"
                                              "")
        self.checkBox_analytics.setObjectName("checkBox_analytics")
        self.horizontalLayout_4.addWidget(self.checkBox_analytics)

        self.frame_assessment = QtWidgets.QFrame(self.rule_frame)
        self.frame_assessment.setGeometry(QtCore.QRect(10, 220, 291, 35))
        self.frame_assessment.setStyleSheet(" border-color:  rgb(74,80 ,106 );\n"
                                            "border-bottom: 1px solid rgb(160, 241, 235);\n"
                                            "padding_bottom: 7px;")
        self.frame_assessment.setObjectName("frame_assessment")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_assessment)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.checkBox_assessment = QtWidgets.QCheckBox(self.frame_assessment)
        self.checkBox_assessment.setStyleSheet(" border-color:  rgb(74,80 ,106 );\n"
                                               "color: rgb(255, 255, 255);\n"
                                               "")
        self.checkBox_assessment.setObjectName("checkBox_assessment")
        self.horizontalLayout_6.addWidget(self.checkBox_assessment)
        self.frame_project = QtWidgets.QFrame(self.rule_frame)
        self.frame_project.setGeometry(QtCore.QRect(10, 140, 291, 35))
        self.frame_project.setStyleSheet(" border-color:  rgb(74,80 ,106 );\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "border-bottom: 1px solid rgb(160, 241, 235);\n"
                                         "padding_bottom: 7px;\n"
                                         "")
        self.frame_project.setObjectName("frame_project")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_project)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.checkBox_project = QtWidgets.QCheckBox(self.frame_project)
        self.checkBox_project.setStyleSheet(" border-color:  rgb(74,80 ,106 );")
        self.checkBox_project.setObjectName("checkBox_project")
        self.horizontalLayout_7.addWidget(self.checkBox_project)
        self.QL_Headline_rule = QtWidgets.QLabel(self.rule_frame)
        self.QL_Headline_rule.setGeometry(QtCore.QRect(10, 30, 291, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.QL_Headline_rule.setFont(font)
        self.QL_Headline_rule.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            " border-color:  rgb(74,80 ,106 );")
        self.QL_Headline_rule.setAlignment(QtCore.Qt.AlignCenter)
        self.QL_Headline_rule.setObjectName("QL_Headline_rule")
        self.QL_Error_rule = QtWidgets.QLabel(self.rule_frame)
        self.QL_Error_rule.setGeometry(QtCore.QRect(20, 270, 271, 16))
        self.QL_Error_rule.setStyleSheet("border-color:  rgb(74,80 ,106 );\n"
                                         "color: rgb(255, 129, 112);")
        self.QL_Error_rule.setObjectName("QL_Error_rule")
        self.frame_personal = QtWidgets.QFrame(self.rule_frame)
        self.frame_personal.setGeometry(QtCore.QRect(10, 60, 291, 35))
        self.frame_personal.setStyleSheet(" border-color:  rgb(74, 80, 106);\n"
                                          "border-bottom: 1px solid rgb(160, 241, 235);\n"
                                          "")
        self.frame_personal.setObjectName("frame_personal")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_personal)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox_personal = QtWidgets.QCheckBox(self.frame_personal)
        self.checkBox_personal.setStyleSheet("color: rgb(255, 255, 255);\n"
                                             " border-color:  rgb(74,80 ,106 );")
        self.checkBox_personal.setObjectName("checkBox_personal")
        self.horizontalLayout_4.addWidget(self.checkBox_personal)

        ############################################################
        self.frame_struct = QtWidgets.QFrame(self.rule_frame)
        self.frame_struct.setGeometry(QtCore.QRect(10, 180, 291, 35))
        self.frame_struct.setStyleSheet(" border-color:  rgb(74,80 ,106 );\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border-bottom: 1px solid rgb(160, 241, 235);\n"
                                        "padding_bottom: 7px;\n"
                                        "")
        self.frame_struct.setObjectName("frame_struct")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_struct)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.checkBox_struct = QtWidgets.QCheckBox(self.frame_struct)
        self.checkBox_struct.setStyleSheet(" border-color:  rgb(74,80 ,106 );")
        self.checkBox_struct.setObjectName("checkBox_struct")
        self.horizontalLayout_8.addWidget(self.checkBox_struct)
        #################################################################

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.checkBox_analytics.setText(_translate("UserRule", "Аналитика"))
        #self.checkBox_struct.setText(_translate("UserRule", "Структура"))
        self.checkBox_assessment.setText(_translate("UserRule", "Оценка"))
        self.checkBox_project.setText(_translate("UserRule", "Проекты"))
        self.QL_Headline_rule.setText(_translate("UserRule", "права пользователя"))
        self.QL_Error_rule.setText(_translate("UserRule", "не выбрано не одно поле"))
        self.checkBox_personal.setText(_translate("UserRule", "Персонал"))
        self.checkBox_struct.setText(_translate("UserRule", "Структура"))


class DialogUserRule(QtWidgets.QDialog):
    def __init__(self):
        super(DialogUserRule, self).__init__()
        self.setObjectName("Dialog")
        self.resize(400, 545)
        self.setStyleSheet("background-color: rgb(74, 80, 106);")
        self.layoutWidget = QtWidgets.QWidget(self)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 20, 321, 451))
        self.layoutWidget.setObjectName("layoutWidget")
        self.VL_Build = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.VL_Build.setContentsMargins(0, 0, 0, 0)
        self.VL_Build.setObjectName("VL_Build")
        self.buttonBox_ONOFF = QtWidgets.QDialogButtonBox(self)
        self.buttonBox_ONOFF.setGeometry(QtCore.QRect(120, 490, 151, 32))
        self.buttonBox_ONOFF.setStyleSheet("background-color: rgb(204, 204, 204);")
        self.buttonBox_ONOFF.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_ONOFF.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_ONOFF.setObjectName("buttonBox_ONOFF")






