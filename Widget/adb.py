from globals import adblist
from PyQt4.QtGui import QWidget
import threading
from subprocess import PIPE,Popen,STDOUT
from PyQt4.QtCore import pyqtSignal,SIGNAL,QThread,QProcess,QString

class WorkThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.process = QProcess()
        self.cmd = None
        self.connect(self.process, SIGNAL("readyReadStandardOutput()"), self.readOutput)
        self.connect(self.process, SIGNAL("readyReadStandardError()"), self.readErrors)
        
    def setCmd(self,val):
        self.cmd = val
        
    def kill_process(self):
        self.process.kill()
        
    def run(self):
        #self.process_thread.run()
        self.process.start(self.cmd)
        #self.exec_()
        self.process.waitForFinished()
        #self.emit(SIGNAL("fini"))
        #self.process.finished.connect(self.fini)
        #self.emit(SIGNAL("finished"),True)
        
    def fini(self):
        self.emit(SIGNAL("fini"))
    def readOutput(self):
        self.emit(SIGNAL("update"),QString(self.process.readAllStandardOutput()))
        
    def readErrors(self):
        self.emit(SIGNAL("update"),QString(self.process.readAllStandardError()))
    
    def __del__(self):
        pass
        #self.wait()


class AdbThread(threading.Thread,QWidget):
    def __init__(self):
        QWidget.__init__(self)
        threading.Thread.__init__(self)
        self.stdout = None
        self.stderr = None
        self.cmd = None
        self.adb_process = None
        
        
    def setCmd(self,val):
        self.cmd = val
        
    def output(self,pipe):
        while True:
            try:
                if self.adb_process.poll() != None:
                    break
                line = pipe.readline().strip()
                if len(line) > 0:  
                     #print line
                     self.emit(SIGNAL("didSomething"),line)
            except:
                print "except"
                #traceback.print_exc()
        
    def run(self):
        if(self.cmd != ""):
            self.adb_process = Popen(self.cmd, creationflags=0x08000000,shell=False,stdout=PIPE,stderr=PIPE)
            t = threading.Thread(target=self.output, args=(self.adb_process.stdout,))
            t.start()
            #t.join()

class Adb(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.adb_process = None
        self.isRunning = False
        self.adb_thread = WorkThread()
        #self.adb_thread = AdbThread()
        self.connect(self.adb_thread, SIGNAL("update"),self.update)
        #self.connect(self.adb_thread, SIGNAL("fini"),self.newstart)
        self.connect(self.adb_thread, SIGNAL("finished"),self.newstart)
        
    def update(self,line):
        self.parent.textEdit.append(line)
        
    def newstart(self):
        print "finished"
        self.parent.textEdit.append("Finshed")
        #self.adb_thread.kill_process()
        #self.parent.textEdit.append("Starting Activity...\n")
        #self.adb_thread.setCmd(adblist[1])
        #self.adb_thread.run()
        #print "finished"
        

    def run(self):
        if self.isRunning == False:
            #if self.adb_process != None and self.adb_process.poll() == None:
            #    self.adb_process.kill()
            self.isRunning = True
            self.parent.action_Run.setDisabled(True)
            self.parent.action_Stop.setEnabled(True)        
            if(self.parent.tabWidget_3.isHidden()):
                self.parent.tabWidget_3.show()
                self.parent.tabWidget_3.setCurrentIndex(1)
            self.parent.textEdit.clear()
        self.parent.textEdit.append("Pushing main.nut...\n")
        self.adb_thread.setCmd(adblist[0])
        self.adb_thread.run()
        #self.adb_thread.finished(self.newstart)
        """
        self.adb_thread.setCmd(adblist[0])
        self.adb_thread.run()
        self.adb_thread.join()
        self.adb_thread.adb_process.kill()
        self.parent.textEdit.append("Starting Activity\n")
        self.adb_thread.setCmd(adblist[1])
        self.adb_thread.run()
        self.adb_thread.join()
        self.adb_thread.adb_process.kill()
        self.parent.textEdit.append("Logging")
        self.adb_thread.setCmd(adblist[2])
        self.adb_thread.run()
        self.adb_thread.join()
        #self.adb_thread.adb_process.kill()
        """
        

    def stop(self):
        if self.isRunning == True:
            self.isRunning = False
            self.adb_thread.setCmd(adblist[3])
            self.adb_thread.run()
            self.adb_thread.join()
            self.adb_thread.adb_process.kill()
            #if self.adb_process != None and self.adb_process.poll() == None:
            #    self.adb_process.kill()
            self.parent.action_Stop.setDisabled(True)
            self.parent.textEdit.append("Stopped")
            if not(self.parent.tabWidget_3.isHidden()):
                self.parent.tabWidget_3.hide()
            self.parent.action_Run.setEnabled(True)
              
    def close(self):
        if self.adb_process != None and self.adb_process.poll() == None:
            self.adb_process.kill()
