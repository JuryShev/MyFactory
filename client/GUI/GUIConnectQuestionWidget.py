from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from .BuildModules.InterfaceWidget import BuilderWidget
from .BuildModules.ConfigWidget import ConfigWidget
from .qss import style_
from .DialogConnectQwest import BuildDialogConnectQuest

_translate = QtCore.QCoreApplication.translate



class BuilderConnectWidget(BuilderWidget):
    """
    Конкретный Строитель виджета для подключения к сервису опросника
    """

    def __init__(self, name_module, minimum_size=(0, 0), maximum_size=(16777215, 16777215)) -> None:
        """

        :param name_module: Имя модуля для построения виджета
        :param minimum_size: минимальный размер виджета
        :param maximum_size: максимальный размер виджета
        """
        super().__init__()
        self._product = None
        self.set_minimum_size=(minimum_size[0],minimum_size[1])
        self.set_maximum_size=(maximum_size[0],maximum_size[1])
        self.name_module = name_module
        # Словарь со списком возмоных виджетов
        self.question_module = {'Google Forms': ConnectGoogleForm()}
        self.reset(name_module=name_module)


    def create_frame(self,scroll_area):
        self._product.HLay_connect.setGeometry(QtCore.QRect(260, 80, 511, 91))
        self._product.HLay_connect.setObjectName("HL_general_frame")
        self._product.HLay_connect.setMinimumSize(QtCore.QSize(self.set_minimum_size[0], self.set_minimum_size[1]))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self._product.HLay_connect)
        self.horizontalLayout.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")


    def h_lay_upper(self) -> None:
        h_lay_up=self._product.add_upper()
        self.horizontalLayout.addWidget(h_lay_up)

    def h_lay_middle(self) -> None:
        h_lay_middle = self._product.add_middle()
        self.horizontalLayout.addWidget(h_lay_middle)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

    def h_lay_lower(self) -> None:
        self._product.add_lower()
        self.horizontalLayout.addLayout(self._product.VL_connect_question)

    def reset(self, name_module) -> None:
        self._product = self.question_module[name_module]

    def set_style(self):
        self._product.set_style()
        self._product.retranslateUI()

    def set_logo(self, dir_logo):
        self._product.LE_logo_question.setPixmap(QtGui.QPixmap(dir_logo))

    def set_inform(self,name, inform):
        self._product.LE_name_question.setText(_translate("Form", name))
        self._product.LE_desc_question.setText(_translate("Form", inform))

    def connect_buttons(self):
        self._product.connect_button()

    def build_full_widget(self, scroll_area):
        self.create_frame(scroll_area)
        self.h_lay_upper()
        self.h_lay_middle()
        self.h_lay_lower()
        self.set_style()
        self.connect_buttons()

    @property
    def product(self):
        return self._product


class ConnectGoogleForm(QtWidgets.QWidget):
    """
    Имеет смысл использовать паттерн Строитель только тогда, когда ваши продукты
    достаточно сложны и требуют обширной конфигурации.

    В отличие от других порождающих паттернов, различные конкретные строители
    могут производить несвязанные продукты. Другими словами, результаты
    различных строителей могут не всегда следовать одному и тому же интерфейсу.
    """

    def __init__(self) -> None:

        super().__init__()
        self.parts = []
        self.HLay_connect = QtWidgets.QFrame(self)



    def set_style(self):
        ConfigWidget.config_style({self.HLay_connect: style_.question_form_connect_style,
                                   self.LE_logo_question: style_.PB_connect_style,
                                   self.LE_name_question: style_.LE_name_question_style,
                                   self.LE_desc_question: style_.LE_desc_question_style,
                                   self.PB_connect_question: style_.PB_connect_question_style,
                                   self.PB_instr_question: style_.PB_instr_question_style})

    def add_upper(self):
        self.LE_logo_question = QtWidgets.QLabel(self.HLay_connect)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LE_logo_question.sizePolicy().hasHeightForWidth())
        self.LE_logo_question.setSizePolicy(sizePolicy)
        self.LE_logo_question.setMaximumSize(QtCore.QSize(30, 30))
        self.LE_logo_question.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.LE_logo_question.setText("")
        self.LE_logo_question.setScaledContents(True)
        self.LE_logo_question.setObjectName("LE_logo_question")

        return self.LE_logo_question

    def add_middle(self):
        self.VL_inform_question = QtWidgets.QFrame(self.HLay_connect)
        self.VL_inform_question.setObjectName("VL_inform_question")
        self.VL_inform_question.setStyleSheet("border:None; background-color: rgb(102, 111, 147,0);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.VL_inform_question)
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.LE_name_question = QtWidgets.QLabel(self.VL_inform_question)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.LE_name_question.setFont(font)
        self.LE_name_question.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.LE_name_question.setObjectName("LE_name_question")
        self.verticalLayout_2.addWidget(self.LE_name_question)
        self.LE_desc_question = QtWidgets.QLabel(self.VL_inform_question)
        self.LE_desc_question.setStyleSheet("color: rgb(230, 230, 230);")
        self.LE_desc_question.setTextFormat(QtCore.Qt.AutoText)
        self.LE_desc_question.setScaledContents(False)
        self.LE_desc_question.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.LE_desc_question.setWordWrap(False)
        self.LE_desc_question.setObjectName("LE_desc_question")
        self.verticalLayout_2.addWidget(self.LE_desc_question)

        return self.VL_inform_question

    def add_lower(self):
        self.VL_connect_question = QtWidgets.QVBoxLayout(self.HLay_connect)
        self.VL_connect_question.setContentsMargins(-1, 20, -1, -1)
        self.VL_connect_question.setObjectName("VL_connect_question")
        self.PB_connect_question = QtWidgets.QPushButton(self.HLay_connect)
        self.PB_connect_question.setMinimumSize(QtCore.QSize(80, 18))
        self.PB_connect_question.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PB_connect_question.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.PB_connect_question.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.PB_connect_question.setObjectName("PB_connect_question")
        print(self.PB_connect_question)
        self.VL_connect_question.addWidget(self.PB_connect_question)
        self.HL_instr_question = QtWidgets.QHBoxLayout(self.HLay_connect)
        self.HL_instr_question.setObjectName("HL_instr_question")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.HL_instr_question.addItem(spacerItem1)
        self.PB_instr_question = QtWidgets.QPushButton(self.HLay_connect)
        self.PB_instr_question.setMinimumSize(QtCore.QSize(14, 0))
        self.PB_instr_question.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PB_instr_question.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./GUI/icon/question1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PB_instr_question.setIcon(icon)
        self.PB_instr_question.setObjectName("PB_instr_question")
        self.HL_instr_question.addWidget(self.PB_instr_question)
        self.VL_connect_question.addLayout(self.HL_instr_question)

    def connect_button(self):
        self.PB_connect_question.clicked.connect(self.dialog_con)

    def retranslateUI(self):
        self.PB_connect_question.setText(_translate("Form", "Подключиться"))

    def dialog_con(self):
        build_dialog = BuildDialogConnectQuest()
        dialog = build_dialog.product
        dialog.exec()



