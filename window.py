from PyQt4.QtGui import (QAction,QIcon,QMessageBox,QWidgetAction,QMenu,QWidget,
                         QHBoxLayout,QVBoxLayout,QTabWidget,QToolBar,QTextEdit,
                         QLineEdit,QPushButton,QToolButton,QSplitter,QStatusBar,
                         QMainWindow)              
from PyQt4.QtCore import QSize,Qt, QT_VERSION_STR,PYQT_VERSION_STR
from Widget import Tab,Tree

from globals import (ospathsep,ospathjoin,ospathbasename,workDir,
                     OS_NAME,PY_VERSION,os_icon,config,workSpace,
                     iconSize,iconDir)


__version__ = "0.47"

class Window(QMainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.setObjectName("self")
        self.resize(758, 673)
        self.setWindowTitle("Sabel")
        self.setWindowIcon(os_icon("sample"))
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        #TabWidgets
        self.tab_1 = QWidget(self)
        self.tab_1.setObjectName("tab_1")
        self.tab_1.setMinimumWidth(500)
        self.tabWidget = Tab(self.tab_1)
        self.tabWidget.setObjectName("tabWidget")
        self.VericalLayout = QVBoxLayout(self.tab_1)
        self.VericalLayout.setMargin(0)
        self.VericalLayout.setObjectName("VericalLayout")
        self.VericalLayout.addWidget(self.tabWidget)
        
        self.tabWidget_2 = QTabWidget(self)
        self.tabWidget_2.setMaximumWidth(200)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidget_3 = QTabWidget(self)
        self.tabWidget_3.setMaximumHeight(200)
        self.tabWidget_3.setObjectName("tabWidget_3")
         
        #Tree
        self.tab_5 = QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tab_5.setMaximumWidth(200)
        self.VerticalLayout_2 = QVBoxLayout(self.tab_5)#QHBoxLayout(self.tab_5)
        self.VerticalLayout_2.setMargin(0)
        self.VerticalLayout_2.setObjectName("horizontalLayout_3")
        self.treeWidget = Tree(self.tab_5)
        self.treeWidget.setObjectName("treeWidget")
        self.treebar = QToolBar()
        action_Folder = QAction(os_icon('newfolder_wiz'),'New Folder', self)
        self.treebar.addAction(action_Folder)
        self.treebar.setIconSize(QSize(16,16))
        self.treebar.setMaximumHeight(23)
        self.VerticalLayout_2.addWidget(self.treebar)
        self.VerticalLayout_2.addWidget(self.treeWidget)
        
        #Output
        self.tab_6 = QWidget()
        self.tab_6.setObjectName("tab_6")
        #GGGGGGGGGGGGGGGGGGGG AWESOME
        self.horizontalLayout_2 = QHBoxLayout(self.tab_6)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit = QTextEdit(self.tab_6)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_2.addWidget(self.textEdit)
        
        #Error
        self.tab_7 = QWidget()
        self.tab_7.setObjectName("tab_7")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_7)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.textEdit_2 = QTextEdit(self.tab_7)
        self.textEdit_2.setObjectName("textEdit_2")
        self.horizontalLayout_4.addWidget(self.textEdit_2)
        
        #Find
        self.tab_8 = QWidget()
        self.tab_8.setObjectName("tab_8")
        self.horizontalLayout_5 = QHBoxLayout(self.tab_8)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineEdit = QLineEdit(self.tab_8)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QLineEdit(self.tab_8)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.find = QPushButton(self.tab_8)
        self.find.setText("Find")
        self.find.clicked.connect(self.findCurrentText)
        self.replacefind = QPushButton(self.tab_8)
        self.replacefind.setText("Replace/Find")
        self.replace = QPushButton(self.tab_8)
        self.replace.setText("Replace")
        self.replace.clicked.connect(self.replaceCurrentText)
        self.replaceAll = QPushButton(self.tab_8)
        self.replaceAll.setText("Replace All")
        self.replaceAll.clicked.connect(self.replaceAllText)
        self.caseSensitive = QToolButton(self.tab_8)
        self.caseSensitive.setText("cs")
        self.caseSensitive.setCheckable(True)
        self.wholeWord = QToolButton(self.tab_8)
        self.wholeWord.setText("ww")
        self.wholeWord.setCheckable(True)
        self.regex = QToolButton(self.tab_8)
        self.regex.setText("re")
        self.regex.setCheckable(True)
        self.backward = QToolButton(self.tab_8)
        self.backward.setText("bk")
        self.backward.setCheckable(True)
        self.backward.setDisabled(True)
        self.horizontalLayout_5.addWidget(self.find)
        self.horizontalLayout_5.addWidget(self.lineEdit)
        self.horizontalLayout_5.addWidget(self.lineEdit_2)
        self.horizontalLayout_5.addWidget(self.caseSensitive)
        self.horizontalLayout_5.addWidget(self.wholeWord)
        self.horizontalLayout_5.addWidget(self.regex)
        self.horizontalLayout_5.addWidget(self.backward)
        self.horizontalLayout_5.addWidget(self.replacefind)
        self.horizontalLayout_5.addWidget(self.replace)
        self.horizontalLayout_5.addWidget(self.replaceAll)
        self.horizontalLayout_5.setMargin(0)
        self.tab_8.setMaximumHeight(25)
        self.VericalLayout.addWidget(self.tab_8)
        self.tab_8.hide()
        
        
        self.tabWidget_2.addTab(self.tab_5,"Projects")
        self.tabWidget_3.addTab(self.tab_7,"Error")
        self.tabWidget_3.addTab(self.tab_6,"Output")
        self.tabWidget_3.setTabIcon(0,os_icon("message_error"))
        self.tabWidget_3.setTabIcon(1,os_icon("monitor_obj"))
        
        
        #Splitters
        self.split1 = QSplitter(Qt.Horizontal)
        self.split1.addWidget(self.tab_1)
        #self.split1.addWidget(self.tab_5)
        self.split1.addWidget(self.tabWidget_2)
        self.split2 = QSplitter(Qt.Vertical)
        self.split2.addWidget(self.split1)
        self.split2.addWidget(self.tabWidget_3)
        self.tabWidget_3.hide()
        self.horizontalLayout.addWidget(self.split2)
        
        
        #Status
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.cmdButton = QPushButton(self)
        self.cmdButton.setFlat(True)
        self.cmdButton.setIcon(os_icon('monitor_obj'))
        self.cmdButton.clicked.connect(self.cmd)
        self.cmdButton.setShortcut('Ctrl+O')
        #self.cmdButton.setToolTip("Opens Console Ctrl+O")
        self.findButton = QPushButton(self)
        self.findButton.setFlat(True)
        self.findButton.setIcon(os_icon('find_obj'))
        self.findButton.setShortcut("Ctrl+F")
        #self.findButton.setToolTip("Opens Find Bar Ctrl+F")
        self.findButton.clicked.connect(self.findBarShow)
        self.statusbar.addWidget(self.cmdButton)
        self.statusbar.addWidget(self.findButton)
        self.statusbar.setFixedHeight(18)
        
        #Init
        self.setCentralWidget(self.centralwidget)
        self.setStatusBar(self.statusbar)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setTabShape(0)
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
    def findBarShow(self):
        if(self.tab_8.isHidden()):
            self.tab_8.show()
        else:
            self.tab_8.hide()
    
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
        self.action_Run.triggered.connect(self.adb.run)
        self.action_RunFile = QAction(os_icon('start_ccs_task'), 'File', self)
        self.action_Stop = QAction(os_icon('term_sbook'), 'Stop', self)
        self.action_Stop.setShortcut('Ctrl+Q')
        self.action_Stop.triggered.connect(self.adb.stop)
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
        men.addAction(QAction("Lua",self))
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
            
    def findCurrentText(self):
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
