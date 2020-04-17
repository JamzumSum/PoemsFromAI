# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\include.ui',
# licensing of '.\include.ui' applies.
#
# Created: Sun Apr  5 22:51:11 2020
#      by: pyside2-uic  running on PySide2 5.11.4a1.dev1546291887
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets

class Ui_include(object):
    introduce='''欢迎体验AI写诗机器人！请按照说明规则来体验！
    
①输入姓名 例如：李白
②选择你喜欢的唐诗格式与写诗模式，并点击“开始”
③输入指定的开头汉字或者藏头汉字
④诗句的下面是系统对诗文做出的评价
⑤选择不满意可重新作诗
⑥选择满意可以得到我们为您精心设计的展示图

注：因为我们原有语料集的不完备，我们做出的诗句暂时不能达到大诗人的水平，希望理解，如果您遇到了喜欢的诗文语料集，欢迎提供给我们哦！
    '''
    def setupUi(self, include):
        include.setObjectName("include")
        include.resize(500, 450)
        #设置窗口属性
        include.setStyleSheet("background:ghostwhite;"
                              "font: 20px \"楷体 \";"
                              "color: darkolivegreen;")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(include.sizePolicy().hasHeightForWidth())
        include.setSizePolicy(sizePolicy)
        include.setMaximumSize(QtCore.QSize(500, 450))
        self.centralwidget = QtWidgets.QWidget(include)
        self.centralwidget.setObjectName("centralwidget")
        self.include_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.include_2.setEnabled(True)
        self.include_2.setGeometry(QtCore.QRect(50, 30, 400, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.include_2.sizePolicy().hasHeightForWidth())
        self.include_2.setSizePolicy(sizePolicy)
        self.include_2.setMinimumSize(QtCore.QSize(400, 300))
        self.include_2.setMaximumSize(QtCore.QSize(400, 300))
        self.include_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        #程序说明书显示栏
        '''background设置背景
        boder:为同时设置 border 的 width style color 属性，但值的顺序必须是按照 width style color 来写，不然不会生效！
        padding设置文字位置，可理解为x,y坐标
        border-radius设置边框圆角，可以做出圆形按钮。单位px像素，border设置边框属性
        color设置文字颜色'''
        self.include_2.setStyleSheet("background:white;"
                                    "border: 1px solid darkolivegreen;" 
                                    "border-left-width: 2px;"
                                    "border-top-width: 2px;"
                                    "border-radius:12px;"
                                    "font:19px;")
        self.include_2.setObjectName("include_2")
        self.include_2.setText(self.introduce)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 350, 80, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(100, 40))
        self.pushButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        #关闭按钮的设置
        self.pushButton.setStyleSheet("background:white;"
                                      "border: 1px solid darkolivegreen;"
                                      "border-right-width: 2px;"
                                      "border-bottom-width: 2px;"                                                                       
                                      "border-radius:12px;"
                                      "padding:2px 2px;")
        self.pushButton.setObjectName("pushButton")
        include.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(include)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 17))
        self.menubar.setObjectName("menubar")
        include.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(include)
        self.statusbar.setObjectName("statusbar")
        include.setStatusBar(self.statusbar)

        self.retranslateUi(include)
        QtCore.QMetaObject.connectSlotsByName(include)

    def retranslateUi(self, include):
        include.setWindowTitle(QtWidgets.QApplication.translate("include", "说明书", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("include", "关闭", None, -1))

