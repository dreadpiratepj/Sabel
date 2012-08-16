from globals import adblist
from PyQt4.QtGui import QWidget
import threading
from subprocess import PIPE,Popen,STDOUT
from PyQt4.QtCore import pyqtSignal,SIGNAL


class Adb(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.adb_process = None
        self.isRunning = False
        self.connect(self, SIGNAL("didSomething"),self.update)
        
    def update(self,line):
        self.parent.textEdit.append(line)
            
    def setCommand(self,comlist):
        pass
        
    def output(self,pipe):
        while True:
            try:
                if self.adb_process.poll() != None:
                    break
                line = pipe.readline().strip()

                if len(line) > 0:
                     self.emit(SIGNAL("didSomething"),line)
            except:
                print "except"
                #traceback.print_exc()


    def run(self):
        if self.isRunning == False:
            if self.adb_process != None and self.adb_process.poll() == None:
                self.adb_process.kill()
            self.isRunning = True
            self.parent.action_Run.setDisabled(True)
            self.parent.action_Stop.setEnabled(True)        
            if(self.parent.tabWidget_3.isHidden()):
                self.parent.tabWidget_3.show()
                self.parent.tabWidget_3.setCurrentIndex(1)
            self.parent.textEdit.clear()
        self.parent.textEdit.append("Pushing main.nut\n")
        self.adb_process = Popen(adblist[0], shell=False, stdout=PIPE,stderr=STDOUT)
        t = threading.Thread(target=self.output, args=(self.adb_process.stdout,))
        t.start()
        t.join()
        #adb_process.wait()
        #self.parent.textEdit.append("Starting Activity\n")
        #adb_process = subprocess.Popen(adb[1], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #self.parent.textEdit.append("Logging")
        #adb_process.wait()
        #adb_process = subprocess.Popen(adb[2], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    def stop(self):
        if self.isRunning == True:
            self.isRunning = False
            if self.adb_process != None and self.adb_process.poll() == None:
                self.adb_process.kill()
            self.parent.action_Stop.setDisabled(True)
            self.parent.textEdit.append("Stopped")
            if not(self.parent.tabWidget_3.isHidden()):
                self.parent.tabWidget_3.hide()
            self.parent.action_Run.setEnabled(True)
              
    def close(self):
        if self.adb_process != None and self.adb_process.poll() == None:
            self.adb_process.kill()