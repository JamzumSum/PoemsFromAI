# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\text.ui',
# licensing of '.\text.ui' applies.
#
# Created: Mon Mar 30 20:40:56 2020
#      by: pyside2-uic  running on PySide2 5.11.4a1.dev1546291887
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_text(object):
    def setupUi(self, textt):
        textt.setObjectName("textt")
        textt.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(textt.sizePolicy().hasHeightForWidth())
        textt.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(textt)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setContentsMargins(-1, 30, -1, -1)
        self.formLayout.setHorizontalSpacing(4)
        self.formLayout.setVerticalSpacing(40)
        self.formLayout.setObjectName("formLayout")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setObjectName("label_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_1)
        self.text_Button = QtWidgets.QPushButton(self.centralwidget)
        self.text_Button.setObjectName("text_Button")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.text_Button)
        textt.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(textt)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 17))
        self.menubar.setObjectName("menubar")
        textt.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(textt)
        self.statusbar.setObjectName("statusbar")
        textt.setStatusBar(self.statusbar)

        self.retranslateUi(textt)
        QtCore.QMetaObject.connectSlotsByName(textt)

    def retranslateUi(self, textt):
        textt.setWindowTitle(QtWidgets.QApplication.translate("textt", "MainWindow", None, -1))
        self.label_1.setText(QtWidgets.QApplication.translate("textt", "   说明 ————————————————", None, -1))
        self.text_Button.setText(QtWidgets.QApplication.translate("textt", "关闭", None, -1))

