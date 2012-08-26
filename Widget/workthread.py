from PyQt4.QtCore import pyqtSignal,SIGNAL,QThread,QProcess,QString,QTimer

class WorkThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.process = QProcess()
        self.cmd = None
        self.process.readyReadStandardOutput.connect(self.readOutput)
        self.process.readyReadStandardError.connect(self.readErrors)
        self.process.finished.connect(self.fini)
        
        
    def setCmd(self,val):
        self.cmd = val
        
    def kill_process(self):
        self.process.kill()
        
    def run(self):
        if(self.process.isOpen()):
            self.process.close()
            #print "open"
            #self.process.kill()
            self.process.start(self.cmd)
        else:
            #print "strgin"
            self.process.start(self.cmd)
        self.exec_()
        self.process.waitForFinished()
        self.process.kill()
        
    def run2(self):
        if(self.process.isOpen()):
            self.process.close()
            #print "open"
            #self.process.kill()
            self.process.start(self.cmd)
        else:
            #print "strgin"
            self.process.start(self.cmd)
        self.exec_()
        #self.process.kill()
        
    def fini(self,no):
        self.emit(SIGNAL("fini"),no,self.cmd)
        
    def readOutput(self):
        self.emit(SIGNAL("update"),QString(self.process.readAllStandardOutput()))
        
    def readErrors(self):
        self.emit(SIGNAL("update"),QString(self.process.readAllStandardError()))
    
    def __del__(self):
        self.wait()