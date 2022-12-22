from functools import partial
import time
import cv2
from io import BytesIO
import base64
from PIL import Image
import numpy as np
import json
import os
import datetime
import codecs
import re
import argon2
import transliterate
from abc import ABC, abstractmethod
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QFileDialog, qApp, QWidget

from GUI.GUIMainWindow import Ui_MainWindow, ExploytListWidget
from GUI.DialofAddPersonal import DialogAddPersonal
from GUI.MassageBox import MassageBox
from GUI.DialogCalendar import DialogCalendar
from GUI.GUIPersonInteraction import GUIPersonInteraction
from GUI.GUIScroll import GUIListPersonal, GUIScrollPersonal
from GUI.GUIPersonalWidget import GUIPersonalWidget, GUIPersonalWidgetScroll, GUIPersonalWidget_2
from GUI.GUIAssessment import GUIAssessment
from GUI.DialogComment import DialogComment
from GUI.DialogIpEnter import DialogEnter
import CreateOpenFactory as COF
from GUI.DialogUserRule import *

basedir = os.path.dirname(__file__)
try:
    from ctypes import windll  # Only exists on Windows.

    myappid = 'MyFactory'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass
import traceback
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot, QRunnable, QThreadPool, QRegExp

from datetime import date

_translate = QtCore.QCoreApplication.translate


def getGrayed(src):
    if isinstance(src, QtGui.QPixmap):
        src = src.toImage()
    dest = QtGui.QImage(src.size(), QtGui.QImage.Format_ARGB32)
    widthRange = range(src.width())
    for y in range(src.height()):
        for x in widthRange:
            pixel = src.pixelColor(x, y)
            alpha = pixel.alpha()
            if alpha < 255:
                alpha //= 3
            gray = QtGui.qGray(src.pixel(x, y))
            pixel.setRgb(gray, gray, gray, alpha)
            dest.setPixelColor(x, y, pixel)
    return QtGui.QPixmap.fromImage(dest)


def start_process(progress_bar, self=None):
    thread_funct = COF.Worker_2(self.load_struct)
    thread_funct.signals.finished.connect(self.finish)
    thred_progress_bar = COF.Worker_2(
        partial(progress_bar.proc_counter, status='on'))  # Any other args, kwargs are passed to the run function
    thred_progress_bar.kwargs['progress_callback'] = thred_progress_bar.signals.progress
    thred_progress_bar.signals.result.connect(progress_bar.print_output)
    thred_progress_bar.signals.finished.connect(progress_bar.thread_complete)
    thred_progress_bar.signals.progress.connect(progress_bar.on_count_changed)
    self.threadpool.start(thread_funct)
    self.threadpool.start(thred_progress_bar)

    progress_bar.setWindowModality(QtCore.Qt.ApplicationModal)
    progress_bar.show()


def view_massage(obj, massage_text, icon, name_dialog='Dialog', point_size=8, button=0):
    massage_box = ImpMassageBox(obj)
    font = QtGui.QFont()
    font.setFamily("Roboto")
    font.setPointSize(point_size)
    font.setBold(True)
    font.setWeight(75)
    dict_icon = {'question': "image: url(./GUI/icon/question [#1444].png);",
                 'warning': "image: url(./GUI/icon/caution.png);",
                 'ok': "image: url(./GUI/icon/done_mini [#1484].png);",
                 'not_found': "image: url(./GUI/icon/emoji_sad_circle [#541]);"}
    if button == 0:
        massage_box.PB_OK_second.hide()
    else:
        massage_box.PB_OK_Canel.hide()
    massage_box.Label_message.setText((_translate(f"{name_dialog}", f"{massage_text}")))
    massage_box.label_2.setStyleSheet(dict_icon[icon])
    massage_box.exec()

    return massage_box.flag_choose


class DeployDialogComment(QDialog, DialogComment):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.CommentPersonal = ''
        # self.PB_EditComment.clicked.connect(self.edit)
        self.PB_SaveComment.clicked.connect(self.save)
        self.PB_CancelComment.clicked.connect(self.cancel)

    def text_view(self):
        self.TextSpace.setText(self.CommentPersonal)

    def edit(self):
        self.TextSpace.setText(self.CommentPersonal)
        self.TextSpace.setEnabled(True)

    def save(self):
        self.CommentPersonal = self.TextSpace.toPlainText()
        self.TextSpace.setEnabled(False)
        self.close()

    def cancel(self):
        self.close()


class Deploy_ChangeLogin(QDialog, DialogEnter):
    def __init__(self, parent):
        super().__init__(parent)
        _translate = QtCore.QCoreApplication.translate
        self.setupUi(self)
        self.resize(380, 110)
        self.LE_IP.hide()
        self.LE_password.hide()
        self.LE_password.setGeometry(QtCore.QRect(60, 65, 271, 20))
        self.NameUser = ''
        self.NameUser_new = ''
        self.PasswordUser = ''
        self.flag_connect = 0
        self.result = ''
        self.path_icon_edit = './GUI/icon/pen [#1320].png'
        self.path_icon_edit_inactive = './GUI/icon/pen_inactive [#1320].png'
        self.LE_name.setGeometry(QtCore.QRect(60, 20, 271, 20))
        self.buttonBox.setGeometry(QtCore.QRect(120, 70, 151, 32))
        self.LE_name.setEnabled(False)
        self.LE_password_new = QtWidgets.QLineEdit(self)
        self.LE_password_new.setGeometry(QtCore.QRect(60, 95, 271, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.LE_password_new.setFont(font)
        self.LE_password_new.setStyleSheet("border:none;\n"
                                           "border-bottom: 1px solid rgb(16,240,207);\n"
                                           "padding_bottom: 7px;\n"
                                           "background-color: rgb(255, 255,255);\n"
                                           "border-radius: 5px;\n"
                                           "")
        self.LE_password_new.setObjectName("LE_password_new")
        self.LE_password_new.setPlaceholderText(_translate("Dialog", "новый пароль"))
        regular_ex = QtCore.QRegExp("[A-Za-z\d@$!%*?&]{20}")  # №\\b^.*(?=.{8,})(?=.*\d)(?=.*[a-z]).*$\\b
        input_validator = QtGui.QRegExpValidator(regular_ex, self.LE_password_new)
        self.LE_password.setValidator(input_validator)
        self.LE_password_new.hide()

        self.LE_password_rep = QtWidgets.QLineEdit(self)
        self.LE_password_rep.setGeometry(QtCore.QRect(60, 125, 271, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.LE_password_rep.setFont(font)
        self.LE_password_rep.setStyleSheet("border:none;\n"
                                           "border-bottom: 1px solid rgb(16,240,207);\n"
                                           "padding_bottom: 7px;\n"
                                           "background-color: rgb(255, 255,255);\n"
                                           "border-radius: 5px;\n"
                                           "")
        self.LE_password_rep.setObjectName("LE_password_new")
        self.LE_password_rep.setPlaceholderText(_translate("Dialog", "повторите пароль"))
        input_validator = QtGui.QRegExpValidator(regular_ex, self.LE_password_rep)
        self.LE_password_rep.setValidator(input_validator)
        self.LE_password_rep.hide()
        self.QL_error.setGeometry(QtCore.QRect(0, 50, 391, 27))
        self.TB_edit_name_user = QtWidgets.QToolButton(self)
        self.icon_edit_name_user = QtGui.QIcon()
        self.icon_edit_name_user.addPixmap(QtGui.QPixmap(self.path_icon_edit),
                                           QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.TB_edit_name_user.setGeometry(QtCore.QRect(340, 21, 17, 17))
        self.TB_edit_name_user.setStyleSheet("\n""border:none\\n")
        self.TB_edit_name_user.setIcon(self.icon_edit_name_user)
        self.TB_edit_name_user.setIconSize(QtCore.QSize(17, 17))
        self.TB_edit_name_user.clicked.connect(self.edit_name)

        self.PB_edit_pass = QtWidgets.QPushButton(self)
        self.PB_edit_pass.setGeometry(QtCore.QRect(37, 40, 150, 15))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(True)
        self.PB_edit_pass.setFont(font)
        self.PB_edit_pass.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PB_edit_pass.setStyleSheet("QPushButton{\n"
                                        "background-color: rgb(74, 80, 106);\n"
                                        "color: rgb(233, 195, 184);;\n"
                                        "border-style: solid;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover {\n"
                                        "\n"
                                        "    color:rgb(176, 223, 198);\n"
                                        "}\n"
                                        "\n"
                                        "rgb(205, 202, 153);\n"
                                        "")
        self.PB_edit_pass.setObjectName("PB_name_user")
        self.PB_edit_pass.setText(_translate("MainWindow", "изменить пароль"))
        self.Asterisk_Name.setGeometry(QtCore.QRect(360, 21, 17, 17))
        self.Asterisk_Name.hide()
        self.Asterisk_Password.setGeometry(QtCore.QRect(340, 61, 17, 17))

        self.Asterisk_Password_new = QtWidgets.QLabel(self)
        self.Asterisk_Password_new.setEnabled(True)
        self.Asterisk_Password_new.setGeometry(QtCore.QRect(340, 96, 17, 17))
        self.Asterisk_Password_new.setStyleSheet("border-image: url(./GUI//icon/asterisk.png);")
        self.Asterisk_Password_new.setText("")
        self.Asterisk_Password_new.setObjectName("Asterisk_FamalyName_3")
        self.Asterisk_Password_new.hide()

        self.Asterisk_Password_rep = QtWidgets.QLabel(self)
        self.Asterisk_Password_rep.setEnabled(True)
        self.Asterisk_Password_rep.setGeometry(QtCore.QRect(340, 126, 17, 17))
        self.Asterisk_Password_rep.setStyleSheet("border-image: url(./GUI//icon/asterisk.png);")
        self.Asterisk_Password_rep.setText("")
        self.Asterisk_Password_rep.setObjectName("Asterisk_FamalyName_3")
        self.Asterisk_Password_rep.hide()

        self.buttonBox.accepted.connect(self.change_)
        self.PB_edit_pass.clicked.connect(self.edit_pass)

    def check_change_pass(self):
        _translate = QtCore.QCoreApplication.translate
        flag_list = []
        regular_pass = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        self.PasswordUser = self.LE_password.text()
        self.PasswordUser_new = self.LE_password_new.text()
        self.PasswordUser_rep = self.LE_password_rep.text()

        if re.match(regular_pass, self.PasswordUser) == None:
            flag_list.append(0)
            self.Asterisk_Password.show()
            self.QL_error.setText(_translate("Dialog", "слишком простой пароль \n"
                                                       "(должен содержать цифру и быть не меньше 8 символов)"))
            return flag_list
        else:
            flag_list.append(1)
            self.Asterisk_Password.hide()

        if re.match(regular_pass, self.PasswordUser_new) == None:
            flag_list.append(0)
            self.Asterisk_Password_new.show()
            self.QL_error.setText(_translate("Dialog", "слишком простой пароль \n"
                                                       "(должен содержать цифру и быть не меньше 8 символов)"))
            return flag_list
        else:
            flag_list.append(1)
            self.Asterisk_Password_new.hide()

        if re.match(regular_pass, self.PasswordUser_rep) == None:
            flag_list.append(0)
            self.Asterisk_Password_rep.show()
            self.QL_error.setText(_translate("Dialog", "слишком простой пароль \n"
                                                       "(должен содержать цифру и быть не меньше 8 символов)"))
            return flag_list
        else:
            flag_list.append(1)
            self.Asterisk_Password_rep.hide()

        if self.PasswordUser == self.PasswordUser_new:
            flag_list.append(0)
            self.Asterisk_Password_new.show()
            self.QL_error.setText(_translate("Dialog", "старый и новый пароль одинаковы \n"
                                             ))
            return flag_list
        else:
            flag_list.append(1)
            self.Asterisk_Password_new.hide()

        if self.PasswordUser_rep != self.PasswordUser_new:
            flag_list.append(0)
            self.Asterisk_Password_rep.show()
            self.QL_error.setText(_translate("Dialog", "пароли не совпадают \n"
                                             ))
            return flag_list
        else:
            flag_list.append(1)
            self.Asterisk_Password_rep.hide()
        return flag_list

    def check_change_name(self):
        _translate = QtCore.QCoreApplication.translate
        flag_list = []
        self.NameUser_new = self.LE_name.text()
        if len(self.NameUser) <= 1:
            flag_list.append(0)
            self.QL_error.setText(_translate("Dialog", "слишком короткое имя"))
            self.Asterisk_Name.show()
            return flag_list
        else:
            flag_list.append(1)
            self.Asterisk_Name.hide()

        if self.NameUser == self.NameUser_new:
            flag_list.append(0)
            self.QL_error.setText(_translate("Dialog", "имя не изменено"))
            self.Asterisk_Name.show()
            return flag_list
        else:
            flag_list.append(1)
            self.Asterisk_Name.hide()
        return flag_list

    def change_(self):
        _translate = QtCore.QCoreApplication.translate
        result = ''
        log_pass = ''
        dlg = ImpMassageBox(self)
        dlg.PB_OK_second.hide()
        if self.LE_password.isHidden() and self.LE_name.isEnabled():
            check_list = self.check_change_name()
            if 0 not in check_list:
                log_pass = '_login'
                dlg.Label_message.setText((_translate("Dialog", "Подтверждаете изменение логина?")))
                dlg.exec()
                if dlg.flag_choose == 'ok':
                    change_ = {
                        "change": "login",
                        "tables": {
                            "users": {
                                "nickname": self.NameUser_new,
                            }
                        }
                    }
                    result = client.change_log_pass(change_).content.decode('utf-8')


        else:
            check_list = self.check_change_pass()
            if 0 not in check_list:
                log_pass = '_pass'
                salt_user_new = os.urandom(32).hex()
                salt_user_new = bytes(salt_user_new, 'utf-8')
                self.PasswordUser_new = argon2.hash_password_raw(time_cost=16, memory_cost=2 ** 15,
                                                                 parallelism=2, hash_len=32,
                                                                 password=bytes(self.PasswordUser_new, 'utf-8'),
                                                                 salt=salt_user_new,
                                                                 type=argon2.low_level.Type.ID)

                print(self.PasswordUser)
                change_ = {
                    "change": "pass",
                    "password_new": self.PasswordUser_new.hex(),
                    "salt_user_new": salt_user_new.decode(),
                    "tables": {
                        "users": {
                            "password": self.PasswordUser,
                            "salt_user": ''
                        }

                    }
                }
                result = client.change_log_pass(change_).content.decode('utf-8')
        if result == 'ok':
            self.result = result + log_pass
            self.close()
        else:
            self.QL_error.setText(_translate("Dialog", "неверный пароль"))

    def edit_pass(self):
        _translate = QtCore.QCoreApplication.translate
        if self.LE_password.isHidden():
            self.resize(380, 230)
            self.QL_error.setGeometry(QtCore.QRect(0, 145, 391, 27))
            self.buttonBox.setGeometry(QtCore.QRect(120, 190, 151, 32))
            self.LE_name.setEnabled(False)
            self.TB_edit_name_user.setEnabled(False)
            original = QtGui.QPixmap(self.path_icon_edit_inactive)
            self.icon_edit_name_user = QtGui.QIcon(original)
            self.icon_edit_name_user.addPixmap(original, QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.QL_error.setText(_translate("Dialog", ""))
            self.Asterisk_Name.hide()
            self.TB_edit_name_user.setIcon(self.icon_edit_name_user)
            self.LE_password.show()
            self.LE_password_new.show()
            self.LE_password_rep.show()
        else:
            self.resize(380, 120)
            self.buttonBox.setGeometry(QtCore.QRect(120, 80, 151, 32))
            self.QL_error.setGeometry(QtCore.QRect(0, 60, 391, 27))
            self.TB_edit_name_user.setEnabled(True)
            original = QtGui.QPixmap(self.path_icon_edit)
            self.icon_edit_name_user = QtGui.QIcon(original)
            self.icon_edit_name_user.addPixmap(original, QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.TB_edit_name_user.setIcon(self.icon_edit_name_user)
            self.LE_password.hide()
            self.LE_password_new.hide()
            self.LE_password_rep.hide()
            self.Asterisk_Password.hide()
            self.Asterisk_Password_new.hide()
            self.Asterisk_Password_rep.hide()
            self.QL_error.setText(_translate("Dialog", ""))

    def edit_name(self):
        self.LE_name.setEnabled(True)


class PersonalWidget(GUIPersonalWidget_2):
    def __init__(self, id_widget, path_icon_edit):
        super(PersonalWidget, self).__init__(id_widget, path_icon_edit)
        self.comment = ''
        self.name_add = ''
        self.name_edit = ''
        self.retraslateUI()
        self.dlg = DeployDialogComment(self)
        self.dlg.PB_SaveComment.hide()
        self.dlg.PB_CancelComment.hide()
        self.dlg.TextSpace.setEnabled(False)
        self.TB_LPersCommentAssessment.clicked.connect(self.comment_button)
        self.TB_LPersUserAssessment.clicked.connect(self.give_assessment)

    def retraslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_name_Lastval.setText(_translate("MainWindow", "посл.знач."))
        self.label_name_Meanval.setText(_translate("MainWindow", "ср. знач."))

    def highlight_line(self):
        self.Label_LpersDate_cr.setStyleSheet("background-color: rgba(135, 154, 169, 80);")

    def setName(self, name, last_name):
        self.Label_LPersName.setText(name)
        self.Label_LPersLastName.setText(last_name)

    def setAssessment(self, mean_assessment, last_assessment):
        self.label_Meanval.setText(mean_assessment)
        self.label_Lastval.setText(last_assessment)

    def setComment(self, comment):
        self.comment = comment

    def set_name_assessment(self, name_add, name_edit):
        self.name_add = name_add.split(" ")

        self.name_add = f"{self.name_add[1]} {self.name_add[2]} {self.name_add[0].replace('$', '(архив)')}"
        if len(name_edit) > 0:
            self.name_edit = name_edit.split(" ")
            self.name_edit = f"{self.name_edit[1]} {self.name_edit[2]} {self.name_edit[0].replace('$', '(архив)')}"

    def give_assessment(self):
        massage_box = ImpMassageBox(self)
        massage_box.PB_OK_Canel.hide()

        if len(self.name_edit) > 0:
            massage_box.Label_message.setText(_translate("MainWindow", f"Оценил {self.name_add} \n"
                                                                       f" Ред. {self.name_edit}"))
        else:
            massage_box.Label_message.setText(_translate("MainWindow", f"Оценил {self.name_add}"))
        massage_box.exec()

    def comment_button(self):
        self.dlg.CommentPersonal = self.comment
        self.dlg.text_view()

        self.dlg.exec()


class PersonalWidgetScroll(GUIPersonalWidgetScroll):
    single_assessment = pyqtSignal(int)
    comment_signal = pyqtSignal(int)
    edit_assessment_signal = pyqtSignal(int)

    def __init__(self, id_widget, path_icon_edit):
        super(PersonalWidgetScroll, self).__init__(id_widget, path_icon_edit)
        self.dlg = DeployDialogComment(self)
        self.dlg.TextSpace.setEnabled(False)
        self.TB_APersCommentAssessment_new.setCheckable(False)
        self.TB_APersCommentAssessment_new.clicked.connect(self.comment_button)
        # self.comment_block()

    def comment_block(self):
        if self.ComboBox_SelectAssessment_new.currentIndex() == 0:  # or self.ComboBox_SelectAssessment_new.isEnabled() == False:
            self.TB_APersCommentAssessment_new.setEnabled(False)
        else:
            self.TB_APersCommentAssessment_new.setEnabled(True)

    def comment_button(self):
        print("comment")
        if len(self.comment) == 0 and self.ComboBox_SelectAssessment_new.isEnabled() \
                and self.ComboBox_SelectAssessment_new.currentIndex() > 0:
            self.dlg.TextSpace.setEnabled(True)
        else:
            self.dlg.CommentPersonal = self.comment
            self.dlg.text_view()
        self.dlg.exec()
        if self.comment != self.dlg.CommentPersonal:
            self.comment = self.dlg.CommentPersonal
            self.comment_signal.emit(self.id)

    def check_comment(self):
        if len(self.comment) > 0:
            self.dlg.TextSpace.setEnabled(False)

    def edit_assessment(self):
        if self.ComboBox_SelectAssessment_new.isEnabled() != True or len(self.comment) > 0:

            if self.ComboBox_SelectAssessment_new.isEnabled() != True:
                self.ComboBox_SelectAssessment_new.setEnabled(True)
            if len(self.comment) > 0:
                self.dlg.TextSpace.setEnabled(True)
            self.icon_APersCheckEdit_new = QtGui.QIcon()
            self.icon_APersCheckEdit_new.addPixmap(QtGui.QPixmap(
                "./GUI/icon/pen y4.png"),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.TB_APersCheckEdit_new = self.config_button(self.TB_APersCheckEdit_new,
                                                            QtCore.QRect(503, 4, 21, 31),
                                                            stylesheet="\n""border:none\\n",
                                                            icon=self.icon_APersCheckEdit_new,
                                                            icon_size=QtCore.QSize(17, 17),
                                                            name="Label_APersCheckEdit_3"
                                                            )
            self.comment_block()
            self.edit_assessment_signal.emit(self.id)
            self.flag_edit = 1

    def combobox_select_assessment_emit(self):
        self.single_assessment.emit(self.id)


class ListPersonal_(GUIListPersonal):
    LoadPersonFromList = pyqtSignal(str)

    def __init__(self, frame_loadList, minimum_size, base_size, style):
        super(ListPersonal_, self).__init__(frame_loadList, minimum_size, base_size, style)
        self._translate = QtCore.QCoreApplication.translate
        self.scrollArea_ListPersonal.itemDoubleClicked.connect(self.extract_index)
        self.set_default_list()

    def set_default_list(self):
        self.start_list_w = []
        self.finish_list_w = []
        self.list_person_widgets = []
        self.count_list_w = 0
        self.step_list_w = 7
        self.flag_filter = 0
        self.verticalLayout_scrollArea = None
        self.Label_NumCurrentList = None
        self.PersonalDataAssessment = None
        self.PersonalDataAssessment_filter = {"tables": {"personal": []}}
        self.current_date = ''  # для виджета TB_Date_LPers в PersonInteraction
        self.current_Crit_LPers = ''
        self.criterion_and_max_coef = {}

    def extract_index(self):
        index = self.scrollArea_ListPersonal.currentIndex().row()
        name = f'{self.list_person_widgets[index].Label_LPersLastName.text()} {self.list_person_widgets[index].Label_LPersName.text()}'
        self.LoadPersonFromList.emit(name)
        print(name)

    def fill_scroll(self, data_person):
        """self.ComboBox_Sorting_APers.setItemText(4, _translate("MainWindow", "Ред. Иванов И.А."))
            self.ComboBox_Sorting_APers.setItemText(5, _translate("MainWindow", "Ред. Артемьев. И.Б,"))"""

        self.list_person_widgets.clear()
        ######################build_list_personal########################################################
        for id, person in enumerate(data_person):
            last_name, name, father_name = person['name'].split(" ")
            if len(person['edit_data'][self.current_Crit_LPers]) > 0:
                path_icon_edit = "./GUI/icon/pen y4.png"
            else:
                path_icon_edit = "./GUI/icon/pen [#1321].png"
            personal_wd = PersonalWidget(id + self.start_list_w[self.count_list_w], path_icon_edit=path_icon_edit)
            if person["assessment"][self.current_Crit_LPers] > 0:
                personal_wd.label_Lastval.setText(str(person["assessment"][self.current_Crit_LPers]))
            if person["average_value"][self.current_Crit_LPers] > 0:
                personal_wd.label_Meanval.setText(str(person["average_value"][self.current_Crit_LPers]))
            if len(person["comments"][self.current_Crit_LPers]) > 0:
                personal_wd.comment = person["comments"][self.current_Crit_LPers]
            if len(person["add_data"][self.current_Crit_LPers]):
                personal_wd.set_name_assessment(person["add_data"][self.current_Crit_LPers],
                                                person["edit_data"][self.current_Crit_LPers])
            if len(person["date_created_pers"]) > 0:
                personal_wd.highlight_line()
                personal_wd.Label_LpersDate_cr.setText(_translate("MainWindow",
                                                                  f"сотрудник зачислен с {person['date_created_pers']}"))

            personal_wd.setName(self._translate("MainWindow", f"{name} {father_name}"),
                                self._translate("MainWindow", last_name))

            self.list_person_widgets.append(personal_wd)
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.scrollArea_ListPersonal)
            self.scrollArea_ListPersonal.setSpacing(1)
            size_v = personal_wd.sizeHint()
            size_v.setHeight(95)
            myQListWidgetItem.setSizeHint(size_v)
            self.scrollArea_ListPersonal.addItem(myQListWidgetItem)
            self.scrollArea_ListPersonal.setItemWidget(myQListWidgetItem, personal_wd)

    def next_left(self):
        """
            Функция для пролистывания списка влево
            :return:
            """
        if self.verticalLayout_scrollArea.count() > 0:
            if self.count_list_w > 0:
                self.count_list_w -= 1
                self.clear_scroll_assessment()
                if self.flag_filter == 0:
                    self.fill_scroll(self.PersonalDataAssessment["tables"]["personal"][
                                     self.start_list_w[self.count_list_w]:self.finish_list_w[self.count_list_w]])
                else:
                    self.fill_scroll(self.PersonalDataAssessment_filter["tables"]["personal"][
                                     self.start_list_w[self.count_list_w]:self.finish_list_w[self.count_list_w]])
                self.Label_NumCurrentList.setText(self._translate("MainWindow", f"{self.count_list_w + 1} "))

    def next_right(self):
        """
            Функция для пролистывания списка вправо
            :return None:
            """
        if self.verticalLayout_scrollArea.count() > 0:

            if self.count_list_w + 1 < len(self.finish_list_w):
                self.count_list_w += 1
                self.clear_scroll_assessment()
                if self.flag_filter == 0:
                    self.fill_scroll(self.PersonalDataAssessment["tables"]["personal"][
                                     self.start_list_w[self.count_list_w]:self.finish_list_w[self.count_list_w]])
                else:
                    self.fill_scroll(self.PersonalDataAssessment_filter["tables"]["personal"][
                                     self.start_list_w[self.count_list_w]:self.finish_list_w[self.count_list_w]])
                self.Label_NumCurrentList.setText(
                    self._translate("MainWindow", f"{self.count_list_w + 1} "))

    def clear_scroll_assessment(self):
        while self.scrollArea_ListPersonal.count() > 0:
            # item=\
            self.scrollArea_ListPersonal.takeItem(0)
            # item.widget().deleteLater()


class ScrollPersonal(GUIScrollPersonal):
    def __init__(self, frame_loadList, base_size):
        super(ScrollPersonal, self).__init__(frame_loadList, base_size)
        self.verticalLayout_scrollArea = QtWidgets.QVBoxLayout(self.scrollArea_AListPersonal_)
        self.set_default_scroll()
        self.retranslateUi()
        self.connect_button()

    def connect_button(self):
        self.TB_Left_APers.clicked.connect(self.next_left)
        self.TB_Right_APers.clicked.connect(self.next_right)

    def set_default_scroll(self):
        self.start_list_w = []
        self.finish_list_w = []
        self.count_list_w = 0
        self.step_list_w = 5
        self.flag_filter = 0
        self.list_person_widgets = []
        self.current_Crit_APers = ''
        self.criterion_and_max_coef = {}
        self.PersonalDataAssessment = None
        self.PersonalDataAssessment_filter = {"tables": {"personal": []}}
        self.CheckBox_SingleAssesm = None

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Label_NumCurrentList.setText(_translate("Form", "1 "))
        self.Label_NumLastList.setText(_translate("Form", "...20"))
        self.Label_AllPersonal.setText(_translate("Form", "всего в отделе 0 сотрудников"))

    def check_assessment(self, wd_id, i=-1):
        #### если flag_edit=1 и пользователь изменил оценку, тогда id_personal[crit][1]=1
        #### если flag_edit=1 и пользователь убрал оценку, тогда id_personal[crit][1]=-1
        #### если flag_edit=0 и пользователь установил оценку, просто прописывается оценка
        if i == -1:
            i = wd_id
        SelectAssessmentID = self.list_person_widgets[
            wd_id - (self.step_list_w * self.count_list_w)].ComboBox_SelectAssessment_new.currentIndex()
        if self.PersonalDataAssessment["tables"]["personal"][i]["id_assessment"][self.current_Crit_APers][0] > 0 \
                and SelectAssessmentID > 0:
            self.PersonalDataAssessment["tables"]["personal"][i]["id_assessment"][self.current_Crit_APers][1] = 1
        elif self.PersonalDataAssessment["tables"]["personal"][i]["id_assessment"][self.current_Crit_APers][0] > 0 \
                and SelectAssessmentID == 0:
            self.PersonalDataAssessment["tables"]["personal"][i]["id_assessment"][self.current_Crit_APers][1] = -1
            if len(self.PersonalDataAssessment["tables"]["personal"][i]["comments"][self.current_Crit_APers]) > 0:
                print("оценка будет удалена из базы данных")
        elif self.PersonalDataAssessment["tables"]["personal"][i]["id_assessment"][self.current_Crit_APers][0] == 0 \
                and SelectAssessmentID == 0:
            self.PersonalDataAssessment["tables"]["personal"][i]["id_assessment"][self.current_Crit_APers][1] = 0
            if len(self.PersonalDataAssessment["tables"]["personal"][i]["comments"][self.current_Crit_APers]) > 0:
                print("комментарий будет удален")
        elif self.PersonalDataAssessment["tables"]["personal"][i]["id_assessment"][self.current_Crit_APers][0] == 0 \
                and SelectAssessmentID > 0:
            self.PersonalDataAssessment["tables"]["personal"][i]["id_assessment"][self.current_Crit_APers][1] = 1

    def next_left(self):
        """
        Функция для пролистывания списка влево
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        if self.verticalLayout_scrollArea.count() > 0:
            if self.count_list_w > 0:
                self.count_list_w -= 1
                self.clear_scroll_assessment()
                if self.flag_filter == 0:
                    self.fill_scroll(self.PersonalDataAssessment["tables"]["personal"][
                                     self.start_list_w[self.count_list_w]:self.finish_list_w[self.count_list_w]])
                else:
                    self.fill_scroll(self.PersonalDataAssessment_filter["tables"]["personal"][
                                     self.start_list_w[self.count_list_w]:self.finish_list_w[self.count_list_w]])
                self.Label_NumCurrentList.setText(_translate("MainWindow", f"{self.count_list_w + 1} "))

    def next_right(self):
        """
        Функция для пролистывания списка вправо
        :return None:
        """

        _translate = QtCore.QCoreApplication.translate
        if self.verticalLayout_scrollArea.count() > 0:

            if self.count_list_w + 1 < len(self.finish_list_w):
                self.count_list_w += 1
                self.clear_scroll_assessment()
                if self.flag_filter == 0:
                    self.fill_scroll(self.PersonalDataAssessment["tables"]["personal"][
                                     self.start_list_w[self.count_list_w]:self.finish_list_w[self.count_list_w]])
                else:
                    self.fill_scroll(self.PersonalDataAssessment_filter["tables"]["personal"][
                                     self.start_list_w[self.count_list_w]:self.finish_list_w[self.count_list_w]])
                self.Label_NumCurrentList.setText(_translate("MainWindow", f"{self.count_list_w + 1} "))

    def clear_scroll_assessment(self):
        while self.verticalLayout_scrollArea.count() > 0:
            item = self.verticalLayout_scrollArea.takeAt(0)
            item.widget().deleteLater()

    def fill_scroll(self, data_person):
        """self.ComboBox_Sorting_APers.setItemText(4, _translate("MainWindow", "Ред. Иванов И.А."))
        self.ComboBox_Sorting_APers.setItemText(5, _translate("MainWindow", "Ред. Артемьев. И.Б,"))"""
        _translate = QtCore.QCoreApplication.translate

        self.list_person_widgets.clear()
        max_coef = self.criterion_and_max_coef[self.current_Crit_APers]

        ######################build_list_personal########################################################
        for id, person in enumerate(data_person):
            last_name, name, father_name = person['name'].split(" ")
            if len(person['edit_data'][self.current_Crit_APers]) > 0:
                path_icon_edit = "./GUI/icon/pen y4.png"
            else:
                path_icon_edit = "./GUI/icon/pen [#1321].png"
            personal_wd = PersonalWidgetScroll(id + self.start_list_w[self.count_list_w], path_icon_edit=path_icon_edit)
            for i in range(1, max_coef + 1):
                personal_wd.ComboBox_SelectAssessment_new.addItem("")
                personal_wd.ComboBox_SelectAssessment_new.setItemText(i, _translate("MainWindow", str(i)))
            if person["assessment"][self.current_Crit_APers] > 0:
                personal_wd.ComboBox_SelectAssessment_new.setCurrentIndex(person["assessment"][self.current_Crit_APers])
                personal_wd.ComboBox_SelectAssessment_new.setEnabled(False)
                self.flag_edit_person = 1
            if len(person["comments"][self.current_Crit_APers]) > 0:
                personal_wd.comment = person["comments"][self.current_Crit_APers]

            personal_wd.Label_APersName_new.setText(_translate("MainWindow", f"{name} {father_name}"))
            personal_wd.Label_APersLastName_new.setText(_translate("MainWindow", last_name))
            personal_wd.single_assessment.connect(self.Single_Assesments)
            personal_wd.comment_signal.connect(self.New_Comment)
            personal_wd.edit_assessment_signal.connect(self.Write_Name_Edit)
            personal_wd.comment_block()
            self.list_person_widgets.append(personal_wd)
            self.verticalLayout_scrollArea.addWidget(personal_wd.Pers_new)

    #  @pyqtSlot(int)
    def Single_Assesments(self, wd_id):
        """Функция для единой оценки персонала
        Оцениается весь список отдела включая не отображаемый персонал"""
        flag_edit = {0: "add", 1: "edit"}
        if self.CheckBox_SingleAssesm.isChecked():
            if self.flag_edit_person == 1:
                print("введите пароль")
                passw = 1
                if passw != 1:
                    return None
            for i in range(len(self.PersonalDataAssessment["tables"]["personal"])):
                self.check_assessment(wd_id=wd_id, i=i)
                self.PersonalDataAssessment["tables"]["personal"][i]["assessment"][
                    self.current_Crit_APers] = self.list_person_widgets[
                    wd_id - (self.step_list_w * self.count_list_w)].ComboBox_SelectAssessment_new.currentIndex()
            self.clear_scroll_assessment()
            self.fill_scroll(self.PersonalDataAssessment["tables"]["personal"][
                             self.start_list_w[self.count_list_w]:self.finish_list_w[self.count_list_w]])

        else:
            self.check_assessment(wd_id)
            if self.flag_filter == 0:
                self.PersonalDataAssessment["tables"]["personal"][wd_id]["assessment"][
                    self.current_Crit_APers] = self.list_person_widgets[
                    wd_id - (self.step_list_w * self.count_list_w)].ComboBox_SelectAssessment_new.currentIndex()
            else:
                self.PersonalDataAssessment_filter["tables"]["personal"][wd_id]["assessment"][
                    self.current_Crit_APers] = self.list_person_widgets[
                    wd_id - (self.step_list_w * self.count_list_w)].ComboBox_SelectAssessment_new.currentIndex()
                id_main_list = self.PersonalDataAssessment_filter["tables"]["personal"][wd_id]['id_main_list']
                self.PersonalDataAssessment["tables"]["personal"][id_main_list]["assessment"][
                    self.current_Crit_APers] = self.list_person_widgets[
                    wd_id - (self.step_list_w * self.count_list_w)].ComboBox_SelectAssessment_new.currentIndex()

        self.list_person_widgets[wd_id - (self.step_list_w * self.count_list_w)].comment_block()

    # @pyqtSlot(int)
    def New_Comment(self, wd_id):
        self.PersonalDataAssessment["tables"]["personal"][wd_id]["id_assessment"][self.current_Crit_APers][1] = 1

        if self.flag_filter == 0:
            self.PersonalDataAssessment["tables"]["personal"][wd_id]["comments"][
                self.current_Crit_APers] = self.list_person_widgets[
                wd_id - (self.step_list_w * self.count_list_w)].comment
        else:
            self.PersonalDataAssessment_filter["tables"]["personal"][wd_id]["comments"][
                self.current_Crit_APers] = self.list_person_widgets[
                wd_id - (self.step_list_w * self.count_list_w)].comment
            id_main_list = self.PersonalDataAssessment_filter["tables"]["personal"][wd_id]['id_main_list']
            self.PersonalDataAssessment["tables"]["personal"][id_main_list]["comments"][
                self.current_Crit_APers] = self.list_person_widgets[
                wd_id - (self.step_list_w * self.count_list_w)].comment

    # @pyqtSlot(int)
    def Write_Name_Edit(self, wd_id):
        if self.flag_filter == 0:
            self.PersonalDataAssessment["tables"]["personal"][wd_id]["edit_data"][
                self.current_Crit_APers] = 'Иванов'
        else:
            self.PersonalDataAssessment_filter["tables"]["personal"][wd_id]["edit_data"][
                self.current_Crit_APers] = 'Иванов'
            id_main_list = self.PersonalDataAssessment_filter["tables"]["personal"][wd_id]['id_main_list']
            self.PersonalDataAssessment["tables"]["personal"][id_main_list]["edit_data"][
                self.current_Crit_APers] = 'Иванов'


class PersonalAssessment(GUIAssessment):
    def __init__(self, cl):
        super(PersonalAssessment, self).__init__()
        self.scroll_personal = ScrollPersonal(self.WorkSpace_Assesment_Personal, (150, 150))
        self.gridLayout_2.addWidget(self.scroll_personal.scrollArea_AListPersonal, 2, 4, 11, 10)
        self.gridLayout_2.addWidget(self.scroll_personal.Label_NumCurrentList, 13, 8, 1, 1)
        self.gridLayout_2.addWidget(self.scroll_personal.Label_NumLastList, 13, 9, 1, 1)
        self.gridLayout_2.addWidget(self.scroll_personal.TB_Left_APers, 13, 6, 1, 1)
        self.gridLayout_2.addWidget(self.scroll_personal.TB_Right_APers, 13, 11, 1, 1)
        self.gridLayout_2.addWidget(self.scroll_personal.Label_AllPersonal, 14, 6, 1, 6)
        self.scroll_personal.CheckBox_SingleAssesm = self.CheckBox_SingleAssesm
        self.client = cl
        self.retranslateUi()
        self.connect_button()

        # self.PB_Load_ListPers.clicked.connect(self.fill_scroll_slot)
        # self.PB_Save_APers.clicked.connect(self.save_data)

    def connect_button(self):
        self.PB_Load_ListPers.clicked.connect(self.fill_scroll_slot)
        self.PB_Save_APers.clicked.connect(self.save_data)
        self.ComboBox_Crit_APers.currentTextChanged.connect(self.ComboBox_Crit_APers_changed)
        self.ComboBox_Sorting_APers.currentTextChanged.connect(self.ComboBox_Sorting_APers_changed_slot)

    def reset_win(self):
        self.scroll_personal.clear_scroll_assessment()
        self.scroll_personal.set_default_scroll()
        self.ComboBox_Crit_APers.clear()
        self.ComboBox_Dep_APers.clear()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label_Crit_APers.setText(_translate("Form", "критерий"))
        self.Label_Dep_APers.setText(_translate("Form", "отдел"))
        self.PB_Load_ListPers.setText(_translate("Form", "загрузить"))
        self.Label_SelectDate.setText(_translate("Form", "выбор даты оценки"))
        self.CheckBox_SingleAssesm.setText(_translate("Form", "Единая оценка"))
        self.ComboBox_Sorting_APers.setItemText(0, _translate("Form", "Все"))
        self.ComboBox_Sorting_APers.setItemText(1, _translate("Form", "Только с оценкой"))
        self.ComboBox_Sorting_APers.setItemText(2, _translate("Form", "Только без оценки"))
        self.ComboBox_Sorting_APers.setItemText(3, _translate("Form", "Только отредактированне"))
        self.Label_Name_Sorting_APers.setText(_translate("Form", "показать"))
        self.PB_Save_APers.setText(_translate("Form", "Сохранить оценку"))

    def load_combobox_assessment(self):
        _translate = QtCore.QCoreApplication.translate
        conf_struct = self.client.get_struct().content
        conf_struct = json.loads(conf_struct.decode('utf-8'))
        conf_criterion = conf_struct['tables']['conf_criterion']
        departments = conf_struct['tables']['department']
        self.ComboBox_Crit_APers.clear()
        self.ComboBox_Dep_APers.clear()
        for id, crit in enumerate(conf_criterion):
            self.scroll_personal.criterion_and_max_coef[crit['title_criterion']] = crit['max_coef']
            self.ComboBox_Crit_APers.addItem("")
            self.ComboBox_Crit_APers.setItemText(id, _translate("MainWindow", crit['title_criterion']))
        for id, department in enumerate(departments):
            self.ComboBox_Dep_APers.addItem("")
            self.ComboBox_Dep_APers.setItemText(id, _translate("MainWindow", department['title']))

    def fill_scroll_slot(self):

        _translate = QtCore.QCoreApplication.translate
        massage = ImpMassageBox(self)
        massage.Label_message.setGeometry(QtCore.QRect(10, 20, 460, 40))
        massage.PB_OK_Canel.setGeometry(QtCore.QRect(100, 65, 201, 21))
        massage.PB_OK_second.setGeometry(QtCore.QRect(190, 65, 61, 20))
        massage.label_2.setGeometry(QtCore.QRect(15, 20, 61, 51))
        massage.label_2.setStyleSheet("image: url(./GUI/icon/caution.png);")
        massage.resize(450, 98)
        massage.PB_OK_second.hide()
        date = self.CalendarWidget_APers.selectedDate()
        year = date.year()
        month = date.month()
        if len(str(month)) == 1:
            month = '0' + str(month)
        day = date.day()
        time_select = datetime.datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y").date()
        div_date = datetime.date.today() - time_select
        if div_date.days < 0:
            print("warning")
            return

        request_send = {
            "comand": 5000,
            "user": "admin",
            "db_comand": 1,
            "date": f"{day}-{month}-{year}",
            "flag_previous_day": 0,
            "tables": {"department": self.ComboBox_Dep_APers.currentText()}
        }
        self.request_date = request_send["date"]
        pers_list = self.client.assessment_personal(request_send).content
        self.scroll_personal.PersonalDataAssessment = json.loads(pers_list.decode('utf-8'))

        if self.scroll_personal.PersonalDataAssessment["error"] == 'Bad date':
            massage.Label_message.setText(_translate("Dialog", "За выбранную дату нельзя поставить оценку"))
            massage.PB_OK_second.show()
            massage.PB_OK_Canel.hide()
            massage.exec()
            return
        elif self.scroll_personal.PersonalDataAssessment["error"] == 'Pending evaluation':

            prev_date = self.scroll_personal.PersonalDataAssessment['prev_date'].split('-')
            massage.Label_message.setText(_translate("Dialog", f"За {prev_date[0]}-"
                                                               f"{prev_date[1]}-"
                                                               f"{prev_date[2]} "
                                                               f"число не доконца проставлены оценки."
                                                               f" \n Загрузить список за это число?"))
            massage.exec_()
            if massage.flag_choose == 'ok':
                request_send["flag_previous_day"] = 1
                request_send["date"] = f"{prev_date[0]}-{prev_date[1]}-{prev_date[2]}"
            else:
                request_send["flag_previous_day"] = 1
                request_send["date"] = f"{day}-{month}-{year}"
            self.request_date = request_send["date"]
            pers_list = self.client.assessment_personal(request_send).content
            self.scroll_personal.PersonalDataAssessment = json.loads(pers_list.decode('utf-8'))

        # with codecs.open("PersonalDataAssessment.json", "r", "utf_8_sig") as outfile:
        #     self.scroll_personal.PersonalDataAssessment=json.load(outfile)
        for i in range(len(self.scroll_personal.PersonalDataAssessment["tables"]["personal"])):
            self.scroll_personal.PersonalDataAssessment["tables"]["personal"][i]['id_main_list'] = i

        if self.scroll_personal.verticalLayout_scrollArea.count() > 0:
            self.scroll_personal.clear_scroll_assessment()
        if len(self.scroll_personal.PersonalDataAssessment["tables"]["personal"]) >= self.scroll_personal.step_list_w:
            num = len(
                self.scroll_personal.PersonalDataAssessment["tables"]["personal"]) // self.scroll_personal.step_list_w
            res = len(
                self.scroll_personal.PersonalDataAssessment["tables"]["personal"]) % self.scroll_personal.step_list_w
            self.scroll_personal.finish_list_w = [i * self.scroll_personal.step_list_w for i in range(1, num + 1)]
            self.scroll_personal.start_list_w = [i * self.scroll_personal.step_list_w for i in range(0, num)]
            self.scroll_personal.finish_list_w[-1] += res
            self.scroll_personal.Label_NumLastList.setText(_translate("MainWindow", f"...{num}"))
        elif self.scroll_personal.step_list_w >= len(
                self.scroll_personal.PersonalDataAssessment["tables"]["personal"]) > 0:
            self.scroll_personal.finish_list_w = [
                len(self.scroll_personal.PersonalDataAssessment["tables"]["personal"])]
            self.scroll_personal.start_list_w = [0]
            self.scroll_personal.Label_NumLastList.setText(_translate("MainWindow", f"...{1}"))
        self.scroll_personal.current_Crit_APers = self.ComboBox_Crit_APers.currentText()
        self.scroll_personal.fill_scroll(self.scroll_personal.PersonalDataAssessment["tables"]["personal"][
                                         self.scroll_personal.start_list_w[self.scroll_personal.count_list_w]
                                         :self.scroll_personal.finish_list_w[self.scroll_personal.count_list_w]])
        self.scroll_personal.Label_AllPersonal.setText(_translate(
            "MainWindow",
            f"всего в отделе {len(self.scroll_personal.PersonalDataAssessment['tables']['personal'])} сотрудников"))
        self.ComboBox_Sorting_APers.setEnabled(True)

    def ComboBox_Sorting_APers_changed_slot(self):
        _translate = QtCore.QCoreApplication.translate
        if self.scroll_personal.PersonalDataAssessment != None:
            data_person = self.scroll_personal.PersonalDataAssessment["tables"]["personal"]
            self.scroll_personal.PersonalDataAssessment_filter[
                "tables"]["personal"] = self.ComboBox_Sorting_APers_changed(data_person)
            self.scroll_personal.clear_scroll_assessment()
            self.scroll_personal.count_list_w = 0
            ############################
            if len(self.scroll_personal.PersonalDataAssessment_filter["tables"][
                       "personal"]) >= self.scroll_personal.step_list_w:
                num = len(self.scroll_personal.PersonalDataAssessment_filter["tables"][
                              "personal"]) // self.scroll_personal.step_list_w
                res = len(self.scroll_personal.PersonalDataAssessment_filter["tables"][
                              "personal"]) % self.scroll_personal.step_list_w
                self.scroll_personal.finish_list_w = [i * self.scroll_personal.step_list_w for i in range(1, num + 1)]
                self.scroll_personal.start_list_w = [i * self.scroll_personal.step_list_w for i in range(0, num)]
                self.scroll_personal.finish_list_w[-1] += res
                self.scroll_personal.Label_NumLastList.setText(_translate("MainWindow", f"...{num}"))
            elif self.scroll_personal.step_list_w >= len(
                    self.scroll_personal.PersonalDataAssessment_filter["tables"]["personal"]) > 0:
                self.scroll_personal.finish_list_w = [
                    len(self.scroll_personal.PersonalDataAssessment_filter["tables"]["personal"])]
                self.scroll_personal.start_list_w = [0]
                self.scroll_personal.Label_NumLastList.setText(_translate("MainWindow", f"...{1}"))
            self.scroll_personal.fill_scroll(self.scroll_personal.PersonalDataAssessment_filter["tables"]["personal"]
                                             [self.scroll_personal.start_list_w[self.scroll_personal.count_list_w]:
                                              self.scroll_personal.finish_list_w[self.scroll_personal.count_list_w]])
            self.scroll_personal.Label_AllPersonal.setText(_translate(
                "MainWindow",
                f"всего в отделе {len(self.scroll_personal.PersonalDataAssessment['tables']['personal'])} сотрудников"))
            self.scroll_personal.Label_NumCurrentList.setText(
                _translate("MainWindow", f"{self.scroll_personal.count_list_w + 1} "))
            ############################

    def ComboBox_Sorting_APers_changed(self, data_person):
        if self.ComboBox_Sorting_APers.currentText() == "Только отредактированные":
            data_person = list(
                filter(lambda d: len(d["edit_data"][self.ComboBox_Crit_APers.currentText()]) > 0, data_person))
            self.flag_filter = 1
            self.CheckBox_SingleAssesm.setEnabled(False)
        elif self.ComboBox_Sorting_APers.currentText() == "Только без оценки":
            data_person = list(
                filter(lambda d: d['assessment'][self.ComboBox_Crit_APers.currentText()] == 0, data_person))
            self.flag_filter = 1
            self.CheckBox_SingleAssesm.setEnabled(False)
        elif self.ComboBox_Sorting_APers.currentText() == "Только с оценкой":
            data_person = list(
                filter(lambda d: d['assessment'][self.ComboBox_Crit_APers.currentText()] > 0, data_person))
            self.flag_filter = 1
            self.CheckBox_SingleAssesm.setEnabled(False)
        elif self.ComboBox_Sorting_APers.currentText() == "Все":
            data_person = self.scroll_personal.PersonalDataAssessment["tables"]["personal"]
            self.flag_filter = 0
            self.CheckBox_SingleAssesm.setEnabled(True)
        return data_person

    def ComboBox_Crit_APers_changed(self):
        """
        Функция срабатывает при изменении критерия
        Заполняет окно списка с данными относительно данного критерия
        :return:
        """
        print("kk")
        if self.scroll_personal.verticalLayout_scrollArea.count() > 0:
            if self.scroll_personal.flag_filter != 0:
                self.ComboBox_Sorting_APers_changed_slot()
                data_personal = self.scroll_personal.PersonalDataAssessment_filter["tables"]["personal"][
                                self.scroll_personal.start_list_w[self.scroll_personal.count_list_w]:
                                self.scroll_personal.finish_list_w[self.scroll_personal.count_list_w]]
                self.CheckBox_SingleAssesm.setEnabled(True)
            else:
                data_personal = self.scroll_personal.PersonalDataAssessment["tables"]["personal"][
                                self.scroll_personal.start_list_w[self.scroll_personal.count_list_w]:
                                self.scroll_personal.finish_list_w[self.scroll_personal.count_list_w]]
            self.scroll_personal.current_Crit_APers = self.ComboBox_Crit_APers.currentText()
            self.scroll_personal.clear_scroll_assessment()
            self.scroll_personal.fill_scroll(data_personal)

    def save_data(self):
        _translate = QtCore.QCoreApplication.translate
        massage = ImpMassageBox(self)
        massage.PB_OK_Canel.hide()
        # with open("send_list_assessment_user_t.json", "r") as outfile:
        #     PersonalDataAssessment_send = json.load(outfile)

        PersonalDataAssessment_send = {"tables": {"personal": []},
                                       "date": self.request_date}

        for pers in self.scroll_personal.PersonalDataAssessment["tables"]["personal"]:
            PersonalDataAssessment_send["tables"]["personal"].append(
                {
                    "id_person": pers["id_person"],
                    "id_assessment": pers["id_assessment"],
                    "name": pers["name"],
                    "assessment": pers["assessment"],
                    "comments": pers["comments"]

                }
            )
        answer = self.client.assessment_personal(PersonalDataAssessment_send, 'send').content.decode('utf-8')
        if answer == 'ok':
            massage.Label_message.setText(_translate("Dialog", "Оценки успешно добавлены"))
        else:
            massage.Label_message.setText(_translate("Dialog", "Что то пошло не так"))
        massage.exec_()


class PersonInteraction(GUIPersonInteraction):

    def __init__(self, cl):
        super(PersonInteraction, self).__init__()
        style_list = """QListView {    

                }
                QListView::item:selected:active:!hover{
                    border-style: inset;
                    background-color: rgb(217, 217, 217); color: white;
                    border-width: 2px;
                    border-color: red;
                }
                QListView::item{
                background-color: rgb(217, 217, 217);
                border-radius: 10px;
                }
                QListView::item:!hover{
                    background-color: rgb(217, 217, 217); color: white;
                }
                    QListView::item:!selected:hover{
                    border-style: inset;
                    border-width: 2px;
                   border-color: rgb(12, 156, 180);
                   border-radius: 5px; color: white;
                }"""
        self.stile_button_rights = """QPushButton{
                                         background-color: rgb(151, 156, 180);
                                         color: rgb(0, 0, 0);
                                         border-style: solid;
                                         border-width: 0.5px;
                                         border-color: rgb(151, 156, 180);
                                         border-bottom-color: rgb(146, 255, 140);
                                         border-radius: 5px;}

                                         QPushButton:hover {
                                         background-color: rgb(140, 148, 180);}
                                        
                                         QPushButton:pressed {
                                         border-style: inset;
                                         background-color: rgb(24, 33, 69);
                                         color: rgb(250, 250, 250)}"""
        self.stile_button_not_rights = """QPushButton{
                                         background-color: rgb(151, 156, 180);
                                         color: rgb(0, 0, 0);
                                         border-style: solid;
                                         border-width: 0.5px;
                                         border-color: rgb(151, 156, 180);
                                         border-radius: 5px;}

                                         QPushButton:hover {
                                         background-color: rgb(140, 148, 180);}
                                        
                                         QPushButton:pressed {
                                         border-style: inset;
                                         background-color: rgb(24, 33, 69);
                                         color: rgb(250, 250, 250)}"""

        self.list_personal = ListPersonal_(self.frame_loadList, (0, 70), (150, 150), style_list)
        self.verticalLayout_5.insertWidget(1, self.list_personal.scrollArea_ListPersonal)
        self.retranslateUi()
        self.date = self.get_date()
        self.connect_button()
        self.TB_EditPersonal.setEnabled(False)
        self.TB_RemovePersonal.setEnabled(False)
        self.PB_right_user.setEnabled(False)
        self.PB_right_admin.setEnabled(False)
        self.PersonalDataSend = {
            "comand": 2001,
            "user": "admin",
            "db_comand": 1,
            "tables": {"personal": [{"name": ''
                                     }
                                    ]}}
        self.PersonalDataGet = {
            "comand": 0,
            "user": "admin",
            "db_comand": 1,
            "tables": {"personal": [
            ]}}

        self.client = cl
        self.flag_get_personal = -1
        self.list_personal.LoadPersonFromList.connect(self.search_personal)
        self.pers_inter_user = ''

    def clear_frame_personal(self):
        self.label_surname.setText(_translate("MainWindow", ''))
        self.label_name.setText(_translate("MainWindow", ''))
        self.label_number.setText(_translate("MainWindow", ''))
        self.label_name_depart.setText(_translate("MainWindow", ''))
        self.label_name_post.setText(_translate("MainWindow", ''))
        self.label_salaryl.setText(_translate("MainWindow", ''))
        self.label_asses_certification.setText(_translate("MainWindow", ''))
        self.label_asses_bonus.setText(_translate("MainWindow", ''))
        self.label_birthDate.setText(_translate("MainWindow", ''))
        self.label_old.setText(_translate("MainWindow", 'Возраст: '))
        self.label_workExp.setText(_translate("MainWindow", ''))
        face = cv2.imread('./GUI/icon/silhouette_icon128x128.png')
        height, width, channel = face.shape
        bytesPerLine = 3 * width
        qFace = QtGui.QImage(face.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(qFace)
        self.label_avatar.setPixmap(pixmap)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./GUI/icon/pen_inactive [#1320].png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TB_EditPersonal.setIcon(icon1)
        self.TB_EditPersonal.setEnabled(False)
        self.TB_RemovePersonal.setEnabled(False)
        self.PB_right_admin.setStyleSheet(self.stile_button_not_rights)
        self.PB_right_user.setStyleSheet(self.stile_button_not_rights)


    def clear_list_personal(self):
        pass

    def reset_win(self):
        self.clear_frame_personal()
        self.list_personal.clear_scroll_assessment()
        self.list_personal.set_default_list()
        self.ComboBox_Crit_LPers.clear()
        self.ComboBox_Dep_LPers.clear()
        self.label_date_assessment.setText(_translate("MainWindow", f""))


    def connect_button(self):
        self.PB_serch_personalList.clicked.connect(self.fill_scroll_slot)
        self.PB_right_user.clicked.connect(self.rule_user_)
        self.TB_Date_LPers.clicked.connect(self.date_slot)
        self.ComboBox_Filter_LPers.currentTextChanged.connect(self.ComboBox_Sorting_APers_changed_slot)
        self.ComboBox_Crit_LPers.currentTextChanged.connect(self.ComboBox_Crit_LPers_changed)
        self.TB_AddPersonal.clicked.connect(self.add_personal)
        self.PB_serch_personal.clicked.connect(self.search_personal)
        self.TB_EditPersonal.clicked.connect(self.edit_personal)
        self.TB_RemovePersonal.clicked.connect(self.remove_personal)
        self.PB_right_admin.clicked.connect(self.new_admin)

    def new_admin(self):
        _translate = QtCore.QCoreApplication.translate
        right_user = self.PersonalDataGet['tables']['personal'][0]['right_user']
        if self.pers_inter_user == 'user' and right_user == 'admin':
            answer = 'Данный сорудник является \n администратором'
            view_massage(self, answer, 'ok', button=1)
        elif self.pers_inter_user == 'user' and (right_user == '' or right_user == 'user'):
            answer = 'Нет прав назначить сотрудника \n администратором'
            view_massage(self, answer, 'warning', button=1)
        elif self.pers_inter_user == 'admin' and right_user == 'admin':
            answer = 'Вы являетесь \n администратором'
            view_massage(self, answer, 'ok', button=1)
        else:
            answer = 'Назначить этого сотрудника \n администратором'
            if view_massage(self, answer, 'question', button=1) == 'ok':
                answer = client.appoint_admin(self.PersonalDataGet).content.decode('utf-8')
                answer = json.loads(answer)
                name_personal = f"{self.PersonalDataGet['tables']['personal'][0]['name'].split(' ')[0]}" \
                                f" {self.PersonalDataGet['tables']['personal'][0]['name'].split(' ')[1]}"
                if len(answer['error'])>0:
                    view_massage(self, answer['error'], 'warning', point_size=10, button=1)
                elif answer['result'] == 'ok_add':
                    answer = f"Сотрудник {name_personal}\nназначен администратором"
                    view_massage(self, answer['result'], 'ok', point_size=10, button=1)
                elif answer['result'] == 'ok_edit':
                    answer = f"Администратор успешно заменен"
                    view_massage(self, answer['result'], 'ok', point_size=10, button=1)

    def set_params_personal(self):
        _translate = QtCore.QCoreApplication.translate
        conf_struct = self.client.get_struct().content
        conf_struct = json.loads(conf_struct.decode('utf-8'))
        conf_criterion = conf_struct['tables']['conf_criterion']
        departments = conf_struct['tables']['department']
        for id, crit in enumerate(conf_criterion):
            self.list_personal.criterion_and_max_coef[crit['title_criterion']] = crit['max_coef']
            self.ComboBox_Crit_LPers.addItem("")
            self.ComboBox_Crit_LPers.setItemText(id, _translate("MainWindow", crit['title_criterion']))
        for id, department in enumerate(departments):
            self.ComboBox_Dep_LPers.addItem("")
            self.ComboBox_Dep_LPers.setItemText(id, _translate("MainWindow", department['title']))

    def date_slot(self):
        calendar = ImpDialogCalendar(self)
        calendar.exec()
        select_date = calendar.calendarWidget.selectedDate()
        year = select_date.year()
        month = select_date.month()
        if len(str(month)) == 1:
            month = '0' + str(month)
        day = select_date.day()
        time_select = datetime.datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y").date()
        div_date = datetime.date.today() - time_select
        if div_date.days < 0:
            print("warning")
        else:
            self.date = f'{day}-{month}-{year}'

    def get_date(self):
        date = datetime.date.today()
        day = str(date.day)
        year = str(date.year)
        month = str(date.month)
        if len(str(month)) == 1:
            month = '0' + str(month)
        return f'{day}-{month}-{year}'

    def ComboBox_Sorting_APers_changed_slot(self):
        _translate = QtCore.QCoreApplication.translate
        if self.list_personal.PersonalDataAssessment != None:
            data_person = self.list_personal.PersonalDataAssessment["tables"]["personal"]
            self.list_personal.PersonalDataAssessment_filter["tables"][
                "personal"] = self.ComboBox_Sorting_APers_changed(data_person)
            self.list_personal.clear_scroll_assessment()
            self.list_personal.count_list_w = 0
            ############################
            if len(self.list_personal.PersonalDataAssessment_filter["tables"][
                       "personal"]) >= self.list_personal.step_list_w:
                num = len(self.list_personal.PersonalDataAssessment_filter["tables"][
                              "personal"]) // self.list_personal.step_list_w
                res = len(self.list_personal.PersonalDataAssessment_filter["tables"][
                              "personal"]) % self.list_personal.step_list_w
                self.list_personal.finish_list_w = [i * self.list_personal.step_list_w for i in range(1, num + 1)]
                self.list_personal.start_list_w = [i * self.list_personal.step_list_w for i in range(0, num)]
                self.list_personal.finish_list_w[-1] += res
                self.Label_NumLastList.setText(_translate("MainWindow", f"...{num}"))
            elif self.list_personal.step_list_w >= len(
                    self.list_personal.PersonalDataAssessment_filter["tables"]["personal"]) > 0:
                self.list_personal.finish_list_w = [
                    len(self.list_personal.PersonalDataAssessment_filter["tables"]["personal"])]
                self.list_personal.start_list_w = [0]
                self.Label_NumLastList.setText(_translate("MainWindow", f"...{1}"))
            self.list_personal.current_Crit_LPers = self.ComboBox_Crit_LPers.currentText()
            self.list_personal.fill_scroll(self.list_personal.PersonalDataAssessment_filter["tables"]["personal"]
                                           [self.list_personal.start_list_w[self.list_personal.count_list_w]:
                                            self.list_personal.finish_list_w[self.list_personal.count_list_w]])
            self.label_AllPersonal.setText(_translate(
                "MainWindow",
                f"всего в отделе {len(self.list_personal.PersonalDataAssessment['tables']['personal'])} сотрудников"))
            self.Label_NumCurrentList.setText(_translate("MainWindow", f"{self.list_personal.count_list_w + 1} "))

    def ComboBox_Sorting_APers_changed(self, data_person):
        if self.ComboBox_Filter_LPers.currentText() == "Отредактированные":
            data_person = list(
                filter(lambda d: len(d["edit_data"][self.ComboBox_Crit_LPers.currentText()]) > 0, data_person))
            self.list_personal.flag_filter = 1
        elif self.ComboBox_Filter_LPers.currentText() == "Без оценки":
            data_person = list(
                filter(lambda d: d['assessment'][self.ComboBox_Crit_LPers.currentText()] == 0, data_person))
            self.list_personal.flag_filter = 1
        elif self.ComboBox_Filter_LPers.currentText() == "C оценкой":
            data_person = list(
                filter(lambda d: d['assessment'][self.ComboBox_Crit_LPers.currentText()] > 0, data_person))
            self.list_personal.flag_filter = 1
        elif self.ComboBox_Filter_LPers.currentText() == "Все":
            data_person = self.list_personal.PersonalDataAssessment["tables"]["personal"]
            self.list_personal.flag_filter = 0
        return data_person

    def ComboBox_Crit_LPers_changed(self):
        """
        Функция срабатывает при изменении критерия
        Заполняет окно списка с данными относительно данного критерия
        :return:
        """
        if self.list_personal.scrollArea_ListPersonal.count() > 0:
            if self.list_personal.flag_filter != 0:
                self.ComboBox_Sorting_APers_changed_slot()
                data_personal = self.list_personal.PersonalDataAssessment_filter["tables"]["personal"][
                                self.list_personal.start_list_w[self.list_personal.count_list_w]:
                                self.list_personal.finish_list_w[self.list_personal.count_list_w]]
            else:
                data_personal = self.list_personal.PersonalDataAssessment["tables"]["personal"][
                                self.list_personal.start_list_w[self.list_personal.count_list_w]
                                :self.list_personal.finish_list_w[self.list_personal.count_list_w]]
            self.list_personal.current_Crit_LPers = self.ComboBox_Crit_LPers.currentText()
            self.list_personal.clear_scroll_assessment()
            self.list_personal.fill_scroll(data_personal)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_head_age.setText(_translate("MainWindow", "Дата рождение"))
        self.label_birthDate.setText(_translate("MainWindow", "-"))
        self.label_old.setText(_translate("MainWindow", "Возраст: - года"))
        self.label_head_workExp.setText(_translate("MainWindow", "Стаж работы"))
        self.label_workExp.setText(_translate("MainWindow", "- год"))
        self.PB_serch_personal.setText(_translate("MainWindow", "Найти"))
        self.label_avatar.setText(_translate("MainWindow", "A"))
        self.label_certification.setText(_translate("MainWindow", "Аттестация"))
        self.label_asses_bonus.setText(_translate("MainWindow", "0"))
        self.label_bonus.setText(_translate("MainWindow", "Бонус"))
        self.label_asses_certification.setText(_translate("MainWindow", "5"))
        self.label_surname.setText(_translate("MainWindow", "-"))
        self.label_name.setText(_translate("MainWindow", "-"))
        self.label_number.setText(_translate("MainWindow", "-"))
        self.label_head_depart.setText(_translate("MainWindow", "Отдел"))
        self.label_name_depart.setText(_translate("MainWindow", "Сборка"))
        self.label_hed_post.setText(_translate("MainWindow", "Должность"))
        self.PB_right_user.setText(_translate("MainWindow", "раздать права"))
        self.label_name_post.setText(_translate("MainWindow", "-"))
        self.label_head_salaryl.setText(_translate("MainWindow", "Базовая ставка"))
        self.label_salaryl.setText(_translate("MainWindow", "-"))
        self.ComboBox_Meanval_LPers.setItemText(0, _translate("MainWindow", "За месяц"))
        self.ComboBox_Meanval_LPers.setItemText(1, _translate("MainWindow", "За квартал"))
        self.ComboBox_Meanval_LPers.setItemText(2, _translate("MainWindow", "За год"))
        self.ComboBox_Filter_LPers.setItemText(0, _translate("MainWindow", "Все"))
        self.ComboBox_Filter_LPers.setItemText(1, _translate("MainWindow", "С оценкой"))
        self.ComboBox_Filter_LPers.setItemText(2, _translate("MainWindow", "Без оценки"))
        self.ComboBox_Filter_LPers.setItemText(3, _translate("MainWindow", "Отредактированные"))
        self.label_Filter_LPers.setText(_translate("MainWindow", "показать"))
        self.TB_Date_LPers.setText(_translate("MainWindow", "..."))
        self.label_Date_Lpers.setText(_translate("MainWindow", "дата"))
        self.Label_Dep_LPers.setText(_translate("MainWindow", "отдел"))
        self.label_Crit_LPers.setText(_translate("MainWindow", "критерий"))
        self.Label_NumCurrentList.setText(_translate("MainWindow", "1 "))
        self.Label_NumLastList.setText(_translate("MainWindow", "...20"))
        self.PB_serch_personalList.setText(_translate("MainWindow", "Загрузить"))
        self.label_AllPersonal.setText(_translate("MainWindow", "всего в отделе - сотрудников"))
        self.PB_right_admin.setText(_translate("MainWindow", "администратор"))

    def fill_scroll_slot(self):
        massage = ImpMassageBox(self)
        massage.Label_message.setGeometry(QtCore.QRect(10, 20, 460, 40))
        massage.PB_OK_Canel.setGeometry(QtCore.QRect(100, 65, 201, 21))
        massage.PB_OK_second.setGeometry(QtCore.QRect(190, 65, 61, 20))
        massage.label_2.setStyleSheet("image: url(./GUI/icon/caution.png);")
        massage.resize(450, 98)
        massage.PB_OK_second.hide()
        _translate = QtCore.QCoreApplication.translate
        if self.ComboBox_Meanval_LPers.currentText() == 'За месяц':
            period_mean = 'month'
        elif self.ComboBox_Meanval_LPers.currentText() == 'За квартал':
            period_mean = 'quarter'
        elif self.ComboBox_Meanval_LPers.currentText() == 'За год':
            period_mean = 'year'
        request_send = {
            "date": self.date,
            "tables": {"department": self.ComboBox_Dep_LPers.currentText()},
            "flag_previous_day": 2,
            "period_mean": period_mean}
        list_person = self.client.assessment_personal(request_send).content.decode('utf-8')
        self.list_personal.PersonalDataAssessment = json.loads(list_person)
        if self.list_personal.PersonalDataAssessment["error"] == 'Bad date':
            massage.Label_message.setText(_translate("Dialog", "За выбранную дату нет оценок"))
            massage.PB_OK_second.show()
            massage.PB_OK_Canel.hide()
            massage.exec()
            return
        cur_date = self.list_personal.PersonalDataAssessment['date'].replace('-', '.')
        self.label_date_assessment.setText(_translate("MainWindow", f"загружено от {cur_date}"))
        for i in range(len(self.list_personal.PersonalDataAssessment["tables"]["personal"])):
            self.list_personal.PersonalDataAssessment["tables"]["personal"][i]['id_main_list'] = i

        # self.PersonalDataAssessment_filter = sorted(self.PersonalDataAssessment_filter, key=lambda d: d['name'])
        if self.list_personal.scrollArea_ListPersonal.count() > 0:
            self.list_personal.clear_scroll_assessment()
        if len(self.list_personal.PersonalDataAssessment["tables"]["personal"]) >= self.list_personal.step_list_w:
            num = len(self.list_personal.PersonalDataAssessment["tables"]["personal"]) // self.list_personal.step_list_w
            res = len(self.list_personal.PersonalDataAssessment["tables"]["personal"]) % self.list_personal.step_list_w
            self.list_personal.finish_list_w = [i * self.list_personal.step_list_w for i in range(1, num + 1)]
            self.list_personal.start_list_w = [i * self.list_personal.step_list_w for i in range(0, num)]
            self.list_personal.finish_list_w[-1] += res
            self.Label_NumLastList.setText(_translate("MainWindow", f"...{num}"))
        elif self.list_personal.step_list_w >= len(self.list_personal.PersonalDataAssessment["tables"]["personal"]) > 0:
            self.list_personal.finish_list_w = [len(self.list_personal.PersonalDataAssessment["tables"]["personal"])]
            self.list_personal.start_list_w = [0]
            self.Label_NumLastList.setText(_translate("MainWindow", f"...{1}"))

        self.list_personal.current_Crit_LPers = self.ComboBox_Crit_LPers.currentText()
        self.list_personal.fill_scroll(self.list_personal.PersonalDataAssessment["tables"]["personal"][
                                       self.list_personal.start_list_w[self.list_personal.count_list_w]:
                                       self.list_personal.finish_list_w[self.list_personal.count_list_w]])
        self.label_AllPersonal.setText(_translate(
            "MainWindow",
            f"всего в отделе {len(self.list_personal.PersonalDataAssessment['tables']['personal'])} сотрудников"))
        self.ComboBox_Filter_LPers.setEnabled(True)

    def age(self, birthdate):
        # Get today's date object
        today = date.today()
        str_age = ''
        # A bool that represents if today's day/month precedes the birth day/month
        one_or_zero = ((today.month, today.day) < (birthdate.month, birthdate.day))

        # Calculate the difference in years from the date object's components
        year_difference = today.year - birthdate.year

        # The difference in years is not enough.
        # To get it right, subtract 1 or 0 based on if today precedes the
        # birthdate's month/day.

        # To do this, subtract the 'one_or_zero' boolean
        # from 'year_difference'. (This converts
        # True to 1 and False to 0 under the hood.)
        age = year_difference - one_or_zero
        if age % 10 == 0 or (age % 10 > 1 and age % 10 < 5):
            str_age = 'года'
        elif age % 10 == 1:
            str_age = 'год'
        else:
            str_age = 'лет'

        return age, str_age

    def remove_personal(self):
        _translate = QtCore.QCoreApplication.translate
        massage = ImpMassageBox(self)
        massage.PB_OK_second.hide()
        massage.Label_message.setText(_translate("Dialog", "Действительно хотите удалить профиль?"))
        massage.exec()
        if massage.flag_choose == 'ok':
            person_remove = {'id_personal': self.PersonalDataGet['tables']['personal'][0]['id_personal']}
            self.PersonalDataGet['tables']['personal'].clear()
            self.PersonalDataGet['tables']['personal'].append(person_remove)
            self.PersonalDataGet["comand"] = 1110
            answer_server = self.client.del_person(self.PersonalDataGet).content
            answer_server = answer_server.decode('utf-8')
            print("remove_personal=", answer_server)
            if answer_server == 'ok':
                massage.PB_OK_Canel.hide()
                massage.PB_OK_second.show()
                massage.Label_message.setText(_translate("Dialog", "Профиль успешно удален"))
                massage.label_2.setStyleSheet("image: url(./GUI/icon/done_mini [#1484].png);")
                massage.exec()
                self.clear_frame_personal()

    def add_personal(self, server):
        print("addpersonal")
        _translate = QtCore.QCoreApplication.translate
        dict_post_id = {}
        dict_department_id = {}
        dlg = ImpDialofAddPersonal(self)
        get_json = self.client.get_struct().content
        get_json = json.loads(get_json.decode('utf-8'))
        for post in get_json["tables"]["posts"]:
            dlg.comboBox_2.addItem(_translate("Dialog", post['label_post']))
            dict_post_id[post['label_post']] = post['id_posts']
        for department in get_json["tables"]["department"]:
            dlg.comboBox.addItem(_translate("Dialog", department['title']))
            dict_department_id[department['title']] = department['id_department']
        dlg.exec()
        if dlg.flag_filling == 1:
            dlg.PersonalData["tables"]["personal"][0][
                "name"] = dlg.LE_FamilyName.text() + " " + dlg.LE_Name.text() + " " + dlg.LE_FatherName.text()
            dlg.PersonalData["tables"]["personal"][0]["education"] = "-"
            dlg.PersonalData["tables"]["personal"][0]["number"] = dlg.LE_NuberPhone.text()
            dlg.PersonalData["tables"]["personal"][0]["certification"] = int(dlg.LE_Attestation.text())
            dlg.PersonalData["tables"]["personal"][0]["id_posts"] = dict_post_id[dlg.comboBox_2.currentText()]
            dlg.PersonalData["tables"]["personal"][0]["id_department"] = dict_department_id[dlg.comboBox.currentText()]
            dlg.PersonalData["tables"]["personal"][0]["salaryl"] = int(dlg.LE_BaseRate.text())
            if len(dlg.PhotoPersonal) > 0:
                dlg.PersonalData["tables"]["personal"][0]["dir_avatar"] = dlg.PhotoPersonal
            else:
                buffered = BytesIO()
                face = cv2.imread('./GUI/icon/silhouette_icon128x128.png')
                face_to_json = Image.fromarray(face)
                face_to_json.save(buffered, format="JPEG")
                img_byte = buffered.getvalue()
                img_base64 = base64.b64encode(img_byte)
                dlg.PersonalData["tables"]["personal"][0]["dir_avatar"] = img_base64.decode('utf-8')
            day = dlg.LE_Day.text()
            if int(day) < 10:
                day = '0' + day
            dlg.PersonalData["tables"]["personal"][0]["birthday"] = dlg.LE_year.text() + '-' + dlg.rev_month[
                dlg.LE_month.text()] + '-' + day
            answer_server = self.client.add_personal(dlg.PersonalData).content.decode("utf-8")
            if answer_server == 'ok':
                massage = ImpMassageBox(self)
                massage.PB_OK_Canel.hide()
                massage.Label_message.setText(_translate("Dialog", "   Сотрудник успешно добавлен"))
                massage.label_2.setStyleSheet("image: url(./GUI/icon/done_mini [#1484].png);")
                massage.exec()

    def edit_personal(self):
        _translate = QtCore.QCoreApplication.translate
        dict_post_id = {}
        dict_department_id = {}
        PersonalDataEdit = {
            "tables": {"personal": [{"id_personal": self.PersonalDataGet["tables"]["personal"][0]["id_personal"],
                                     "name": "Петров Иван Иванович",
                                     "education": "ГМИ",
                                     "number": "+7(988)-834-15-41",
                                     "certification": 5,
                                     "id_posts": 1,
                                     "id_department": 2,
                                     "salaryl": 50000,
                                     "bonus": 0,
                                     "dir_avatar": self.PersonalDataGet["tables"]["personal"][0]["dir_avatar"],
                                     "birthday": '',
                                     "right_user": '',
                                     "rules": []}]
                       }}
        answer_server = ''
        name_column_file = {'personal': 'dir_avatar'}
        dlg = ImpDialofAddPersonal(self)
        get_json = self.client.get_struct().content
        get_json = json.loads(get_json.decode('utf-8'))
        dlg.comboBox_2.addItem(_translate("Dialog", self.PersonalDataGet["tables"]["personal"][0]["id_posts"]))
        dlg.comboBox.addItem(_translate("Dialog", self.PersonalDataGet["tables"]["personal"][0]["id_department"]))

        for post in get_json["tables"]["posts"]:
            if post['label_post'] != self.PersonalDataGet["tables"]["personal"][0]["id_posts"]:
                dlg.comboBox_2.addItem(_translate("Dialog", post['label_post']))
            dict_post_id[post['label_post']] = post['id_posts']
        for department in get_json["tables"]["department"]:
            if department['title'] != self.PersonalDataGet["tables"]["personal"][0]["id_department"]:
                dlg.comboBox.addItem(_translate("Dialog", department['title']))
            dict_department_id[department['title']] = department['id_department']

        self.PersonalDataGet["tables"]["personal"][0]["id_department"] = dict_department_id[
            self.PersonalDataGet["tables"]["personal"][0]["id_department"]]
        self.PersonalDataGet["tables"]["personal"][0]["id_posts"] = dict_post_id[
            self.PersonalDataGet["tables"]["personal"][0]["id_posts"]]

        FamilyName, Name, FatherName = self.PersonalDataGet["tables"]["personal"][0]['name'].split(" ")
        year, month, day = self.PersonalDataGet["tables"]["personal"][0]['birthday'].split("-")
        dlg.LE_FamilyName.setText(_translate("Form", FamilyName))
        dlg.LE_Name.setText(_translate("Form", Name))
        dlg.LE_FatherName.setText(_translate("Form", FatherName))
        dlg.LE_NuberPhone.setText(_translate("Form", self.PersonalDataGet["tables"]["personal"][0]['number']))
        dlg.LE_Attestation.setText(
            _translate("Form", str(self.PersonalDataGet["tables"]["personal"][0]['certification'])))
        dlg.LE_BaseRate.setText(_translate("Form", str(self.PersonalDataGet["tables"]["personal"][0]['salaryl'])))
        dlg.LE_Day.setText(_translate("Form", day))
        dlg.LE_month.setText(_translate("Form", dlg.month[int(month)]))
        dlg.LE_year.setText(_translate("Form", year))

        avatar = self.PersonalDataGet["tables"]["personal"][0]["dir_avatar"]

        img = base64.b64decode(avatar)  # Convert image data converted to base64 to original binary data# bytes
        img = BytesIO(img)  # _io.Converted to be handled by BytesIO pillow
        img = Image.open(img)
        face = np.asarray(img)
        height, width, channel = face.shape
        bytesPerLine = 3 * width
        qFace = QtGui.QImage(face.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(qFace)
        dlg.Label_SpaceImage.setPixmap(pixmap)
        dlg.exec()
        if dlg.flag_filling == 1:

            PersonalDataEdit["tables"]["personal"][0][
                "name"] = dlg.LE_FamilyName.text() + " " + dlg.LE_Name.text() + " " + dlg.LE_FatherName.text()
            PersonalDataEdit["tables"]["personal"][0]["education"] = "-"
            PersonalDataEdit["tables"]["personal"][0]["number"] = dlg.LE_NuberPhone.text()
            PersonalDataEdit["tables"]["personal"][0]["certification"] = int(dlg.LE_Attestation.text())
            PersonalDataEdit["tables"]["personal"][0]["id_posts"] = dict_post_id[dlg.comboBox_2.currentText()]
            PersonalDataEdit["tables"]["personal"][0]["id_department"] = dict_department_id[dlg.comboBox.currentText()]
            PersonalDataEdit["tables"]["personal"][0]["salaryl"] = int(dlg.LE_BaseRate.text())
            PersonalDataEdit["tables"]["personal"][0]["birthday"] = dlg.LE_year.text() + '-' + dlg.rev_month[
                dlg.LE_month.text()] + '-' + dlg.LE_Day.text()
            if len(dlg.PhotoPersonal) > 0:
                PersonalDataEdit["tables"]["personal"][0]["dir_avatar"] = dlg.PhotoPersonal

            value_edit_list = []
            value_list_copy = PersonalDataEdit["tables"]["personal"]
            value_list = self.PersonalDataGet["tables"]["personal"]

            for v in range(len(value_list)):
                v_keys = list(value_list[v].keys())
                equal = value_list[v] == value_list_copy[v]  # проверка на редактирование
                value_edit_dict = {}
                if equal == False:
                    value_edit_dict[v_keys[0]] = value_list[v][v_keys[0]]
                    for v_key in v_keys:
                        v_orig = value_list[v][v_key]
                        v_copy = value_list_copy[v][v_key]
                        if v_orig != v_copy:
                            value_edit_dict[v_key] = v_copy
                if len(value_edit_dict.keys()) > 0:
                    value_edit_list.append(value_edit_dict)
            if len(value_edit_list) > 0:
                massage = ImpMassageBox(self)
                massage.PB_OK_second.hide()
                massage.exec()
                if massage.flag_choose == 'ok':
                    dlg.PersonalData["tables"]["personal"] = value_edit_list
                    dlg.PersonalData["comand"] = 1110
                    answer_server = self.client.edit_person(data_send=dlg.PersonalData,
                                                            name_column_file=name_column_file)

        if answer_server == 'ok':
            print("Профиль работника отредактирован")
            massage = ImpMassageBox(self)
            massage.PB_OK_Canel.hide()
            massage.Label_message.setText(_translate("Dialog", "Профиль успешно изменен"))
            massage.label_2.setStyleSheet("image: url(./GUI/done_mini [#1484].png);")
            massage.exec()
            self.get_personal(PersonalDataEdit["tables"]["personal"][0]["name"])
        else:
            self.PersonalDataGet["tables"]["personal"][0]["id_posts"] = dlg.comboBox_2.currentText()
            self.PersonalDataGet["tables"]["personal"][0]["id_department"] = dlg.comboBox.currentText()

    def search_personal(self, NamePerson=''):
        if type(NamePerson) == bool:
            NamePerson = self.LE_serch_personal.text()
        self.get_personal(NamePerson)

    def get_personal(self, NamePerson):
        import itertools
        _translate = QtCore.QCoreApplication.translate
        rev_month = {'01': 'января',
                     '02': 'февраля',
                     '03': 'марта',
                     '04': 'апреля',
                     '05': 'мая',
                     '06': 'июня',
                     '07': 'июля',
                     '08': 'августа',
                     '09': 'сентября',
                     '10': 'октября',
                     '11': 'ноября',
                     '12': 'декабря'}
        print(NamePerson)
        self.PersonalDataSend["tables"]["personal"][0]["name"] = NamePerson
        person = self.client.get_personal(data_send=self.PersonalDataSend).content
        person = json.loads(person.decode('utf-8'))
        if 'error' in person:
            massage = ImpMassageBox(self)
            massage.PB_OK_Canel.hide()
            massage.PB_OK_second.show()
            massage.Label_message.setText(_translate("Dialog", "   " + person['error']))
            massage.label_2.setStyleSheet("image: url(./GUI/icon/emoji_sad_circle [#541].png);")
            massage.exec()
            print(person['error'])
            return None

        index = self.flag_get_personal
        if len(person) == 1:
            index = 0
        elif len(person) > 1:
            person_list = ExploytListWidget()
            for person_ in person:
                icon = person_["dir_avatar"]
                img = base64.b64decode(icon)  # Convert image data converted to base64 to original binary data# bytes
                img = BytesIO(img)  # _io.Converted to be handled by BytesIO pillow
                img = Image.open(img)
                face = np.asarray(img)
                face = cv2.resize(face, (80, 80))
                height, width, channel = face.shape
                bytesPerLine = 3 * width
                qFace = QtGui.QImage(face.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
                pixmap = QtGui.QPixmap(qFace)
                person_list.dynamicListWidget(person_['name'], pixmap, person_["id_posts"])
            person_list.exec()
            index = person_list.index

        if index != -1:
            person = person[index]
            FamilyName, Name, FatherName = person['name'].split(" ")
            self.label_surname.setText(_translate("MainWindow", FamilyName))
            self.label_name.setText(_translate("MainWindow", Name + ' ' + FatherName))
            self.label_number.setText(_translate("MainWindow", person['number']))
            self.label_name_depart.setText(_translate("MainWindow", person["id_department"]))
            self.label_name_post.setText(_translate("MainWindow", person["id_posts"]))
            self.label_salaryl.setText(_translate("MainWindow", str(person["salaryl"])))
            self.label_asses_certification.setText(_translate("MainWindow", str(person["certification"])))
            self.label_asses_bonus.setText(_translate("MainWindow", str(person["bonus"])))
            year, month, day = person['birthday'].split('-')
            year_cr, month_cr, day_cr = person['created_pers'].split(' ')[0].split('-')

            age, str_year = self.age(date(int(year), int(month), int(day)))
            age_cr, str_year_cr = self.age(date(int(year_cr), int(month_cr), int(day_cr)))
            if age_cr <= 0:
                work_exp = 'меньше года'
            else:
                work_exp = str(age_cr) + str_year_cr
            self.label_birthDate.setText(_translate("MainWindow", day + ' ' + rev_month[month] + ' ' + year + ' года'))
            self.label_old.setText(_translate("MainWindow", 'Возраст: ' + str(age) + ' ' + str_year))
            self.label_workExp.setText(_translate("MainWindow", work_exp))
            person.pop('created_pers')
            avatar = person["dir_avatar"]
            img = base64.b64decode(avatar)  # Convert image data converted to base64 to original binary data# bytes
            img = BytesIO(img)  # _io.Converted to be handled by BytesIO pillow
            img = Image.open(img)
            face = np.asarray(img)
            height, width, channel = face.shape
            bytesPerLine = 3 * width
            qFace = QtGui.QImage(face.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
            pixmap = QtGui.QPixmap(qFace)
            self.label_avatar.setPixmap(pixmap)
        self.flag_get_personal = index
        if self.flag_get_personal > -1:
            self.TB_EditPersonal.setEnabled(True)
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(
                "./GUI/icon/pen [#1320].png"),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.TB_EditPersonal.setIcon(icon1)

            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap(
                "./GUI/icon/icons8-удалить-96.png"),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.TB_RemovePersonal.setIcon(icon2)
            self.TB_RemovePersonal.setEnabled(True)
            self.PB_right_user.setEnabled(True)
            self.PB_right_admin.setEnabled(True)
            self.PersonalDataGet['tables']['personal'].clear()
            self.PersonalDataGet["tables"]["personal"].append(person)
            if 'rules' in person:
                self.PB_right_user.setStyleSheet(self.stile_button_rights)
                if person['right_user'] == 'admin':
                    self.PB_right_admin.setStyleSheet(self.stile_button_rights)
                else:
                    self.PB_right_admin.setStyleSheet(self.stile_button_not_rights)
            else:
                self.PB_right_user.setStyleSheet(self.stile_button_not_rights)
                self.PB_right_admin.setStyleSheet(self.stile_button_not_rights)

    def rule_user_(self):
        _translate = QtCore.QCoreApplication.translate
        massage_box = ImpMassageBox(self)
        massage_box.PB_OK_second.hide()
        login_personal = transliterate.translit(self.label_surname.text() + self.label_name.text().split(' ')[0],
                                                reversed=True)
        rule_user = ImpDialogUserRule()
        rule_user.lay_reg.LE_Name.setText(_translate("Form", login_personal))
        if 'rules' in self.PersonalDataGet['tables']['personal'][0]:
            rule_user.get_right = self.PersonalDataGet['tables']['personal'][0]['rules']
            if self.PersonalDataGet['tables']['personal'][0]['right_user'] == 'admin':
                rule_user.set_CheckBox(blocked=1)
            else:
                rule_user.set_CheckBox()
        else:
            rule_user.VL_Build.addWidget(rule_user.lay_reg.registr_frame)

        rule_user.VL_Build.addWidget(rule_user.lay_rule.rule_frame)
        rule_user.exec()
        if rule_user.flag_successful_register == 1:
            json_reg = {
                "status": 'register',
                "tables": {
                    "users": {
                        "id_personal": self.PersonalDataGet['tables']['personal'][0]['id_personal'],
                        "nickname": rule_user.login,
                        "password": rule_user.password.hex(),
                        "salt_user": rule_user.salt_user.decode()
                    },

                    "access_rule": rule_user.rule_inform,

                }
            }

            result = client.register(json_reg).content.decode("utf-8")
            if result == 'ok':
                massage_box.Label_message.setText(_translate("UserRule", "Пользователь успешно зарегистрирован"))
            else:
                massage_box.Label_message.setText(_translate("UserRule", "что то пошло не так"))
            massage_box.exec()

        elif rule_user.flag_register_user == 0 and rule_user.flag_change_right == 1:
            json_reg = {
                "status": 'change',
                "tables": {

                    "users": {
                        "id_personal": self.PersonalDataGet['tables']['personal'][0]['id_personal']
                    },

                    "access_rule": {"add_right": list(rule_user.add_right),
                                    "del_right": list(rule_user.del_right)}

                }
            }
            result = client.register(json_reg).content.decode("utf-8")
            if result == 'ok':
                massage_box.Label_message.setText(_translate("UserRule", "Права пользователя успешно изменены"))

            else:
                massage_box.Label_message.setText(_translate("UserRule", "что то пошло не так"))
            massage_box.exec()


        elif rule_user.flag_del_user == 1:
            json_reg = {
                "status": 'del_user',
                "tables": {

                    "users": {
                        "id_personal": self.PersonalDataGet['tables']['personal'][0]['id_personal']
                    },

                    "access_rule": {}
                }
            }
            result = client.register(json_reg).content.decode("utf-8")

            if result == 'ok':
                massage_box.Label_message.setText(_translate("UserRule", "Пользователь успешно удален"))
            else:
                massage_box.Label_message.setText(_translate("UserRule", "что то пошло не так"))
            massage_box.exec()


class ImpDialogCalendar(QDialog, DialogCalendar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.flag_choose = ''
        self.PB_OK.clicked.connect(self.accept)
        self.BirthDay = None

    def accept(self):
        self.flag_choose = 'ok'
        self.close()


class ImpDialofAddPersonal(QDialog, DialogAddPersonal):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.rejected.connect(self.reject_)
        self.TB_calendar.clicked.connect(self.EditCalendar)
        self.TB_AddPhoto.clicked.connect(self.AddPhoto)
        self.PersonalData = {
            "comand": 2000,
            "user": "admin",
            "db_comand": 1,
            "tables": {"personal": [{"name": "Петров Иван Иванович",
                                     "education": "ГМИ",
                                     "number": "+7(988)-834-15-41",
                                     "certification": 5,
                                     "id_posts": 1,
                                     "id_department": 2,
                                     "salaryl": 50000,
                                     "bonus": 0,
                                     "dir_avatar": 'q',
                                     "birthday": '1992-05-16'}
                                    ]}}
        self.month = {1: 'январь',
                      2: 'февраль',
                      3: 'март',
                      4: 'апрель',
                      5: 'май',
                      6: 'июнь',
                      7: 'июль',
                      8: 'август',
                      9: 'сентябрь',
                      10: 'октябрь',
                      11: 'ноябрь',
                      12: 'декабрь'}

        self.rev_month = {'январь': '01',
                          'февраль': '02',
                          'март': '03',
                          'апрель': '04',
                          'май': '05',
                          'июнь': '06',
                          'июль': '07',
                          'август': '08',
                          'сентябрь': '09',
                          'октябрь': '10',
                          'ноябрь': '11',
                          'декабрь': '12'}
        self.PhotoPersonal = ''

        ################asteric########################
        self.Asterisk_FamalyName = QtWidgets.QLabel(self)
        self.Asterisk_FamalyName.setEnabled(True)
        self.Asterisk_FamalyName.hide()
        self.Asterisk_FamalyName.setGeometry(QtCore.QRect(297, 52, 17, 17))
        self.Asterisk_FamalyName.setStyleSheet("border-image: url(./GUI/icon/asterisk.png);")
        self.Asterisk_FamalyName.setText("")
        self.Asterisk_FamalyName.setObjectName("Asterisk_FamalyName")
        self.Asterisk_Name = QtWidgets.QLabel(self)
        self.Asterisk_Name.hide()
        self.Asterisk_Name.setEnabled(True)
        self.Asterisk_Name.setGeometry(QtCore.QRect(297, 82, 17, 17))
        self.Asterisk_Name.setStyleSheet("border-image: url(./GUI/icon/asterisk.png);")
        self.Asterisk_Name.setText("")
        self.Asterisk_Name.setObjectName("Asterisk_Name")
        self.Asterisk_BaseRate = QtWidgets.QLabel(self)
        self.Asterisk_BaseRate.hide()
        self.Asterisk_BaseRate.setEnabled(True)
        self.Asterisk_BaseRate.setGeometry(QtCore.QRect(158, 377, 17, 17))
        self.Asterisk_BaseRate.setStyleSheet("border-image: url(./GUI/icon/asterisk.png);")
        self.Asterisk_BaseRate.setText("")
        self.Asterisk_BaseRate.setObjectName("Asterisk_BaseRate")
        self.Asterisk_Attestation = QtWidgets.QLabel(self)
        self.Asterisk_Attestation.setEnabled(True)
        self.Asterisk_Attestation.hide()
        self.Asterisk_Attestation.setGeometry(QtCore.QRect(297, 377, 17, 17))
        self.Asterisk_Attestation.setStyleSheet("border-image: url(./GUI/icon/asterisk.png);")
        self.Asterisk_Attestation.setText("")
        self.Asterisk_Attestation.setObjectName("Asterisk_Attestation")
        self.Asterisk_FatherName = QtWidgets.QLabel(self)
        self.Asterisk_FatherName.setEnabled(True)
        self.Asterisk_FatherName.hide()
        self.Asterisk_FatherName.setGeometry(QtCore.QRect(297, 112, 17, 17))
        self.Asterisk_FatherName.setStyleSheet("border-image: url(./GUI/icon/asterisk.png);")
        self.Asterisk_FatherName.setText("")
        self.Asterisk_FatherName.setObjectName("Asterisk_FatherName")
        self.Asterisk_Day = QtWidgets.QLabel(self)
        self.Asterisk_Day.setEnabled(True)
        self.Asterisk_Day.hide()
        self.Asterisk_Day.setGeometry(QtCore.QRect(297, 180, 17, 17))
        self.Asterisk_Day.setStyleSheet("border-image: url(./GUI/icon/asterisk.png);")
        self.Asterisk_Day.setText("")
        self.Asterisk_Day.setObjectName("Asterisk_Day")
        self.Asterisk_NumberPhone = QtWidgets.QLabel(self)
        self.Asterisk_NumberPhone.setEnabled(True)
        self.Asterisk_NumberPhone.hide()
        self.Asterisk_NumberPhone.setGeometry(QtCore.QRect(297, 240, 17, 17))
        self.Asterisk_NumberPhone.setStyleSheet("border-image: url(./GUI/icon/asterisk.png);")
        self.Asterisk_NumberPhone.setText("")
        self.Asterisk_NumberPhone.setObjectName("Asterisk_NumberPhone")

        self._translate = QtCore.QCoreApplication.translate
        ################################################

    def EditCalendar(self):

        calendar = ImpDialogCalendar(self)
        if len(self.LE_Day.text()) != 0 and len(self.LE_month.text()) != 0 and len(self.LE_year.text()) != 0:
            date = QtCore.QDate(int(self.LE_year.text()), int(self.rev_month[self.LE_month.text()]),
                                int(self.LE_Day.text()))
            calendar.calendarWidget.setSelectedDate(date)
        calendar.exec()
        calendar.BirthDay = calendar.calendarWidget.selectedDate()
        self.LE_Day.setText(self._translate("Dialog", str(calendar.BirthDay.day())))
        self.LE_month.setText(self._translate("Dialog", self.month[calendar.BirthDay.month()]))
        self.LE_year.setText(self._translate("Dialog", str(calendar.BirthDay.year())))

    def accept(self) -> None:
        self.flag_filling = 1
        LE_list = [self.LE_Name,
                   self.LE_FatherName,
                   self.LE_FamilyName,
                   self.LE_NuberPhone,
                   self.LE_Day,
                   self.LE_BaseRate,
                   self.LE_Attestation]

        Asteric_list = [self.Asterisk_Name,
                        self.Asterisk_FatherName,
                        self.Asterisk_FamalyName,
                        self.Asterisk_NumberPhone,
                        self.Asterisk_Day,
                        self.Asterisk_BaseRate,
                        self.Asterisk_Attestation]
        self.Asterisk_NumberPhone.show()
        for id, LE in enumerate(LE_list):
            text = LE.text()
            Asteric_list[id].hide()
            if len(text) == 0 or (text.find('+') != -1 and len(text.replace(' ', '')) < 15):
                Asteric_list[id].show()
                self.flag_filling = 0

        if self.flag_filling == 0:
            print("Не все заполнено")
        if self.flag_filling == 1:
            print("все отлично")
            self.close()
            self.flag_filling = 1
            print(f"self.flag_filling={self.flag_filling}")

    def reject_(self) -> None:
        self.close()
        self.flag_filling = 0

    def find_face(self, path):
        img = cv2.imread(path, 0)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.1, 4)
        # faces = face_cascade.detectMultiScale(img, 1.2, 1)
        if len(faces) > 0:
            x, y, w, h = faces[0]
            percent = 0.08
            percent_w = 0
            percent_h = 0
            max_h, max_w = img.shape
            if max_h < max_w:
                dev = max_w / max_h
                percent_h = percent * dev
                percent_w = percent
            elif max_h > max_w:
                dev = max_h / max_w
                percent_h = percent
                percent_w = percent * dev
            else:
                percent_h = percent
                percent_w = percent

            x_p = 0
            w_p = 0
            y_p = 0
            h_p = 0
            if x - max_w * percent_w > 0:
                x_p = int(max_w * percent_w)
            if x + w + max_w * percent_w < max_w:
                w_p = int(max_w * percent_w)

            if y - max_h * percent_h > 0:
                y_p = int(max_h * percent_h)
            if y + h + max_h * percent_h < max_h:
                h_p = int(max_h * percent_h)
            img = cv2.imread(path)
            face_save = img[y - y_p:y + h + h_p, x - x_p:x + w + w_p, :]
            scale_percent = int(13500 / max(face_save.shape))
            width_res = int(face_save.shape[1] * scale_percent / 100)
            height_res = int(face_save.shape[0] * scale_percent / 100)
            dim = (width_res, height_res)
            face_save = cv2.resize(face_save, dim, interpolation=cv2.INTER_AREA)
        else:
            face_save = -1
        return face_save

    def AddPhoto(self):
        face = None
        buffered = BytesIO()
        path_image = f'C:/Users/{os.getlogin()}/Pictures/'
        if not os.path.exists(path_image):
            os.makedirs(path_image)
        image_name = QFileDialog.getOpenFileName(self, "Openfile", path_image,
                                                 "All Files (*);;PNG files (*.png);; Jpg Files (*.jpg)")
        if len(image_name[0]) > 0:
            face = self.find_face(image_name[0])

        if type(face) == np.ndarray:
            face_to_json = Image.fromarray(face)
            face_to_json.save(buffered, format="JPEG")
            img_byte = buffered.getvalue()
            img_base64 = base64.b64encode(img_byte)
            self.PhotoPersonal = img_base64.decode('utf-8')
            height, width, channel = face.shape
            bytesPerLine = 3 * width
            qFace = QtGui.QImage(face.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
            self.pixmap = QtGui.QPixmap(qFace)
            self.Label_SpaceImage.setPixmap(self.pixmap)
        elif face == -1:
            self.Label_SpaceImage.setText(self._translate("Dialog", "Загрузите изображения\n с лицом"))


class ImpMassageBox(QDialog, MassageBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.flag_choose = ''
        self.PB_OK_second.clicked.connect(self.accept)

    def accept(self):
        self.flag_choose = 'ok'
        self.close()

        pass


class ImpDialogUserRule(DialogUserRule):
    def __init__(self):

        super(ImpDialogUserRule, self).__init__()
        _translate = QtCore.QCoreApplication.translate
        inform_password = "<html><head/><body><p><span style=\" color:#ffffff;\">" \
                          "Пароль должен содержать минимум восемь символов, минимум одну букву и одна цифру" \
                          "</span></p></body></html>"
        self.lay_reg = LayRegistr()
        self.lay_rule = LayRule()
        self.lay_reg.set_registr(layoutWidget=self.layoutWidget, maximum_size=(16777215, 150))
        self.lay_rule.set_rule(layoutWidget=self.layoutWidget)
        regular_ex = QtCore.QRegExp("[a-zA-Z0-9_]{30}")
        input_validator = QtGui.QRegExpValidator(regular_ex, self.lay_reg.LE_Name)
        self.lay_reg.LE_Name.setValidator(input_validator)
        regular_ex = QtCore.QRegExp("[A-Za-z\d@$!%*?&]{20}")  # №\\b^.*(?=.{8,})(?=.*\d)(?=.*[a-z]).*$\\b
        input_validator = QtGui.QRegExpValidator(regular_ex, self.lay_reg.LE_Password)
        self.lay_reg.LE_Password.setValidator(input_validator)
        input_validator = QtGui.QRegExpValidator(regular_ex, self.lay_reg.LE_Password_rep)
        self.lay_reg.LE_Password_rep.setValidator(input_validator)
        self.lay_reg.QL_Error_pass.setToolTip(_translate("MainWindow",
                                                         inform_password))
        self.lay_reg.QL_Error_pass.hide()
        self.lay_reg.QL_Error_name.hide()
        self.lay_rule.QL_Error_rule.hide()
        self.buttonBox_ONOFF.rejected.connect(self.reject)
        self.buttonBox_ONOFF.accepted.connect(self.accept)
        self.flag_successful_register = 0
        self.flag_register_user = 1
        self.flag_change_right = 0
        self.flag_del_user = 0

        self.login = ''
        self.password = ''
        self.salt_user = ''
        self.rule_inform = {}

        self.check_boxes = {1: self.lay_rule.checkBox_personal,
                            2: self.lay_rule.checkBox_analytics,
                            3: self.lay_rule.checkBox_project,
                            4: self.lay_rule.checkBox_struct,
                            5: self.lay_rule.checkBox_assessment}
        self.get_right = []
        self.cur_right = []
        self.add_right = []
        self.del_right = []

    def reject_(self):
        print("close")
        self.close()

    def accept(self):
        print('ok')
        if self.flag_register_user == 1:
            reg_inform = self.get_reg_inform()
            rule_ch = self.get_rule_inform()
            if type(reg_inform) == tuple and rule_ch == True:
                self.login, self.password, self.salt_user = reg_inform[0], reg_inform[1], reg_inform[2]
                print(f'login={self.login}, pass={self.password}, salt={self.salt_user}')
                self.flag_successful_register = 1
        else:
            self.add_right, self.del_right, residue_right = list(self.check_change_CheckBox())
            _translate = QtCore.QCoreApplication.translate
            massage_box = ImpMassageBox(self)
            massage_box.PB_OK_second.hide()
            if len(self.add_right) > 0 or (len(self.del_right) > 0 and len(residue_right) > 0):
                massage_box.Label_message.setText(_translate("UserRule", "Вы хотите изменить права?"))
                massage_box.exec()
                if massage_box.flag_choose == 'ok':
                    self.flag_change_right = 1
            elif len(self.add_right) == 0 and len(residue_right) == 0 and len(self.del_right) > 0:
                massage_box.Label_message.setText(_translate("UserRule", "Вы хотите удалить пользователя?"))
                massage_box.exec()
                if massage_box.flag_choose == 'ok':
                    self.flag_del_user = 1
        self.close()

    def check_reg(self):
        regular_pass = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        _translate = QtCore.QCoreApplication.translate
        self.lay_reg.QL_Error_pass.hide()
        self.lay_reg.QL_Error_name.hide()
        if not 3 < len(self.lay_reg.LE_Name.text()) < 20:
            self.lay_reg.QL_Error_name.show()
            answer = -2  # 'Логин меньше 3 или больше 20 символов'
        elif re.match(regular_pass, self.lay_reg.LE_Password.text()) == None:
            self.lay_reg.QL_Error_pass.show()
            answer = -1  # "пароль должен содержать минимум восемь символов, минимум одну букву и одну цифру"
        elif self.lay_reg.LE_Password.text() != self.lay_reg.LE_Password_rep.text():
            self.lay_reg.QL_Error_pass.show()
            self.lay_reg.QL_Error_pass.setText(_translate("UserRule", "пароли не совпадают"))
            answer = 0
        else:
            answer = 1

        return answer

    def check_rule(self):
        if 1 not in list(self.rule_inform.values()):
            self.lay_rule.QL_Error_rule.show()
            return False
        else:
            return True

    def set_CheckBox(self, blocked=0):
        self.flag_register_user = 0
        for i in self.get_right:
            self.check_boxes[i].setChecked(True)
            if blocked == 1:
                self.check_boxes[i].setEnabled(False)

    def check_change_CheckBox(self):
        for ch_key in self.check_boxes:
            ch_condition = self.check_boxes[ch_key].isChecked()
            if ch_condition:
                self.cur_right.append(ch_key)
        self.cur_right = set(self.cur_right)
        self.get_right = set(self.get_right)

        add_right = self.cur_right - self.get_right
        del_right = self.get_right - self.cur_right
        residue_right = self.get_right - del_right
        return add_right, del_right, residue_right

    def get_reg_inform(self):
        ch = self.check_reg()
        if ch != 1:
            return False
        else:
            salt_user = os.urandom(32).hex()
            salt_user = bytes(salt_user, 'utf-8')
            password = argon2.hash_password_raw(time_cost=16, memory_cost=2 ** 15,
                                                parallelism=2, hash_len=32,
                                                password=bytes(self.lay_reg.LE_Password.text(), 'utf-8'),
                                                salt=salt_user,
                                                type=argon2.low_level.Type.ID)
            login = self.lay_reg.LE_Name.text()

        return (login, password, salt_user)

    def get_rule_inform(self):

        self.rule_inform = {"analytics": 1 if self.lay_rule.checkBox_analytics.isChecked() == True else 0,
                            "assessment_personall": 1 if self.lay_rule.checkBox_assessment.isChecked() == True else 0,
                            "project": 1 if self.lay_rule.checkBox_project.isChecked() == True else 0,
                            "interaction_personall": 1 if self.lay_rule.checkBox_personal.isChecked() == True else 0,
                            "inside_struct": 1 if self.lay_rule.checkBox_struct.isChecked() == True else 0,
                            }
        ch = self.check_rule()

        return ch

    def set_rule(self):
        pass


class MainWindow_all_3(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self, client, parent=None):
        qApp.setStyleSheet("QMessageBox QPushButton {color: rgb(255, 255, 255);}"
                           " QMessageBox QPushButton {background-color: rgb(145, 158, 208);}"
                           "QMessageBox QLabel {color: rgb(255, 255, 255);}")
        self._translate = QtCore.QCoreApplication.translate
        super(MainWindow_all_3, self).__init__(parent=parent)
        self.x_start = 0
        self.y_start = 0
        self.resized.connect(self.position)
        self.WorkWindow = Ui_MainWindow()
        self.WorkWindow.setupUi(self)
        self.center = int(1011 / 2)
        self.center_struct = int(1390 / 2)
        self.x_start_struct = 60

        self.pers_inter = PersonInteraction(cl=client)
        self.pers_assessment = PersonalAssessment(cl=client)
        self.struct = COF.Table_start_(cr_ed='edit')
        self.client = client
        self.struct.refreshButton.clicked.connect(self.refresh_inside_structure)
        self.struct.ButtonNext.setText(self._translate("Form", "ОТПРАВИТЬ"))

        # self.WorkWindow.stackedWidget.addWidget(self.struct)#стек№1
        # self.WorkWindow.stackedWidget.addWidget(self.page_2)

        self.WorkWindow.stackedWidget.addWidget(self.pers_inter)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.WorkWindow.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_2")
        self.WorkWindow.stackedWidget.addWidget(self.page_3)
        self.WorkWindow.stackedWidget.addWidget(self.struct)  # стек№4

        self.WorkWindow.stackedWidget.addWidget(self.pers_assessment)

        self.WorkWindow.TB_structure.clicked.connect(self.inside_structure)
        self.WorkWindow.TB_search_personal.clicked.connect(self.personal)
        self.WorkWindow.TB_project.clicked.connect(self.projects)
        self.WorkWindow.TB_analytics.clicked.connect(self.analytics)
        self.WorkWindow.TB_assessment.clicked.connect(self.assessment)
        self.WorkWindow.TB_EditPersonal.setEnabled(False)
        self.WorkWindow.TB_RemovePersonal.setEnabled(False)
        self.WorkWindow.PB_name_user.clicked.connect(self.change_log)

        face = cv2.imread('./GUI/icon/silhouette_icon128x128.png')
        height, width, channel = face.shape
        bytesPerLine = 3 * width
        qFace = QtGui.QImage(face.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(qFace)
        self.WorkWindow.label_avatar.setPixmap(pixmap)
        self.pers_inter.label_avatar.setPixmap(pixmap)

        self.progress_bar = COF.PopUpProgressB()
        self.threadpool = QtCore.QThreadPool()
        self.flag_one_load_struct = 0
        self.flag_get_personal = -1
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setObjectName("MainWindow")
        self.resize(1500, 901)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet("background-color: rgb(74, 80, 106);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.GlobalstackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.GlobalstackedWidget.setGeometry(
            QtCore.QRect(self.x_start, self.y_start, self.screen.width() - self.x_start,
                         self.screen.height() - self.y_start))
        self.GlobalstackedWidget.setAutoFillBackground(False)
        self.GlobalstackedWidget.setStyleSheet("")
        self.GlobalstackedWidget.setObjectName("stackedWidget")
        self.PersonalDataSend = {
            "comand": 2001,
            "user": "admin",
            "db_comand": 1,
            "tables": {"personal": [{"name": ''
                                     }
                                    ]}}
        self.PersonalDataGet = {
            "comand": 0,
            "user": "admin",
            "db_comand": 1,
            "tables": {"personal": [
            ]}}
        self.NamePerson = ''
        self.MassageBox_ = ''
        self.flag_personal = 0
        self.flag_assessment = 0
        self.user = ''
        self.dir_line_button = {
            1: self.WorkWindow.line_search_personal,
            2: self.WorkWindow.line_analytics,
            3: self.WorkWindow.line_project,
            4: self.WorkWindow.line_structure,
            5: self.WorkWindow.line_assessment
        }

        # self.menubar = QtWidgets.QMenuBar(MW)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1274, 21))
        # self.menubar.setObjectName("menubar")
        # MW.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MW)
        # self.statusbar.setObjectName("statusbar")
        # MW.setStatusBar(self.statusbar)

        # self.GlobalstackedWidget.setCurrentIndex(0)

        # MW.setWindowFlags(MW.windowFlags()| QtCore.Qt.MSWindowsFixedSizeDialogHint)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.WorkWindow.PB_esc.clicked.connect(self.sign_out)

    def hide_line_button(self, id_button):

        self.dir_line_button[id_button].show()
        for id in self.dir_line_button:
            if id != id_button:
                self.dir_line_button[id].hide()

    def sign_out(self):
        massage = 'Выйти из аккаунта?'
        if view_massage(self, massage, 'question') == 'ok':
            client.clear_cookies()
            self.WorkWindow.reset_menu_frame()
            self.pers_inter.reset_win()
            self.struct.reset_drop_row()
            self.struct.drop_all_row()
            self.flag_one_load_struct = 0
            self.pers_assessment.reset_win()
            start_w_width = 784
            start_w_height = 545
            self.GlobalstackedWidget.setCurrentIndex(0)
            self.resize(start_w_width, start_w_height)
            self.setMaximumWidth(start_w_width)
            self.setMaximumHeight(start_w_height)
            start_w.reset_win()

    def change_log(self):
        _translate = QtCore.QCoreApplication.translate
        nickname = client.get_nick_user()
        dlg_change_login = Deploy_ChangeLogin(self)
        dlg_change_login.NameUser = nickname
        dlg_change_login.LE_name.setText(self._translate("Form", nickname))
        dlg_change_login.exec()
        massage_box = ImpMassageBox(self)
        massage_box.PB_OK_Canel.hide()
        if dlg_change_login.result == 'ok_pass':
            massage_box.Label_message.setText((_translate("Dialog", "Пароль успешно изменен")))
            massage_box.exec()
        elif dlg_change_login.result == 'ok_login':
            massage_box.Label_message.setText((_translate("Dialog", "Логин успешно изменен")))
            massage_box.exec()

    def add_worksapace(self):
        self.GlobalstackedWidget.addWidget(self.WorkWindow.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.GlobalstackedWidget.setCurrentIndex(0)

    def load_struct(self):
        print("load_struct")
        dir_table_name = {"conf_criterion": self.struct.table_conf_criterion,
                          "department": self.struct.table_department,
                          "posts": self.struct.table_posts,
                          "bonus_koeficient": self.struct.table_bonus_koeficient}

        try:
            self.struct.label_name_factory.setText(self._translate("Form", self.client.name_db))
            get_json = self.client.get_struct().content
            get_json = json.loads(get_json.decode('utf-8'))
            self.struct.data_load["tables"] = get_json["tables"].copy()
            # self.struct.data_load["tables"] = get_json["tables"].copy()
            for table_server in get_json["tables"]:

                row = 0
                table_vision = dir_table_name[table_server]
                table_vision.setRowCount(len(get_json["tables"][table_server]))
                for row_s in get_json["tables"][table_server]:
                    keys_row_s = list(row_s.keys())
                    column = 0
                    for key_row_s in keys_row_s[1:]:
                        if type(row_s[key_row_s]) == str:
                            table_vision.setItem(row, column, QtWidgets.QTableWidgetItem(row_s[key_row_s]))
                        elif type(row_s[key_row_s]) != str:
                            table_vision.setItem(row, column, QtWidgets.QTableWidgetItem(str(row_s[key_row_s])))
                        column += 1
                    row += 1
        except:
            print("load_struct  2")
            self.struct.label_error.setText(self._translate("Form", "Ошибка подключения к серверу"))
        finally:
            self.progress_bar.status_ = 'ok'

    def cont_test(self):
        a = 0
        for i in range(5):
            time.sleep(0.5)
            print(i)
        self.progress_bar.status_ = 'ok'
        return a

    def finish(self):
        print("finish")
        return None

    ###############function_button##################################################

    def set_params_start_win(self):
        if self.WorkWindow.stackedWidget.currentIndex() == 0:
            self.pers_inter.set_params_personal()
            self.pers_inter.pers_inter_user = self.user
            self.flag_personal = 1

        elif self.WorkWindow.stackedWidget.currentIndex() == 4:
            self.pers_assessment.load_combobox_assessment()
            self.flag_assessment = 1

    def personal(self):
        if self.flag_personal == 0:
            self.pers_inter.set_params_personal()
            self.flag_personal = 1
        self.hide_line_button(1)
        self.WorkWindow.stackedWidget.setCurrentIndex(0)
        print(0)

    def analytics(self):
        print("1")
        self.hide_line_button(2)
        self.WorkWindow.stackedWidget.setCurrentIndex(1)
        pass

    def projects(self):
        print("2")
        self.hide_line_button(3)
        self.WorkWindow.stackedWidget.setCurrentIndex(2)
        pass

    def assessment(self):
        if self.flag_assessment == 0:
            self.pers_assessment.load_combobox_assessment()
            self.flag_assessment = 1
            print("4")
        self.hide_line_button(5)
        self.WorkWindow.stackedWidget.setCurrentIndex(4)

    def inside_structure(self):
        self.WorkWindow.stackedWidget.setCurrentIndex(3)
        self.struct.reset_drop_row()
        if self.flag_one_load_struct == 0:
            start_process(self.progress_bar, self=self)
            self.progress_bar.status_ = 'on'
            self.flag_one_load_struct = 1
        self.hide_line_button(4)

    def refresh_inside_structure(self):
        start_process(self.progress_bar, self=self)
        self.progress_bar.status_ = 'on'
        self.flag_one_load_struct = 1
        self.struct.reset_drop_row()

    def resizeEvent(self, event):
        self.resized.emit()

    def position(self):
        self.w = self.width()
        self.h = self.height()
        self.move_ = int(self.w / 2 - self.WorkWindow.x_start)
        self.move_struct = int(self.w / 2 - self.x_start_struct)
        self.WorkWindow.groupBox.setGeometry(QtCore.QRect(self.move_ - self.center, 30, 1011, 741))
        self.struct.main_frame.setGeometry(QtCore.QRect(self.move_struct - self.center_struct, 30, 1311, 741))


class RuleForm():

    def __init__(self, ui_):
        ui_.resize(500, 500)
        ui_.setWindowFlags(ui_.windowFlags() | QtCore.Qt.MSWindowsFixedSizeDialogHint)


#################################################################################

if __name__ == "__main__":
    import sys
    print('start')
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, './GUI/icon/bee_2.ico')))
    COF.client = COF.config_connect(user='admin')
    client = COF.client
    ui = MainWindow_all_3(client)
    table_start_ = COF.Table_start_(ui)
    count_crit = COF.CountCriterion(ui, table_start_)
    start_w = COF.mywindow(ui, count_crit)
    start_w.start_win.connect(ui.set_params_start_win)
    ui.GlobalstackedWidget.addWidget(start_w)
    ui.GlobalstackedWidget.addWidget(count_crit)
    ui.GlobalstackedWidget.addWidget(table_start_)
    ui.add_worksapace()
    ui.show()
    start_w.maxres()
    # ui=PersonalAssessment(2)
    # ui.show()
    sys.exit(app.exec_())
