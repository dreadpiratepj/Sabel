from PyQt4.QtGui import (QTreeWidgetItem,QTreeWidget,QMessageBox,
                         QIcon,QDrag,QMenu,QAction,QInputDialog,QCursor,QToolBar)
from PyQt4.QtCore import SIGNAL,Qt,QMimeData,QUrl,QPoint
from globals import (oslistdir,ospathisdir,ospathsep,ospathjoin,ospathexists,
                     ospathbasename,os_icon,osremove,osrename,ospathdirname,
                     recycle,ospathnormpath,oswalk)


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
    ext = [".txt",".nut",".py",".cpp",".c",".h"]
    def __init__(self,parent,name,path):
        QTreeWidgetItem.__init__(self,parent)
        self.path = ospathjoin(path,name)
        self.setText (0, name)
        self.doc = False
        self.pic = False
        #mime = QMimeData()
        #mime.setUrls([QUrl.fromLocalFile(self.path)])
        #print self.path+":"+str(mime.hasUrls())
        self.Doc(name)
        self.Pic(name)
        if not (self.doc and self.pic):
            self.setIcon(0,os_icon("file_obj"))
        
        
    def Doc(self,name):
        for e in self.ext:
            if name.endswith(e):
                self.setIcon(0,os_icon("file_obj"))
                self.doc = True
        #if(name.endswith(".txt") or name.endswith(".nut") or name.endswith(".py")):
        #    self.setIcon(0,os_icon("file_obj"))
        #    self.doc = True
            
    def Pic(self,name):
        if(name.endswith(".png") or name.endswith(".gif") or name.endswith(".jpg")):
            self.setIcon(0,os_icon("file_obj"))
            self.pic = True
        
    def getPath(self):
        return self.path
    def isProject(self):
        return False
    def isDir(self):
        return False
    def isFile(self):
        return True
    def isDoc(self):
        return self.doc
    def isPic(self):
        return self.pic
        
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
        self.setText (0, ospathbasename(ospathnormpath(startDir))) # set the text of the first 0
        self.setToolTip(0,startDir)
        self.Count += 1
        self.setExpanded(True)
        
        
    
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
            if  ospathisdir(ospathjoin(path,d)):
                if not ospathjoin(d).startswith('.'):
                    i = Dir(parent,d,path)
                    self.readFiles(i,ospathjoin(path,d))
                    
    def readMainDir(self,parent,path):
        for d in oslistdir(path):
            if  ospathisdir(ospathjoin(path,d)):
                if not ospathjoin(d).startswith('.'):
                    i = Dir(parent,d,path)
                    self.readMainFiles(i,ospathjoin(path,d))
        
    def readFiles(self,parent,path):
        for f in oslistdir(path):
            if ospathisdir(ospathjoin(path,f)):
                d = Dir(parent,f,path)
                self.readFiles(d,ospathjoin(path,f))    
            else:
                if not ospathjoin(f).startswith('.'):
                        File(parent,f,path)
                        
                        
    def readMainFiles(self,parent,path):
        for f in oslistdir(path):
            if not ospathisdir(ospathjoin(path,f)):
                if not ospathjoin(f).startswith('.'):
                        File(parent,f,path)
                
                
    def addProject(self,startDir):
        self.projects.append(startDir)
        self.closed.append(False)
        i = Project(self,startDir)
        self.addTopLevelItem(i)
        self.readDir(i,startDir)
        self.readMainFiles(i,startDir)
            
    def addClosedProject(self,startDir):
        if(ospathexists(startDir)):
            self.closed[self.projects.index(startDir)] = True
            i = Project(self,startDir,True) 
            self.addTopLevelItem(i)
        else:
            QMessageBox.about(self,"Can't Close Project","Project Does Not Exist %s"%startDir)
      
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
        action_File = QAction(os_icon('new_untitled_text_file'),'New File', self)
        action_File.triggered.connect(lambda:self.newFile(item))
        action_Open = QAction('Open', self)
        action_Open.triggered.connect(lambda:self.openProject(item))
        action_Close = QAction('Close', self)
        action_Close.triggered.connect(lambda:self.closeProject(item))
        
        action_OpenFile = QAction(os_icon('__imp_obj'),'Open', self)
        action_OpenFile.triggered.connect(lambda:self.openFile(item))
        action_RunFile = QAction(os_icon('nav_go'),'Python Run', self)
        action_RunFile.triggered.connect(lambda:self.runFile(item))
        action_CopyFile = QAction(os_icon('file_obj'),'Copy', self)
        action_CopyFile.triggered.connect(lambda:self.copyFile(item))
        action_CopyDir = QAction(os_icon('file_obj'),'Copy', self)
        action_CopyDir.triggered.connect(lambda:self.copyDir(item))
        action_PasteFile = QAction(os_icon('paste_edit'),'Paste', self)
        action_PasteFile.triggered.connect(lambda:self.pasteFile(item))
        action_PasteDir = QAction(os_icon('paste_edit'),'Paste', self)
        action_PasteDir.triggered.connect(lambda:self.pasteDir(item))
        action_RefreshProject = QAction(os_icon('refresh_tab'),'Refresh', self)
        action_RefreshProject.triggered.connect(lambda:self.refreshProject(item))
        action_RemoveProject = QAction('Remove', self)
        action_RemoveProject.triggered.connect(lambda:self.removeProject(item))
        action_RenameProject = QAction('Rename...', self)
        action_RenameProject.triggered.connect(lambda:self.renameProject(item))
        action_RenameDir = QAction('Rename...', self)
        action_RenameDir.triggered.connect(lambda:self.renameDir(item))
        action_RenameFile = QAction('Rename...', self)
        action_RenameFile.triggered.connect(lambda:self.renameFile(item))
        action_DeleteFile = QAction(os_icon('trash'),'Delete', self)
        action_DeleteFile.triggered.connect(lambda:self.deleteFile(item))
        action_DeleteDir = QAction(os_icon('trash'),'Delete', self)
        action_DeleteDir.triggered.connect(lambda:self.deleteDir(item))
        action_DeleteProject = QAction(os_icon('trash'),'Delete', self)
        action_DeleteProject.triggered.connect(lambda:self.deleteProject(item))
        if(item.isProject()):
            if not(item.isClosed()):
                menu.addAction(action_Folder)
                menu.addAction(action_File)
                menu.addSeparator()
                menu.addAction(action_RenameProject)
                menu.addAction(action_RemoveProject)
                menu.addAction(action_DeleteProject)
                menu.addSeparator()
                menu.addAction(action_RefreshProject)
                menu.addAction(action_Close)
            else:
                menu.addAction(action_Open)
        else:
            if(item.isDir()):
                menu.addAction(action_Folder)
                menu.addAction(action_File)
                menu.addSeparator()
                menu.addAction(action_CopyDir)
                menu.addAction(action_PasteDir)
                menu.addAction(action_RenameDir)
                menu.addAction(action_DeleteDir)      
            else:
                menu1 = QMenu(self)
                menu1.setTitle("Run As")
                menu1.addAction(action_RunFile)
                
                menu.addAction(action_OpenFile)
                menu.addMenu(menu1)
                menu.addSeparator()
                menu.addAction(action_CopyFile)
                menu.addAction(action_PasteFile)
                menu.addAction(action_RenameFile)
                menu.addAction(action_DeleteFile)
                
        menu.popup(QCursor.pos())
        
    def openProject(self,item):
        itempath = item.getPath()
        self.closed[self.projects.index(itempath)] = False
        self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        self.addProject(itempath)
        
    def closeProject(self,item):
        self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        self.addClosedProject(item.getPath())
    
    def refreshProject(self,item):
        #must check this
        itempath = item.getPath()
        self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        self.addProject(itempath)
        
    def refreshAllProjects(self):
        for pro in self.projects:
            ind = self.projects.index(pro)
            #self.takeTopLevelItem(ind)
            if(self.closed[ind]):
                print ind+pro
                self.addClosedProject(pro)
            else:
                print ind+pro
                self.addProject(pro)
        
    def removeProject(self,item):
        pass
    
    def newFolder(self,item):
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","Name:")
        if (ok and text != ''):
            fname = ospathdirname(item.getPath())
            try:
                print fname+'/'+text
                #osmkdir(fname+'/'+text,0755)
            except:
                QMessageBox.about(self,"Error","Could Not Create The File")
    def newFile(self,item):
        itempath = item.getPath()
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","Name:") 
        if (ok and text != ''):
            fname = ospathjoin(ospathdirname(itempath),str(text))
            try:
                nfile = open(fname,'w')
                nfile.close()
                f = File(item,ospathbasename(fname),ospathdirname(fname))
                item.addChild(f)
            except:
                QMessageBox.about(self,"Error","Could Not Create The File")
    
    def openFile(self):
        pass
                
    def runFile(self):
        pass
                
    def copyFile(self):
        pass
    
    def copyDir(self):
        pass
    
    def pasteFile(self):
        pass
    
    def pasteDir(self):
        pass
    
    def renameProject(self,item):
        itempath = item.getPath()
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","New Name:")
        if (ok and text != ''):
            newname = ospathjoin(ospathdirname(itempath))
            try:
                print itempath
                print newname
                #osrename(itempath,newname)
                #self.takeTopLevelItem(self.indexOfTopLevelItem(item))
                #self.addProject(newname)
            except:
                QMessageBox.about(self,"Error","Could Not Rename The File")
    
    def renameDir(self,item):
        itempath = item.getPath()
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","New Name:")
        if (ok and text != ''):
            newname = ospathjoin(ospathdirname(itempath),str(text))
            try:
                print newname
                osrename(itempath,newname)
                p = item.parent()
                p.removeChild(item)
                #self.refreshAllProjects()
            except:
                QMessageBox.about(self,"Error","Could Not Rename The File")
        
    def renameFile(self,item):
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","New Name:")
        itempath = item.getPath()
        if (ok and text != ''):
            newname = ospathjoin(ospathdirname(itempath),str(text))
            try:
                #print newname
                osrename(itempath,newname)
                p = item.parent()
                p.removeChild(item)
                f = File(p,ospathbasename(newname),ospathdirname(newname))
                p.addChild(f)
            except:
                QMessageBox.about(self,"Error","Could Not Rename The File")
                
    def deleteDir(self,item):
        reply = QMessageBox.question(self,
                    "Delete",
                    "Are you sure you want to Delete,This Will Send To Recycle Bin?",
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.No:
            return
        elif reply == QMessageBox.Yes:
            try:
                pass
            #implement
            except:
                QMessageBox.about(self,"Error","Could Not Delete The File")
                
    def deleteProject(self,item):
        reply = QMessageBox.question(self,
                    "Delete",
                    "Are you sure you want to Delete,This Will Send To Recycle Bin?",
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.No:
            return
        elif reply == QMessageBox.Yes:
            try:
                pass
            #implement
            except:
                QMessageBox.about(self,"Error","Could Not Delete The File")
        
    def deleteFile(self,item):
        reply = QMessageBox.question(self,
                    "Delete",
                    "Are you sure you want to Delete,This Will Send To Recycle Bin?",
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.No:
            return
        elif reply == QMessageBox.Yes:
            try:
                itempath = item.getPath()
                p = item.parent()
                p.removeChild(item)
                recycle(itempath)
            except:
                QMessageBox.about(self,"Error","Could Not Delete The File")