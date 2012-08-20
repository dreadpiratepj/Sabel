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