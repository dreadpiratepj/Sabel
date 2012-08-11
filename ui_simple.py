from PyQt4 import QtCore, QtGui
from Widget import Tab,Tree

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(758, 673)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        #TabWidgets
        self.tabWidget = Tab(self)
        self.tabWidget.setMinimumSize(QtCore.QSize(500, 0))
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget_2 = QtGui.QTabWidget(self)
        self.tabWidget_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidget_3 = QtGui.QTabWidget(self)
        self.tabWidget_3.setMaximumSize(16777215,200)
        self.tabWidget_3.setMinimumSize(0,75)
        self.tabWidget_3.setObjectName("tabWidget_3")
        #bottom = QtGui.QFrame(self)
        #bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        #bottom.setMaximumSize(16777215,200)
         
        #Tree
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.tab_5)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 9, 191, 601))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.treeWidget = Tree(self.horizontalLayoutWidget_2)
        self.treeWidget.setObjectName("treeWidget")
        self.horizontalLayout_3.addWidget(self.treeWidget)
        
        #Output
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName("tab_6")
        #GGGGGGGGGGGGGGGGGGGG AWESOME
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab_6)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit = QtGui.QTextEdit(self.tab_6)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_2.addWidget(self.textEdit)
          
        #Error
        self.tab_7 = QtGui.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.horizontalLayoutWidget_4 = QtGui.QWidget(self.tab_7)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, -1, 16777215, 200))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.textEdit_2 = QtGui.QTextEdit(self.horizontalLayoutWidget_4)
        self.textEdit_2.setObjectName("textEdit_2")
        self.horizontalLayout_4.addWidget(self.textEdit_2)
        
        self.tabWidget_2.addTab(self.tab_5,"Projects")
        self.tabWidget_3.addTab(self.tab_7,"Error")
        self.tabWidget_3.addTab(self.tab_6,"Output")
        #Splitters
        self.split1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.split1.addWidget(self.tabWidget)
        self.split1.addWidget(self.tabWidget_2)
        self.split2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.split2.addWidget(self.split1)
        self.split2.addWidget(self.tabWidget_3)
        self.tabWidget_3.hide()
        self.horizontalLayout.addWidget(self.split2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tabWidget.setCurrentIndex(-1)
        self.tabWidget_2.setCurrentIndex(0)
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

