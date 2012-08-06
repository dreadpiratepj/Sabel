#!/usr/bin/env python
# -*- coding: latin1 -*-
 
"""
Basic use of the QScintilla2 widget
 
Note : name this file "qt4_sci_ac_test.py"
Base code originally from: http://kib2.free.fr/tutos/PyQt4/QScintilla2.html
"""
 
import sys
from PyQt4.QtGui import QApplication
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerPython
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = QsciScintilla()
 
    ## Choose a lexer
    ## This can be any Scintilla lexer, but the original example used Python
    lexer = QsciLexerPython()
 
    ## Create an API for us to populate with our autocomplete terms
    api = Qsci.QsciAPIs(lexer)
    ## Add autocompletion strings
    #api.loadPrepared("pyqt4")
    file = open("pyqt.api").readlines()
    #for i in file:
        #i.rstrip()
        #api.add(i)
    #api.load("pyqt.api")
    ## Compile the api for use in the lexer
    api.add("QtCore.BitArray?10")
    api.add("QtCore.Bitmap?10")
    api.add("QtCore.QRectF.height?4() -> float")
    api.prepare()
 
    editor.setLexer(lexer)
 
    ## Set the length of the string before the editor tries to autocomplete
    ## In practise this would be higher than 1
    ## But its set lower here to make the autocompletion more obvious
    editor.setAutoCompletionThreshold(1)
    ## Tell the editor we are using a QsciAPI for the autocompletion
    editor.setAutoCompletionSource(QsciScintilla.AcsAPIs)
 
    ## Render on screen
    editor.show()
 
    ## Show this file in the editor
    editor.setText(open("scint.py").read())
    sys.exit(app.exec_())