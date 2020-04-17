# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 21:08:05 2020

@author: a99gc
"""
from pro_py.mainwindow_ui import Ui_MainWindow
from PySide2.QtWidgets import *
from PySide2  import QtCore
from pro_py.three import three

class mainwindow(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
'''        self.ui.Number_1.editingFinished.connect(self.w_1)
        
    def w_1(self):
        name={}
        ui_3=three()
        name=self.ui.Number_1.text()
        ui_3.ui.text_8.setText("for "+name)
        return  name
'''    