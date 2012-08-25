from globals import adblist
from PyQt4.QtGui import QWidget
import threading
from subprocess import PIPE,Popen,STDOUT
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
        #self.process_thread.run()
        self.process.start(self.cmd)
        self.exec_()
        self.process.waitForFinished(-1)
        self.process.kill()
        #self.emit(SIGNAL("finished"))
        #self.setCmd(adblist[1])
        #self.process.kill()
        #self.process.start(self.cmd)
        #self.process.waitForFinished()
        
        #self.emit(SIGNAL("fini"))
        #self.process.finished.connect(self.fini)
        #self.emit(SIGNAL("finished"),True)
        #return
        
    def fini(self,no):
        self.emit(SIGNAL("fini"),no,self.cmd)
        
    def readOutput(self):
        self.emit(SIGNAL("update"),QString(self.process.readAllStandardOutput()))
        
    def readErrors(self):
        self.emit(SIGNAL("update"),QString(self.process.readAllStandardError()))
    
    def __del__(self):
        self.wait()


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
        self.timer = QTimer()
        #self.adb_thread = AdbThread()
        self.connect(self.adb_thread, SIGNAL("update"),self.update)
        #self.connect(self.adb_thread, SIGNAL("fini"),self.newstart)
        self.connect(self.adb_thread, SIGNAL("fini"),self.newstart)
        #self.connect(self.timer , SIGNAL('timeout()') , self.onTimeout)
        #self.connect(self.adb_thread , SIGNAL('started()') , self.onThreadStarted)
        #self.connect(self.adb_thread , SIGNAL('finished()'), self.onThreadFinished) 
        
    def onTimeout(self):
        print "timeout"
        """
        # Update the progress bar
        value = self.pbar.value()
        # Going forward or backwards?
        if self.pbar.invertedAppearance():
            if value-2 < self.pbar.minimum():
                self.pbar.setValue(self.pbar.minimum())
                self.pbar.setInvertedAppearance(False)
            else:
                self.pbar.setValue(value-2)
        else:
            if value+2 > self.pbar.maximum():
                self.pbar.setValue(self.pbar.maximum())
                self.pbar.setInvertedAppearance(True)
            else:
                self.pbar.setValue(value+2)
        """
        
    def onThreadStarted(self):
        print "Thread has been started"
        self.timer.start(10)
        #self.enableButtons(False)
 
    def onThreadFinished(self):
        print "Thread has finished"
        self.timer.stop()
        #self.enableButtons(True)
        #self.pbar.setValue(0)
        
    def update(self,line):
        self.parent.textEdit.append(line)
        
    def newstart(self,no,cmd):
        if(cmd == "adb -d push "+adblist[0]):
            self.parent.textEdit.append(str(no))
            self.parent.textEdit.append(cmd)
            self.parent.textEdit.append("Finshed")
            self.adb_thread.setCmd("adb -d shell am start -a android.intent.action.MAIN -n "+adblist[1])
            self.adb_thread.run()
        elif(cmd == "adb -d push "+adblist[0]):
            self.parent.textEdit.append(str(no))
            self.parent.textEdit.append(cmd)
            self.parent.textEdit.append("Finshed")
            self.adb_thread.setCmd("adb -d logcat -s "+adblist[2])
            self.adb_thread.run()
        #self.adb_thread.kill_process()
        #self.parent.textEdit.append("Starting Activity...\n")
        #self.adb_thread.setCmd(adblist[1])
        #self.adb_thread.run()
        
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
        self.adb_thread.setCmd("adb -d push "+adblist[0])
        self.adb_thread.run()
        
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
            self.adb_thread.kill_process()
            self.parent.action_Stop.setDisabled(True)
            self.parent.textEdit.append("Stopped.")
            if not(self.parent.tabWidget_3.isHidden()):
                self.parent.tabWidget_3.hide()
            self.parent.action_Run.setEnabled(True)
              
    def close(self):
        if self.adb_process != None and self.adb_process.poll() == None:
            #self.adb_thread.kill_process()
            self.adb_thread.quit()
