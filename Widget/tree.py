from PyQt4.QtGui import (QTreeWidgetItem,QTreeWidget,QMessageBox,
                         QIcon,QDrag,QMenu,QAction,QInputDialog,QCursor)
from PyQt4.QtCore import SIGNAL,Qt,QMimeData
from globals import oslistdir,ospathisdir,ospathsep,ospathjoin,ospathexists,ospathbasename

class Item(QTreeWidgetItem):
    def __init__(self,parent):
        QTreeWidgetItem.__init__(self,parent)
        self.path = []
        
    def addPath(self,path):
        self.path.append(path)
    
    def getPath(self):
        return ospathjoin(self.path)
        
        
        
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
        for d in oslistdir(path):
            if  ospathisdir(ospathjoin(path+d)) is True:
                if not ospathjoin(d).startswith('.'):
                    i = Item(parent) # create QTreeWidget the sub i
                    i.setText (0, d) # set the text of the first 0
                    i.setIcon(0,self.os_icon("fldr_obj"))
                    i.addPath(path+d)
                    self.readFiles(path+d,i) 
        self.readFiles(path,parent)           
            
    def readFiles(self,path,i):
        for f in oslistdir(path):
            if  ospathisdir(ospathjoin(path+f)) is False:
                if not ospathjoin(f).startswith('.'):
                    j = Item(i)
                    j.setText (0,f)
                    j.setIcon(0,self.os_icon("alert_obj"))
                    j.addPath(path+f)
                
    def addProject(self,startDir):
        if(ospathexists(startDir)):    
            #self.treeWidget.setDragDropMode(QAbstractItemView.InternalMove)
            i = Item(self) # create QTreeWidget the sub i
            i.setText (0, startDir) # set the text of the first 0
            i.setToolTip(0,startDir)
            i.setIcon(0,self.os_icon('prj_obj'))
            i.addPath(startDir)
            self.addTopLevelItem(i)
            self.readDir(i,startDir)
            self.projects+=1
        else:
            QMessageBox.about(self,"Can't Open Project","Project Does Not Exist %s"%startDir)
        
    def removeProject(self,startDir):
        self.clear()
     
        
    def os_icon(self,name):
        return QIcon(":/{0}.gif".format("Icons"+ospathsep+name))
    
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
                item.setText(0, ospathbasename(str(url.toLocalFile())))
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
        action_Folder = QAction(self.os_icon('newfolder_wiz'),'New Folder', self)
        action_Folder.triggered.connect(lambda:self.newFolder(item))
        action_addFolder = QAction(self.os_icon('importdir_wiz'),'Add Folder', self)
        action_addFolder.triggered.connect(lambda:self.addFolder(item))
        action_File = QAction(self.os_icon('new_untitled_text_file'),'New File', self)
        action_File.triggered.connect(lambda:self.newFile(item))
        action_addFile = QAction(self.os_icon('impc_obj'),'Add File', self)
        action_addFile.triggered.connect(lambda:self.addFile(item))
        action_Rename = QAction('Rename', self)
        action_Rename.triggered.connect(lambda:self.rename(item))
        action_Delete = QAction(self.os_icon('trash'),'Delete', self)
        action_Delete.triggered.connect(lambda:self.delete(item))
        menu.addAction(action_Folder)
        menu.addAction(action_addFolder)
        menu.addAction(action_File)
        menu.addAction(action_addFile)
        menu.addSeparator()
        menu.addAction(action_Rename)
        menu.addAction(action_Delete)
        menu.popup(QCursor.pos())
        
    def closeProject(self,item):
        print item.parent()
        
        
    def newFolder(self,item):
        pass
    def addFolder(self,item):
        pass
    def newFile(self,item):
        pass
    def addFile(self,item):
        pass
    
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
           