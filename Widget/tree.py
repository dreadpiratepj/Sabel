import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *
from Dialog import *

class Item(QTreeWidgetItem):
    def __init__(self,parent):
        QTreeWidgetItem.__init__(self,parent)
        self.path = []
        
    def addPath(self,path):
        self.path.append(path)
    
    def getPath(self):
        return os.path.join(self.path)
        
        
        
class Tree(QTreeWidget):
    def __init__(self,parent = None):
        QTreeWidget.__init__(self,parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setColumnCount(1)
        self.projects = 0
        self.header().close()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self,SIGNAL("customContextMenuRequested(const QPoint &)"), self.doMenu)
        self.connect(self, SIGNAL("dropped"), self.addItem)
         
    def readDir(self,parent,path):
        for d in os.listdir(path):
            if  os.path.isdir(os.path.join(path+d)) is True:
                if not os.path.join(d).startswith('.'):
                    i = Item(parent) # create QTreeWidget the sub i
                    i.setText (0, d) # set the text of the first 0
                    i.setIcon(0,self.os_icon("alert_obj"))
                    i.addPath(path+d)
                    self.readFiles(path+d,i) 
        self.readFiles(path,parent)           
            
    def readFiles(self,path,i):
        for f in os.listdir(path):
            if  os.path.isdir(os.path.join(path+f)) is False:
                if not os.path.join(f).startswith('.'):
                    j = Item(i)
                    j.setText (0,f)
                    j.setIcon(0,self.os_icon("alert_obj"))
                    j.addPath(path+f)
                
    def addProject(self,startDir):
        if(os.path.exists(startDir)):    
            #self.treeWidget.setDragDropMode(QAbstractItemView.InternalMove)
            i = Item(self) # create QTreeWidget the sub i
            i.setText (0, startDir) # set the text of the first 0
            i.setToolTip(0,startDir)
            i.setIcon(0,self.os_icon('alert_obj'))
            i.addPath(startDir)
            self.addTopLevelItem(i)
            self.readDir(i,startDir)
            self.projects+=1
        else:
            QMessageBox.about(self,"Can't Open Project","Project Does Not Exist %s"%startDir)
        
    def removeProject(self,startDir):
        self.clear()
     
        
    def os_icon(self,name):
        return QIcon(":/{0}.gif".format("Icons"+os.path.sep+name))
    
    def addItem(self,links):
        print links
                
    def startDrag(self, dropAction):
        # create mime data object
        mime = QMimeData()
        mime.setData('text/xml', '???')
        # start drag 
        drag = QDrag(self)
        drag.setMimeData(mime)        
        drag.start(Qt.CopyAction | Qt.CopyAction)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()    

    def dropEvent(self, event): 
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
                item = Item(self)
                item.setText(0, os.path.basename(str(url.toLocalFile())))
                self.addTopLevelItem(item)
            self.emit(SIGNAL("dropped"), links)      
        else:
            event.ignore()    
                
    def doMenu(self, pos):
        index = self.indexAt(pos)

        if not index.isValid():
            return

        item = self.itemAt(pos)
        #name = item.getPath()

        menu = QMenu(self)
        action_Rename = QAction('Rename', self)
        action_Rename.triggered.connect(lambda:self.rename(item))
        action_Delete = QAction('Delete', self)
        action_Delete.triggered.connect(lambda:self.delete(item))
        menu.addAction(action_Rename)
        menu.addAction(action_Delete)
        menu.popup(QCursor.pos())
        
    def closeProject(self,item):
        print item.parent()
        
    def rename(self,item):
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","New Name:")
        if (ok and text != ''):
            print text
        
    def delete(self,item):
        reply = QMessageBox.question(self,
                    "Delete",
                    "Are you sure you want to Delete,You Can never get this file Back?",
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.No:
            return
        elif reply == QMessageBox.Yes:
            try:
                #os.remove(name)
                print item.getPath()
            except:
                QMessageBox.about(self,"Could Not Delete","Could Not Delete The File")
           