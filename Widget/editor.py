from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciLexerPython ,QsciAPIs
from globals import ospathjoin,workDir

class Editor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self,fontSize=10,fontName='Courier',parent=None):
        super(Editor, self).__init__(parent)
        
        
        font = QFont()
        font.setFamily(fontName)
        font.setFixedPitch(True)
        font.setPointSize(fontSize)
        self.setFont(font)
        self.setMarginsFont(font)
        #self.addAction(QAction("gg",self))
        #self.findFirst("function",False,True,True,True)
        #self.setEdgeColumn(70)
        #self.setEdgeColor(QColor(0,0,0))
        #self.setEdgeMode(self.EDGE_LINE)
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
        self.registerImage(0,QPixmap(":/Icons/class_obj.gif"))
        self.registerImage(1,QPixmap(":/Icons/method_obj.gif"))
        self.registerImage(2,QPixmap(":/Icons/field_public_obj.gif"))

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))
        
        
        self.lexer = QsciLexerPython()
        #print ospathjoin(workDir,"emo.api")
        self.api = QsciAPIs(self.lexer)
        #api.load(ospathjoin(workDir,"emo.api"))
        self.code_complete()
        self.api.prepare()
        self.lexer.setDefaultFont(font)
        self.setLexer(self.lexer) #Very important do not change line otherwise gg
        
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        #self.setAutoCompletionSource(QsciScintilla.AcsAll)
        #self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
        

    def code_complete(self):
        self.api.add("emo.Runtime?0(use = runtime)")
        self.api.add("runtime.import?1(filename)")
        self.api.add("emo.Runtime.import?1(filename)")
        self.api.add("runtime.log?1(LOG_INFO,msg)")
        self.api.add("runtime.info?1(msg)")
        self.api.add("runtime.error?1(msg)")
        self.api.add("runtime.warn?1(msg)")
        self.api.add("runtime.setLogLevel?1(LOG_WARN);")
        self.api.add("runtime.setOptions?1(OPT_ORIENTATION_PORTRAIT)")
        self.api.add("OPT_ORIENTATION_PORTRAIT?2")
        self.api.add("OPT_ORIENTATION_LANDSCAPE?2")
        self.api.add("OPT_ORIENTATION_LANDSCAPE_LEFT?2 (*iOS Only*)")
        self.api.add("OPT_ORIENTATION_LANDSCAPE_RIGHT?2 (*iOS Only*)")
        self.api.add("runtime.os?1()")
        self.api.add("OS_ANDROID?2")
        self.api.add("OS_IOS?2")
        self.api.add("runtime.device?1()")
        self.api.add("runtime.isSimulator?1()")
        self.api.add("runtime.finish(?1Finshes activity *android) ")
        self.api.add("emo.Runtime.clearTextureCache?1()")
        self.api.add("emo.Runtime.compilebuffer?1(script)")
        self.api.add("emo.Runtime.compile?1(script, TYPE_ASSET)")
        self.api.add("emo.Runtime.compile?1script, TYPE_DOCUMENT)")
        self.api.add("emo.Runtime.compile?1(script) ")
        self.api.add("emo.Runtime.getDocumentDir?1()")
        self.api.add("emo.Runtime.enableSimpleLog?1(enable = true *iOS)")
        self.api.add("emo.Runtime.enableSimpleLogWithLevel?1(enable = true);")
        self.api.add("emo.Runtime.random?1()")
        self.api.add("emo.Runtime.random?1(max)")
        self.api.add("emo.Runtime.getDefaultLocale?1()")
        self.api.add("emo.Runtime().uptime?1()")
        
        #Stage
        self.api.add("emo.Stage?0(use = stage)")
        self.api.add("stage.load?1()")
        self.api.add("stage.load?1(nextScene, currentSceneModifier, nextSceneModifier, immediate)")
        self.api.add("stage.getWindowWidth?1()")
        self.api.add("stage.windowWidth?1(value)")
        self.api.add("stage.getWindowHeight?1()")
        self.api.add("stage.windowHeight?1(value)")
        self.api.add("stage.viewport?1(width, height)")
        self.api.add("stage.ortho?1(width, height)")
        self.api.add("stage.interval?1(100)")
        self.api.add("stage.getCenterX?1()")
        self.api.add("stage.getCenterY?1()")
        self.api.add("stage.setContentScale?1()")
        
        #Sprite
        self.api.add("emo.Sprite?0(imageFile)")
        self.api.add("sprite.load?1()")
        self.api.add("sprite.hide?1()")
        self.api.add("sprite.show?1()")
        self.api.add("sprite.alpha?1(value)")
        self.api.add("sprite.red?1(1)")
        self.api.add("sprite.green?1(1)")
        self.api.add("sprite.blue?1(1)")
        self.api.add("sprite.color?1(0, 0, 0, 1)")
        self.api.add("sprite.red?1()")
        self.api.add("sprite.green?1()")
        self.api.add("sprite.blue?1()")
        self.api.add("sprite.isLoaded?1()")
        self.api.add("sprite.move?1(x,y)")
        self.api.add("sprite.getX?1()")
        self.api.add("sprite.getY?1()")
        self.api.add("sprite.getZ?1()")
        self.api.add("sprite.setZ?1(1)")
        self.api.add("sprite.getWidth?1()")
        self.api.add("sprite.getHeight?1()")
        self.api.add("sprite.setWidth?1(width)")
        self.api.add("sprite.setHeight?1(height)")
        self.api.add("sprite.setSize?1(width,height)")
        self.api.add("sprite.scale?1(scaleX, scaleY)")
        self.api.add("sprite.scale?1(scaleX, scaleY, centerX, centerY)")
        self.api.add("sprite.getScale?1()")
        self.api.add("sprite.getScaleX?1()")
        self.api.add("sprite.getScaleY?1()")
        self.api.add("sprite.rotate?1(angle)")
        self.api.add("sprite.rotate?1(angle, centerX, centerY)")
        self.api.add("sprite.getAngle?1()")
        self.api.add("sprite.remove?1()")
        self.api.add("sprite.contains?1(x,y)")
        self.api.add("sprite.collidesWith?1(otherSprite)")
        self.api.add("sprite.getName?1()")
        self.api.add("sprite.addModifier?1(modifier(from, to, duration, equation, repeatCount=0, startTime = null))")
        
        #Rectangle Extends sprite
        self.api.add("emo.Rectangle?0(use = rectangle)")
        self.api.add("rectangle.load?1()")
        self.api.add("rectangle.setSize?1()")
        
        #Line
        self.api.add("emo.Line?0()")
        self.api.add("line.setWidth?1(value)")
        self.api.add("line.move?1(startX, startY, endX, endY);")
        self.api.add("line.load?1()")
        
        #TextSprite extends MapSprite
        self.api.add("emo.TextSprite?0(name,textbase,width,height,border = null,margin = null)")
        self.api.add("text.setText?1()")
        
        #FontSprite extends sprite
        self.api.add("emo.FontSprite?0(name,fontsize = null,fontface = null,isBold = false,isItalic = false)")
        self.api.add("text.setParam?1()")
        self.api.add("text.reload?1()")
        self.api.add("text.reload?1(name)")
        
        #SpriteSheet extends sprite
        self.api.add("emo.SpriteSheet?0(name, width, height, border = 0, margin=0, frameIndex=0) use = spritesheet")
        self.api.add("emo.SpriteSheet?0(xml_formatted_texture_atlas_data)")
        self.api.add("spritesheet.setFrame?1(1)")
        self.api.add("spritesheet.selectFrame?1()")
        self.api.add("spritesheet.animate?1(startFrame, frameCount, interval, loopCount = 0)")
        self.api.add("spritesheet.animate?1(frame indices, null, interval, loopCount = 0)")
        self.api.add("spritesheet.pause?1()")
        self.api.add("spritesheet.pauseAt?1(frame)")
        self.api.add("spritesheet.stop?1()")
        self.api.add("spritesheet.load?1()")
        self.api.add("spritesheet.load?1(x, y, frameIndex)")
        self.api.add("spritesheet.getFrameIndex?1()")
        self.api.add("spritesheet.getFrameCount?1()")
        self.api.add("spritesheet.isAnimationFinished?1()")
        
        #MapSprite extends Sprite
        self.api.add("emo.MapSprite?0(name, frameWidth, frameHeight, border = 0, margin = 0)")
        self.api.add("mapsprite.setTile?1(tiles)")
        self.api.add("mapsprite.clearTiles?1()")
        self.api.add("mapsprite.addRow?1(tile)")
        self.api.add("mapsprite.setTileAt?1(row, column, value)")
        self.api.add("mapsprite.getTileAt?1(row, column)")
        self.api.add("mapsprite.getTileIndexAtCoord?1(x, y)")
        self.api.add("mapsprite.getTilePositionAtCoord?1(x, y)")
        self.api.add("mapsprite.load?1()")
        self.api.add("mapsprite.load?1(x, y)")
        
        #Controller
        self.api.add("emo.AnalogOnScreenController?0(base_name ='controller_base.png', knob_name='controller_knob.png', alpha=0.5) use=controller")
        self.api.add("emo.DigitalOnScreenController?0(base_name ='controller_base.png', knob_name='controller_knob.png', alpha=0.5) use=controller")
        self.api.add("controller.updateInterval = 16")
        self.api.add("onControlEvent?1(controller, controlX, controlY, hasChanged)")
        
        #Modifier
        self.api.add("emo.AlphaModifier?0(from, to, duration, equation, repeatCount=0, startTime = null)")
        self.api.add("emo.ScaleModifier?0(from, to, duration, equation, repeatCount=0, startTime = null)")
        self.api.add("emo.RotateModifier?0(from, to, duration, equation, repeatCount=0, startTime = null)")
        self.api.add("emo.MoveModifier?0(from, to, duration, equation, repeatCount=0, startTime = null)")
        self.api.add("emo.MoveCenterModifier?0(from, to, duration, equation, repeatCount=0, startTime = null)")
        self.api.add("emo.ColorModifier?0(from, to, duration, equation, repeatCount=0, startTime = null)")
        
        #Easing
        self.api.add("emo.easing?0")
        self.api.add("emo.easing.Linear?2")
        self.api.add("emo.easing.CubicIn?2")
        self.api.add("emo.easing.CubicOut?2")
        self.api.add("emo.easing.CubicInOut?2")
        self.api.add("emo.easing.BackIn?2")
        self.api.add("emo.easing.BackOut?2")
        self.api.add("emo.easing.BackInOut?2")
        self.api.add("emo.easing.ElasticIn?2")
        self.api.add("emo.easing.ElasticOut?2")
        self.api.add("emo.easing.ElasticInOut?2")
        self.api.add("emo.easing.BounceOut?2")
        self.api.add("emo.easing.BounceIn?2")
        self.api.add("emo.easing.BounceInOut?2")
        self.api.add("emo.easing.ExpoIn?2")
        self.api.add("emo.easing.ExpoOut?2")
        self.api.add("emo.easing.ExpoInOut?2")
        self.api.add("emo.easing.QuadIn?2")
        self.api.add("emo.easing.QuadOut?2")
        self.api.add("emo.easing.QuadInOut?2")
        self.api.add("emo.easing.SineIn?2")
        self.api.add("emo.easing.SineOut?2")
        self.api.add("emo.easing.SineInOut?2")
        self.api.add("emo.easing.CircIn?2")
        self.api.add("emo.easing.CircOut?2")
        self.api.add("emo.easing.CircInOut?2")
        self.api.add("emo.easing.QuintIn?2")
        self.api.add("emo.easing.QuintOut?2")
        self.api.add("emo.easing.QuintInOut?2")
        self.api.add("emo.easing.QuartIn?2")
        self.api.add("emo.easing.QuartOut?2")
        self.api.add("emo.easing.QuartInOut?2")
        
        #Audio
        self.api.add("emo.Audio?0(channelCount)")
        self.api.add("audio.createChannel?1(channelIndex) use=ch0")
        self.api.add("emo.Audio?0.vibrate?1(vibration requires android.permission.VIBRATE permission)")
        
        #DataBase
        self.api.add("emo.Database?0(use = database)")
        self.api.add("database.getPath?1(DEFAULT_DATABASE_NAME)")
        self.api.add("database.getLastError?1()")
        self.api.add("database.getLastErrorMessage?1()")
        self.api.add("database.deleteDatabase?1(DEFAULT_DATABASE_NAME)")
        
        #Preference
        self.api.add("emo.Preference?0(use = preference)")
        self.api.add("preference.openOrCreate?1() == EMO_NO_ERROR")
        self.api.add("preference.open?1() == EMO_NO_ERROR")
        self.api.add("preference.set?1(key, value)")
        self.api.add("preference.get?1(key)")
        self.api.add("preference.keys?1()")
        self.api.add("preference.del?1(key)")
        self.api.add("preference.close?1()")
        
        #Motion
        self.api.add("onMotionEvent?1(mevent)")
        self.api.add("mevent.getAction?1() = MOTION_EVENT_ACTION_DOWN")
        self.api.add("mevent.getPointerId?1(Android Only)")
        self.api.add("mevent.getX?1()")
        self.api.add("mevent.getY?1()")
        self.api.add("MOTION_EVENT_ACTION_DOWN?2")
        self.api.add("MOTION_EVENT_ACTION_UP?2")
        self.api.add("MOTION_EVENT_ACTION_MOVE?2")
        self.api.add("MOTION_EVENT_ACTION_CANCEL?2")
        self.api.add("MOTION_EVENT_ACTION_OUTSIDE?2")
        self.api.add("MOTION_EVENT_ACTION_POINTER_DOWN?2")
        self.api.add("MOTION_EVENT_ACTION_POINTER_UP?2")
        
        #keys
        self.api.add("onKeyEvent?1(kevent)")
        self.api.add("kevent.getAction(?1) = KEY_EVENT_ACTION_DOWN")
        self.api.add("kevent.getKeyCode?1()")
        self.api.add("kevent.getRepeatCount?1()")
        self.api.add("kevent.MetaState?1()")
        self.api.add("KEY_EVENT_ACTION_DOWN")
        
        #Sensor
        self.api.add("emo.Event?0(use = event)")
        self.api.add("event.registerSensors?1(SENSOR_TYPE_ACCELEROMETER) onLoad")
        self.api.add("event.enableSensor?1(SENSOR_TYPE_ACCELEROMETER, 100) onGainedFocus")
        self.api.add("event.disableSensor?1(SENSOR_TYPE_ACCELEROMETER) onLostFocus")
        self.api.add("onSensorEvent?1(sevent)")
        self.api.add("SENSOR_TYPE_ACCELEROMETER?2")
        self.api.add("sevent.getType?1() == SENSOR_TYPE_ACCELEROMETER")
        self.api.add("sevent.getAccelerationX?1()")
        self.api.add("sevent.getAccelerationY?1()")
        self.api.add("sevent.getAccelerationZ?1()")
        
        #Draw
        self.api.add("event.enableOnDrawCallback?1(5000)")
        self.api.add("onDrawFrame?1(dt)")
        self.api.add("event.disableOnDrawCallback?1()")
        self.api.add("onLowMemory?1()")
        self.api.add("onError?1(message)")
        
        #Http
        self.api.add("emo.Net.request?1(MY_REQUEST_NAME, 'http://www.example.com/')")
        self.api.add("emo.Net.request?1(MY_REQUEST_NAME_BY_GET, 'http://www.example.com/', 'GET'', 1000)")
        self.api.add("emo.Net.request?1(MY_REQUEST_NAME_BY_POST, 'http://www.example.com/','POST', 1000, 'key1', 'value1', 'key2', 'value2')")
        self.api.add("onNetCallback?1(name, response, err)")
        #Physics
        self.api.add("")
        self.api.add("")               
        self.api.add("")
        self.api.add("")
        self.api.add("")
        self.api.add("")


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
        

