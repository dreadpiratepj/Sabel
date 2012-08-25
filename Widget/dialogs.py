from PyQt4 import QtGui 
from PyQt4 import QtCore
from globals import adblist,config 
"""    
class UIProject(QDialog):
    def __init__(self, parentWindow):
        QDialog.__init__(self, parentWindow)
        from PyQt4 import uic  # lazy import for better startup performance
        uic.loadUi(ospathjoin(ospathdirname(__file__), 'Project.ui'), self)
        
        
class UIOptions(QDialog):
    def __init__(self, parentWindow):
        QDialog.__init__(self, parentWindow)
        from PyQt4 import uic  # lazy import for better startup performance
        uic.loadUi(ospathjoin(ospathdirname(__file__), 'Options.ui'), self)
        #self.tabWidget.
        #fname = unicode(QFileDialog.getExistingDirectory(self,
        #                "Open File", '.', "Files (*.*)"))

"""
class DialogAndroid(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(400, 420)
        self.horizontalLayoutWidget = QtGui.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 361))
        self.horizontalLayoutWidget.setObjectName(("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.horizontalLayoutWidget)
        self.tabWidget.setObjectName(("tabWidget"))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(("tab_4"))
        self.formLayoutWidget = QtGui.QWidget(self.tab_4)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 311))
        self.formLayoutWidget.setObjectName(("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(("formLayout"))
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label_2)
        self.lineEdit_2 = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setText((""))
        self.lineEdit_2.setObjectName(("lineEdit_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.lineEdit_2)
        self.lineEdit_3 = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_3.setText((""))
        self.lineEdit_3.setObjectName(("lineEdit_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.lineEdit_3)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(("label_4"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.label_4)
        self.lineEdit_4 = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_4.setText((""))
        self.lineEdit_4.setObjectName(("lineEdit_4"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.lineEdit_4)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(("label_5"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.SpanningRole, self.label_5)
        self.lineEdit_5 = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEdit_5.setText((""))
        self.lineEdit_5.setObjectName(("lineEdit_5"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.SpanningRole, self.lineEdit_5)
        self.tabWidget.addTab(self.tab_4, (""))
        self.horizontalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(40, 370, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(("buttonBox"))
        self.tabWidget.setCurrentIndex(1)
        self.setWindowTitle("Tools")
        self.label_2.setText("Push Main File:")
        self.label_3.setText("Start Activity:")
        self.label_4.setText("Logcat:")
        self.label_5.setText("Exit Activity:")
        self.tabWidget.setTabText(0,"Android")
        self.buttonBox.clicked.connect(self.ok)
        self.lineEdit_2.setText(adblist[0])
        self.lineEdit_3.setText(adblist[1])
        self.lineEdit_4.setText(adblist[2])
        self.lineEdit_5.setText(adblist[3])
        
    def ok(self,btn):
        val = []
        if(btn.text() == "OK"):
            val.append(str(self.lineEdit_2.text()))
            val.append(str(self.lineEdit_3.text()))
            val.append(str(self.lineEdit_4.text()))
            val.append(str(self.lineEdit_5.text()))
            config.setAdb(val)
        self.close()
class DialogAnt(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(400, 420)
        
class DialogSquirrel(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(400, 420)                