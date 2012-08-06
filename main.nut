stage      <- emo.Stage();//dfdffgfg
event      <- emo.Event();
runtime    <- emo.Runtime();
database   <- emo.Database();
preference <- emo.Preference();

useHD   <- false;
kawazOn <- false;
debug   <- true;
//audio <- AudioLoader();
// preloaded sprites
background          <- null;

//AT DF MP MV R A+ D+ troops spells
//garret = [23,21,0,6,3,2,2,{},{}]

local scoreText     = null;
local timesLeftText = null;
local highScoreText = null;
local fpsText       = null;
    
local main_layer0   = null;
local main_layer1   = null;
local main_ready    = null;
local main_go       = null;
local main_finish   = null;
    
local retry_button  = null;
local return_button = null;
    
local targets       = null;

local stageCenterX  = null;
local stageCenterY  = null;



class World {
	objects = [];
    static map = [];
	
	function add(obj){
	  objects.append(obj);
	}
	function del(obj){
	  local index = objects.find(obj);
	  objects.remove(index);
	}
	function print(){
		foreach(val in objects)
		{
		::print(value);
		}
	}
}

class Troop{
    hp=10;
	at=0;
	df=0
	mv=0
	tile=0
	cost=0
	sprite = emo.SpriteSheet("dog.png", 34, 42, 1, 1);
	text = emo.TextSprite("font_16x16.png",
        " !\"c*%#'{}@+,-./0123456789:;[|]?&ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        16, 16, 2, 1);
		
	constructor(){
	
	}
	
	
}

enum side{
  hero,gtroop,enemy,btroop,npc
}


class Tile{
	id=0;
	x=50;
	y=50;
	mod=0;
}

class Unit extends emo.SpriteSheet {
	id="0";
    hp=10;
	at=0;
	df=0;
	mv=0;
	tile=null;
	x=50;
	y=50;
	z=1;
	currentFrame = 0;
	isSelected = 0;
	tileMarker = emo.Rectangle();
	isPlayer = true;
	isTroop = false;
	isEnemy = false;
	turnEnd = false;
	
	//sprite = emo.SpriteSheet("allies.png",23,35,0,0);
	text = emo.TextSprite("font_16x16.png",
        " !\"c*%#'{}@+,-./0123456789:;[|]?&ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        16, 16, 2, 1);
		
	constructor(_id){
		id=_id;
		base.constructor("allies.png",23,35,0,0);
		//x=tile.x;
		//y=tile.y;
	//	saveData(); //First time needed to create the store the default key values
	//	print("hero created");
	//	loadData();
		load(x,y);
		setFrame(1);
		tileMarker.setSize(getWidth(), getWidth());
        tileMarker.color(1, 0, 0);
        tileMarker.hide();
        tileMarker.setZ(99);
        tileMarker.load();
		tileMarker.move(x,y);
	
	}
	
	function getTile(){
		return tile;
	}
	
	function setTile(_tile){
		tile=_tile;
	}
	
	
	function heal(_hp){
		if(hp<=10)
	     hp+=_hp;
	}
	
	function loadData(){
	 for (local i = 0; i < 5; i++)
	 {
	 print("loading data"); 
	 }
	 if (preference.openOrCreate() == EMO_NO_ERROR) {
			id = preference.get("id");
            x = preference.get("x"+id).tointeger();
            y = preference.get("y"+id).tointeger();
			z = preference.get("z"+id).tointeger();
			at = preference.set("at"+id, at).tointeger();
			df = preference.set("df"+id, df).tointeger();
			hp = preference.set("hp"+id, hp).tointeger();
			mv = preference.set("mv"+id, mv).tointeger();
            preference.close();
        } else {
            print("failed to store the position");
            print(format("ERROR CODE:    %d", database.getLastError()));
            print(format("ERROR MESSAGE: %s", database.getLastErrorMessage()));
        }
	}
	
	function saveData() {
		for (local i = 0; i < 5; i++)
		{
		print("Saving data"); 
		}
        if (preference.open() == EMO_NO_ERROR) {
			preference.set("id", id);
            preference.set("x"+id, getX());
			preference.set("y"+id, getY());
			preference.set("z"+id, getZ());
			preference.set("at"+id, at);
			preference.set("df"+id, df);
			preference.set("hp"+id, hp);
			preference.set("mv"+id, mv);
           // local keys = preference.keys();
           // for (local i = 0; i < keys.len(); i++) {
           //     print(format("SAVED: %s = %s", keys[i], preference.get(keys[i])));
           // }
            
            // if you want to delete the preference value, uncomment below.
            //preference.del(KEY_RECTANGLE_X);
            //preference.del(KEY_RECTANGLE_Y);
            
            preference.close();
    
            // if you want to delete emo framework database completely, uncomment below.
            // NOTE: by using deleteDatabase, all of the tables used by emo framework are deleted.
            //       this function might be useful for developing or testing your program.
            // database.deleteDatabase(DEFAULT_DATABASE_NAME);
        } else {
            print("failed to store the latest position");
        }
    }
	
	function remove(){
		base.remove();
		tileMarker.remove();
		
	}
	
}

class Hero extends Unit
{	
	level=0;
	faction=0;
	mp = 0;
	data = [23,21,0,6,3,2,2,{},{}];
	atr=0;
	dfr =0;
	constructor(_id){
		base.constructor(_id);
		//emo.Event().addMotionListener(this);
	}	
	
	function regen(_mp){
	 if(mp<=10)
	    mp+=_mp;
	}
	
	function onMotionEvent(mevent) {
        local mx = mevent.getX();
        local my = mevent.getY();
		local timeLast = 0;
		local timeElapsed = mevent.getEventTime() - 10;
		print(isSelected);
		if(timeLast == 0)
		{
		if(isSelected==1){
		  if(mx > getWidth() && my > getHeight())
		  {
		  moveCenter(mx,my);
		  x=getX();
		  y=getY();
		  tileMarker.moveCenter(x,y);
		  tileMarker.hide();
		  isSelected = 0;
		  }
		}
        if (mevent.getAction() == MOTION_EVENT_ACTION_DOWN ||
			mevent.getAction() == MOTION_EVENT_ACTION_UP ||
            mevent.getAction() == MOTION_EVENT_ACTION_CANCEL  ||
            mevent.getAction() == MOTION_EVENT_ACTION_OUTSIDE ||
            mevent.getAction() == MOTION_EVENT_ACTION_POINTER_UP) 
		{
			
            if (contains(mx, my)) {
                print("Clicked");
				isSelected = 1;
				tileMarker.show();
				print("this is X");
				print(getX());
				print("this is Y");
				print(getY());
				print("this is Z");
				print(getZ());
				print("Time");
				print(timeElapsed);
				//timeLast= mevent.getEventTime() - timeElapsed;
				
				
			//	currentFrame++;
				if (currentFrame >= getFrameCount()) {
                currentFrame = 0;
				}			
				setFrame(currentFrame);	
            }
			else{
				isSelected = 0;
			}
		}
	  }
    }
	
	function remove() {
		base.remove();
       // emo.Event().removeOnUpdateListener(this);
        emo.Event().removeMotionListener(this);
	//	sprite.remove();
	//	text.remove();
       // return base.remove();
    }
}
const BLOCK_SIZE   = 32;

class Scenario1 {

    // create map sprite with 32x32, 2 pixel border and 2 pixel margin
    sprite = emo.MapSprite("blocks.png", BLOCK_SIZE, BLOCK_SIZE, 2, 2);
    
    // 16x16 text sprite with 2 pixel border and 1 pixel margin
    text = emo.TextSprite("font_16x16.png",
        " !\"c*%#'{}@+,-./0123456789:;[|]?&ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        16, 16, 2, 1);
        
    lastMoveX  = 0;
    lastMoveY  = 0;
    
    tileMarker = emo.Rectangle();

    /*
     * Called when this class is loaded
     */
    function onLoad() {
        print("onLoad"); 

        // Below statements is an example of multiple screen density support.
        // (i.e. Retina vs non-Retina, cellular phone vs tablet device).
        if (stage.getWindowWidth() > 320) {
            // if the screen has large display, scale contents twice
            // that makes the stage size by half.
            // This examples shows how to display similar-scale images
            // on Retina and non-Retina display.
            stage.setContentScale(stage.getWindowWidth() / 320.0);
        }
        
        local tiles = [
            [-1,  8,  9, 10, -1, 11, 12, 13, 14, 15, -1, -1, -1, -1, -1,  8,  9, 10, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1,  8,  9, 10, -1, -1, -1,  8,  9, 10, -1, 11, 12, 13, 14, 15, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 13, 14, 15, -1, -1, -1,  8,  9, 10, -1, 13, 14, 15, -1, -1, -1,  8,  9, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 18, 19, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 16, 17, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1   0,  1,  2,  3,  4,  5, -1,  6,  7, -1   7,  6,  7,  6,  7,  6,  7,  6,  7, -1],
        ];
        sprite.setMap(tiles);
        sprite.move(0, stage.getWindowHeight() - (BLOCK_SIZE * tiles.len()));

        // load sprite to the screen
        sprite.load();
        
        // change the text
        text.setText("DRAG TO MOVE THE TILE");
        text.scale(0.7, 0.7);
        
        local tX = (stage.getWindowWidth()  - text.getScaledWidth())  / 2;
        text.move(tX, text.getScaledHeight());

        text.load();
        
        tileMarker.setSize(BLOCK_SIZE, BLOCK_SIZE);
        tileMarker.color(1, 0, 0);
        tileMarker.hide();
        tileMarker.setZ(99);
        tileMarker.load();
    }

    /*
     * Called when the app has gained focus
     */
    function onGainedFocus() {
        print("onGainedFocus");
    }

    /*
     * Called when the app has lost focus
     */
    function onLostFocus() {
        print("onLostFocus"); 
    }

    /*
     * Called when the class ends
     */
    function onDispose() {
        print("onDispose");
        
        // remove sprite from the screen
        sprite.remove();
    }

    /*
     * this tiled map can be dragged along x-axis
     */
    function onMotionEvent(mevent) {
        if (mevent.getAction() == MOTION_EVENT_ACTION_DOWN) {
            lastMoveX = mevent.getX();
            lastMoveY = mevent.getY();
        
            updateTileMarker(mevent.getX(), mevent.getY());
            tileMarker.show();
        } else if (mevent.getAction() == MOTION_EVENT_ACTION_MOVE) {
            local x = sprite.getX() - (lastMoveX - mevent.getX());
            local y = sprite.getY() - (lastMoveY - mevent.getY());
            if (x <= 0 && x >= stage.getWindowWidth() - sprite.getWidth()) { 
                sprite.move(x, y);
            }
            lastMoveX = mevent.getX();
            lastMoveY = mevent.getY();
            
            updateTileMarker(mevent.getX(), mevent.getY());
        } else if (mevent.getAction() == MOTION_EVENT_ACTION_UP) {
            tileMarker.hide();
        }
    }
    
    function updateTileMarker(x, y) {
        // move the marker (the red box) to the given position.
        local tilePos   = sprite.getTilePositionAtCoord(x, y);
        tileMarker.move(tilePos.x, tilePos.y);
        
         //to change the tile dynamically at given position, uncomment below.
        local tileIndex = sprite.getTileIndexAtCoord(x, y);
   //     print(format("change %d x %d tile %d -> %d",
   //         tileIndex.x, tileIndex.y, sprite.getTileAt(tileIndex.x, tileIndex.y), 1));
        sprite.setTileAt(tileIndex.row, tileIndex.column, 1);
    }
}
class Main {
	scale = stage.getWindowWidth() / 160.0;
	text = emo.TextSprite("font_16x16.png",
        " !\"c*%#'{}@+,-./0123456789:;[|]?&ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        16, 16, 2, 1);
		
	//hero = Hero("0");
	rectangles = {};
	stageSize=1.0;
	y0 =0;
	y1 =0;
		
    function onLoad() {
        print("onLoad"); 
		setSizing();
        text.setText("HELLO, WORLD!");
        local x = (stage.getWindowWidth()  - text.getWidth())  / 2;
        local y = (stage.getWindowHeight() - text.getHeight()) / 2;
        text.move(x-100, y);
        text.load();
		
        //img.scale(4, 4);
		
	//	event.enableOnDrawCallback(33);
	//	img.animate(0,5,200,-1);
    }

    function onGainedFocus() {
		//hero.loadData();
        print("onGainedFocus");
    }

    function onLostFocus() {
        print("onLostFocus"); 
		//hero.saveData();
	//	hero.remove();
    }

    function onDispose() {
        print("onDispose");
		//hero.saveData();
	//	hero.remove();
    }
     
	 
	function setSizing(){
		 if (stage.getWindowWidth() > 320) {
            stage.setContentScale(scale);
        }  
	}
	 
     /*
     * touch event
     */
    function onMotionEvent(mevent) {
        // pointer id is a unique id of the pointer.
        local id = mevent.getPointerId();
        local action = mevent.getAction();
		print("ID is : " + id);
		

        if (!rectangles.rawin(id)) {
            // if new pointer comes in, create new rectangle
            local rectangle = emo.Rectangle();
            rectangle.setSize(stage.getWindowWidth() * 0.2, stage.getWindowWidth() * 0.2);
            rectangle.color(1, 0, 0);
            rectangle.moveCenter(mevent.getX(), mevent.getY());
            rectangle.load();
            
            // add rectangle to the hash table.
            rectangles[id] <- rectangle;
        }
        if (action == MOTION_EVENT_ACTION_UP || action == MOTION_EVENT_ACTION_POINTER_UP) {
            print("UP: " + id);
        } else if (action == MOTION_EVENT_ACTION_DOWN || action == MOTION_EVENT_ACTION_POINTER_DOWN) { 
            print("DOWN: " + id);
        }
        handleTouch(rectangles[id], mevent);
		if(y0 != 0 && y1 != 0){
			stageSize = y1-y0;
			print(stageSize);
		}
		
		
    }
    
    /*
     * move and remove the rectangle
     */
    function handleTouch(rectangle, mevent) {
        local action = mevent.getAction();
        if (action == MOTION_EVENT_ACTION_DOWN || action == MOTION_EVENT_ACTION_POINTER_DOWN) {
            rectangle.moveCenter(mevent.getX(), mevent.getY());
        } else if (action == MOTION_EVENT_ACTION_MOVE) {
            rectangle.moveCenter(mevent.getX(), mevent.getY());
        } else if (action == MOTION_EVENT_ACTION_UP ||
                   action == MOTION_EVENT_ACTION_CANCEL ||
                   action == MOTION_EVENT_ACTION_OUTSIDE ||
                   action == MOTION_EVENT_ACTION_POINTER_UP) {
            delete rectangles[mevent.getPointerId()];
            rectangle.remove();
        }
    }
    
}

class Main2 {

    // 16x16 text sprite with 2 pixel border and 1 pixel margin
    text = emo.TextSprite("font_16x16.png",
        " !\"c*%#'{}@+,-./0123456789:;[|]?&ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        16, 16, 2, 1);
	y0 =0;
	y1=0;
        
    /*
     * Called when this class is loaded
     */
    function onLoad() {
        print("onLoad"); 
        
        // Below statements is an example of multiple screen density support.
        // (i.e. Retina vs non-Retina, cellular phone vs tablet device).
        if (stage.getWindowWidth() > 320) {
            // if the screen has large display, scale contents twice
            // that makes the stage size by half.
            // This examples shows how to display similar-scale images
            // on Retina and non-Retina display.
            stage.setContentScale(stage.getWindowWidth() / 320.0);
        }
        
        // change the text
        text.setText("DRAG TO TEST MULTITOUCH");
        text.scale(0.7, 0.7);
        
        local tX = (stage.getWindowWidth()  - text.getScaledWidth())  / 2;
        text.move(tX, text.getScaledHeight());

        text.load();
    }

    /*
     * Called when the app has gained focus
     */
    function onGainedFocus() {
        print("onGainedFocus");
    }

    /*
     * Called when the app has lost focus
     */
    function onLostFocus() {
        print("onLostFocus"); 
    }

    /*
     * Called when the class ends
     */
    function onDispose() {
        print("onDispose");
    }

    /*
     * touch event
     */
    function onMotionEvent(mevent) {
        // pointer id is a unique id of the pointer.
        local id = mevent.getPointerId();
        local action = mevent.getAction();
		if(id == 0){
			//print("ID is : " + id);
			y0=handleTouch(mevent);
		}
		
		if(id == 1){
			//print("ID is : " + id);
			y1=handleTouch(mevent);
		}
		text.setText(y0.tostring()+"-"+y1.tostring()+" Diff  "+fabs((y1-y0)/1000));
		stage.setContentScale(1.0);
        
    }
    
    /*
     * move and remove the rectangle
     */
    function handleTouch(mevent) {
        local action = mevent.getAction();
        if (action == MOTION_EVENT_ACTION_DOWN || action == MOTION_EVENT_ACTION_POINTER_DOWN) {
            print(mevent.getY());
        } else if (action == MOTION_EVENT_ACTION_MOVE) {
            print(mevent.getY());
        } else if (action == MOTION_EVENT_ACTION_UP ||
                   action == MOTION_EVENT_ACTION_CANCEL ||
                   action == MOTION_EVENT_ACTION_OUTSIDE ||
                   action == MOTION_EVENT_ACTION_POINTER_UP) {
           print("POINTER IS UP OUT");
        }
		return mevent.getY();
    }
}


function emo::onLoad() {
    //stage.load(Main2());
	stage.load(Scenario1());
}


