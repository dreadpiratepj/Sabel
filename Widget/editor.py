from globals import ospathjoin,os_pixmap,apiDir

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QFontMetrics, QFont, QPixmap, QColor
from PyQt4.Qsci import QsciScintilla, QsciLexerPython ,QsciAPIs ,QsciLexerCPP
from lexersquirrel import LexerSquirrel
from style import Style


        
class Editor(QsciScintilla):
    ARROW_MARKER_NUM = 8
    def __init__(self,parent,text,lang = 2,styleIndex = 0):
        QsciScintilla.__init__(self,parent)
        self.parent = parent
        self.styleIndex = styleIndex
        self.lang = lang
        self.colorStyle = None
        self.init()
        self.setText(text)
        #self.addAction(QAction("gg",self))
        #self.findFirst("function",False,True,True,True)
        #self.setEdgeColumn(70)
        #self.setEdgeColor(QColor(0,0,0))
        #self.setEdgeMode(self.EDGE_LINE)           
        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.connect(self,SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow,self.ARROW_MARKER_NUM)
        self.registerImage(0,os_pixmap("class_obj"))
        self.registerImage(1,os_pixmap("method_obj"))
        self.registerImage(2,os_pixmap("field_public_obj"))
        # Brace matching: enable for a brace immediately before or after
        # the current position
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        #self.setAutoCompletionSource(QsciScintilla.AcsAll)
        #self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
        
    def init(self):
        self.setColorStyle(self.styleIndex)
        self.font = self.colorStyle.font
        self.setFont(self.font)
        self.fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        self.setMarginWidth(0, self.fontmetrics.width("000") + 6)
        # Margin 0 is used for line numbers
        self.setMarginLineNumbers(0, True)
        self.setCaretLineVisible(True)
        if self.lang == 0:
            self.lexer = QsciLexerPython()
        elif self.lang == 1:
            self.lexer = QsciLexerCPP()
        elif self.lang == 2:
            self.lexer = LexerSquirrel(self.colorStyle,self)
        self.lexer.setDefaultFont(self.font)
        self.api = QsciAPIs(self.lexer)
        self.api.load(ospathjoin(apiDir,"emo.api"))
        self.api.prepare()
        self.lexer.setAPIs(self.api) #Very important do not change line otherwise gg
        self.setLexer(self.lexer) #Very important do not change line otherwise gg
        
        
    def setColorStyle(self,styleIndex):
        if styleIndex == 0:
            self.colorStyle = Style()
        elif styleIndex == 1:
            self.colorStyle = Style()
        self.setCaretLineBackgroundColor(self.colorStyle.caret)
        self.setMarginsBackgroundColor(self.colorStyle.margin)
        self.setMarkerBackgroundColor(self.colorStyle.marker,self.ARROW_MARKER_NUM)
            
    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
            
            
    """
    findFirst     (     const QString &      expr,
        bool      re,
        bool      cs,
        bool      wo,
        bool      wrap,
        bool      forward = true,
        int      line = -1,
        int      index = -1,
        bool      show = true,
        bool      posix = false 
    )         [virtual]
    """
    def findText(self,text,re,cs,wo,bk):
        if(text != ''):
            done = self.findFirst(text,re,cs,wo,True,not bk)
            return done
     
    def replaceText(self,text):
        self.replace(text)
        
    def replaceFindText(self,text):
        self.replace(text)
        

