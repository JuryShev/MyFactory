# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Yura\PycharmProjects\pythonProject\my_project\furniture_factory\GUI_designer\MassageBox.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class MassageBox(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 98)
        Dialog.setStyleSheet("background-color: rgb(74, 80, 106);  ")
        self.PB_OK_Canel = QtWidgets.QDialogButtonBox(Dialog)
        self.PB_OK_Canel.setGeometry(QtCore.QRect(80, 65, 201, 21))
        self.PB_OK_Canel.setStyleSheet("background-color: rgb(213, 213, 213);\n"
"")
        self.PB_OK_Canel.setOrientation(QtCore.Qt.Horizontal)
        self.PB_OK_Canel.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.PB_OK_Canel.setObjectName("PB_OK_Canel")
        self.Label_message = QtWidgets.QLabel(Dialog)
        self.Label_message.setGeometry(QtCore.QRect(10, 24, 391, 28))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.Label_message.setFont(font)
        self.Label_message.setStyleSheet("color: rgb(222, 222, 222);")
        self.Label_message.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_message.setObjectName("Label_message")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 61, 51))
        self.label_2.setStyleSheet("image: url(./GUI/icon/question [#1444].png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.PB_OK_second = QtWidgets.QPushButton(Dialog)
        self.PB_OK_second.setGeometry(QtCore.QRect(170, 65, 61, 25))
        self.PB_OK_second.setStyleSheet("background-color: rgb(213, 213, 213);")
        self.PB_OK_second.setObjectName("PB_OK_second")

        self.retranslateUi(Dialog)
        self.PB_OK_Canel.accepted.connect(Dialog.accept)
        self.PB_OK_Canel.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Label_message.setText(_translate("Dialog", "Подтвердить изменения профиля?\n jgjgjgjgjgjgj"))
        self.PB_OK_second.setText(_translate("Dialog", "OK"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MassageBox()
    ui.setupUi(Dialog)
    ui.PB_OK_second.hide()
    Dialog.show()
    sys.exit(app.exec_())
