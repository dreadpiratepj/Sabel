#!/usr/bin/env python
__author__ = "pyros2097"
__license__ = "GPLv3"
__version__ = "0.45"
__copyright__ = 'Copyright (c) 2012, pyros2097'
__credits__ = ['pyros2097', 'eclipse']
__email__ = 'pyros2097@gmail.com'

#TODO:
#Add options for all GUI
#Add Project Options
#Add error markers

from PyQt4.QtGui import (QMainWindow,QApplication,QPixmap,QSplashScreen,QMessageBox,
                         QIcon,QAction,QCheckBox,QFileDialog)
from PyQt4.QtCore import SIGNAL,Qt,QStringList,QString
                        

from ui import Ui_MainWindow
import icons_rc

from Widget import Editor,PyInterp,Adb
#from Dialog import *
from adb import Adb
from globals import (ospathsep,ospathjoin,ospathbasename,workDir,
                     OS_NAME,PY_VERSION,os_icon,config,workSpace,
                     iconSize,iconDir)




class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
	#Important must be empty this is a reference
        self.files = []
        self.projects = []
        self.recent = None
        self.dirty = None
        self.isFull = False
        self.adb = Adb(self)
        self.setWindowTitle("Sabel")
        self.setWindowIcon(os_icon("sample"))
        self.init()

    def init(self):
        self.initConfig()
        self.initToolBar()
        self.initProjects()
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)
        self.connect(self.tabWidget,SIGNAL("dropped"), self.createTab)
        #self.initInterpreter()

    def initConfig(self):
        self.projects = config.projects()
        self.recent = config.recent()
        self.dirty = []
        self.createTab(config.files())
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.treeWidget.itemDoubleClicked.connect(self.ss)
        
    def initProjects(self):
        if len(self.projects) != 0:
            for pro in self.projects:
                self.treeWidget.addProject(pro)

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
            if len(self.files) != 0:
                for i in self.files:
                    if(i == nfile):
                        QMessageBox.about(self,"Can't Open","File Already Open\n"+nfile)
                        return
            if type(nfile) == str:
                try:
                    infile = open(nfile, 'r')
                    config.addFile(nfile)
                    self.files.append(nfile)
                    self.dirty.append(False)
                    tab = Editor(self,infile.read())
                    self.tabWidget.addTab(tab,ospathbasename(nfile))
                    tab.textChanged.connect(lambda:self.setDirty(nfile))
                except:
                    QMessageBox.about(self,"Can't Open","File Does Not Exist\n"+nfile)
            else:
                for i in nfile:
                    self.createTab(i)
            #This line sets the opened file to display first Important not checked
            self.tabWidget.setCurrentIndex(len(self.files)-1)



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

        if(done):
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
        fname = str(QFileDialog.getExistingDirectory(self,"Open File"))
        if not (fname == ""):
            fname = fname+"/"
            #print fname
            for nfile in self.projects:
                if(nfile != fname):
                    self.createProjects(fname)
                    config.addProject(fname)
                    return
                else:
                    QMessageBox.about(self, "Already Open","Project Already Open\n"+fname)
                    return
        return

    def syntax(self):
        pass

    def style(self):
        pass
            
    def options(self):
        pass

    def fileOpen(self):
        '''Open file'''
        fname = str(QFileDialog.getOpenFileName(self,
                        "Open File", '.', "Files (*.*)"))
        if not (fname == ""):
            for file in self.files:
                if(file != fname):
                    self.createTab(fname)
                    self.files.append(fname)
                    return
                else:
                    QMessageBox.about(self, "Already Open","File Already Open")
                    return
        else:
            return

    def fileSave(self):
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
        for file in self.files:
            fileSaveIndex(self.files.index(file))


    def closeEvent(self, event):
        #check this ine adb.exe process is always on
        self.adb.close()
        for i in self.dirty:
            if i:
                reply = QMessageBox.question(self,
                                             "Simple Editor - Unsaved Changes",
                                             "Save unsaved changes?",
                                             QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
                if reply == QMessageBox.Cancel:
                    pass
                elif reply == QMessageBox.Yes:
                    self.fileSaveAll()
        

if __name__ == "__main__":
    app = QApplication([])
    splash_pix = QPixmap(':/Icons/logo.gif')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    #app.processEvents()
    # Simulate something that takes time
    frame = MainWindow()
    frame.showMaximized()
    splash.finish(frame)
    app.exec_()


