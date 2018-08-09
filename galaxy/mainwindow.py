#!/usr/bin/env python
import sys
import os
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTabWidget, QMainWindow, QApplication, QAction, QFileDialog, QInputDialog, QDialogButtonBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT  as NavigationToolBar
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

import numpy as np
from astroquery.skyview import SkyView
from astropy.wcs import WCS
from astropy.utils.data import download_file
from astropy.io import fits

filename = ''

class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Galaxy'
        self.left = 10
        self.top = 20
        self.width = 500
        self.height = 500
        self.path0, file0 = os.path.split(__file__)
        # Style
        
        # with open(self.path0 + '/stylesheet.css', "r") as fh:
        #    self.setStyleSheet(fh.read())
        
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = TABLE_WIDGET(self)
        self.setCentralWidget(self.table_widget)
        self.toolbar = self.addToolBar('Toolbar')   
        
        
        openFile = QAction(QIcon(self.path0 + '/icons/openfile.png'), 'File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)     
        
        self.toolbar.addAction(openFile) 
        
        self.show()
    
    def showDialog(self):
        global filename
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/Users/dannaxue')
        filename = fname[0]
        
class TABLE_WIDGET(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        global filename
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabArray = []
        for i in [1,2]:
            tab = QWidget()
            self.tabs.addTab(tab, 'Tab ' + str(i))
            self.tabArray.append(tab)
        for i, tab in enumerate(self.tabArray):
            tab.layout = QVBoxLayout()
            print(filename)
            self.plotFigure = IMAGE_PLOT(self)
            tab.layout.addWidget(self.plotFigure)
            tab.setLayout(tab.layout)
            
        # for i in [0,1]:
            # self.tab1 = QWidget()
            # self.tab2 = QWidget()
            # self.tabs.resize(500, 500)
            # self.tabs.addTab(self.tab1, "Tab 1")
            # self.tabs.addTab(self.tab2, "Tab 2")
            
            # self.tab1.layout = QVBoxLayout()
            # self.tab2.layout = QVBoxLayout()
            # self.plotFigure = IMAGE_PLOT(self)
            # self.tab1.layout.addWidget(self.plotFigure)
            # self.tab2.layout.addWidget(IMAGE_PLOT(self))
            # self.tab1.setLayout(self.tab1.layout)
            # self.tab2.setLayout(self.tab2.layout)
        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class IMAGE_PLOT(QWidget):

    
    def __init__(self, parent):
        super(QWidget,self).__init__(parent)
        global filename
        self.filename =filename
        self.figure = Figure()
        self.initUI()

    def initUI(self):
        """User interface."""
        
        # Creates a Canvas and Navigation Toolbar
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        #self.button = QPushButton('Plot')
        #self.button.clicked.connect(self.plot)
        
        # Sets up layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        # layout.addWidget(self.button)
        self.setLayout(layout)
    
    # Plots data
    def plot(self):
        self.plotFigure = PLOTTER(self)      

class PLOTTER():    
    def __init__(self, parent):
        global filename
        try:
            self.filename = filename
            self.figure = parent.figure
            self.canvas = parent.canvas
            self.initImage()
        except Exception:
            print('Error passing images, creating figure')
    
    def initImage(self):
        try:                
            # image_file = download_file(self.filename, cache=True)
            # hdulist = fits.open(image_file, memmap=False)
            print(self.filename)
            hdulist = fits.open(self.filename, memmap=False)
            header = hdulist['PRIMARY'].header
            data = hdulist['PRIMARY'].data
            # start coord middle (half height, width)
            # n = np.shape(data)
            # nx = n[0]; ny = n[1]
            hdulist.close()
            wcs = WCS(header)
            ax = self.figure.add_axes([0.1, 0.1, 0.8, 0.8], projection = wcs)
            ax.set_xlabel('RA')
            ax.set_ylabel('Dec')
            ax.imshow(data, cmap = 'gist_heat', origin = 'lower')
            ra = ax.coords[0]
            ra.set_major_formatter('hh:mm:ss')
            dec = ax.coords[1]
            dec.set_major_formatter('dd:mm:ss')
            self.canvas.draw()
            
        except Exception:
            print('Error creating plot')
            
class NavigationToolbar(NavigationToolBar):
    def __init__(self,canvas,parent):
        # Select only a few buttons
        self.iconDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons")
        self.toolitems = [
            ('Home','Go back to original limits','home','home'),
            ('Pan','Pan figure','move','pan'),
            ('Zoom','Zoom in','zoom_to_rect','zoom'),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
            # ('Plot', 'plot', 'plot', 'plot'),
        ]
        self.parent = parent
        super().__init__(canvas,parent)
        self.path0, file0 = os.path.split(__file__)
        icon = self.path0 + '/icons/plot.png'
        #self.addAction(self._icon('plot.png'), 'Plot', self.parent.plot)
        self.addAction(QIcon(icon), 'Plot', self.parent.plot)

            
def main():
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    screen_resolution = app.desktop().screenGeometry()
    width = screen_resolution.width()
    gui.setGeometry(width * 0.025, 0, width * 0.95, width * 0.45)
    sys.exit(app.exec_())
    
    
    