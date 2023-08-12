base_background_color="background-color: rgb(74, 80, 106)"
text_error="""color: rgb(255, 129, 112);"""
style_buttonBox_ONOFF="""background-color: rgb(204, 204, 204);"""
style_TB_icon="""border:none;"""
style_asterisk_show="border-image: url(./GUI/icon/asterisk.png);"
style_asterisk_hide="border-image: url();"
style_label_text_240="color: rgb(240, 240, 240);"
style_base_ComboBox = """
QComboBox {
color: rgb(45, 45, 45);
	background-color: rgb(181, 188, 218);
font-size: 10pt;
border-radius: 5px;
}

QComboBox::drop-down {
border:none;
}

QComboBox::down-arrow
{
image: url(:/newPrefix/icon/arrow down.png);
height:12px;
weight:12px
}

QComboBox:on{
border: 3px solid rgb(50, 62, 118, 150);

}


QComboBox QAbstractItemView {
  padding: 2px;
  selection-background-color:rgb(102, 111, 147);

}
"""

style_gray_PB = """
QPushButton{
border:none;
border-radius: 5px;

background-color: #B5BCDA;
}


QPushButton:hover{
border:none;
background-color: rgb(140, 148, 180);
border-radius: 5px;
}


QPushButton:pressed{
border:none;
	background-color: rgb(102, 111, 147);
	color: rgb(255, 255, 255);
border-radius: 5px;
}
"""
style_LE_fields="""
    border:none;
    border-bottom: 1px solid rgb(16,240,207);
    padding_bottom: 7px;
    background-color: rgb(255, 255,255);
    border-radius: 5px;

"""
style_list_connect_question="""
QListWidget{
    background-color: rgb(110, 120, 158,200);
    border: none}

QListView::item:hover{
    background-color: rgb(11, 120, 158);}
"""

style_tab_question="""
QTabWidget::pane {
    border-top: 0px solid rgb(0, 0, 0);
    border-left: 0px solid rgb(0, 0, 0);
    border-right: 0px solid rgb(0, 0, 0);
    border-bottom: 0px solid rgb(0, 0, 0);}

QTabBar::tab {
    background-color: rgb(74, 80, 106);
    border: -1px solid lightgray;
    padding: 10px;
    color: rgb(230, 230, 230);}

QTabBar::tab:selected {
    background: rgb(245, 245, 245);
    border: 1px solid lightgray;
    border-bottom-color: rgb(0, 255, 127);
    color: rgb(4, 4, 4);}
"""

PB_connect_style="""
QPushButton{
    background-color: rgb(74, 80, 106);
    image: url(./GUI/icon/arrow.png);
    border:None}
    QPushButton:hover {image: url(./GUI/icon/arrow active.png);}
"""

float_menu_style="""
    background-color: rgba(255, 255, 255, 0);
"""

LE_logo_question_style="""
    border-bottom-color: rgb(102, 111, 147);background-color: rgb(102, 111, 147,0);
"""
LE_desc_question_style="""
    color: rgb(230, 230, 230);
"""
LE_name_question_style="""
    color: rgb(230, 230, 230);
    border-bottom-color: rgb(102, 111, 147);
"""

question_form_connect_style="""
.QFrame {background-color: rgb(102, 111, 147);
    border: 1.3px solid black;
    border-bottom-color: rgb(220, 220, 220);
    border-right-color: rgb(102, 111, 147);
    border-left-color: rgb(102, 111, 147);
    border-top-color: rgb(102, 111, 147);}
    
.QFrame:hover{background-color: rgb(123, 135, 177)}"
"""
question_form_connect_style_on = """
.QFrame {background-color: rgb(102, 111, 147);
    border: 1.3px solid black;
    border-bottom-color: rgb(116, 252, 152);
    border-right-color: rgb(102, 111, 147);
    border-left-color: rgb(102, 111, 147);
    border-top-color: rgb(102, 111, 147);}

.QFrame:hover{background-color: rgb(123, 135, 177)}"
"""


VL_inform_question_style = """
border:None; background-color: rgb(102, 111, 147,0);"""

PB_connect_question_style = """
QPushButton{
    background-color: rgb(132, 144, 190);
    border:None;
    border-radius: 5px;}

QPushButton:hover{
    background-color: rgb(154, 169, 222);
    border:None;
    border-radius: 5px;}

QPushButton:pressed {
     border-style: inset;
     background-color: rgb(24, 33, 69);
     color: rgb(250, 250, 250);
     }"""
PB_connect_question_style_on = """
QPushButton{
    background-color: rgb(116, 252, 152);
    border:None;
    border-radius: 5px;}

QPushButton:hover{
    background-color: rgb(154, 169, 222);
    border:None;
    border-radius: 5px;}

QPushButton:pressed {
     border-style: inset;
     background-color: rgb(24, 33, 69);
     color: rgb(250, 250, 250);
     }"""
PB_instr_question_style="""
QPushButton{
    background-color: rgb(230,230, 230);
    border:None;
    border-radius:8px;}
    
QPushButton:hover{
    background-color: rgb(250,250, 250);
    border:None;
    border-radius:8px;}
    
QPushButton:pressed {
    border-style: inset;
    background-color: rgb(210, 210, 210);
    }"""

##########StyleDialogConnectQuest#########################################

style_TB_open_json="""
        border:none;
        background-color: rgba(255, 255, 255, 0);
        border-radius: 5px;
"""

################StyleQuestionWidget###########################################
##############################################################################
LE_quest_form_style = """
QLineEdit {
        color: rgb(45, 45, 45);
        font-size: 10pt;
        background-color: rgb(140, 148, 180);
        border-top-color: rgb(151, 156, 180);
        border-right-color: rgb(151, 156, 180);
        border-left-color:  rgb(151, 156, 180);
        border-radius: 5px; }

QLineEdit:hover {
        font-size: 10pt;
        border: 2px solid black;
        border-top-color: rgb(151, 156, 180);
        border-right-color: rgb(151, 156, 180);
        border-left-color: rgb(151, 156, 180);
        border-bottom-color:  rgb(50, 62, 118);
        border-radius: 5px;} """

ComboBox_quest_style = """
QComboBox {
        color: rgb(45, 45, 45);
        font-size: 10pt;
        border-radius: 5px;}

QComboBox::drop-down {border:none;}

QComboBox::down-arrow{
        image: url(:./icon/arrow down.png);
        height:12px;
        weight:12px;}

QComboBox:on{border: 3px solid rgb(50, 62, 118, 150);}

QComboBox QAbstractItemView {
        padding: 2px;
        selection-background-color:rgb(102, 111, 147);}"""

label_short_quest_style = """
        border-top-color: rgb(151, 156, 180);
        border-right-color: rgb(151, 156, 180);
        border-left-color: rgb(151, 156, 180);"""

PB_quest_copy_style = """
QPushButton{
        border:none;
        border-radius: 5px;}

QPushButton:hover{
        border:none;
        background-color: rgb(140, 148, 180);
        border-radius: 5px;}

QPushButton:pressed{
        border:none;
        background-color: rgb(102, 111, 147);
        border-radius: 5px;}
                                                """
PB_quest_remove_style = """
QPushButton{
        border:none;
        border-radius: 5px;}

QPushButton:hover{
        border:none;
        background-color: rgb(140, 148, 180);
        border-radius: 5px;}

        QPushButton:pressed{
        border:none;
        background-color: rgb(102, 111, 147);
        border-radius: 5px;} """

CheckBox_quest_mandatory_style = """
QCheckBox {
        spacing: 5px;
        border:none;}
QCheckBox::indicator{
        width :15px;
        height : 15px;}

QCheckBox::indicator:unchecked:hover{
        width :16px;
        height : 16px;}
        
QCheckBox::indicator:unchecked {image: url(:./icon/chek_box_off.png);}

QCheckBox::indicator:checked{
        image: url(:./icon/check-box_on3.png);
        height:30px;
        weight:30px;}"""

CheckBox_first_style = """
QCheckBox {
        spacing: 5px;
        border:none;}
QCheckBox::indicator{
        width :15px;
        height : 15px;
}

QCheckBox::indicator:unchecked:hover{
        width :16px;
        height : 16px;
}
QCheckBox::indicator:unchecked {image: url(:./icon/chek_box_off.png);}

QCheckBox::indicator:checked{
        image: url(:./icon/check-box_on3.png);
        height:30px;
        weight:30px;
}"""

##########################StyleAnalytiscs############################################################
#####################################################################################################
TableAnalytics_style = """

QTableWidget{
                background:  rgb(151, 156, 180);
                outline: 0;
                border:none;
} 

QTableCornerButton::section {background-color:#8D5D6A; }

QHeaderView::section {
    background-color:#8D5D6A;
	color:rgb(220,220,220);
	border:none;
}
QTableWidget::item
{
    color:rgb(24, 33, 69);
    background: rgb(151, 156, 180);
    outline: none;
    background-repeat: no-repeat;
	border:none;
	
}

QTableWidget::item:selected
{
    color:rgb(220,220,220);
    background:#3E4150;
    outline: none;
    background-repeat: no-repeat;
    background-position: center right;
}
        
"""

ScrollBarTableAnalytics_style="""
QScrollBar:vertical
    {
        width: 12px;
		margin: 0px 1px 0px 0px;
		border: 5px transparent #2A2929;
    }


QScrollBar::handle:vertical
    {
        background-color: #C6A1AB;         /* #605F5F; */
        min-height: 5px;
        border-radius: 4px;
    }

    QScrollBar::sub-line:vertical
    {
        margin: 3px 0px 3px 0px;
        border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
        height: 10px;
        width: 5px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:vertical
    {
        margin: 3px 0px 3px 0px;
        border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
        height: 10px;
        width: 10px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;

    }

    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
    {
       
	background-color: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
    {
        
	
		
	background-color: rgb(151, 156, 180);
    }
"""

style_LE_name_chart="""
QLineEdit {
color: rgb(230, 230, 230);
font-size: 10pt;
background-color: rgb(74, 80, 106);
border: 1px solid;
border-top-color: rgb(74, 80, 106);
	border-right-color: rgb(74, 80, 106);
	border-left-color: rgb(74, 80, 106);
	border-bottom-color: rgb(181, 188, 218);

}

QLineEdit:hover {
font-size: 10pt;
border: 2px solid black;
	background-color: rgb(84, 91, 120);
	border-top-color: rgb(94, 102, 135);
	border-right-color: rgb(94, 102, 135);
	border-left-color: rgb(94, 102, 135);
	border-bottom-color: rgb(181, 188, 218);
}

"""
style_Button_float_menu = """
QPushButton{
border:none;
background-color: rgb(110, 120, 158,200);
border-radius: 5px;
}

QPushButton:hover{
border:none;
	background-color: rgba(150, 155, 179, 200);
}

QPushButton:pressed {border-style: inset;
background-color: rgb(24, 33, 69);
color: rgb(250, 250, 250);
}
"""
style_PB_BarChart = """
QPushButton{
image: url(./GUI/icon/chart line.png);
border:none;
background-color: rgb(110, 120, 158,200);
border-radius: 5px;
}

QPushButton:hover{
border:none;
	background-color: rgba(150, 155, 179, 200);
}

QPushButton:pressed {border-style: inset;
background-color: rgb(24, 33, 69);
color: rgb(250, 250, 250);
}
"""

style_PB_CircleDiagram="""
QPushButton{
image: url(./GUI/icon/circle-chart.png);
border:none;
background-color: rgb(110, 120, 158,200);
border-radius: 5px;
}

QPushButton:hover{
border:none;
	background-color: rgba(150, 155, 179, 200);
}

QPushButton:pressed {border-style: inset;
background-color: rgb(24, 33, 69);
color: rgb(250, 250, 250);
}
"""

style_PB_LineChart="""
QPushButton{
image: url(./GUI/icon/line_point_chart.png);
border:none;
background-color: rgb(110, 120, 158,200);
border-radius: 5px;
}

QPushButton:hover{
border:none;
	background-color: rgba(150, 155, 179, 200);
}

QPushButton:pressed {border-style: inset;
background-color: rgb(24, 33, 69);
color: rgb(250, 250, 250);
}
"""
style_PB_ScatterChart="""
QPushButton{

image: url(./GUI/icon/scatter_chart.png);
border:none;
background-color: rgb(110, 120, 158,200);
border-radius: 5px;
}

QPushButton:hover{
border:none;
	background-color: rgba(150, 155, 179, 200);
}

QPushButton:pressed {border-style: inset;
background-color: rgb(24, 33, 69);
color: rgb(250, 250, 250);
}
"""
style_verticalFrame_Menu="""
border:none;
background-color: rgb(110, 120, 158,200);
"""
################################################################################################################