from PyQt4.QtGui import (QTreeWidgetItem,QTreeWidget,QMessageBox,
                         QIcon,QDrag,QMenu,QAction,QInputDialog,QCursor)
from PyQt4.QtCore import SIGNAL,Qt,QMimeData
from globals import (oslistdir,ospathisdir,ospathsep,ospathjoin,ospathexists,
                     ospathbasename,os_icon,osremove,osrename,ospathdirname,
                     recycle)


class Dir(QTreeWidgetItem):
    def __init__(self,parent,name,path):
        QTreeWidgetItem.__init__(self,parent)
        self.path = ospathjoin(path,name)
        self.setText (0, name)
        self.setIcon(0,os_icon("package_obj"))
    
    def getPath(self):
        return self.path
    def isProject(self):
        return False
    def isDir(self):
        return True
    def isFile(self):
        return False

class File(QTreeWidgetItem):
    def __init__(self,parent,name,path):
        QTreeWidgetItem.__init__(self,parent)
        self.path = ospathjoin(path,name)
        self.setText (0, name)
        #mime = QMimeData()
        #print mime.hasFormat(path)
        if(name.endswith(".txt")):
            self.setIcon(0,os_icon("file_obj"))
        elif(name.endswith(".nut")):
            self.setIcon(0,os_icon("file_obj"))
        elif(name.endswith(".py")):
            self.setIcon(0,os_icon("file_obj"))
        elif(name.endswith(".c")):
            self.setIcon(0,os_icon("file_obj"))
        else:
            self.setIcon(0,os_icon("file_obj"))
    def getPath(self):
        return self.path
    def isProject(self):
        return False
    def isDir(self):
        return False
    def isFile(self):
        return True
    def isDoc(self):
        return True
        
class Project(QTreeWidgetItem):
    Count = 0
    def __init__(self,parent,startDir,closed = False):
        QTreeWidgetItem.__init__(self,parent)
        self.path = ospathjoin(startDir)
        self.closed = closed
        if(self.closed):
            self.setIcon(0,os_icon('cprj_obj'))
        else:
            self.setIcon(0,os_icon('prj_obj'))
        self.setText (0, startDir) # set the text of the first 0
        self.setToolTip(0,startDir)
        self.Count += 1
        
    
    def getPath(self):
        return self.path
    
    def isProject(self):
        return True
    def isDir(self):
        return False
    def isFile(self):
        return False
    def isClosed(self):
        return self.closed
        
class Tree(QTreeWidget):
    def __init__(self,parent = None):
        QTreeWidget.__init__(self,parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setColumnCount(1)
        self.header().close()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self,SIGNAL("customContextMenuRequested(const QPoint &)"), self.doMenu)
        self.connect(self, SIGNAL("dropped"), self.addItem)
        self.projects = []
        self.closed = []
         
    def readDir(self,parent,path):
        for d in oslistdir(path):
            if  ospathisdir(ospathjoin(path+d)) is True:
                if not ospathjoin(d).startswith('.'):
                    i = Dir(parent,d,path) # create QTreeWidget the sub i
                    self.readFiles(ospathjoin(path,d),i) 
        self.readFiles(path,parent)
                 
            
    def readFiles(self,path,i):
        for f in oslistdir(path):
            if  ospathisdir(ospathjoin(path+f)) is False:
                if not ospathjoin(f).startswith('.'):
                    File(i,f,path)
                
    def addProject(self,startDir):
        if(ospathexists(startDir)): 
            self.projects.append(startDir)
            self.closed.append(False)
            i = Project(self,startDir)
            self.addTopLevelItem(i)
            self.readDir(i,startDir)
        else:
            QMessageBox.about(self,"Can't Open Project","Project Does Not Exist %s"%startDir)
            
    def addClosedProject(self,startDir):
        if(ospathexists(startDir)):
            self.closed[self.projects.index(startDir)] = True
            i = Project(self,startDir,True) 
            self.addTopLevelItem(i)
        else:
            QMessageBox.about(self,"Can't Open Project","Project Does Not Exist %s"%startDir)
      
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
                #item = File(self)
                #item.setText(0, ospathbasename(str(url.toLocalFile())))
                #self.addTopLevelItem(item)
            self.emit(SIGNAL("dropped"), links)      
        else:
            event.ignore()    
                
    def doMenu(self, pos):
        index = self.indexAt(pos)

        if not index.isValid():
            return

        item = self.itemAt(pos)
        menu = QMenu(self)
        action_Folder = QAction(os_icon('newfolder_wiz'),'New Folder', self)
        action_Folder.triggered.connect(lambda:self.newFolder(item))
        action_addFolder = QAction(os_icon('importdir_wiz'),'Add Folder', self)
        action_addFolder.triggered.connect(lambda:self.addFolder(item))
        action_File = QAction(os_icon('new_untitled_text_file'),'New File', self)
        action_File.triggered.connect(lambda:self.newFile(item))
        action_addFile = QAction(os_icon('__imp_obj'),'Add File', self)
        action_addFile.triggered.connect(lambda:self.addFile(item))
        action_Open = QAction('Open', self)
        action_Open.triggered.connect(lambda:self.openProject(item))
        action_Close = QAction('Close', self)
        action_Close.triggered.connect(lambda:self.closeProject(item))
        action_RenameProject = QAction('Rename Project', self)
        action_RenameProject.triggered.connect(lambda:self.renameProject(item))
        action_RenameDir = QAction('Rename Dir', self)
        action_RenameDir.triggered.connect(lambda:self.renameDir(item))
        action_Rename = QAction('Rename', self)
        action_Rename.triggered.connect(lambda:self.rename(item))
        action_Delete = QAction(os_icon('trash'),'Delete', self)
        action_Delete.triggered.connect(lambda:self.delete(item))
        if(item.isProject()):
            if not(item.isClosed()):
                menu.addAction(action_Folder)
                menu.addAction(action_addFolder)
                menu.addAction(action_File)
                menu.addAction(action_addFile)
                menu.addSeparator()
                menu.addAction(action_RenameProject)
                menu.addAction(action_Delete)
                menu.addSeparator()
                menu.addAction(action_Close)
            else:
                menu.addAction(action_Open)
        else:
            if(item.isDir()):
                menu.addAction(action_Folder)
                menu.addAction(action_addFolder)
                menu.addAction(action_File)
                menu.addAction(action_addFile)
                menu.addSeparator()
                menu.addAction(action_RenameDir)
                menu.addAction(action_Delete)      
            else:
                menu.addAction(action_Rename)
                menu.addAction(action_Delete)
                
        menu.popup(QCursor.pos())
        
    def openProject(self,item):
        itempath = item.getPath()[0]
        self.closed[self.projects.index(itempath)] = False
        self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        self.addProject(itempath)
        
    def closeProject(self,item):
        self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        self.addClosedProject(item.getPath()[0])
        
        
    def newFolder(self,item):
        pass
    def addFolder(self,item):
        pass
    def newFile(self,item):
        pass
    def addFile(self,item):
        pass
    
    def renameProject(self,item):
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","New Name:")
        if (ok and text != ''):
            newname = ospathjoin(ospathdirname(item.getPath()),str(text))
            try:
                #print newname
                osrename(item.getPath(),newname)
            except:
                QMessageBox.about(self,"Could Not Rename","Could Not Rename The File")
    
    def renameDir(self,item):
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","New Name:")
        if (ok and text != ''):
            newname = ospathjoin(ospathdirname(item.getPath()),str(text))
            try:
                #print newname
                osrename(item.getPath(),newname)
            except:
                QMessageBox.about(self,"Could Not Rename","Could Not Rename The File")
        
    def rename(self,item):
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","New Name:")
        if (ok and text != ''):
            newname = ospathjoin(ospathdirname(item.getPath()),str(text))
            try:
                #print newname
                osrename(item.getPath(),newname)
            except:
                QMessageBox.about(self,"Could Not Rename","Could Not Rename The File")
        
    def delete(self,item):
        reply = QMessageBox.question(self,
                    "Delete",
                    "Are you sure you want to Delete,This Will Send To Recycle Bin?",
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.No:
            return
        elif reply == QMessageBox.Yes:
            try:
                #print item.getPath()
                recycle(item.getPath())
            except:
                QMessa