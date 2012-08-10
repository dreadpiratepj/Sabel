
import sys
from PyQt4.QtCore import SIGNAL, SLOT, QString,QStringList
from PyQt4.QtGui import QApplication, QMainWindow, QColor, QFont
from PyQt4.Qsci import QsciScintilla, QsciLexerCustom

# The most important and hard part of this code was given by Baz WALTER on the PyQt list.

if sys.hexversion < 0x020600F0:
    print('python 2.6 or greater is required by this program')
    sys.exit(1)

_sample = """
This example shows how to highlight some specific lines or words.

+ A first level title bold and red
    + A secund level title bold and blue with a yellow background
Some text with green in green but also bold and underlined.
The digits are gray with an orange backround. You don't believe it, look at that : 1 , 2 , ... , 123456789...

It's very uggly but it shows how to do more pretty "highlighters".

/*
 * credit scene
 */
class CreditScene {
    foreground = null;
    okButton   = null;
    layer      = null;

    fadingOut = false;

    function onLoad() {
        stage.bgcolor(0, 0, 0, 1);

        local stageCenterX = stage.getWindowWidth()  * 0.5;
        local stageCenterY = stage.getWindowHeight() * 0.5;

        local bgWidth  = 480;
        local bgHeight = 320;

        if (useHD) {
            bgWidth  = 960;
            bgHeight = 640;
        }

        if (background != null) {
            background.remove();
        }

        background = emo.Sprite(getHdImageName("credit_background.png"));
        background.moveCenter(stageCenterX, stageCenterY);
        background.setZ(0);
        background.load();

        layer = emo.Rectangle();
        layer.setSize(stage.getWindowWidth(), stage.getWindowHeight());
        layer.color(0.5, 0.5, 0.5, 0.78);
        layer.setZ(1);
        layer.load();

        foreground = emo.SpriteSheet(getHdImageName("credit.png"), bgWidth, bgHeight);
        foreground.moveCenter(stageCenterX, stageCenterY);
        foreground.setZ(2);
        foreground.load();

        foreground.animate(0, 2, 200, -1);

        local btWidth  = 159;
        local btHeight = 52;

        if (useHD) {
            btWidth  = 318;
            btHeight = 104;
        }

        okButton = emo.SpriteSheet(getHdImageName("credit_button.png"), btWidth, btHeight);
        okButton.move(
            foreground.getX() + foreground.getWidth()  - okButton.getWidth(),
            foreground.getY() + foreground.getHeight() - okButton.getHeight());
        okButton.setZ(3);
        okButton.load();
        okButton.setFrame(1);
    }

    /*
     * Called when the app has gained focus
     */
    function onGainedFocus() {
        audio.playBGM();
    }

    /*
     * Called when the app has lost focus
     */
    function onLostFocus() {
        audio.pauseBGM();
    }

    function onDispose() {
        okButton.remove();
        foreground.remove();
        layer.remove();
        background.remove();

        background = null;
    }

    /*
     * touch event
     */
    function onMotionEvent(mevent) {
        local x = mevent.getX();
        local y = mevent.getY();
        if (mevent.getAction() == MOTION_EVENT_ACTION_DOWN) {
            if (okButton.contains(x, y)) {
                okButton.setFrame(0);
                audio.playSE0();
                if (!fadingOut) {
                    fadingOut = true;
                    stage.load(TitleScene(),
                        null, emo.AlphaModifier(0, 1, 500, emo.easing.CubicOut));
                }
            }
        }
    }
}

"""



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Custom Lexer For Config Files')
        self.setGeometry(50, 200, 400, 400)
        self.editor = QsciScintilla(self)
        self.editor.setUtf8(True)

# LINES' NUMBER IN THE MARGIN
        self.editor.setMarginLineNumbers(1,True)
        self.editor.setMarginWidth(1, QString("-------"))
                # OK for 3 digits. This was found by direct tests...
# WRAPING
        self.editor.setWrapMode(True)

        self.setCentralWidget(self.editor)
        self.lexer = ConfigLexer(self.editor)
        self.editor.setLexer(self.lexer)
        self.editor.setText(_sample)


class ConfigLexer(QsciLexerCustom):
    def __init__(self, parent):
        QsciLexerCustom.__init__(self, parent)
        self._styles = {
            0: 'Default',
            1: 'FirstLevelTitle',
            2: 'SecundLevelTitle',
            3: 'Green',
            4: 'Digits',
            5: 'KeyWord1',
            6: 'KeyWord2',
            7: 'KeyWord3',
            8: 'KeyWord4',
            }
        for key,value in self._styles.iteritems():
            setattr(self, value, key)
            
        self.lis = QStringList()
        self.lis<<"class" << "function"
        self.words1 = ['class','int', 'str', 'local', 'const', 'function', 'return', 'break']
        """
        'int', 'str', 'local', 'const', 'function', 'return', 'break',
        'continue', 'extends', 'constructor', 'foreach', 'for',
        'while', 'do', 'case', 'try', 'vargc', 'default', 'resume', 'typeof',
        'vargv', 'catch', 'delegate', 'instanceof', 'delete', 'if', 'switch',
        'parent', 'clone', 'else', 'in', 'this', 'yield', 'enum', 'throw',
        'static'
        ]
    """
        self.words2 = ['true', 'false', 'null']

        self.words3 = [
        'rawdelete', 'rawin', 'array', 'seterrorhandler', 'setdebughook',
        'enabledebuginfo', 'getroottable', 'setroottable', 'getconsttable',
        'setconsttable', 'assert', 'print', 'compilestring', 'collectgarbage',
        'type', 'getstackinfos', 'newthread', 'tofloat', 'tostring',
        'tointeger', 'tochar', 'weakref', 'slice', 'find', 'tolower',
        'toupper', 'len', 'rawget', 'rawset', 'clear', 'append', 'push',
        'extend', 'pop', 'top', 'insert', 'remove', 'resize', 'sort',
        'reverse', 'call', 'pcall', 'acall', 'pacall', 'bindenv', 'instance',
        'getattributes', 'getclass', 'getstatus', 'ref'
        ]

        self.words4 = [
        'init', 'dest', 'onLoad', 'onDispose', 'onGainedFocus','onMotionEvent',
        'onLostFocus','onUpdate'
        ]

    def language(self):
        return 'Squirrel'

    def foldCompact(self):
        return self._foldcompact

    def setFoldCompact(self, enable):
        self._foldcompact = bool(enable)

    def description(self, style):
        return self._styles.get(style, '')

    def defaultColor(self, style):
        if style == self.Default:
            return QColor('#000000')
        elif style == self.FirstLevelTitle:
            return QColor('#FF0000')
        elif style == self.SecundLevelTitle:
            return QColor('#0000FF')
        elif style == self.Green:
            return QColor('#00FF00')
        elif style == self.Digits:
            return QColor('#AAAAAA')
        elif style == self.KeyWord1:
            return QColor('#8000FF')
        elif style == self.KeyWord2:
            return QColor('#400080')
        elif style == self.KeyWord3:
            return QColor('#FF0000')
        elif style == self.KeyWord4:
            return QColor('#000000')

        return QsciLexerCustom.defaultColor(self, style)

    def defaultFont(self, style):
        font = QsciLexerCustom.defaultFont(self, style)

        if style == self.FirstLevelTitle or style == self.SecundLevelTitle:
            font.setBold(True)
        elif style == self.Green:
            font.setBold(True)
            font.setUnderline(True)

        return font

    def defaultPaper(self, style):
# Here we change the color of the background.
# We want to colorize all the background of the line.
# This is done by using the following method defaultEolFill() .
        if style == self.SecundLevelTitle:
            return QColor('#FFFF99')
        elif style == self.Digits:
            return QColor('#FFCC66')

        return QsciLexerCustom.defaultPaper(self, style)

    def defaultEolFill(self, style):
# This allowed to colorize all the background of a line.
        if style == self.SecundLevelTitle:
            return True
        return QsciLexerCustom.defaultEolFill(self, style)
    
    def paintKeywords(self,source,start):
        for word in self.lis:
            word = QString(word)
            if(source.contains(word)):
                p = source.count(word)
                index = 0
                while (p != 0):
                    begin = source.indexOf(word,index)
                    index = begin +1
                    self.startStyling (start + begin)
                    self.setStyling (len(word), self.Green)
                    self.startStyling (start + begin)
                    p-=1

        
    def styleText(self, start, end):
        editor = self.editor()
        if editor is None:
            return

        SCI = editor.SendScintilla
        set_style = self.setStyling

        source = ''
        if end > editor.length():
            end = editor.length()
        if end > start:
            data = bytearray(end - start + 1)
            source = QString(data)
            SCI(QsciScintilla.SCI_GETTEXTRANGE, start, end, source)
        if not source:
            return
        self.paintKeywords(source, start)
        #self.startStyling(start, 0x1f)

        #index = SCI(QsciScintilla.SCI_LINEFROMPOSITION, start)
        

        """
        for line in source.splitlines(True):
# Try to uncomment the following line to see in the console
# how Scintiallla works. You have to think in terms of isolated
# lines rather than globally on the whole text.
          #  print line

            length = len(line)

            if line.startswith('+'):
                newState = self.FirstLevelTitle
            elif line.startswith('\t+') or line.startswith('    +'):
                newState = self.SecundLevelTitle
            else:
                pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index) - length + 1
                i = 0
                while i < length:
                    wordLength = 1

                    self.startStyling(i + pos, 0x1f)

                    if chr(line[i]) in '0123456789':
                        #newState = self.Digits
                        pass
                    else:
                        newState = self.gett(line[i:])
                        wordLength = 5
                        
                        
                        if line[i:].startswith("class"):
                                newState = self.KeyWord2
                                wordLength = len('class')
                        elif line[i:].startswith('function'):
                                newState = self.KeyWord2
                                wordLength = len('function')
                        elif line[i:].startswith('null'):
                                newState = self.KeyWord2
                                wordLength = len('null')
                        else:
                                    newState = self.Default
                                

                    i += wordLength
                    set_style(wordLength, newState)
                newState = None

            if newState:
                set_style(length, newState)

            index += 1
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
