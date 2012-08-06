# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\CODE\IDE\simple.ui'
#
# Created: Fri Aug 03 14:22:10 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from Widget import Tab,Tree

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(758, 673)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = Tab(self)
        self.tabWidget.setMinimumSize(QtCore.QSize(500, 0))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.horizontalLayout.addWidget(self.tabWidget)
        self.split1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        #self.tabWidget_2 = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget_2 = QtGui.QTabWidget(self)
        self.split1.addWidget(self.tabWidget)
        self.split1.addWidget(self.tabWidget_2)
        self.tabWidget_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.tabWidget_2.setObjectName(_fromUtf8("tabWidget_2"))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.tab_5)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 9, 191, 601))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.treeWidget = Tree(self.horizontalLayoutWidget_2)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.horizontalLayout_3.addWidget(self.treeWidget)
        self.tabWidget_2.addTab(self.tab_5, _fromUtf8(""))
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName(_fromUtf8("tab_6"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.tab_6)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, -1, 191, 611))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.textEdit = QtGui.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.tabWidget_2.addTab(self.tab_6, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.split1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_New = QtGui.QAction(MainWindow)
        self.action_New.setObjectName(_fromUtf8("action_New"))
        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setObjectName(_fromUtf8("action_Open"))
        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setObjectName(_fromUtf8("action_Save"))
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.actionA_bout = QtGui.QAction(MainWindow)
        self.actionA_bout.setObjectName(_fromUtf8("actionA_bout"))
        self.action_Help = QtGui.QAction(MainWindow)
        self.action_Help.setObjectName(_fromUtf8("action_Help"))

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QObject.connect(self.action_Quit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Simple Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), QtGui.QApplication.translate("MainWindow", "Files", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QtGui.QApplication.translate("MainWindow", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New.setText(QtGui.QApplication.translate("MainWindow", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("MainWindow", "Save &As", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionA_bout.setText(QtGui.QApplication.translate("MainWindow", "A&bout", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Help.setText(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))

