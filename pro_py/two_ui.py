# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\two.ui',
# licensing of '.\two.ui' applies.
#
# Created: Mon Apr  6 21:27:06 2020
#      by: pyside2-uic  running on PySide2 5.11.4a1.dev1546291887
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_two(object):
    def setupUi(self, two):
        two.setObjectName("two")
        two.resize(900, 450)
        #设置窗口整体的背景颜色和字体属性（大小、字体、颜色）
        two.setStyleSheet("background:ghostwhite;"
                          "font: 20px \"楷体 \";"
                          "color: darkolivegreen;")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        #设置水平的间隔和竖直方向的间隔
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(two.sizePolicy().hasHeightForWidth())
        two.setSizePolicy(sizePolicy)
        #设置输入和输出框合成的整体的最小大小和最大大小
        two.setMinimumSize(QtCore.QSize(500, 450))
        two.setMaximumSize(QtCore.QSize(918, 505))
        self.centralwidget = QtWidgets.QWidget(two)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(400, 450))
        #在label中放入准备好的图片
        self.label.setObjectName("label")
        self.label.setPixmap('1.jpg')
        self.horizontalLayout_3.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        #左，上，右，下的间隔设置
        self.gridLayout.setContentsMargins(10, 50, 10, -1)
        #横向间隔
        self.gridLayout.setHorizontalSpacing(0)
        #竖向间隔
        self.gridLayout.setVerticalSpacing(30)
        self.gridLayout.setObjectName("gridLayout")
        self.Number_5 = QtWidgets.QTextBrowser(self.centralwidget)
        self.Number_5.setMaximumSize(QtCore.QSize(400, 35))
        #评语栏设置为透明背景，更改字体大小
        self.Number_5.setStyleSheet("background:transparent;"
                                    "font: 18px;")
        self.Number_5.setObjectName("Number_5")
        #设置Number_5的所在位置（7号），以及占位大小等
        self.gridLayout.addWidget(self.Number_5, 7, 0, 1, 5)
        self.Number_3 = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Number_3.sizePolicy().hasHeightForWidth())
        self.Number_3.setSizePolicy(sizePolicy)
        self.Number_3.setMinimumSize(QtCore.QSize(340, 80))
        self.Number_3.setMaximumSize(QtCore.QSize(340, 200))
        #诗歌输出栏的设置
        self.Number_3.setStyleSheet("background:white;"
                                    "border: 1px solid darkolivegreen;" )
        self.Number_3.setObjectName("Number_3")
        self.gridLayout.addWidget(self.Number_3, 5, 0, 2, 4)
        self.Number_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.Number_2.setMinimumSize(QtCore.QSize(200, 0))
        self.Number_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.Number_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        #开头字输入栏，设置左上的边框做出凹陷的效果
        '''background设置背景
        boder:为同时设置 border 的 width style color 属性，但值的顺序必须是按照 width style color 来写，不然不会生效！
        padding设置文字位置，可理解为x,y坐标
        border-radius设置边框圆角，可以做出圆形按钮。单位px像素，border设置边框属性
        color设置文字颜色'''
        self.Number_2.setStyleSheet("background:white;"
                                    "border: 1px solid darkolivegreen;" 
                                    "border-left-width: 2px;"
                                    "border-top-width: 2px;"
                                    "border-radius:12px;" )
        self.Number_2.setObjectName("Number_2")
        self.gridLayout.addWidget(self.Number_2, 0, 1, 1, 1)
        self.text_3 = QtWidgets.QLabel(self.centralwidget)
        #“请输入开头字”的文字属性设置
        self.text_3.setStyleSheet("font: 20px ;" )
        self.text_3.setObjectName("text_3")
        #设置坐标和大小
        self.gridLayout.addWidget(self.text_3, 0, 0, 1, 1)
        self.Button_4 = QtWidgets.QPushButton(self.centralwidget)
        self.Button_4.setMaximumSize(QtCore.QSize(60, 30))
        #满意按钮的设置，padding设置文字在按钮中的位置
        self.Button_4.setStyleSheet("background:white;"
                                    "border: 1px solid darkolivegreen;"
                                    "border-right-width: 2px;"
                                    "border-bottom-width: 2px;"  
                                    "font: 16px ;"                                                                     
                                    "border-radius:12px;"
                                    "padding:2px 2px;")
        self.Button_4.setObjectName("Button_4")
        self.gridLayout.addWidget(self.Button_4, 6, 4, 1, 1)
        self.Button_3 = QtWidgets.QPushButton(self.centralwidget)
        self.Button_3.setMaximumSize(QtCore.QSize(60, 30))
        #不满意按钮的设置，与上方的满意按钮相同
        self.Button_3.setStyleSheet("background:white;"
                                    "border: 1px solid darkolivegreen;"
                                    "border-right-width: 2px;"
                                    "border-bottom-width: 2px;" 
                                    "font: 16px ;"                                                                      
                                    "border-radius:12px;"
                                    "padding:2px 2px;")
        self.Button_3.setObjectName("Button_3")
        self.gridLayout.addWidget(self.Button_3, 5, 4, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout)
        two.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(two)
        #setGeometry():第一二个为坐标，后两个为窗口大小
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 17))
        self.menubar.setObjectName("menubar")
        two.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(two)
        self.statusbar.setObjectName("statusbar")
        two.setStatusBar(self.statusbar)
        self.retranslateUi(two)
        QtCore.QMetaObject.connectSlotsByName(two)
    #设置初始显示的文字
    def retranslateUi(self, two):
        two.setWindowTitle(QtWidgets.QApplication.translate("two", "AI写诗机器人", None, -1))
        self.text_3.setText(QtWidgets.QApplication.translate("two", "请输入开头文字：", None, -1))
        self.Button_4.setText(QtWidgets.QApplication.translate("two", "满意", None, -1))
        self.Button_3.setText(QtWidgets.QApplication.translate("two", "不满意", None, -1))

