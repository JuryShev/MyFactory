import json
import re
from multipledispatch import dispatch
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
from .BuildModules.IntefaceDialog import BuilderDialogFields
from .BuildModules.ConfigWidget import ConfigWidget
from .qss import style_

_translate = QtCore.QCoreApplication.translate


class BuildDialogConnectQuest(BuilderDialogFields):
    def __init__(self):
        self.dialog_connect = None
        self.build_dialog()

    def create_dialog(self, geometry: tuple):
        self.dialog_connect = DialogConnectGoogle(geometry)

        self.dialog_connect.widget.setGeometry(QtCore.QRect(60, 20, 301, 161))
        self.dialog_connect.widget.setObjectName("widget")

        self.dialog_connect.VLay_dialog.setContentsMargins(0, 0, 0, 0)
        self.dialog_connect.VLay_dialog.setObjectName("VLay_dialog")

    def header(self):
        pass

    def fields_space(self):
        for conf_field in self.dialog_connect.config_fields['fields']:
            HLay_field = QtWidgets.QHBoxLayout()
            HLay_field.setObjectName(f"HLay_{conf_field['name']}")
            field, asterisk = self.dialog_connect.creat_label()
            self.set_config_fields(field, conf_field)
            self.set_config_asterisk(asterisk, self.dialog_connect.config_asterisk)
            HLay_field.addWidget(field)
            HLay_field.addWidget(asterisk)
            self.dialog_connect.VLay_dialog.addLayout(HLay_field)

    def massage(self):
        self.dialog_connect.create_massage_label()
        ConfigWidget.config_size(self.dialog_connect.label_massage,
                                 maximum_size=(self.dialog_connect.config_massage["size"]["maximum"][0],
                                               self.dialog_connect.config_massage["size"]["maximum"][1]))
        ConfigWidget.config_style({self.dialog_connect.label_massage: style_.text_error})
        ConfigWidget.set_size_policy(self.dialog_connect.label_massage,
                                     self.dialog_connect.config_massage)
        self.dialog_connect.VLay_dialog.addWidget(self.dialog_connect.label_massage)

    def buttons(self):
        self.dialog_connect.create_buttons()
        self.dialog_connect.connect_buttons()

    def set_config_fields(self, field, config):
        ConfigWidget.config_style({field: style_.style_LE_fields})
        field.setObjectName(config['name'])
        self.dialog_connect.fields_text[config["name"]] = config["id"]
        # regular_ex = QtCore.QRegExp(config['regular'])
        # input_validator = QtGui.QRegExpValidator(regular_ex, field)
        # field.setValidator(input_validator)
        field = self.set_font(field, config)
        ConfigWidget.set_size_policy(field, config)
        size = config["size"]
        ConfigWidget.config_size(field,
                                 maximum_size=(size["maximum"]),
                                 minimum_size=(size["minimum"]))
        field.setPlaceholderText(_translate("Dialog", config['placeholder']))

    def set_config_asterisk(self, asterisk, config):
        size_asterisk = config["size"]
        ConfigWidget.config_style({asterisk: style_.style_asterisk_hide})
        ConfigWidget.set_size_policy(asterisk, config)
        ConfigWidget.config_size(asterisk,
                                 maximum_size=size_asterisk["maximum"],
                                 minimum_size=size_asterisk["minimum"])

    def set_font(self, obj, config):
        font = QtGui.QFont()
        font.setFamily(config['Family'])
        font.setPointSize(config["PointSize"])
        obj.setFont(font)
        return obj

    def build_dialog(self):
        self.create_dialog((420, 239))
        self.fields_space()
        self.massage()
        self.buttons()

    @property
    def product(self):
        return self.dialog_connect


class DialogConnectGoogle(QtWidgets.QDialog):
    def __init__(self, geometry=(0, 0)):
        super(DialogConnectGoogle, self).__init__()
        self.widget = QtWidgets.QWidget(self)
        self.VLay_dialog = QtWidgets.QVBoxLayout(self.widget)
        self.HLay_field = QtWidgets.QHBoxLayout()
        self.HLay_field.setObjectName("HLay_mail")
        self.resize(geometry[0], geometry[1])
        ConfigWidget.config_style({self: style_.base_background_color})
        config_fields = "config_google_connect_fields.json"
        config_massage = "config_massage_dialog.json"
        config_asterisk = "config_asterisk.json"
        self.config_fields = ConfigWidget.load_config(config_fields)
        self.config_massage = ConfigWidget.load_config(config_massage)
        self.config_asterisk = ConfigWidget.load_config(config_asterisk)
        self.control = Control()
        self.fields_text = {}

    def creat_label(self):
        LE_field = QtWidgets.QLineEdit(self.widget)
        asterisk = self.create_asterisk()
        return LE_field, asterisk

    def create_asterisk(self):
        asterisk = QtWidgets.QLabel(self.widget)
        asterisk.setEnabled(True)
        asterisk.setText("")
        asterisk.setObjectName("Asterisk_dir_json")
        #asterisk.hide()
        return asterisk

    def create_massage_label(self):
        self.label_massage = QtWidgets.QLabel(self.widget)
        self.label_massage.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_massage.setObjectName("label_massage")

    def create_buttons(self):
        self.TB_open_json = QtWidgets.QToolButton(self)
        ConfigWidget.config_size(self.TB_open_json, (301, 121, 31, 21))
        self.TB_open_json.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.TB_open_json = ConfigWidget.set_icon(self.TB_open_json, "./GUI/icon/open_wb.png", (18, 18))
        self.TB_open_json.setObjectName("TB_open_json")

        self.buttonBox_ONOFF = QtWidgets.QDialogButtonBox(self)
        ConfigWidget.config_size(self.buttonBox_ONOFF, (130, 190, 156, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox_ONOFF.sizePolicy().hasHeightForWidth())
        self.buttonBox_ONOFF.setSizePolicy(sizePolicy)
        self.buttonBox_ONOFF.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_ONOFF.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_ONOFF.setObjectName("buttonBox_ONOFF")
        ConfigWidget.config_style({self.TB_open_json: style_.style_TB_open_json,
                                   self.buttonBox_ONOFF: style_.style_buttonBox_ONOFF})
        self.TB_open_json.raise_()
        self.buttonBox_ONOFF.raise_()

    def open_json_auth(self):
        dir_name = QFileDialog.getOpenFileName(self, "Open File", './json_data/google_form_auth/',
                                               "Json files (*.json)")
        self.VLay_dialog.itemAt(3).itemAt(0).widget().setText(_translate("hhh", f"{dir_name[0]}"))

    def get_data_field(self):
        pass

    def connect_buttons(self):
        self.buttonBox_ONOFF.accepted.connect(self.accept)
        self.buttonBox_ONOFF.rejected.connect(self.reject)
        self.TB_open_json.clicked.connect(self.open_json_auth)

    def extract_field(self):
        for field_id in range(self.VLay_dialog.count()-1):
            field = self.VLay_dialog.itemAt(field_id).itemAt(0).widget()
            yield field_id, field

    def show_message(self, error):
        self.label_massage.setText(_translate("massage", f"{error}"))

    def accept(self):
        for field_id, field in self.extract_field():
            report = self.control.control_widget(self.config_fields["fields"][field_id], field)
            asterisk = self.VLay_dialog.itemAt(field_id).itemAt(1).widget()
            if report is 'ok':
                ConfigWidget.config_style({asterisk: style_.style_asterisk_hide})
            else:
                print(report)
                self.show_message(self.config_fields["fields"][field_id][report])
                ConfigWidget.config_style({asterisk: style_.style_asterisk_show})
                return
        self.close()



class ControlLineEdit:
    def __init__(self, lineedit, config):
        self.config = config
        self.lineedit = lineedit
        pass

    def check_lineedit(self):

        def regular_check():
            if re.match(self.config["regular"], self.lineedit.text()) is None:
                return "regular error"
            else:
                return 'ok'

        def len_check():
            if len(self.lineedit.text())<self.config["minSymbol"]:
                return "length error"
            else:
                return "ok"

        check = len_check()
        if check is not 'ok':
            return check

        check = regular_check()
        if check is not 'ok':
            return check

        return check


class Control:
    def __init__(self):
        pass

    @dispatch(dict, QtWidgets.QLineEdit)
    def control_widget(self, config, widget):
        control=ControlLineEdit(lineedit=widget, config=config)
        return control.check_lineedit()

    @dispatch(dict, QtWidgets.QLabel)
    def control_widget(self, config, widget):
        print("label")
