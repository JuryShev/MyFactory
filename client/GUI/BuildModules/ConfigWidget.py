from PyQt5 import QtWidgets, QtCore, QtGui
import json
config_path="./json_data/config_widget/"


class ConfigWidget:
    @staticmethod
    def config_size(obj, geometry=(0, 0, 0, 0), maximum_size=(16777215, 16777215), minimum_size=(0, 0)):
        obj.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))
        obj.setMinimumSize(QtCore.QSize(minimum_size[0], minimum_size[1]))
        obj.setMaximumSize(QtCore.QSize(maximum_size[0], maximum_size[1]))
        return obj

    @staticmethod
    def config_style(kstyles_obj:dict):
        for obj in kstyles_obj:
            obj.setStyleSheet(kstyles_obj[obj])

    @staticmethod
    def set_icon(obj, dir_icon: str, icon_size: tuple):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(dir_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        obj.setIcon(icon)
        obj.setIconSize(QtCore.QSize(icon_size[0], icon_size[1]))
        return obj

    @staticmethod
    def set_size_policy( obj, config):

        size_policy={
            "Fixed": QtWidgets.QSizePolicy.Fixed,
            "Minimum": QtWidgets.QSizePolicy.Minimum,
            "Maximum": QtWidgets.QSizePolicy.Maximum,
            "Preferred": QtWidgets.QSizePolicy.Preferred
        }
        if "sizePolicy" in config:
            sizePolicy = QtWidgets.QSizePolicy(size_policy[config["sizePolicy"][0]],
                                               size_policy[config["sizePolicy"][1]])
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(obj.sizePolicy().hasHeightForWidth())
            obj.setSizePolicy(sizePolicy)

    @staticmethod
    def load_config(name):
        with open(config_path+name, encoding='utf-8') as json_file:
            config = json.load(json_file)
        return config





