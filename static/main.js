/**
 * Author: Oliver Bachmann
 * Asset Credits:
 *  - Asciibox
 */

// Assuming your base game dimensions are stored in variables called 'baseWidth' and 'baseHeight'
let TOTAL_WIDTH;
let VISIBLE_WIDTH_CHARACTERS;
let VISIBLE_HEIGHT_CHARACTERS;
let TOTAL_HEIGHT_CHARACTERS;
let LIMIT_TO_VISIBLE_WIDTH;
let baseWidth;
let baseHeight;

let initCalled = false;

  function updateSizes(x, y) {
    TOTAL_WIDTH = x;
    VISIBLE_WIDTH_CHARACTERS = x;
    VISIBLE_HEIGHT_CHARACTERS = y;
    TOTAL_HEIGHT_CHARACTERS = y;
    LIMIT_TO_VISIBLE_WIDTH = true;

    baseWidth = VISIBLE_WIDTH_CHARACTERS * 8;  // The total width space plus 8px for the scrollbar
    baseHeight = VISIBLE_HEIGHT_CHARACTERS * 16; // 16px at the bottom for the scrollbar

    
    config = {
        title: 'Ascii box',
        type: Phaser.AUTO,
        width: baseWidth,
        height: baseHeight,
        pixelArt: true,
        parent: "game-container",
        scene: {
          preload: preload,
          create: create,
          update: update
        },
        scale: {
            mode: Phaser.Scale.NONE, // Use custom scaling
            autoCenter: Phaser.Scale.CENTER_BOTH // Center the canvas in both horizontal and vertical
        }
    };


}

mode="html"; // html or editor
let thumbVertical;
let thumbHeight;
let thumbY = 0;
let thumbX = 0;
let isDraggingVertical = false;
let isDraggingHorizontal = false;
let insert = false;

let enableScrolling = true; // In rare case when viewing ansi files you can set this to false
let maxReachedY = 0;  // Variable to keep track of the maximum reached y coordinate

var config = {};


var backgroundColor = 0;
var shiftPressed = false;
var altgrPressed = false;
var currentX = 0;
var currentY = 0;
var startX = 0;
var startY = 0;
var scrolledXChars = 0;
var scrolledYChars = 0;
var removedYChars = 0;
var currentColor = 15;
var isColorPalette = false;
var storedTiles = [];
var canvas = [];
var canvasbg = [];
var secondCanvas = [];
var canvasColor = [];
var secondCanvasColor = [];
var specialKeyCharacterSet = 0;
    


  function initPage(dataArray) {

     // Sort the array based on minWidth for easy comparison.
     dataArray.sort((a, b) => a.minWidth - b.minWidth);

     dataArray.forEach((data) => {
         if (window.innerWidth >= data.minWidth) {
             // If window.innerWidth is greater than or equal to data.minWidth, update sizes.
             updateSizes(data.x, data.y);
         }
     });

    game = new Phaser.Game(config);
    displayWidth = game.scale.displaySize.width;
    displayHeight = game.scale.displaySize.height;
    
    scaleX = displayWidth / baseWidth;
    scaleY = window.innerHeight / baseHeight;
    
    DEFAULT_INSERT = false;
    VISIBLE_HEIGHT = Math.floor(baseHeight/16);
    console.log("VISIBLE_HEIGHT:"+VISIBLE_HEIGHT);
  
    VISIBLE_WIDTH = Math.floor(baseWidth/8);



  }

  function preload() {
     this.load.image("tiles", "static/ansi.png");
     this.load.image("ansibgs", "static/ansi.png");
     this.load.image("underscore_white", "static/underscore_white.png");
     loader = this.load;
     adder = this.add;
  }

  function writeString(string, x, y, color, func) {
      for (var i = 0; i < string.length; i++) {
            var index = getCharIndex(color, string.charCodeAt(i));
            layer.putTileAt(index, x+i, y);
      }

      if (typeof(func)=='function') {
        fields.push({
            startX : x,
            endX : x+string.length,
            startY : y,
            myfunc : func 
        });
      }
  }
 
 
function initPosition() {
    currentX = 0;
    currentY = 0;
    startX = 0;
    startY = 0;
    scrolledXChars = 0;
    scrolledYChars = 0;
    cam.scrollX = 0;
    cam.scrollY = 0;
    clearScreen();
    redrawCursor();
}

function clear() {
    initPosition();    
    for (var x = 0; x < TOTAL_WIDTH; x++) {
        for (var y = 0; y < TOTAL_HEIGHT_CHARACTERS_CHARACTERS; y++) {
        if (!canvas[y]) canvas[y]=[];
        canvas[y][x]=32;
        if (!canvasbg[y]) canvasbg[y]=[];
        canvasbg[y][x]=0;
        }
    }
    
}

    function drawbg(index, x, y, backgroundColor) {
        y = y-removedYChars;
        layer.putTileAt(index, x, y);
        if (!canvasbg[y]) {
            canvasbg[y]=[];
        }
        canvasbg[y][x]=backgroundColor;
    }

    function draw(index, x, y, currentColor) {
   
        y = y-removedYChars;

        bglayer.putTileAt(index, x, y);

            if (!canvas[y]) {
                canvas[y]=[];
            }
            canvas[y][x]=index;
            if (!canvasColor[y]) {
                canvasColor[y]=[];
            }
            canvasColor[y][x]=currentColor;
    }

    
  function create() {
    // Load a map from a 2D array of tile indices
    // prettier-ignore

    var map = [];

    for (var y = 0; y < 16*8*2; y++) {
        var rowY = [];
        for (var x = 0; x < 32*16; x++) {
            rowY.push(32);
        }
        map.push(rowY);

    }
  
    map = this.make.tilemap({ data: map, tileWidth: 8, tileHeight: 16, width: 512, height: 128  });
    tiles = map.addTilesetImage("tiles");
    layer = map.createDynamicLayer(0, tiles, 0, 0);

    var map2 = [];

    for (var y = 0; y < 16*8*2; y++) {
        var rowY2 = [];
        for (var x = 0; x < 32*16; x++) {
            rowY2.push(0);
        }
        map2.push(rowY2);

    }
  

    bgmap = this.make.tilemap({ data: map2, tileWidth: 8, tileHeight: 16, width: 512, height: 128  });        
    bg = bgmap.addTilesetImage("ansibgs");
    bglayer = bgmap.createDynamicLayer(0, bg, 0, 0);

    sprite = this.add.sprite(4, 8, 'underscore_white');

    cursorInterval = setInterval(function() {

    sprite.visible=!sprite.visible;

    }, 600);


    
    cam = this.cameras.main;

    clicks = 0;
    
   document.body.addEventListener('keydown',
    function(e)
    {
        var key = e.key;
        handleKeyCode(key);
        e.preventDefault();
    },
    false);

   
    
    document.body.addEventListener('keyup',
    function(e)
    {
     
        var keyCode = e.which;
        if (keyCode==18) {
            altgrPressed = false;
        } else
        if (keyCode==16) {
            e.preventDefault();
            shiftPressed = false;
        } else
            if (keyCode == 17) {
                                
            ctrlKey=false;
        } 
    
    },
    false);

   // Calculate the thumb height based on the percentage of content that is visible
   thumbHeight = (VISIBLE_HEIGHT_CHARACTERS / TOTAL_HEIGHT_CHARACTERS) * baseHeight;
   console.log("THUMBHEIGHT:"+thumbHeight+"/"+baseHeight);
   if (thumbHeight < baseHeight) {
   // Draw the scrollbar thumb
   thumbVertical = this.add.graphics();
   thumbVertical.fillStyle(0xFFFF00, 1);
   thumbVertical.fillRect(baseWidth - 5, 0, 5, thumbHeight);

   }
   

   // Calculate the thumb width based on the percentage of content that is visible horizontally
   console.log(VISIBLE_WIDTH_CHARACTERS+" / "+TOTAL_WIDTH);
    thumbWidth = (VISIBLE_WIDTH_CHARACTERS / TOTAL_WIDTH) * baseWidth;
    if (thumbWidth < baseWidth) {
    // Draw the horizontal scrollbar thumb
    thumbHorizontal = this.add.graphics();
    thumbHorizontal.fillStyle(0xFFFF00, 1);
    thumbHorizontal.fillRect(0, baseHeight - 5, thumbWidth, 5);
    }

  

   socket.emit('onload', { x : TOTAL_WIDTH, y : TOTAL_HEIGHT_CHARACTERS});

   this.input.on('pointerdown', function (pointer) {
        // Check if clicked within the vertical thumb
        if (pointer.x >= baseWidth - 5 && pointer.x <= baseWidth && pointer.y >= thumbY && pointer.y <= thumbY + thumbHeight) {
            isDraggingVertical = true;
        }

        // Check if clicked within the horizontal thumb
        if (pointer.y >= baseHeight - 8 && pointer.y <= baseHeight && pointer.x >= thumbX && pointer.x <= thumbX + thumbWidth) {

            //if ((cam.scrollY / maxScrollY) < 1) {
            isDraggingHorizontal = true;
            //}
        }
    });

    this.input.on('pointerup', function () {
        isDraggingVertical = false;
        isDraggingHorizontal = false;
    });

  }


  function updateThumbVertical() {
     // Get the camera
     // Calculate the maximum scrollable area
     if (typeof(thumbVertical)!="undefined") {
     let maxScrollY = (TOTAL_HEIGHT_CHARACTERS) * 16; // Assuming each character is 16 pixels tall
 
     // Calculate the thumb position based on the camera's scrollY
     thumbY = (cam.scrollY / maxScrollY) * (baseHeight);
     
     // Clear and redraw the thumb at the new position
     thumbVertical.clear();
     thumbVertical.fillStyle(0xFFFF00, 1);
     thumbVertical.fillRect(cam.scrollX+baseWidth - 5, thumbY+cam.scrollY, 5, thumbHeight);
     }
}

function updateScrolledChars() {
    scrolledXChars = Math.floor(cam.scrollX / 8);
    scrolledYChars = Math.floor(cam.scrollY / 16);
}

function updateThumbHorizontal() {
    // Get the camera
    
    if (typeof(thumbHorizontal)!="undefined") {
    // Calculate the maximum scrollable area horizontally
    let maxScrollX = (TOTAL_WIDTH) * 8; // Assuming each character is 8 pixels wide

    // Calculate the thumb position based on the camera's scrollX
    thumbX = (cam.scrollX / maxScrollX) * (baseWidth);

    // Clear and redraw the thumb at the new position
    thumbHorizontal.clear();
    thumbHorizontal.fillStyle(0xFFFF00, 1);
    thumbHorizontal.fillRect(thumbX + cam.scrollX, cam.scrollY + baseHeight - 8, thumbWidth, 8);
    }
}

  function writeAsciiHTML(string, currentColor, backgroundColor) {

    for (var i = 0; i < string.length; i++) {
        var index = getCharIndex(currentColor, string.charCodeAt(i));
    
        draw(index, currentX+i, currentY, currentColor);

        var charIndex = getCharIndex(backgroundColor, 219);
        drawbg(charIndex, currentX+i, currentY, backgroundColor);   
    }

  }

  function shiftTilesUp(layer) {
    for (let y = 1; y < TOTAL_HEIGHT_CHARACTERS; y++) {  // Start from the second row
        for (let x = 0; x < TOTAL_WIDTH; x++) {
            const tile = layer.getTileAt(x, y);
            if (tile) {
                layer.putTileAt(tile.index, x, y - 1);  // Move the tile up by one row
            }
        }
    }
    // Clear the last row (optional)
    for (let x = 0; x < TOTAL_WIDTH; x++) {
        layer.removeTileAt(x, TOTAL_HEIGHT_CHARACTERS - 1);
    }
}

function clearLine(y) {
    const defaultChar = 32;  // ASCII code for space
    const defaultColor = 15;  // Default foreground color
    const defaultBGColor = 0;  // Default background color (black)

    for (let x = 0; x < TOTAL_WIDTH; x++) {
        // Clear the character layer
        const charIndex = getCharIndex(defaultColor, defaultChar);
        bglayer.putTileAt(charIndex, x, y);
        if (!canvas[y]) canvas[y] = [];
        canvas[y][x] = defaultChar;
        if (!canvasColor[y]) canvasColor[y] = [];
        canvasColor[y][x] = defaultColor;

        // Clear the background layer
        const bgIndex = getCharIndex(defaultBGColor, 219);
        layer.putTileAt(bgIndex, x, y);
        if (!canvasbg[y]) canvasbg[y] = [];
        canvasbg[y][x] = defaultBGColor;
    }
}
  
  function writeAsciiHTMLPos(ascii_codes, currentColor, backgroundColor, x, y) {
    
    return new Promise((resolve, reject) => {

        if (enableScrolling) {
            if (y < TOTAL_HEIGHT_CHARACTERS) {
                maxReachedY = y;
            }
            // Scroll until we've made room for the y-coordinate we're trying to reach
            while ((y > maxReachedY) && (y >= TOTAL_HEIGHT_CHARACTERS)) {

                // Shift all lines up by one
                canvas.shift();
                canvasbg.shift();
                canvasColor.shift();

                shiftTilesUp(bglayer);  // Shift the tiles up in bglayer
                shiftTilesUp(layer);  // Shift the tiles up in layer

                removedYChars++;
                maxReachedY++;
                
                // Optionally clear the line at the new bottom of the canvas
                clearLine(y - removedYChars);
            }
        }
        if (ascii_codes.length==0) {
            
            currentX = x;
            currentY = y;
            redrawCursor();
            resolve();
            return;
        }
        try {
           
            for (var i = 0; i < ascii_codes.length; i++) {
                var index = getCharIndex(currentColor, ascii_codes[i]);


                draw(index, x + i, y, currentColor);
                var charIndex = getCharIndex(backgroundColor, 219);
                drawbg(charIndex, x + i, y, backgroundColor);
            }
            currentX = x + ascii_codes.length;
            currentY = y;
            redrawCursor();
            resolve();
        } catch (error) {
            reject(error);
        }
    });
}  



function writeAsciiToStatusBar(ascii_codes, currentColor, backgroundColor) {
    
    return new Promise((resolve, reject) => {
        let y;
        if (VISIBLE_WIDTH_CHARACTERS>50) {
            y = VISIBLE_HEIGHT_CHARACTERS-1;
        } else {
            y = VISIBLE_HEIGHT_CHARACTERS+1;
        }
       
       
        try {
           
            var charIndex = getCharIndex(backgroundColor, 219);
            for (var i = 0; i < ascii_codes.length; i++) {
                var index = getCharIndex(currentColor, ascii_codes[i]);
                draw(index, i, y, currentColor);
                drawbg(charIndex, i, y, backgroundColor);
            }

            for (var i = ascii_codes.length; i < VISIBLE_WIDTH_CHARACTERS; i++) {
                index = getCharIndex(backgroundColor, 32);
                draw(index, i, y, currentColor);
                drawbg(charIndex, i, y, backgroundColor);
            }
           
            resolve();
        } catch (error) {
            reject(error);
        }
    });
}  





  function clearScreen() {
    removedYChars=0;
    maxReachedY=0;
    var index = getCharIndex(0, 32);
    for (var x = 0; x < TOTAL_WIDTH; x++) {
        for (var y = 0; y < TOTAL_HEIGHT_CHARACTERS; y++) {
        bglayer.putTileAt(index, x, y);
        layer.putTileAt(index, x, y);
        }
    }
}


  function update(time, delta) {

    if (initCalled == false) {

        // Update the canvas style to fit the window height
        // Calculate the scale factor for vertical scaling

        if (window.matchMedia("(max-width: 515px)").matches) {
            document.getElementById('simple-keyboard').style.display='inline';
        } else {


        var verticalScale = window.innerHeight / baseHeight;
        if (verticalScale > 1) verticalScale = 1;
        var canvasElement = document.querySelector("#game-container canvas");
        canvasElement.style.height = (baseHeight * verticalScale) + "px";
        }
        document.documentElement.style.height = null;  // for the html tag
        document.body.style.height = null;  // for the body tag
        document.getElementById('spinner').style.display='none';
     
    initCalled = true;

    }
     
    this.input.on('pointermove', function (pointer) {
        if (isDraggingVertical) {
            let newY = pointer.y - thumbHeight / 2;
            moveVerticalThumb(newY);
        }
    
        if (isDraggingHorizontal) {
            let newX = pointer.x - thumbWidth / 2;
            moveHorizontalThumb(newX);
        }
    });

  }

  function moveVerticalThumb(newY) {
    // Clamp the new Y position within the scrollbar track
    newY = Phaser.Math.Clamp(newY, 0, baseHeight - thumbHeight);

    // Update the thumb position
    thumbVertical.clear();
    thumbVertical.fillStyle(0xFFFF00, 1);
    thumbVertical.fillRect(baseWidth - 8, newY, 8, thumbHeight);

    // Update camera scrollY based on thumb position
    cam.scrollY = (newY / (baseHeight - thumbHeight)) * (TOTAL_HEIGHT_CHARACTERS * 16 - baseHeight);

    updateThumbHorizontal();
    updateThumbVertical();
    updateScrolledChars();
}

function moveHorizontalThumb(newX) {
    // Clamp the new X position within the scrollbar track
    newX = Phaser.Math.Clamp(newX, 0, baseWidth - thumbWidth);

    // Update the thumb position
    thumbHorizontal.clear();
    thumbHorizontal.fillStyle(0xFFFF00, 1);
    thumbHorizontal.fillRect(newX, baseHeight - 16, thumbWidth, 16);

    // Update camera scrollX based on thumb position
    cam.scrollX = (newX / (baseWidth - thumbWidth)) * (TOTAL_WIDTH * 8 - baseWidth);
    updateThumbHorizontal();
    updateThumbVertical();
    updateScrolledChars();
}



  function getCharIndex(foreground, asciiCode) {

    var xpos=foreground;
    while (xpos >= 16) xpos=xpos-16;
    var ypos = Math.floor(foreground/16);       
    var myx = (asciiCode % 32) * 8+(xpos*256);
    var myy = Math.floor(asciiCode / 32) * 16 + (ypos*128);
    myx = myx / 8;
    myy = myy / 16;
    return myx+myy*16*32;

  }

  function handleKeyCode(keyCode) {
    console.log(keyCode);
    socket.emit('input_keypress', { key: keyCode });
}

function redrawCursor() {

    sprite.x = currentX * 8 + 4;
    sprite.y = (currentY) * 16 + 4;
    sprite.visible=true;
    clearInterval(cursorInterval);
    cursorInterval = setInterval(function() {
        
        if (!isColorPalette) {
            sprite.visible=!sprite.visible;
        } else {
            sprite.visible = false;
        }

        }, 600);
}

