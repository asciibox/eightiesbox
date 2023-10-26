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

  function updateSizes(x, y) {

    TOTAL_WIDTH = x;
    VISIBLE_WIDTH_CHARACTERS = x;
    VISIBLE_HEIGHT_CHARACTERS = y;
    TOTAL_HEIGHT_CHARACTERS = y;
    LIMIT_TO_VISIBLE_WIDTH = true;

    baseWidth = VISIBLE_WIDTH_CHARACTERS*8;  // The total width space plus 8px for the scrollbar
    baseHeight = VISIBLE_HEIGHT_CHARACTERS*16; // 16px at the bottom for the scrollbar

    if ( (mode=="html") || (mode=="timeline") ) {

        config = {
            title: 'Ascii box',
            type: Phaser.AUTO,
            width: baseWidth, // window.innerWidth,
            height: baseHeight, // window.innerHeight*4,
            pixelArt: true, // Force the game to scale images up crisply
            parent: "game-container",
            scene: {
              preload: preload,
              create: create,
              update: update
            }, scale: {
                mode: Phaser.Scale.FIT, // Fit to window while maintaining the aspect ratio
                autoCenter: Phaser.Scale.CENTER_BOTH // Center the canvas in both horizontal and vertical
            }
          };
        
        } else {
        
        config = {
            title: 'Ascii box',
            type: Phaser.AUTO,
            pixelArt: true, // Force the game to scale images up crisply
            parent: "game-container",
            scene: {
              preload: preload,
              create: create,
              update: update
            }, scale: {
                mode: Phaser.Scale.ENVELOP, // Fit to window while maintaining the aspect ratio
                autoCenter: Phaser.Scale.CENTER_BOTH // Center the canvas in both horizontal and vertical
            }
          };
        
        }
        

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
var keys = [];
var enterFilename = false;
    
var shiftkeys = [ 33, 34, 21, 36, 37, 38, 47, 40, 41, 61 ];

var onScreenKeyboard = false;

keys[0] = [ 49, 50, 51, 52, 53, 54, 55, 56, 57, 48 ];
keys[1] = [ 218, 191, 192, 217, 196, 179, 195, 180, 193, 194 ];
keys[2] = [ 201, 187, 200, 188, 205, 186, 204, 185, 202, 203 ];
keys[3] = [ 251, 184, 212, 190, 205, 179, 198, 181, 207, 209 ];
keys[4] = [ 161, 183, 211, 135, 179, 186, 199, 182, 208, 144 ];
keys[5] = [ 197, 206, 139, 140, 232, 163, 155, 156, 153, 239 ];
keys[6] = [ 176, 177, 178, 219, 223, 220, 124, 141, 254, 250 ];
keys[7] = [ 001, 002, 003, 004, 005, 006, 196, 127, 014, 207 ];
keys[8] = [ 024, 025, 024, 025, 016, 017, 023, 023, 020, 021 ];
keys[9] = [ 174, 175, 061, 243, 169, 170, 253, 246, 171, 172 ];
keys[10] = [ 149, 241, 020, 021, 235, 157, 227, 167, 251, 252 ];
keys[11] = [ 162, 225, 147, 228, 230, 232, 235, 236, 237, 237 ];
keys[12] = [ 128, 135, 165, 164, 152, 159, 044, 249, 173, 168 ];
keys[13] = [ 131, 132, 133, 160, 248, 134, 142, 143, 145, 146 ];
keys[14] = [ 136, 137, 138, 130, 144, 140, 139, 141, 161, 158 ];
keys[15] = [ 147, 148, 149, 224, 167, 150, 129, 151, 163, 154 ];

var currentRedrawStep = 0;
var steps = [];
var isRedrawing = false;

var htmlElements = [];
var htmlCurrentField = 0;

var centerwidth;

var asciitable = {
    32 : ' ',
    39 : '"',
    44 : ',',
    45 : '=',
    61 : '-',
    46 : '.',
    48 : '0',
    49 : '1',
    50 : '2',
    51 : '3',
    52 : '4',
    53 : '5',
    54 : '6',
    55 : '7',
    56 : '8',
    57 : '9',
    91 : '[',
    93 : ']',
    97 : 'a',
    98 : 'b',
    99 : 'c',
    100 : 'd',
    101 : 'e',
    102 : 'f',
    103 : 'g',
    104 : 'h',
    105 : 'i',
    106 : 'j',
    107 : 'k',
    108 : 'l',
    109 : 'm',
    110 : 'n',
    111 : 'o',
    112 : 'p',
    113 : 'q',
    114 : 'r',
    115 : 's',
    116 : 't',
    117 : 'u',
    118 : 'v',
    119 : 'w',
    120 : 'x',
    121 : 'y',
    122 : 'z',
    189: '-',
    190 : '.',
}

var asciitable_shift = {
    32 : ' ',
    33 : '!',
    48 : '=',
    49 : '!',
    50 : '"',
    51 : '§',
    52 : '$',
    53 : '%',
    54 : '&',
    55 : '/',
    56 : '(',
    57 : ')',
    62 : '<',
    60 : '>',
    65 : 'A',
    66 : 'B',
    67 : 'C',
    68 : 'D',
    69 : 'E',
    70 : 'F',
    71 : 'G',
    72 : 'H',
    73 : 'I',
    74 : 'J',
    75 : 'K',
    76 : 'L',
    77 : 'M',
    78 : 'N',
    79 : 'O',
    80 : 'P',
    81 : 'Q',
    82 : 'R',
    83 : 'S',
    84 : 'T',
    85 : 'U',
    86 : 'V',
    87 : 'W',
    88 : 'X',
    89 : 'Y',
    90 : 'Z',
    126 : '~',
    64 : '@',
    36 : '$',
    37 : '%',
    94 : '^',
    38 : '&',
    42 : '*',
    40 : '(',
    41 : ')',
    95 : '_',
    43 : '+',
    39 : '´',
    123 : '{',
    125 : '}',
    124 : '|',
    
    189: '_',
    190 : ':',
    
}

var onscreenkeys = [];
onscreenkeys[0]=[126, 33, 64, 35, 36, 37, 94, 38, 42, 40, 41, 95, 43];
onscreenkeys[1]=[39, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 61, 45, 8, 8];
onscreenkeys[2]=[9, 9, 81, 87, 69, 82, 84, 89, 86, 73, 79, 80, 123, 125, 124];
onscreenkeys[3]=[9, 9, 113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93];
onscreenkeys[4]=[65,83,68, 70, 71, 72, 74, 75, 76, 13];
onscreenkeys[5]=[97, 115, 100, 102, 103, 104, 106, 107, 108];
onscreenkeys[6]=[90, 88, 67, 86, 66, 78, 77, 60, 62, 63];
onscreenkeys[7]=[90, 88, 67, 86, 66, 78, 109, 44, 46];

var hasShiftPressed = [];
hasShiftPressed[0]=true;
hasShiftPressed[1]=false;
hasShiftPressed[2]=true;
hasShiftPressed[3]=false;
hasShiftPressed[4]=true;
hasShiftPressed[5]=false;
hasShiftPressed[6]=true;
hasShiftPressed[7]=false;

var inputfield = {
    x : 0,
    y : 0,
    value : '',
    width: 80,
    active : false,
    filename : false,
    type : 'text'
}

var fields = [];

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
    scaleY = displayHeight / baseHeight;
    
    // Calculate the real size of your tiles  
    realTileWidth = 8 * scaleX;
    realTileHeight = 16 * scaleY;
  
    console.log("realTileHeight:"+realTileHeight);
    DEFAULT_INSERT = false;
    VISIBLE_HEIGHT = Math.floor(baseHeight/16);
    console.log("VISIBLE_HEIGHT:"+VISIBLE_HEIGHT);
  
    VISIBLE_WIDTH = Math.floor(baseWidth/8);



  }

  function countHTMLElements(type) {
    var counter = 0;
    for (var i = 0; i < htmlElements.length; i++) {
        if (htmlElements[i].type==type) {
            counter++;
        }
    }
    return counter;
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
    steps = [];

}

function redraw() {
    initPosition();
    isRedrawing = true;
    insert = DEFAULT_INSERT;
    clearScreen();
    currentRedrawStep = 0;

    setTimeout(function() {
            redrawStep();
    }, 10);
}

function redrawStep() {
    if (currentRedrawStep < steps.length) {
        var step = steps[currentRedrawStep];
        currentX = step.x;
        currentY = step.y;
        currentColor = step.fgColor;
        backgroundColor = step.bgColor;
        specialKeyCharacterSet = step.characterSet;
        
        keydown(step.keyCode);
        redrawCursor();

        setTimeout(function() {
            currentRedrawStep++;
            redrawStep();
        }, 10);
    } else {
        isRedrawing = false;
        isColorPalette = false;
        shiftPressed = false;
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

    function removeCurrentChar() {

        setTimeout(function() {
            for (var i = currentX; i < TOTAL_WIDTH; i++) {
            
                previousColor = 15;
                if ( (canvas[currentY]) && (canvas[currentY][i+1]) ) nextChar = canvas[currentY][i+1]; else nextChar = 32;
                if ( ( canvasColor[currentY] ) && (canvasColor[currentY][i+1]) ) nextColor = canvasColor[currentY][i+1]; else nextColor = 15;
                bglayer.putTileAt(nextChar, i, currentY);
                if (!canvas[currentY]) canvas[currentY]=[];
                canvas[currentY][i]=nextChar;
                if (!canvasColor[currentY]) canvasColor[currentY]=[];
                canvasColor[currentY][i]=nextColor;

                if ( ( canvasbg[currentY] ) && (canvasbg[currentY][i+1]) ) nextBGColor = canvasbg[currentY][i+1]; else nextBGColor = 0;
                var index = getCharIndex(nextBGColor, 219);
                layer.putTileAt(index, i, currentY);
                if (!canvasbg[currentY]) canvasbg[currentY]=[];
                canvasbg[currentY][i]=nextBGColor;

            }
        }, 1);
    }

    function insertChar() {
        setTimeout(function() {
            for (var i = TOTAL_WIDTH; i > currentX+1; i--) {
                previousColor = 15;
                if ( (canvas[currentY]) && (canvas[currentY][i-1]) ) previousChar = canvas[currentY][i-1]; else previousChar = 32;
                if ( ( canvasColor[currentY] ) && (canvasColor[currentY][i-1]) ) previousColor = canvasColor[currentY][i-1]; else previousColor = 15;
                bglayer.putTileAt(previousChar, i, currentY);
                canvas[currentY][i]=previousChar;
                canvasColor[currentY][i]=previousColor;

                if ( ( canvasbg[currentY] ) && (canvasbg[currentY][i-1]) ) previousBGColor = canvasbg[currentY][i-1]; else previousBGColor = 0;
                var index = getCharIndex(previousBGColor, 219);
                layer.putTileAt(index, i, currentY);
                canvasbg[currentY][i]=previousBGColor;

            }
        }, 1);

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

    this.input.on('pointerdown', function (pointer) {
      
        clicks++;
        setTimeout(function() {
            clicks = 0;
        }, 200);

        
           

        

    }, this);
 
    
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

   if (mode=="timeline") {

   }
   
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

  function getRandomHexColor() {
    const letters = '0123456789ABCDEF';
    let color = '0x';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
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




  function backSpace() {
    /*'var index = getCharIndex(currentColor, 32);    
    bglayer.putTileAt(index, currentX-1, currentY);        
    draw(getCharIndex(backgroundColor, 219), currentX-1, currentY, currentColor);
    removeCurrentChar();
    cursorLeft();*/
    socket.emit('input_keypress', { key: 'Backspace' });

  }


  function enterButton() {
    if (isSelect == true) {
        var selectedValue = files[filechooserY+filechooserStart];
        inputfield.value=selectedValue;
        updateForm();
        restoreTileset();
        redrawInputfield();
        inputfield.active=true;
        return;
    } else {
        loadFile(files[filechooserY+filechooserStart]);
    }
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

function saveTileset() {
    console.log("SAVED");

}
function restoreTileset() {
   
    var x = 0;
    var y = 0;

    for (var ix = 0; ix <= 16*16*256; ix++) {
   
        if ( (canvas[y]) && (canvas[y][x]) ) {
            bglayer.putTileAt(canvas[y][x], x, y);
        } else {
            bglayer.putTileAt(32, x, y);
        }
        if ( (canvasbg[y]) && (canvasbg[y][x]) ) {
            var index = getCharIndex(canvasbg[y][x], 219);
            
            layer.putTileAt(index, x, y);
        } else {
            layer.putTileAt(32, x, y);
        }
       
        if (x < 32*16-1) {
            x++;
        } else {
            x = 0;
            y++;
        }
       
}

}

  function update(time, delta) {
     
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


  function characterSet() {

     x = 0;
     y = 0;
     cnt = 0;

    for (var ix = 0; ix <= 16*16*256; ix++) {
       
            if (x < 32*16-1) {
                draw(cnt++, x,y);
                x++;
            } else {
                draw(cnt++, x,y);
                x = 0;
                y++;
            }
      
    }

  }

  function cursorLeft() {
    socket.emit('input_keypress', { key: 'ArrowLeft' });
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

function storeStep(keyCode) {
if (keyCode == 27) return;

if ( (!isRedrawing) && (!isColorPalette) ) {
    steps.push({
        keyCode : keyCode,
        x : currentX,
        y : currentY,
        fgColor : currentColor,
        bgColor : backgroundColor,
        characterSet : specialKeyCharacterSet
    });
}

}

function updateContent(state) {
    console.log(state);
}
