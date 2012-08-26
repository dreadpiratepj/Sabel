from PyQt4.QtGui import QWidget,QInputDialog
from PyQt4.QtCore import SIGNAL
from workthread import WorkThread

class Command(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.cmd = ""
        self.cmdThread = WorkThread()
        self.connect(self.cmdThread, SIGNAL("update"),self.update)
        self.connect(self.cmdThread, SIGNAL("fini"),self.finished)
        
    def setCmd(self):
        text, ok = QInputDialog.getText(self, 'Run Command', 'Command:')
        self.cmd = str(text)
        if ok and self.cmd != "":
            self.parent.textEdit.clear()
            self.run()
            
    def setCmdLine(self):
        self.cmd = str(self.parent.lineeEdit.text())
        if self.cmd != "":
            self.parent.textEdit.clear()
            self.run()
        
    def finished(self,no,cmd):
        if(no == 0):
            self.parent.textEdit.append("Finshed")
            self.parent.textEdit.append(cmd)
        else:
            self.parent.textEdit.append("Error Canceled")
            self.parent.textEdit.append(cmd) 
        
    def update(self,line):
        self.parent.textEdit.append(line)
        if(self.parent.tabWidget_3.isHidden()):
            self.parent.tabWidget_3.show()
        self.parent.tabWidget_3.setCurrentIndex(1)


    def run(self):
        self.cmdThread.setCmd(self.cmd)
        self.cmdThread.run()
        
    def close(self):
        self.cmdThread.quit()