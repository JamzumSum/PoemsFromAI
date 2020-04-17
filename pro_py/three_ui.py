# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\three.ui',
# licensing of '.\three.ui' applies.
#
# Created: Mon Apr  6 22:07:19 2020
#      by: pyside2-uic  running on PySide2 5.11.4a1.dev1546291887
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_three(object):
    def setupUi(self, three):
        three.setObjectName("three")
        three.resize(900, 450) 
        #设置窗口整体的背景颜色和字体属性（大小、字体、颜色）
        three.setStyleSheet("background:ghostwhite;"
                            "font: 20px \"楷体 \";"
                            "color: darkslategray;")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(three.sizePolicy().hasHeightForWidth())
        three.setSizePolicy(sizePolicy)
        #设置文字部分所在框的最小大小和最大大小
        three.setMinimumSize(QtCore.QSize(500, 450))
        three.setMaximumSize(QtCore.QSize(900, 450))
        three.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(three)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(875, 450))
        #把图片放进label
        self.label.setPixmap('1.jpg')
        #让图片自适应控件，避免图片尺寸不合适的问题
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        '''表单布局formkayout.setWidget(int row, ItemRole role, QWidget *widget)
        row为行，值：0（输入框始终在标签旁边）
                    1（标签有足够的空间适应，如果最小大小比可用空间大，输入框会被换到下一行）
                    2（输入框始终在标签下边）
        其后设置行row所对应的控件，如果role为LabelRole时，设置的为标签所对应的控件，
        如果role为FieldRole时，设置的为输入框所对应的控件'''
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(20)
        #左上右下的间隔
        self.gridLayout.setContentsMargins(330, 155, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.text_8 = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_8.setMaximumSize(QtCore.QSize(200, 35))
        self.text_8.setObjectName("text_8")
        self.text_8.setStyleSheet("background:transparent")
        self.gridLayout.addWidget(self.text_8, 0, 0, 1, 1)
        self.Button_5 = QtWidgets.QPushButton(self.centralwidget)
        self.Button_5.setMaximumSize(QtCore.QSize(100, 40))
        #按钮“返回第一步”的设置，设置透明背景
        '''background设置背景
        boder:为同时设置 border 的 width style color 属性，但值的顺序必须是按照 width style color 来写，不然不会生效！
        padding设置文字位置，可理解为x,y坐标
        border-radius设置边框圆角，可以做出圆形按钮。单位px像素，border设置边框属性
        color设置文字颜色'''
        self.Button_5.setStyleSheet("background:transparent;"
                                    "font: 16px ;"
                                    "color:darkolivegreen")
        self.Button_5.setObjectName("Button_5")
        self.gridLayout.addWidget(self.Button_5, 4, 0, 1, 1)
        self.Button_6 = QtWidgets.QPushButton(self.centralwidget)
        self.Button_6.setMaximumSize(QtCore.QSize(100, 40))
        #按钮“返回第二步”的设置
        self.Button_6.setStyleSheet("background:transparent;"
                                    "font: 16px ;" 
                                    "color:darkolivegreen")
        self.Button_6.setObjectName("Button_6")
        self.gridLayout.addWidget(self.Button_6, 4, 1, 1, 1)
        self.Nember_4 = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Nember_4.sizePolicy().hasHeightForWidth())
        self.Nember_4.setSizePolicy(sizePolicy)
        self.Nember_4.setMinimumSize(QtCore.QSize(440, 150))
        self.Nember_4.setMaximumSize(QtCore.QSize(500, 150))
        self.Nember_4.setObjectName("Nember_4")
        #将诗歌输出，并且设置透明背景
        self.Nember_4.setStyleSheet("background:transparent")
        self.gridLayout.addWidget(self.Nember_4, 1, 0, 1, 2)
        self.text_9 = QtWidgets.QLabel(self.centralwidget)   
        self.text_9.setObjectName("text_9")  
        #“from……”的设置，设为背景透明的文字
        self.text_9.setStyleSheet("background:transparent;"
                                  "font: 20px \"楷体 \";")
        self.gridLayout.addWidget(self.text_9, 3, 0, 1, 2)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.gridLayout)
        three.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(three)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 17))
        self.menubar.setObjectName("menubar")
        three.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(three)
        self.statusbar.setObjectName("statusbar")
        three.setStatusBar(self.statusbar)
        self.retranslateUi(three)
        QtCore.QMetaObject.connectSlotsByName(three)
    #设置初始显示的文字
    def retranslateUi(self, three):
        three.setWindowTitle(QtWidgets.QApplication.translate("three", "AI写诗机器人", None, -1))       
        self.Button_5.setText(QtWidgets.QApplication.translate("three", " 返回第一步 ", None, -1))
        self.Button_6.setText(QtWidgets.QApplication.translate("three", " 返回第二步 ", None, -1))
        self.text_9.setText(QtWidgets.QApplication.translate("three", " From AI小诗人", None, -1))

