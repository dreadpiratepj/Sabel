from PyQt4.QtGui import (QTabWidget, QMenu, QDrag, QApplication,
                                QTabBar, QShortcut, QKeySequence, QWidget,
                                QHBoxLayout)
from PyQt4.QtCore import SIGNAL, Qt, QPoint, QMimeData, QByteArray

from PyQt4 import QtGui
from PyQt4 import QtCore

import os
import os.path as osp

class MyTabBar(QTabBar):
    """Tabs base class with drag and drop support"""
    def __init__(self,parent):
        QTabBar.__init__(self,parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore() 
                    
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()

class Tab(QTabWidget):
    def __init__(self,parent):
        QTabWidget.__init__(self,parent)
        self.setTabBar(MyTabBar(self))
        self.setAcceptDrops(True)
        self.connect(self.tabBar(), SIGNAL("dropped"), self.addItem)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore() 
                    
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()
       
    def addItem(self,l):
        self.emit(SIGNAL("dropped"),l)
        
        
class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        self.centralwidget=QtGui.QWidget(self)
        self.tabMain = Tab(self.centralwidget)
        self.tabOne = QtGui.QWidget()
        self.tabOne.edit = QtGui.QLineEdit(self.tabOne)
        self.tabOne.edit.setText(QtCore.PYQT_VERSION_STR) #Qt Version
        self.tabOneLayout = QtGui.QVBoxLayout(self.tabOne)
        self.tabOneLayout.addWidget(self.tabOne.edit)
        self.tabMain.addTab(self.tabOne, "First Tab")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.addWidget(self.tabMain)
        self.setCentralWidget(self.centralwidget)
        self.connect(self.tabMain, SIGNAL("dropped"), self.addg)
        
    def addg(self,l):
        print l
        
        
    

if __name__ == '__main__':
    app = QtGui.QApplication([])
    frame = MyWindow()
    frame.show()
    app.exec_()

    

        
