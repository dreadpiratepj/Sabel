#!/usr/bin/env python
__author__ = "pyros2097"
__license__ = "GPLv3"
__version__ = "0.43"
__copyright__ = 'Copyright (c) 2012, pyros2097'
__credits__ = ['pyros2097', 'eclipse']
__email__ = 'pyros2097@gmail.com'

#TODO:
#Add options for all GUI
#Add Project Options
#Add error markers

from PyQt4.QtGui import (QMainWindow,QApplication,QPixmap,QSplashScreen,
                         QIcon,QAction,QMenu,QMessageBox,QWidgetAction,
                         QCheckBox,QFileDialog,QToolButton,QPushButton)
from PyQt4.QtCore import (SIGNAL,Qt,QStringList,QString,
                          QT_VERSION_STR,PYQT_VERSION_STR,QSize)

from ui import Ui_MainWindow
import icons_rc

from Widget import Editor,PyInterp,Adb
#from Dialog import *
from config import Config
from adb import Adb
from globals import (ospathsep,ospathjoin,ospathbasename,workDir,
                     OS_NAME,PY_VERSION,os_icon,config,workSpace,fontSize,fontName,
                     iconSize,iconDir,adb)




class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
	#Important must be empty
        self.files = []
        self.projects = []
        self.recent = None
        self.dirty = None
        self.isFull = False
        self.aaa = Adb(self)
        self.setWindowTitle("Sabel")
        self.setWindowIcon(os_icon("sample"))
        self.init()

    def init(self):
        self.initConfig()
        self.initToolBar()
        self.initTree()
        self.initProjects()
        #self.initStyles()
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)
        self.connect(self.tabWidget,SIGNAL("dropped"), self.createTab)
        #self.initInterpreter()

    def initConfig(self):
        self.tabWidget.setTabsClosable(True)
        self.projects = config.projects()
        self.recent = config.recent()
        self.dirty = []
        self.createTab(config.files())
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.tabWidget.setTabShape(1)

    def initTree(self):
        self.treeWidget.itemDoubleClicked.connect(self.ss)

    def initProjects(self):
        if len(self.projects) != 0:
            for i in self.projects:
                self.createProjects(i)


    def createProjects(self,startDir):
        self.treeWidget.addProject(startDir)

    def ss(self,item):
        if(item.isFile()):
            self.createTab(item.getPath())

    def initStyles(self):
        self.tabWidget.setStyleSheet(stl)
        #self.statusBar().setStyleSheet(statl)
        #self.textEdit.setStyleSheet(scl)
        #self.toolbar.setStyleSheet(ttl)

    def initInterpreter(self):
        self.ipy = PyInterp(self)
        self.ipy.initInterpreter(locals())
        self.tabWidget_3.addTab(self.ipy, "Python")


    def initToolBar(self):
        self.action_NewProject = QAction(os_icon('newprj_wiz'), 'Project', self)
        self.action_NewProject.setShortcut('Ctrl+P')
        self.action_NewProject.triggered.connect(self.newProject)
        self.action_NewProject.setToolTip("Create a New Project")
        self.action_NewProject.setStatusTip("Create a New Project")

        self.action_Open = QAction(os_icon('__imp_obj'), 'Open', self)
        self.action_Open.setShortcut('Ctrl+O')
        self.action_Open.triggered.connect(self.fileOpen)
        self.action_Open.setToolTip("Open File")
        self.action_Open.setStatusTip("Open File")

        self.action_Save = QAction(os_icon('save_edit'), 'Save', self)
        self.action_Save.setShortcut('Ctrl+S')
        self.action_Save.triggered.connect(self.fileSave)
        self.action_Save.setToolTip("Save Current File")
        self.action_Save.setStatusTip("Save Current File")

        self.action_SaveAll = QAction(os_icon('saveall_edit'), 'SaveAll', self)
        self.action_SaveAll.setShortcut('Ctrl+A')
        self.action_SaveAll.triggered.connect(self.fileSaveAll)
        self.action_SaveAll.setToolTip("Save All Files")
        self.action_SaveAll.setStatusTip("Save All Files")
        self.action_Help = QAction(os_icon('toc_open'), 'Help', self)
        self.action_Help.triggered.connect(self.help)
        self.action_About = QAction(os_icon('alert_obj'), 'About', self)
        self.action_About.triggered.connect(self.about)
        self.action_Run = QAction(os_icon('lrun_obj'), 'Run', self)
        self.action_Run.setShortcut('Ctrl+R')
        self.action_Run.triggered.connect(self.aaa.run)
        self.action_RunFile = QAction(os_icon('start_ccs_task'), 'File', self)
        self.action_Stop = QAction(os_icon('term_sbook'), 'Stop', self)
        self.action_Stop.setShortcut('Ctrl+Q')
        self.action_Stop.triggered.connect(self.aaa.stop)
        self.action_Design = QAction(os_icon('task_set'), 'Design', self)
        #self.action_Design.triggered.connect(self.stop)
        self.action_Todo = QAction(os_icon('task_set'), 'Todo', self)
        #self.action_Todo.triggered.connect(self.stop)
        #Only variation CHeck Later
        self.action_Options = QAction(QIcon(":/{0}.png".format("Icons"+ospathsep+'emblem-system')), 'Options', self)
        self.action_Options.triggered.connect(self.options)
        self.action_Full = QAction(os_icon('task_set'), 'Full', self)
        self.action_Full.setShortcut('Shift+Enter')
        self.action_Full.triggered.connect(self.full)

        self.action_Syntax = QAction(os_icon('task_set'), 'Syntax', self)
        men = QMenu()#public_co.gif
        #chkBox =QCheckBox(men)
        #chkBox.setText("MyCheckBox")
        chkBoxAction=QWidgetAction(men)
        #chkBoxAction.setDefaultWidget(QPixmap(":/Icons/public_co"))
        men.addAction(chkBoxAction)

        men.addAction(QAction("C",self))
        men.addAction(QAction("C++",self))
        men.addAction(QAction("C#",self))
        men.addAction(QAction("Java",self))
        men.addAction(QAction("Lua",self))
        men.addAction(QAction("Python",self))
        men.addAction(QAction("Ruby",self))
        men.addAction(QAction("Squirrel",self))
        self.action_Syntax.setMenu(men)



        self.action_Style = QAction(os_icon('welcome16'), 'Style', self)
        self.action_Style.triggered.connect(self.style)
        men1 = QMenu()
        men1.addAction(QAction("All Hallow's Eve",self))
        men1.addAction(QAction("Amy",self))
        men1.addAction(QAction("Aptana Studio",self))
        men1.addAction(QAction("Bespin",self))
        men1.addAction(QAction("Blackboard",self))
        men1.addAction(QAction("Choco",self))
        men1.addAction(QAction("Cobalt",self))
        men1.addAction(QAction("Dawn",self))
        men1.addAction(QAction("Eclipse",self))
        men1.addAction(QAction("IDLE",self))
        men1.addAction(QAction("Mac Classic",self))
        men1.addAction(QAction("Monokai",self))
        men1.addAction(QAction("Monokai Dark",self))
        men1.addAction(QAction("Pastels on Dark",self))
        men1.addAction(QAction("Sunburst",self))
        men1.addAction(QAction("Twilight",self))
        self.action_Style.setMenu(men1)



        self.action_Stop.setDisabled(True)
        self.toolbar = self.addToolBar('ToolBar')
        self.toolbar.setIconSize(QSize(16,16))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.setAllowedAreas(Qt.AllToolBarAreas)

        self.toolbar.addAction(self.action_NewProject)
        self.toolbar.addAction(self.action_Open)
        self.toolbar.addAction(self.action_Save)
        self.toolbar.addAction(self.action_SaveAll)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_Run)
        self.toolbar.addAction(self.action_RunFile)
        self.toolbar.addAction(self.action_Stop)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_Design)
        self.toolbar.addAction(self.action_Todo)
        self.toolbar.addAction(self.action_Options)
        self.toolbar.addAction(self.action_Syntax)
        self.toolbar.addAction(self.action_Style)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_Help)
        self.toolbar.addAction(self.action_About)
        self.toolbar.addAction(self.action_Full)

    def createTab(self,nfile):
        if(nfile != None):
            if len(self.files) != 0:
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
                    self.tabWidget.addTab(tab,ospathbasename(nfile))
                    tab.setText(infile.read())
                    tab.textChanged.connect(lambda:self.setDirty(nfile))
                except:
                    QMessageBox.about(self,"Can't Open","File Does Not Exist")
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

    def about(self):
        QMessageBox.about(self, "About Sabel IDE",
                """
                <b>Sabel</b> v%s
                <p>
                All rights reserved in accordance with
                GPL v3 or later.
                <p>This application can be used for Squirrel and EmoFramework Projects.
                <p>Squirrel Shell (c) 2006-2011, Constantin Makshin
                <p>Squirrel (c) Alberto Demichelis
                <p>zlib (c) Jean-loup Gailly and Mark Adler
                <p>Icons (c) Eclipse EPL
                <p>Python %s - Qt %s - PyQt %s on %s
                <p>Copyright (c) 2011 emo-framework project
                <p>Created By: pyros2097
                <p>THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
                 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,INCLUDING, BUT NOT
                 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
                 FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
                 EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
                 FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
                 OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
                 PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
                 OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
                 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
                 OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
                 OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
                 POSSIBILITY OF SUCH DAMAGE.
                """ % (
                __version__,PY_VERSION,
                QT_VERSION_STR, PYQT_VERSION_STR,OS_NAME))

    def help(self):
        QMessageBox.about(self, "About Simple Editor","This is The Help")

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
                    QMessageBox.about(self, "Already Open","Project Already Open")
                    return
        return

    def syntax(self):
        pass

    def style(self):
        pass

    def full(self):
        if not self.isFull:
            self.setWindowState(Qt.WindowFullScreen)
            self.isFull = True
        else:
            self.setWindowState(Qt.WindowMaximized)
            self.isFull = False
            
    def cmd(self):
        if(self.tabWidget_3.isHidden()):
            self.tabWidget_3.show()
        else:
            self.tabWidget_3.hide()

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
        self.aaa.close()
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
    
    def findCurrentText(self):
        #print self.caseSensitive.isChecked()
        #print self.wholeWord.isChecked()
        #print self.regex.isChecked()
        #print self.backward.isChecked()
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        edt.findText(self.lineEdit.text(),self.regex.isChecked(),self.caseSensitive.isChecked(),self.wholeWord.isChecked(),self.backward.isChecked())
        
    def replaceCurrentText(self):
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        done = edt.findText(self.lineEdit.text(),self.regex.isChecked(),self.caseSensitive.isChecked(),self.wholeWord.isChecked(),self.backward.isChecked())
        if(done):
            edt.replaceText(self.lineEdit_2.text())
        else:
            QMessageBox.about(self, "About Sabel IDE","Could Not Find Text")
        return done
            
    def replaceAllText(self):
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        while(edt.findText(self.lineEdit.text(),self.regex.isChecked(),self.caseSensitive.isChecked(),self.wholeWord.isChecked(),self.backward.isChecked())):
            edt.replaceText(self.lineEdit_2.text())
        

if __name__ == "__main__":
    app = QApplication([])
    splash_pix = QPixmap(':/Icons/logo.gif')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    frame = MainWindow()
    frame.showMaximized()
    splash.finish(frame)
    app.exec_()


