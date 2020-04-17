# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:54:43 2020

@author: a99gc
"""

from pro_py.include_ui import Ui_include
from PySide2.QtWidgets import *

class include(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_include()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

