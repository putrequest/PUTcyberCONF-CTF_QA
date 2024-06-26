# Form implementation generated from reading ui file '.\CTF_QA_gui.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CTF_QA(object):
    def setupUi(self, CTF_QA):
        CTF_QA.setObjectName("CTF_QA")
        CTF_QA.resize(800, 600)
        CTF_QA.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(parent=CTF_QA)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.title = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setStyleSheet("background-color: #00000000;")
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("title")
        self.verticalLayout_3.addWidget(self.title)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scroll_area_tasks = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scroll_area_tasks.setWidgetResizable(True)
        self.scroll_area_tasks.setObjectName("scroll_area_tasks")
        self.scroll_area_tasks_widget = QtWidgets.QWidget()
        self.scroll_area_tasks_widget.setGeometry(QtCore.QRect(0, 0, 778, 498))
        self.scroll_area_tasks_widget.setObjectName("scroll_area_tasks_widget")
        self.scroll_area_tasks.setWidget(self.scroll_area_tasks_widget)
        self.verticalLayout_2.addWidget(self.scroll_area_tasks)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        CTF_QA.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=CTF_QA)
        self.statusbar.setObjectName("statusbar")
        CTF_QA.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(parent=CTF_QA)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menuBar.setObjectName("menuBar")
        self.menu_file = QtWidgets.QMenu(parent=self.menuBar)
        self.menu_file.setObjectName("menu_file")
        self.menu_appearance = QtWidgets.QMenu(parent=self.menuBar)
        self.menu_appearance.setObjectName("menu_appearance")
        CTF_QA.setMenuBar(self.menuBar)
        self.action_reset_progress = QtGui.QAction(parent=CTF_QA)
        self.action_reset_progress.setObjectName("action_reset_progress")
        self.action_appearance_light = QtGui.QAction(parent=CTF_QA)
        self.action_appearance_light.setCheckable(True)
        self.action_appearance_light.setObjectName("action_appearance_light")
        self.action_appearance_dark = QtGui.QAction(parent=CTF_QA)
        self.action_appearance_dark.setCheckable(True)
        self.action_appearance_dark.setChecked(True)
        self.action_appearance_dark.setObjectName("action_appearance_dark")
        self.menu_file.addAction(self.action_reset_progress)
        self.menu_appearance.addAction(self.action_appearance_light)
        self.menu_appearance.addAction(self.action_appearance_dark)
        self.menuBar.addAction(self.menu_file.menuAction())
        self.menuBar.addAction(self.menu_appearance.menuAction())

        self.retranslateUi(CTF_QA)
        QtCore.QMetaObject.connectSlotsByName(CTF_QA)

    def retranslateUi(self, CTF_QA):
        _translate = QtCore.QCoreApplication.translate
        CTF_QA.setWindowTitle(_translate("CTF_QA", "PUTcyberCONF"))
        self.title.setText(_translate("CTF_QA", "TextLabel"))
        self.menu_file.setTitle(_translate("CTF_QA", "Plik"))
        self.menu_appearance.setTitle(_translate("CTF_QA", "Wygląd"))
        self.action_reset_progress.setText(_translate("CTF_QA", "Zresetuj postęp"))
        self.action_appearance_light.setText(_translate("CTF_QA", "Jasny"))
        self.action_appearance_dark.setText(_translate("CTF_QA", "Ciemny"))
