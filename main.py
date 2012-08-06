#!/usr/bin/env python
__author__ = "pyros2097"
__license__ = "GPLv3"
__version__ = "0.3"
__copyright__ = 'Copyright 2012, pyros2097'
__credits__ = ['pyros2097', 'eclipse']
__email__ = 'pyros2097@gmail.com'

import sys
import os
import platform


from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL,Qt,QProcess,QThread,QString,QT_VERSION_STR,PYQT_VERSION_STR

from ui_simple import Ui_MainWindow
import icons_rc

from Widget import Editor
from Dialog import *
from config import Config
from styles import *
import threading
import platform


config = Config()
workSpace = config.workSpace()
fontSize = config.fontSize() 
fontName = config.fontName()
iconSize = config.iconSize()
workDir = os.getcwd()
iconDir = os.path.join(workDir,"Icons")

           
#TODO:
#Need to add options for all GUI
#Need to check filename != none in createTab
class myThread (threading.Thread):
    def __init__(self, proc, name = None, counter = None):
        self.proc = proc
        self.name = name
        self.counter = counter
        threading.Thread.__init__(self)
    def run(self):
        self.proc()
        print "Starting " + self.name
        print "Exiting " + self.name

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
      #  self.resize(800, 600) 
        #self.setWindowFlags(Qt.FramelessWindowHint)     
        self.isRunning = False
        self.isFull = False
        self.isCmd = False
        self.process = QProcess(self)
        #self.CmdThread = myThread(self.run())
        self.cmdText = ""
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)
        
        self.setWindowTitle("Sabel")
        self.setWindowIcon(self.os_icon("eclipse"))
        
        self.initConfig()
        self.initToolBar()
        self.initCommand()
        for i in self.projects:      
            self.createProjects(i)
        self.initTree()
        self.connect(self.tabWidget,SIGNAL("dropped"), self.createTab)
        #self.ipy = PyInterp(self)
        #self.ipy.initInterpreter(locals()) 
        #self.tabWidget_2.addTab(self.ipy, "Python")
        #self.initSytles()
        #print self.files.pop()
        print platform.system()
        print os.name    
        print os.path.join("C:",os.sep,"Code")
        
    def initConfig(self):
        self.tabWidget.setTabsClosable(True)
        self.files = [""]
        self.projects = config.projects()
        self.recent = config.recent()
        self.dirty = []
        self.createTab(config.files())
        self.tabWidget.setCurrentIndex(len(self.files)-1)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.tabWidget.setTabShape(1)
   
    def initCommand(self):
        self.connect(self.process, SIGNAL("readyReadStandardOutput()"), self.readOutput)
        self.connect(self.process, SIGNAL("readyReadStandardError()"), self.readErrors)
        
    def initToolBar(self):
        self.action_NewProject = QAction(self.os_icon('newprj_wiz'), 'Project', self)
        self.action_NewProject.setShortcut('Ctrl+P')
        self.action_NewProject.triggered.connect(self.openProject)
        self.action_NewProject.setToolTip("Create a New Project")
        self.action_NewProject.setStatusTip("Create a New Project")
        
        self.action_New = QAction(self.os_icon('new_untitled_text_file'), 'New', self)
        self.action_New.setShortcut('Ctrl+N')
        self.action_New.triggered.connect(self.fileNew)
        self.action_New.setToolTip("Create a New File")
        self.action_New.setStatusTip("Create a New File")
        
        self.action_Open = QAction(self.os_icon('fldr_obj'), 'Open', self)
        self.action_Open.setShortcut('Ctrl+O')
        self.action_Open.triggered.connect(self.fileOpen)
        self.action_Open.setToolTip("Open File")
        self.action_Open.setStatusTip("Open File")
        
        self.action_Save = QAction(self.os_icon('save_edit'), 'Save', self)
        self.action_Save.setShortcut('Ctrl+S')
        self.action_Save.triggered.connect(self.fileSave)
        self.action_Save.setToolTip("Save Current File")
        self.action_Save.setStatusTip("Save Current File")
        
        self.action_SaveAll = QAction(self.os_icon('saveall_edit'), 'SaveAll', self)
        self.action_SaveAll.setShortcut('Ctrl+A')
        self.action_SaveAll.triggered.connect(self.fileSaveAll)
        self.action_SaveAll.setToolTip("Save All Files")
        self.action_SaveAll.setStatusTip("Save All Files")
        self.action_Help = QAction(self.os_icon('toc_open'), 'Help', self)
        self.action_Help.triggered.connect(self.help)
        self.action_About = QAction(self.os_icon('alert_obj'), 'About', self)
        self.action_About.triggered.connect(self.about)
        self.action_Run = QAction(self.os_icon('lrun_obj'), 'Run', self)
        self.action_Run.setShortcut('Ctrl+R')
        self.action_Run.triggered.connect(self.runn)
        self.action_Stop = QAction(self.os_icon('term_sbook'), 'Stop', self)
        self.action_Stop.setShortcut('Ctrl+Q')
        self.action_Stop.triggered.connect(self.stop)
        self.action_Cmd = QAction(self.os_icon('monitor_obj'), 'Cmd', self)
        self.action_Cmd.setShortcut('Ctrl+B')
        self.action_Cmd.triggered.connect(self.cmd)
        self.action_Todo = QAction(self.os_icon('task_set'), 'Todo', self)
        self.action_Todo.setShortcut('Ctrl+T')
        self.action_Todo.triggered.connect(self.stop)
        #Only variation CHeck Later
        self.action_Options = QAction(QIcon(":/{0}.png".format("Icons"+os.path.sep+'emblem-system')), 'Options', self)
        self.action_Options.triggered.connect(self.options)
        
        self.action_Syntax = QAction(self.os_icon('task_set'), 'Syntax', self)
        men = QMenu()
        men.addAction(QAction("C",self))
        men.addAction(QAction("C++",self))
        men.addAction(QAction("C#",self))
        men.addAction(QAction("Java",self))
        men.addAction(QAction("Lua",self))
        men.addAction(QAction("Python",self))
        men.addAction(QAction("Ruby",self))
        men.addAction(QAction("Squirrel",self))
        self.action_Syntax.setMenu(men)
        self.action_Full = QAction(self.os_icon('task_set'), 'Full', self)
        self.action_Full.setShortcut('Shift+Enter')
        self.action_Full.triggered.connect(self.full)
        
        self.action_Stop.setDisabled(True)
        self.toolbar = self.addToolBar('ToolBar')
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.addAction(self.action_NewProject)
        self.toolbar.addAction(self.action_New)
        self.toolbar.addAction(self.action_Open)
        self.toolbar.addAction(self.action_Save)
        self.toolbar.addAction(self.action_SaveAll)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_Run)
        self.toolbar.addAction(self.action_Stop)
        self.toolbar.addAction(self.action_Cmd)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_Todo)
        self.toolbar.addAction(self.action_Options)
        self.toolbar.addAction(self.action_Syntax)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_Help)
        self.toolbar.addAction(self.action_About)
        self.toolbar.addAction(self.action_Full)
        
    def createProjects(self,startDir):
        self.treeWidget.addProject(startDir)
        
    def initTree(self):
        self.treeWidget.itemDoubleClicked.connect(self.ss)
        
    def ss(self,item):
        self.createTab(item.getPath())
        #print item.getPath()
        
    def initStyles(self):
        self.tabWidget.setStyleSheet(stl)
        #self.dockWidget.setStyleSheet(dtl)
        self.statusBar().setStyleSheet(statl)
        self.textEdit.setStyleSheet(scl) 
        self.toolbar.setStyleSheet(ttl)     
            
    def createTab(self,nfile):
        for i in self.files:
            if(i == nfile):
                QMessageBox.about(self,"Can't Open","File Already Open")
                return      
        if type(nfile) == str:
                config.addFile(nfile)
                self.files.append(nfile)
                self.dirty.append(False)
                try:
                    infile = open(nfile, 'r')
                    tab = Editor(fontSize,fontName)
                    tab.setObjectName("tab"+nfile)
                    self.tabWidget.addTab(tab,os.path.basename(nfile))
                    tab.setText(infile.read())
                    tab.textChanged.connect(lambda:self.setDirty(nfile)) 
                except:
                    QMessageBox.about(self,"Can't Open","File Does Not Exist")                 
        else:
            for i in nfile:
                self.createTab(i) 
                     
                     
        
    def closeTab(self,index):
        '''Boolean result invocation method.'''
        done = True
        if self.dirty[index]:
            reply = QMessageBox.question(self,
                    "IDE - Unsaved Changes",
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
        return True
        
    def setDirty(self,file):
        '''On change of text in textEdit window, set the flag
        "dirty" to True'''
        index = self.files.index(file)
        if self.dirty[index]:
            return True
        self.dirty[index] = True
        flbase = os.path.basename(self.files[index])
        self.tabWidget.setTabText(index,"*"+flbase)

    def clearDirty(self,index):
        '''Clear the dirty.'''
        self.dirty[index] = False
        flbase = os.path.basename(self.files[index])
        self.tabWidget.setTabText(index,flbase)

    def about(self):
        QMessageBox.about(self, "About IDE",
                """
                <b>IDE</b> v%s
                <p>
                All rights reserved in accordance with
                GPL v3 or later.
                <p>This application can be used for
                Squirrel and EmoFramework Projects.
                <p>Python %s - Qt %s - PyQt %s on %s
                <p>Created By: pyros2097
                """ % ( 
                __version__,platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def help(self):
        QMessageBox.about(self, "About Simple Editor","This is The Help")
        
    def newProject(self):
        pass
    
    def openProject(self):
        fname = unicode(QFileDialog.getExistingDirectory(self,"Open File"))
        if not (fname == ""):
            for file in self.projects:
                if(file != fname):
                    self.createProjects(fname)
                    config.addProject(fname)
                    return
                else:
                    QMessageBox.about(self, "Already Open","File Already Open")
                    return
        else:
            QMessageBox.about(self, "No File","No File Selected")
            return
    
    def syntax(self):
        pass

    def full(self):
        if not self.isFull:
            super(MainWindow, self).setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
            self.isFull = True
        else:
            super(MainWindow, self).setWindowFlags(Qt.Window)
            self.isFull = False
            
    def options(self):
        opt = UIOptions(self)
        opt.show()
        
        
    def fileNew(self):
        pass
        #self.createTab("untilted")
        #self.statusBar().showMessage('File menu: New selected', 5000)

    def fileOpen(self):
        '''Open file'''
        fname = unicode(QFileDialog.getOpenFileName(self,
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
            QMessageBox.about(self, "No File","No File Selected")
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
    
    def cmd(self):
        self.CmdThread.setCommand("cmd")
        self.CmdThread.setArguments("dir")
        if self.isCmd == False:
            self.isCmd = True
            self.action_Cmd.setIcon(self.os_icon('monitor_view'))
            self.action_Cmd.setDisabled(True)
            self.action_Stop.setEnabled(True)
            self.textEdit.clear()
            self.tabWidget_2.setCurrentIndex(1)
            self.CmdThread.start()
     
     
    def runn(self):
        self.CmdThread.start()
           
    def run(self):
        if self.isRunning == False:
            if self.process.isOpen():
                self.process.kill()
            self.isRunning = True
            self.action_Run.setIcon(self.os_icon('run_exc'))
            self.action_Run.setDisabled(True)
            self.action_Stop.setEnabled(True)
            self.textEdit.clear()
            self.tabWidget_2.setCurrentIndex(1)
            self.textEdit.append("Pushing main.nut\n")          
            self.process.start("adb -d push C:\\CODE\\main.nut /sdcard/")
            self.process.waitForFinished()
            self.process.kill()
            self.textEdit.append("Starting Activity\n")
            self.process.start("adb -d shell am start -a android.intent.action.MAIN -n com.emo_framework.examples/com.emo_framework.EmoActivity")
            self.process.waitForFinished()
            self.textEdit.append("Logging")
            self.process.kill()
            self.process.start("adb -d logcat -s EmoFramework")
            
    def stop(self):
        if self.isRunning == True:
            self.isRunning = False
            self.action_Stop.setDisabled(True)
            self.textEdit.append("Stopped")
            self.process.kill()
            self.process.start("adb -d shell ps | grep com.emo_framework.examples | awk '{print $2}' | xargs adb shell kill")
            self.process.waitForFinished()
            self.process.kill()
            self.tabWidget_2.setCurrentIndex(0)
            self.action_Run.setIcon(self.os_icon('lrun_obj'))
            self.action_Run.setEnabled(True)
            
    def os_icon(self,name):
        return QIcon(":/{0}.gif".format("Icons"+os.path.sep+name))
    
    def readOutput(self):
        self.textEdit.append(QString(self.process.readAllStandardOutput()))
       # self.cmdText += self.textEdit.toPlainText()
       # print self.cmdText
    def readErrors(self):
        self.textEdit.append("error: " + QString(self.process.readAllStandardError()))

if __name__ == "__main__":
    app = QApplication([])
    # Create and display the splash screen
    splash_pix = QPixmap('logo.gif')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    
    # Simulate something that takes time
    frame = MainWindow()
    frame.showMaximized()
    splash.finish(frame)
    app.exec_()


