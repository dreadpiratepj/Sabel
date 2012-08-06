import sys
from PyQt4 import QtGui, QtCore

class TestTreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        super(TestTreeWidget, self).__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)

    def startDrag(self, dropAction):
        # create mime data object
        mime = QtCore.QMimeData()
        mime.setData('text/xml', '???')
        # start drag 
        drag = QtGui.QDrag(self)
        drag.setMimeData(mime)        
        drag.start(QtCore.Qt.CopyAction | QtCore.Qt.CopyAction)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()    

    def dropEvent(self, event): 
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
                item = QtGui.QTreeWidgetItem(self)
                item.setText(0, str(url.toLocalFile()))
                self.addTopLevelItem(item)
            self.emit(QtCore.SIGNAL("dropped"), links)      
        else:
            event.ignore()    

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.view = TestTreeWidget(self)
        self.view.setColumnCount(1)
        item0 = QtGui.QTreeWidgetItem(self.view)
        item0.setText(0, 'item0')
        item1 = QtGui.QTreeWidgetItem(self.view)
        item1.setText(0, 'item1')
        self.view.addTopLevelItems([item0, item1])

        self.setCentralWidget(self.view)

def main():
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
