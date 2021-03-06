from globals import fontSize,fontName,ospathjoin,os_pixmap,apiDir,threshold,config
from PyQt4.QtCore import SIGNAL,QString
from PyQt4.QtGui import QFontMetrics, QFont, QPixmap, QColor ,QPalette
from PyQt4.Qsci import QsciScintilla, QsciLexerPython ,QsciAPIs ,QsciLexerCPP
from lexersquirrel import LexerSquirrel
        
class Editor(QsciScintilla):
    ARROW_MARKER_NUM = 8
    #fontSize = fontSize
    def __init__(self,parent,text,lang,colorStyle):
        QsciScintilla.__init__(self,parent)
        self.parent = parent
        self.lang = lang
        self.fontSize = fontSize
        self.colorStyle = colorStyle
        #self.init()
        self.setText(text)
        #self.addAction(QAction("gg",self))  
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
        self.setAutoCompletionThreshold(threshold)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        #self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        #self.setAutoCompletionSource(QsciScintilla.AcsAll)
        #self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
        self.init()
        
    def init(self):
        self.setCaretLineBackgroundColor(self.colorStyle.caret)
        self.setMarginsBackgroundColor(self.colorStyle.margin)
        self.setMarkerBackgroundColor(self.colorStyle.marker,self.ARROW_MARKER_NUM)
        self.font = QFont()
        self.font.setFamily(fontName)
        #self.font.setFixedPitch(True)
        self.font.setPointSize(self.fontSize)
        self.setFont(self.font)
        self.fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        # Margin 0 is used for line numbers
        #self.setMarginLineNumbers(0, True)
        #self.setMarginWidth(0, self.fontmetrics.width("0000") + 6)
        self.setMarginLineNumbers(1, True)
        self.setMarginWidth(1, QString("-------"))
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
        
        
    def setColorStyle(self,colorStyle):
        self.colorStyle = colorStyle
        self.setCaretLineBackgroundColor(self.colorStyle.caret)
        self.setMarginsBackgroundColor(self.colorStyle.margin)
        self.setMarkerBackgroundColor(self.colorStyle.marker,self.ARROW_MARKER_NUM)
        if self.lang == 2:
            self.lexer.setColorStyle(self.colorStyle)
            self.lexer.setColor(QColor("#008000"),0)       
    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
    
    def zoomin(self):
        self.fontSize += 1
        config.setFontSize(self.fontSize)
        self.font.setPointSize(self.fontSize)
        #self.setFont(self.font)
        self.lexer.setFont(self.font)
        self.setMarginsFont(self.font)
        
    def zoomout(self):
        self.fontSize -= 1
        config.setFontSize(self.fontSize)
        self.font.setPointSize(self.fontSize)
        #self.setFont(self.font)
        self.lexer.setFont(self.font)
        self.setMarginsFont(self.font)
        
    def setFontName(self,name):
        self.font.setFamily(name)
        self.lexer.setFont(self.font)
        
    def setThreshold(self,val):
        self.setAutoCompletionThreshold(val)
        
            
            
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
        

