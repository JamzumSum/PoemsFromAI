# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 23:02:08 2020

@author: a99gc
"""

from pro_py.two_ui import Ui_two
from PySide2.QtWidgets import *

class two(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_two()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

