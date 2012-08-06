from PyQt4.QtGui import *
import os


class UIAbout(QDialog):
    """About dialogue
    """
    def __init__(self, parentWindow):
        QDialog.__init__(self, parentWindow)
        from PyQt4 import uic  # lazy import for better startup performance
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'About.ui'), self)
        
class UIProject(QDialog):
    """Project dialogue
    """
    def __init__(self, parentWindow):
        QDialog.__init__(self, parentWindow)
        from PyQt4 import uic  # lazy import for better startup performance
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'Project.ui'), self)
        
class UIRename(QDialog):
    """Project dialogue
    """
    def __init__(self, parentWindow):
        QDialog.__init__(self, parentWindow)
        from PyQt4 import uic  # lazy import for better startup performance
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'Rename.ui'), self)
        
class UIOptions(QDialog):
    """Project dialogue
    """
    def __init__(self, parentWindow):
        QDialog.__init__(self, parentWindow)
        from PyQt4 import uic  # lazy import for better startup performance
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'Options.ui'), self)
        #self.tabWidget.
        #fname = unicode(QFileDialog.getExistingDirectory(self,
        #                "Open File", '.', "Files (*.*)"))





class MainForm(QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        qtt = QTextEdit(self)
        self.setCentralWidget(qtt)
        qtt.textChanged.connect(self.dd)
        
    def dd(self):
        main = UIAbout(self)
        main.show()
        
def main():
    app = QApplication([])
    form = MainForm()
    form.show()
    app.exec_()   
    
if __name__ == '__main__':
    main()    

