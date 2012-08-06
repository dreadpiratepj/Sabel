from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciLexerPython ,QsciAPIs

class Editor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self,fontSize=10,fontName='Courier',parent=None):
        super(Editor, self).__init__(parent)
        # Set the default font
        font = QFont()
        font.setFamily(fontName)
        font.setFixedPitch(True)
        font.setPointSize(fontSize)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))
        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.connect(self,SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow,self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"),self.ARROW_MARKER_NUM)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))
        # Set Python lexer
        # Set style for Python comments (style number 1) to a fixed-width
        # courier.
        # QsciLexerSquirrel()
        self.lexer = QsciLexerPython()
        self.api = QsciAPIs(self.lexer)
        self.lexer.setDefaultFont(font)
        self.code_complete()
        self.api.prepare()
        self.setLexer(self.lexer) #Very important do not change line otherwise gg
        
        
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
      #  self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # not too small
       # self.setMinimumSize(600, 450)


    def code_complete(self):
        #self.api.load("test.api")
        self.api.add("emo.Runtime()")
        self.api.add("emo.Runtime().uptime()")
        self.api.add("emo.Stage()")
        self.api.add("emo.Sprite()")
        self.api.add("emo.Rectangle()")
        self.api.add("emo.Line")
        self.api.add("emo.TextSprite()")
        self.api.add("emo.FontSprite()")
        self.api.add("emo.SpriteSheet()")
        self.api.add("emo.MapSprite()")
        self.api.add("emo.AnalogOnScreenController()")
        self.api.add("emo.DigitalOnScreenController()")
        
        
        #sprite
        self.api.add("sprite.addModifier(modifier(from, to, duration, equation, repeatCount=0, startTime = null))")
        
        
        
        #Controller
        self.api.add("emo.AnalogOnScreenController(base_name ='controller_base.png', knob_name='controller_knob.png', alpha=0.5) use=controller")
        self.api.add("emo.DigitalOnScreenController(base_name ='controller_base.png', knob_name='controller_knob.png', alpha=0.5) use=controller")
        self.api.add("controller.updateInterval = 16")
        self.api.add("onControlEvent(controller, controlX, controlY, hasChanged)")
        self.api.add("")
        
        #modifier
        self.api.add("emo.AlphaModifier")
        self.api.add("emo.ScaleModifier")
        self.api.add("emo.RotateModifier")
        self.api.add("emo.MoveModifier")
        self.api.add("emo.MoveCenterModifier")
        self.api.add("emo.ColorModifier")
        
        #easing
        self.api.add("emo.easing.Linear")
        self.api.add("emo.easing.CubicIn")
        self.api.add("emo.easing.CubicOut")
        self.api.add("emo.easing.CubicInOut")
        self.api.add("emo.easing.BackIn")
        self.api.add("emo.easing.BackOut")
        self.api.add("emo.easing.BackInOut")
        self.api.add("emo.easing.ElasticIn")
        self.api.add("emo.easing.ElasticOut")
        self.api.add("emo.easing.ElasticInOut")
        self.api.add("emo.easing.BounceOut")
        self.api.add("emo.easing.BounceIn")
        self.api.add("emo.easing.BounceInOut")
        self.api.add("emo.easing.ExpoIn")
        self.api.add("emo.easing.ExpoOut")
        self.api.add("emo.easing.ExpoInOut")
        self.api.add("emo.easing.QuadIn")
        self.api.add("emo.easing.QuadOut")
        self.api.add("emo.easing.QuadInOut")
        self.api.add("emo.easing.SineIn")
        self.api.add("emo.easing.SineOut")
        self.api.add("emo.easing.SineInOut")
        self.api.add("emo.easing.CircIn")
        self.api.add("emo.easing.CircOut")
        self.api.add("emo.easing.CircInOut")
        self.api.add("emo.easing.QuintIn")
        self.api.add("emo.easing.QuintOut")
        self.api.add("emo.easing.QuintInOut")
        self.api.add("emo.easing.QuartIn")
        self.api.add("emo.easing.QuartOut")
        self.api.add("emo.easing.QuartInOut")
        
        #Audio
        self.api.add("emo.Audio(channelCount) use=audio")
        self.api.add("audio.createChannel(channelIndex) use=ch0")
        self.api.add("emo.Audio.vibrate(vibration requires android.permission.VIBRATE permission)")
        
        #DataBase
        self.api.add("emo.Database(use = database)")
        self.api.add("database.getPath(DEFAULT_DATABASE_NAME)")
        self.api.add("database.getLastError()")
        self.api.add("database.getLastErrorMessage()")
        self.api.add("database.deleteDatabase(DEFAULT_DATABASE_NAME)")
        
        #Preference
        self.api.add("emo.Preference(use = preference)")
        self.api.add("preference.openOrCreate() == EMO_NO_ERROR")
        self.api.add("preference.open() == EMO_NO_ERROR")
        self.api.add("preference.set(key, value)")
        self.api.add("preference.get(key)")
        self.api.add("preference.keys()")
        self.api.add("preference.del(key)")
        self.api.add("preference.close()")
        
        #Motion
        self.api.add("onMotionEvent(mevent)")
        self.api.add("mevent.getAction() = MOTION_EVENT_ACTION_DOWN")
        self.api.add("mevent.getPointerId(Android Only)")
        self.api.add("mevent.getX()")
        self.api.add("mevent.getY()")
        self.api.add("MOTION_EVENT_ACTION_DOWN")
        self.api.add("MOTION_EVENT_ACTION_UP")
        self.api.add("MOTION_EVENT_ACTION_MOVE")
        self.api.add("MOTION_EVENT_ACTION_CANCEL")
        self.api.add("MOTION_EVENT_ACTION_OUTSIDE")
        self.api.add("MOTION_EVENT_ACTION_POINTER_DOWN")
        self.api.add("MOTION_EVENT_ACTION_POINTER_UP")
        
        #keys
        self.api.add("onKeyEvent(kevent)")
        self.api.add("kevent.getAction() = KEY_EVENT_ACTION_DOWN")
        self.api.add("kevent.getKeyCode()")
        self.api.add("kevent.getRepeatCount()")
        self.api.add("kevent.MetaState()")
        self.api.add("KEY_EVENT_ACTION_DOWN")
        
        #Sensor
        self.api.add("emo.Event(use = event)")
        self.api.add("event.registerSensors(SENSOR_TYPE_ACCELEROMETER) onLoad")
        self.api.add("event.enableSensor(SENSOR_TYPE_ACCELEROMETER, 100) onGainedFocus")
        self.api.add("event.disableSensor(SENSOR_TYPE_ACCELEROMETER) onLostFocus")
        self.api.add("onSensorEvent(sevent)")
        self.api.add("SENSOR_TYPE_ACCELEROMETER")
        self.api.add("sevent.getType() == SENSOR_TYPE_ACCELEROMETER")
        self.api.add("sevent.getAccelerationX()")
        self.api.add("sevent.getAccelerationY()")
        self.api.add("sevent.getAccelerationZ()")
        
        #Draw
        self.api.add("event.enableOnDrawCallback(5000)")
        self.api.add("onDrawFrame(dt)")
        self.api.add("event.disableOnDrawCallback()")
        self.api.add("onLowMemory()")
        self.api.add("onError(message)")
        
        #Http
        self.api.add("emo.Net.request(MY_REQUEST_NAME, 'http://www.example.com/')")
        self.api.add("emo.Net.request(MY_REQUEST_NAME_BY_GET, 'http://www.example.com/', 'GET'', 1000)")
        self.api.add("emo.Net.request(MY_REQUEST_NAME_BY_POST, 'http://www.example.com/','POST', 1000, 'key1', 'value1', 'key2', 'value2')")
        self.api.add("onNetCallback(name, response, err)")
        self.api.add("")
        self.api.add("")
        
        
        
                           
        #self.api.add("emo.")


    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

