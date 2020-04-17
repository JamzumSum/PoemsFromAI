# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow.ui',
# licensing of '.\mainwindow.ui' applies.
#
# Created: Mon Apr  6 21:45:51 2020
#      by: pyside2-uic  running on PySide2 5.11.4a1.dev1546291887
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #设置窗口大小
        MainWindow.resize(900, 450)
        #设置窗口整体的背景颜色和字体属性（大小、字体、颜色）
        MainWindow.setStyleSheet("background:ghostwhite;"
                                 "font: 20px \"楷体 \";"
                                 "color: darkolivegreen;")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        #设置选择窗口栏的最小大小和最大大小
        MainWindow.setMinimumSize(QtCore.QSize(500, 450))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 515))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(500, 450))
        #用label显示图片1.jpg
        self.label.setPixmap('1.jpg')
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        #设置左、上、右、下的间隔大小，使界面看起来顺眼
        self.formLayout.setContentsMargins(10, 30, 10, 0)
        self.formLayout.setHorizontalSpacing(5)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.Button_1 = QtWidgets.QPushButton(self.centralWidget)
        self.Button_1.setObjectName("Button_1")
        #设置说明书按钮的属性，设置背景颜色为seagreen,边框圆角并做成椭圆形的按钮    
        '''background设置背景
        boder:为同时设置 border 的 width style color 属性，但值的顺序必须是按照 width style color 来写，不然不会生效！
        padding设置文字位置，可理解为x,y坐标
        border-radius设置边框圆角，可以做出圆形按钮。单位px像素，border设置边框属性
        color设置文字颜色'''
        self.Button_1.setStyleSheet("background:seagreen;"
                                    "border: 1px solid darkolivegreen;" 
                                    #"border-right-width: 2px;"
                                    #"border-bottom-width: 2px;"
                                    "font: 14px \"Times New Roman \";"
                                    "color: white;"
                                    "border-radius:8px;"
                                    #"padding:2px 4px;"
                                    )
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Button_1)
        self.Number_1 = QtWidgets.QLineEdit(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Number_1.sizePolicy().hasHeightForWidth())
        self.Number_1.setSizePolicy(sizePolicy)
        self.Number_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.Number_1.setObjectName("Number_1")
        #姓名输入栏，设置白色背景，用加粗左上的边框来做凹陷的效果并设置圆角
        self.Number_1.setStyleSheet("background:white;"
                                    "border: 1px solid darkolivegreen;" 
                                    "border-left-width: 2px;"
                                    "border-top-width: 2px;"
                                    "border-radius:12px;" )
        '''表单布局formkayout.setWidget(int row, ItemRole role, QWidget *widget)
           row为行，值：0（输入框始终在标签旁边）
                       1（标签有足够的空间适应，如果最小大小比可用空间大，输入框会被换到下一行）
                       2（输入框始终在标签下边）
           其后设置行row所对应的控件，如果role为LabelRole时，设置的为标签所对应的控件，
           如果role为FieldRole时，设置的为输入框所对应的控件
        '''
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Number_1)
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 50))
        self.groupBox.setObjectName("groupBox")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName("formLayout_3")
        #把select_3放进groupBox中，剩下的select_6，select_7和select_5也放进去，使得这四个选项只能选其中一个
        self.select_5 = QtWidgets.QRadioButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_5.sizePolicy().hasHeightForWidth())
        self.select_5.setSizePolicy(sizePolicy)
        self.select_5.setMaximumSize(QtCore.QSize(16777215, 40))
        self.select_5.setObjectName("select_5")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.select_5)
        self.select_6 = QtWidgets.QRadioButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_6.sizePolicy().hasHeightForWidth())
        self.select_6.setSizePolicy(sizePolicy)
        self.select_6.setMaximumSize(QtCore.QSize(16777215, 50))
        self.select_6.setObjectName("select_6")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.select_6)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.groupBox)
        self.Button_2 = QtWidgets.QPushButton(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_2.sizePolicy().hasHeightForWidth())
        self.Button_2.setSizePolicy(sizePolicy)
        self.Button_2.setObjectName("Button_2")
        #开始按钮的设置，用加粗右下的边框做凸出的效果，白底绿框
        self.Button_2.setStyleSheet("background:white;"
                                    "border: 1px solid darkolivegreen;"
                                    "border-right-width: 2px;"
                                    "border-bottom-width: 2px;"                                                                       
                                    "border-radius:12px;"
                                    "padding:2px 2px;")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.Button_2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(299, 50))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_4 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_4.setObjectName("formLayout_4")
        #把select_2和select_1放进groupBox_2中，使用户在其中二选一
        self.select_2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.select_2.setObjectName("select_2")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.select_2)
        self.select_4 = QtWidgets.QRadioButton(self.groupBox_2)
        self.select_4.setObjectName("select_4")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.select_4)
        self.select_3 = QtWidgets.QRadioButton(self.groupBox_2)
        self.select_3.setObjectName("select_3")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.select_3)
        self.select_1 = QtWidgets.QRadioButton(self.groupBox_2)
        self.select_1.setObjectName("select_1")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.select_1)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.groupBox_2)
        self.horizontalLayout.addLayout(self.formLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 500, 17))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    #设置初始显示的文字，可在此处得到按钮与名称的对应关系
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "AI写诗机器人", None, -1))
        self.Button_1.setText(QtWidgets.QApplication.translate("MainWindow", " ? ", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "选择模式", None, -1))
        self.select_5.setText(QtWidgets.QApplication.translate("MainWindow", "藏头", None, -1))
        self.select_6.setText(QtWidgets.QApplication.translate("MainWindow", "一字", None, -1))
        self.Button_2.setText(QtWidgets.QApplication.translate("MainWindow", "  开始  ", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", "选择格式", None, -1))
        self.select_2.setText(QtWidgets.QApplication.translate("MainWindow", "五律", None, -1))
        self.select_4.setText(QtWidgets.QApplication.translate("MainWindow", "七律", None, -1))
        self.select_3.setText(QtWidgets.QApplication.translate("MainWindow", "七绝", None, -1))
        self.select_1.setText(QtWidgets.QApplication.translate("MainWindow", "五绝", None, -1))

