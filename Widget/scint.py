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
    lexer = QsciLexerPython()
 
    api = Qsci.QsciAPIs(lexer)
    api.load("emo.api")
    api.prepare()
    editor.setLexer(lexer)
    editor.setAutoCompletionThreshold(1)
    editor.setAutoCompletionSource(QsciScintilla.AcsAPIs)
    editor.show()
    editor.setText(open("scint.py").read())
    sys.exit(app.exec_())
    
    

    
        