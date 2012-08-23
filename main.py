#TODO:
#Add options for all GUI
#Add Project Options
#Add error markers

from PyQt4.QtGui import (QApplication,QPixmap,QSplashScreen,QMessageBox,
                         QIcon,QAction,QCheckBox,QFileDialog)
from PyQt4.QtCore import SIGNAL,Qt,QStringList,QString
import icons_rc
from window import Window
from Widget import Editor,PyInterp,Adb,Parser
from globals import (ospathsep,ospathjoin,ospathbasename,workDir,
                     OS_NAME,os_icon,config,workSpace,
                     iconSize,iconDir,ospathexists,os_pixmap) 


class MainWindow(Window):
    def __init__(self, parent = None):
        Window.__init__(self,parent)
	#Important must be empty this is a reference
        self.files = []
        self.projects = None
        self.recent = None
        self.dirty = None
        self.isFull = False
        self.adb = Adb(self)
        self.parser = Parser(self)
        self.init()

    def init(self):
        self.initConfig()
        self.initToolBar()
        self.initProjects()
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)
        self.connect(self.tabWidget,SIGNAL("dropped"), self.createTabs)
        #self.initInterpreter()

    def initConfig(self):
        self.projects = config.projects()
        self.recent = config.recent()
        self.dirty = []
        if(config.files() != None):
            for i in config.files():
                self.createTab(i)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.treeWidget.itemDoubleClicked.connect(self.ss)
        
    def initProjects(self):
        if self.projects != None:
            if len(self.projects) != 0:
                for pro in self.projects:
                    self.createProject(pro)
          
    #Important all projects must go through this          
    def createProject(self,startDir):
        if(ospathexists(startDir)): 
            self.treeWidget.addProject(startDir)
        else:
            config.removeProject(startDir)
            QMessageBox.about(self,"Can't Open Project","Project Does Not Exist %s"%startDir)

    def ss(self,item):
        if(item.isFile()):
            if(item.isDoc()):
                self.createTab(item.getPath())
            elif(item.isPic()):
                self.createTab(item.getPath())

    def initInterpreter(self):
        self.ipy = PyInterp(self)
        self.ipy.initInterpreter(locals())
        self.tabWidget_3.addTab(self.ipy, "Python")

    def createTab(self,nfile):
        if(nfile != None):
            if self.files != None:
                if len(self.files) != 0:
                    for i in self.files:
                        if(i == nfile):
                            #print "File Already Open\n"+nfile
                            self.tabWidget.setCurrentIndex(self.files.index(nfile))
                            return
            if type(nfile) == str:
                if(ospathexists(nfile)):
                    text = ""
                    try:
                        infile = open(nfile, 'r')
                        text = infile.read()
                        infile.close()
                        config.addFile(nfile) 
                        self.dirty.append(False)
                        self.files.append(nfile)
                        #print len(self.files)
                    except:
                        config.removeFile(nfile)
                        QMessageBox.about(self,"Can't Open","File Does Not Exist or Locked\n"+nfile)
                    
                    tab = Editor(self,text,self.syntax(nfile),self.colorStyle) 
                    self.tabWidget.addTab(tab,ospathbasename(nfile))
                    tab.textChanged.connect(lambda:self.setDirty(nfile)) 
                    if(self.files != None):
                        if(len(self.files)) != 0:
                            #This line sets the opened file to display first Important not checked
                            self.tabWidget.setCurrentIndex(len(self.files)-1)
                else:
                    #dont know must check this the last file is not removed executes only
                    #twice when it has to remove 3 files
                    #check sel.files 
                    #print len(config.files())
                    config.removeFile(nfile)
                    QMessageBox.about(self,"Can't Open","File Does Not Exist or Locked\n"+nfile) 
                           
    def createTabs(self,link):
        for i in link:
            self.createTab(i)
            
    def closeTab(self,index):
        '''Boolean result invocation method.'''
        done = True
        if self.dirty[index]:
            reply = QMessageBox.question(self,
                    "Sabel IDE - Unsaved Changes",
                    "Save unsaved changes?",
                    QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                done = False
            elif reply == QMessageBox.Yes:
                done = self.fileSave(index)
            elif reply == QMessageBox.No:
                self.clearDirty(index)
                done = True
        if(done):
            #print index
            config.removeFile(self.files[index])
            self.files.remove(self.files[index])
            self.tabWidget.removeTab(index)
        #return True

    def setDirty(self,file):
        '''On change of text in textEdit window, set the flag
        "dirty" to True'''
        index = self.files.index(file)
        if self.dirty[index]:
            return True
        self.dirty[index] = True
        flbase = ospathbasename(self.files[index])
        self.tabWidget.setTabText(index,"*"+flbase)

    def clearDirty(self,index):
        '''Clear the dirty.'''
        self.dirty[index] = False
        flbase = ospathbasename(self.files[index])
        self.tabWidget.setTabText(index,flbase)

    def newProject(self):
        fname = str(QFileDialog.getExistingDirectory(self,"Open Project Folder"))
        if not (fname == ""):
            fname = fname+"/"
            #print fname
            if self.projects != None:
                for nfile in self.projects:
                    if(nfile != fname):
                        self.createProject(fname)
                        config.addProject(fname)
                        return
                    else:
                        QMessageBox.about(self, "Already Open","Project Already Open\n"+fname)
                        return
            else:
                self.treeWidget.addProject(fname)
                config.addProject(fname)     
        return

    def fileOpen(self):
        fname = str(QFileDialog.getOpenFileName(self,
                        "Open File", '.', "Files (*.*)"))
        if not (fname == ""):
            if self.files != None:
                if len(self.files) != 0:
                    for file in self.files:
                        if(file != fname):
                            self.createTab(fname)
                            return
                        else:
                            QMessageBox.about(self, "Already Open","File Already Open")
                            return
                else:
                    self.createTab(fname)
            else:
                print "not"
                #this is when the files list is empty and None type
                if(self.files == None):
                    self.files = []
                self.createTab(fname)
        else:
            return

    def fileSave(self):
        if(self.files != None):
            if len(self.files) != 0:
                index = self.tabWidget.currentIndex()
                if not self.dirty[index]:
                    return
                fname = self.files[index]
                fl = open(fname, 'w')
                tempText = self.tabWidget.widget(index).text()
                if tempText:
                    fl.write(tempText)
                    fl.close()
                    self.clearDirty(index)
                    self.parser.run(self.files[index])
                else:
                    QMessageBox.about(self, "Can't Save","Failed to save ...")
                    self.statusBar().showMessage('Failed to save ...', 5000)

    def fileSaveAll(self):
        def fileSaveIndex(index):
                if not self.dirty[index]:
                    return
                fname = self.files[index]
                fl = open(fname, 'w')
                tempText = self.tabWidget.widget(index).text()
                if tempText:
                    fl.write(tempText)
                    fl.close()
                    self.clearDirty(index)
                else:
                    QMessageBox.about(self, "Can't Save","Failed to save ...")
                    self.statusBar().showMessage('Failed to save ...', 5000)
        if(self.files != None):
            if len(self.files) != 0:
                for file in self.files:
                    fileSaveIndex(self.files.index(file))


    def closeEvent(self, event):
        #check this ine adb.exe process is always on
        self.adb.close()
        self.parser.close()
        notSaved = False
        for files in self.dirty:
            if files == True:
                notSaved = True
        if notSaved:
            reply = QMessageBox.question(self,
                                             "Simple Editor - Unsaved Changes",
                                             "Save unsaved changes?",
                                             QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                    pass
            elif reply == QMessageBox.Yes:
                    self.fileSaveAll()
                    
    def syntax(self,nfile):
        lang = 0
        if nfile.endswith(".py"):
            lang = 0
        elif (nfile.endswith(".cpp") or nfile.endswith(".h") or nfile.endswith(".c")):
            lang = 1
        elif nfile.endswith(".nut"):
            lang = 2
        return lang
            
    def options(self):
        pass
        

if __name__ == "__main__":
    app = QApplication([])
    splash_pix = os_pixmap('logo')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    # Simulate something that takes time
    frame = MainWindow()
    frame.showMaximized()
    splash.finish(frame)
    app.exec_()
