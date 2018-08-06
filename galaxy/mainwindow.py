#!/usr/bin/env python
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QInputDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon

class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Sofia'
        self.left = 10
        self.top = 20
        self.width = 500
        self.height = 500
        self.path0, file0 = os.path.split(__file__)
        
        # Style
        
        with open(self.path0 + '/stylesheet.css', "r") as fh:
            self.setStyleSheet(fh.read())
        
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
        
def main():
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    screen_resolution = app.desktop().screenGeometry()
    width = screen_resolution.width()
    gui.setGeometry(width * 0.025, 0, width * 0.95, width * 0.45)
    sys.exit(app.exec_())