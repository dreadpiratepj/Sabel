from globals import sqcDir
from PyQt4.QtGui import QWidget
import threading
from subprocess import PIPE,Popen,STDOUT
from PyQt4.QtCore import pyqtSignal,SIGNAL


class Parser(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.parser_process = None
        self.isRunning = False
        self.connect(self, SIGNAL("parse"),self.update)
        
    def update(self,line):
        self.parent.textEdit_2.append(line)
        if(self.parent.tabWidget_3.isHidden()):
            self.parent.tabWidget_3.show()
            self.parent.tabWidget_3.setCurrentIndex(0)
        
    def output(self,pipe):
        while True:
            try:
                if self.parser_process.poll() != None:
                    break
                line = pipe.readline().strip()

                if len(line) > 0:
                     self.emit(SIGNAL("parse"),line)
            except:
                print "except"
                #traceback.print_exc()


    def run(self,nfile):
        #print nfile
        if(nfile.endswith(".nut")):
            self.parent.textEdit_2.clear()
            if self.parser_process != None and self.parser_process.poll() == None:
                self.parser_process.kill()
            self.parser_process = Popen(sqcDir+" "+nfile, creationflags=0x08000000, shell=False, stdout=PIPE,stderr=PIPE)
            t = threading.Thread(target=self.output, args=(self.parser_process.stdout,))
            t.start()
            t.join()
        
                    
    def close(self):
        if self.parser_process != None and self.parser_process.poll() == None:
            self.parser_process.kill()