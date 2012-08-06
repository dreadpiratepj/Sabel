# begin sample application #
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *
import sys

# Examle API
TESTAPI= """
Constant1
Constant2
unknownFunction(??)
knownFunction(name, directory)
knownFunction2(number,string)
module.function(??)
"""

class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.start()

    def start(self):
        lexer =  self.lexer = QsciLexerPython()
        api = QsciAPIs(lexer)
        # write the API to a file
        self.api = api
        # load the api into
        assert api.load("test.api")
        api.connect(api, SIGNAL("apiPreparationStarted()"),self.started)
        api.connect(api, SIGNAL("apiPreparationFinished()"),self.finished)
        # prepare the binary version of the API, suitable for loading
        api.prepare()

    def started(self):
        pass#QMessageBox.information(self, "Started", "Started")

    def finished(self):
        # save the api to a binary file
        self.api.savePrepared("test.prepared")
        # Shows how to use the prepared API inside Scintilla with a  prettier
        #  Python Mode
        editor = self.editor = QsciScintilla(self.centralWidget())
        #editor.show()
        lexer =  QsciLexerPython()
        api = QsciAPIs(lexer)
        # load the api into the lexer so code-completion should
        #  work
        assert api.loadPrepared("test.prepared")
        lexer.setAPIs(api)
        editor.setAutoCompletionSource(editor.AcsAPIs)
        editor.setAutoCompletionThreshold(1)
        editor.setLexer(lexer)
        # set up the editor the prettier Python editing
        editor.setIndentationsUseTabs(False)
        font = QFont()
        fm = QFontMetrics(font)
        editor.setIndentationWidth(4)
        editor.setTabWidth(4)
        editor.show()
        if sys.platform != "win32":
            editor.zoomIn(3)
        editor.setIndentationsUseTabs(False)
        editor.setIndentationWidth(4)
        editor.setTabWidth(4)
        # conventionnaly, margin 0 is for line numbers
        editor.setMarginWidth(0, fm.width( "00000" ) + 5)
        editor.setMarginLineNumbers(0, True)
        ## Edge Mode shows a red vetical bar at 80 chars
        editor.setEdgeMode(QsciScintilla.EdgeLine)
        editor.setEdgeColor(QColor("#FF0000"))
        ## Folding visual : we will use boxes
        editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        ## Braces matching
        editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        ## Editing line color
        editor.setCaretLineVisible(True)
        editor.setCaretLineBackgroundColor(QColor("#CDA869"))
        ## Margins colors
        # line numbers margin
        editor.setMarginsBackgroundColor(QColor("#333333"))
        editor.setMarginsForegroundColor(QColor("#CCCCCC"))
        # folding margin colors (foreground,background)
        editor.setFoldMarginColors(QColor("#99CC66"),QColor("#333300"))
        # uncommenting this exception causes code-completion not to  work.
        raise Exception("Why does this exception make code-completion work?")


app = QApplication(sys.argv)
mw = Main()
mw.show()
app.exec_()