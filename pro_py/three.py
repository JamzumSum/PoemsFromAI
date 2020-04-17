# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 23:05:31 2020

@author: a99gc
"""

from pro_py.three_ui import Ui_three
from PySide2.QtWidgets import *

class three(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_three()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
