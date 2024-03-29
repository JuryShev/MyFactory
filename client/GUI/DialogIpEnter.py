# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Yura\PycharmProjects\pythonProject\my_project\furniture_factory\GUI_designer\ip_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class DialogEnter(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(393, 164)
        Dialog.setStyleSheet("background-color: rgb(74, 80, 106);")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(120, 130, 151, 32))
        self.buttonBox.setStyleSheet("background-color: rgb(204, 204, 204);")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.LE_IP = QtWidgets.QLineEdit(Dialog)
        self.LE_IP.setGeometry(QtCore.QRect(60, 20, 271, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.LE_IP.setFont(font)
        self.LE_IP.setStyleSheet("border:none;\n"
"border-bottom: 1px solid rgb(16,240,207);\n"
"padding_bottom: 7px;\n"
"background-color: rgb(255, 255,255);\n"
"border-radius: 5px;\n"
"")
        self.LE_IP.setObjectName("lineEdit")
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        reg_rate = QtCore.QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        input_validator = QtGui.QRegExpValidator(reg_rate, self.LE_IP)
        self.LE_IP.setValidator(input_validator)
        self.LE_password = QtWidgets.QLineEdit(Dialog)
        self.LE_password.setGeometry(QtCore.QRect(60, 80, 271, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.LE_password.setFont(font)
        self.LE_password.setStyleSheet("border:none;\n"
"border-bottom: 1px solid rgb(16,240,207);\n"
"padding_bottom: 7px;\n"
"background-color: rgb(255, 255,255);\n"
"border-radius: 5px;\n"
"")
        self.LE_password.setObjectName("lineEdit_2")
        self.LE_name = QtWidgets.QLineEdit(Dialog)
        self.LE_name.setGeometry(QtCore.QRect(60, 50, 271, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.LE_name.setFont(font)
        self.LE_name.setStyleSheet("border:none;\n"
"border-bottom: 1px solid rgb(16,240,207);\n"
"padding_bottom: 7px;\n"
"background-color: rgb(255, 255,255);\n"
"border-radius: 5px;\n"
"")

        self.LE_name.setObjectName("lineEdit_3")
        reg_ex = QtCore.QRegExp("[a-z]{30}")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.LE_name)
        self.LE_name.setValidator(input_validator)
        self.Asterisk_IP = QtWidgets.QLabel(Dialog)
        self.Asterisk_IP.setEnabled(True)
        self.Asterisk_IP.setGeometry(QtCore.QRect(340, 21, 17, 17))
        self.Asterisk_IP.setStyleSheet("border-image: url(./GUI/icon/asterisk.png);")
        self.Asterisk_IP.setText("")
        self.Asterisk_IP.setObjectName("Asterisk_FamalyName")
        self.Asterisk_IP.hide()
        self.Asterisk_Name = QtWidgets.QLabel(Dialog)
        self.Asterisk_Name.setEnabled(True)
        self.Asterisk_Name.setGeometry(QtCore.QRect(340, 51, 17, 17))
        self.Asterisk_Name.setStyleSheet("border-image: url(./GUI/icon/asterisk.png);")
        self.Asterisk_Name.setText("")
        self.Asterisk_Name.setObjectName("Asterisk_FamalyName_2")
        self.Asterisk_Name.hide()
        self.Asterisk_Password = QtWidgets.QLabel(Dialog)
        self.Asterisk_Password.setEnabled(True)
        self.Asterisk_Password.setGeometry(QtCore.QRect(340, 82, 17, 17))
        self.Asterisk_Password.setStyleSheet("border-image: url(./GUI//icon/asterisk.png);")
        self.Asterisk_Password.setText("")
        self.Asterisk_Password.setObjectName("Asterisk_FamalyName_3")
        self.Asterisk_Password.hide()
        self.QL_error = QtWidgets.QLabel(Dialog)
        self.QL_error.setGeometry(QtCore.QRect(0, 100, 391, 27))
        self.QL_error.setStyleSheet("color: rgb(255, 129, 112);")
        self.QL_error.setAlignment(QtCore.Qt.AlignCenter)
        self.QL_error.setObjectName("label")

        self.retranslateUi(Dialog)

        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.LE_IP.setPlaceholderText(_translate("Dialog", "IP адрес"))
        self.LE_password.setPlaceholderText(_translate("Dialog", "пароль"))
        self.LE_name.setPlaceholderText(_translate("Dialog", "имя"))


