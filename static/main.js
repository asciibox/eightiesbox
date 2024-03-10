/**
 * Author: Oliver Bachmann
 * Asset Credits:
 *  - Asciibox
 */

// Assuming your base dimensions are stored in variables called 'baseWidth' and 'baseHeight'
let TOTAL_WIDTH;
let VISIBLE_WIDTH_CHARACTERS;
let VISIBLE_HEIGHT_CHARACTERS;
let TOTAL_HEIGHT_CHARACTERS;
let LIMIT_TO_VISIBLE_WIDTH;
let baseWidth;
let baseHeight;
let enableTrackerKeyboard = false;

let initCalled = false;
let popupOpened = false;

let popupClickCounter = 0;

const BACKGROUND_LAYER_DEPTH = 0;  // Lowest depth
const IMAGE_LAYER_DEPTH = 10;      // Depth higher than background but lower than bglayer
const BGLAYER_DEPTH = 20;          // Highest depth


function updateSizes(x, y) {
  TOTAL_WIDTH = x;
  VISIBLE_WIDTH_CHARACTERS = x;
  VISIBLE_HEIGHT_CHARACTERS = y;
  TOTAL_HEIGHT_CHARACTERS = y;
  LIMIT_TO_VISIBLE_WIDTH = true;

  baseWidth = VISIBLE_WIDTH_CHARACTERS * 8; // The total width space plus 8px for the scrollbar
  baseHeight = VISIBLE_HEIGHT_CHARACTERS * 16; // 16px at the bottom for the scrollbar

  // Don't calculate scaleX and scaleY here
  // Just set the base dimensions for now
  
}

mode = "html"; // html or editor
let thumbVertical;
let thumbHeight;
let thumbY = 0;
let thumbX = 0;
let isDraggingVertical = false;
let isDraggingHorizontal = false;
let insert = false;

let enableScrolling = true; // In rare case when viewing ansi files you can set this to false
let maxReachedY = 0; // Variable to keep track of the maximum reached y coordinate

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
var drawcanvas = [];
var drawcanvasbg = [];
var secondCanvas = [];
var canvasColor = [];
var secondCanvasColor = [];
var specialKeyCharacterSet = 0;

var shiftPressed = false;
var ctrlKeyPressed = false;
var altgrPressed = false;
var game;


class MyScene extends Phaser.Scene {
  constructor() {
    super('YourSceneKey'); // Assign a key to your scene
  }

  preload() {
    this.load.image("tiles", "static/ansi.png");
    this.load.image("ansibgs", "static/ansi.png");
    this.load.image("underscore_white", "static/underscore_white.png");

    // Set up an event listener for when files complete loading
    this.load.on('filecomplete', (key, type, data) => {
        if (key === 'tiles' || key === 'ansibgs') {
            // Assuming you want NEAREST filter for pixel art
            this.textures.get(key).setFilter(Phaser.ScaleModes.LINEAR);
        }
    });

    window.loader = this.load;
    window.adder = this.add;
}

  create() {
      // Load a map from a 2D array of tile indices
      // prettier-ignore
    
      var map = [];
    
      for (var y = 0; y < 16 * 8 * 2; y++) {
        var rowY = [];
        for (var x = 0; x < 32 * 16; x++) {
          rowY.push(32);
        }
        map.push(rowY);
      }
    
    
      map = this.make.tilemap({
        data: map,
        tileWidth: 8,
        tileHeight: 16,
        width: 512,
        height: 128,
      });
      window.tiles = map.addTilesetImage("tiles");
      window.layer = map.createLayer(0, tiles, 0, 0);
      layer.setDepth(BACKGROUND_LAYER_DEPTH);
      var map2 = [];
    
      for (var y = 0; y < 16 * 8 * 2; y++) {
        var rowY2 = [];
        for (var x = 0; x < 32 * 16; x++) {
          rowY2.push(0);
        }
        map2.push(rowY2);
      }
    
      
      
    
      window.bgmap = this.make.tilemap({
        data: map2,
        tileWidth: 8,
        tileHeight: 16,
        width: 512,
        height: 128,
      });
      window.bg = window.bgmap.addTilesetImage("ansibgs");
      window.bglayer = window.bgmap.createLayer(0, bg, 0, 0);
      window.bglayer.setDepth(BGLAYER_DEPTH);
      console.log("Created bglayer");
    
    
      window.sprite = this.add.sprite(4, 8, "underscore_white");
    
      window.cursorInterval = setInterval(function () {
        window.sprite.visible = !window.sprite.visible;
      }, 600);
    
      window.cam = this.cameras.main;
    
      // Calculate the thumb height based on the percentage of content that is visible
      window.thumbHeight =
        (VISIBLE_HEIGHT_CHARACTERS / TOTAL_HEIGHT_CHARACTERS) * baseHeight;
      console.log("THUMBHEIGHT:" + thumbHeight + "/" + baseHeight);
      if (window.thumbHeight < window.baseHeight) {
        // Draw the scrollbar thumb
        thumbVertical = this.add.graphics();
        thumbVertical.fillStyle(0xffff00, 1);
        thumbVertical.fillRect(window.baseWidth - 5, 0, 5, window.thumbHeight);
      }
    
      // Calculate the thumb width based on the percentage of content that is visible horizontally
      console.log(VISIBLE_WIDTH_CHARACTERS + " / " + TOTAL_WIDTH);
      window.thumbWidth = (VISIBLE_WIDTH_CHARACTERS / TOTAL_WIDTH) * baseWidth;
      if (window.thumbWidth < baseWidth) {
        // Draw the horizontal scrollbar thumb
        thumbHorizontal = this.add.graphics();
        thumbHorizontal.fillStyle(0xffff00, 1);
        thumbHorizontal.fillRect(0, baseHeight - 5, thumbWidth, 5);
      }
    
    
    
    
      socket.emit("onload", { x: TOTAL_WIDTH, y: TOTAL_HEIGHT_CHARACTERS });
    
    
    
    
      this.input.on("pointerdown", function (pointer) {
    
         // Check for click in the last 16px of the screen
        if (pointer.y >= baseHeight - 16) {
          // Action to perform when the bottom-right 20px area is clicked
          toggleKeyboard();
        } else {
    
         let tileX = Math.floor(pointer.x /  8) + 1;
         let tileY = Math.floor(pointer.y / 16) + 1;
         for (let i = 0; i < hrefs.length; i++) {
          let href = hrefs[i];
          let hrefLength;
          if (href.length) {
            hrefLength = href.length; // Assuming length is the length of the string
          } else {
          hrefLength = href.href.length; // Assuming href string length corresponds to its display length
          }
          // Check if the click is within the horizontal range of the href and on the same vertical line
          console.log(tileX + " >= " + href.x + " && " + tileX + " < " + (Number(href.x) + Number(hrefLength)));
          console.log(tileY + " == " + (Number(href.y) + 1));
          if (tileX >= parseInt(href.x) && 
              tileX < (parseInt(href.x) + parseInt(hrefLength)) && 
              tileY > parseInt(href.y) && 
              tileY <= (parseInt(href.y) + parseInt(href.height))) {
    
              if (href.callback_name) {
                  socket.emit("link_callback", { callback_name: href.callback_name });
              } else {
                  window.open(href.href, "_blank");
              }
              return; // Stop checking after finding a match
          }
    
        }
    
         socket.emit("pointerdown", { x: tileX, y: tileY });
    
          if ( (popupOpened == false) && (popupClickCounter > 5) ) {
    
          if (getCookie("popupOpened")==null) {
    
          window.open(
            "https://documentation.eightiesbox.com/index.html",
            "_blank"
          );
           
          setCookie("popupOpened", "true", 30);
          }
          popupOpened = true;
    
          }
          popupClickCounter++;
    
        }
    
        return;
    
        // Check if clicked within the vertical thumb
        if (
          pointer.x >= baseWidth - 5 &&
          pointer.x <= baseWidth &&
          pointer.y >= thumbY &&
          pointer.y <= thumbY + thumbHeight
        ) {
          isDraggingVertical = true;
        }
    
        // Check if clicked within the horizontal thumb
        if (
          pointer.y >= baseHeight - 8 &&
          pointer.y <= baseHeight &&
          pointer.x >= thumbX &&
          pointer.x <= thumbX + thumbWidth
        ) {
          //if ((cam.scrollY / maxScrollY) < 1) {
          isDraggingHorizontal = true;
          //}
        }
      });
    
    
    
      this.input.on("pointerup", function () {
        isDraggingVertical = false;
        isDraggingHorizontal = false;
      });
  }

  update() {
    if (initCalled == false) {
      // Update the canvas style to fit the window height
      // Calculate the scale factor for vertical scaling
  
      

      if (window.matchMedia("(max-width: 515px)").matches) {
        document.getElementById("simple-keyboard").style.display = "inline";
      } else {
        var verticalScale = window.innerHeight / baseHeight;
        if (verticalScale > 1) verticalScale = 1;
        var canvasElement = document.querySelector("#game-container canvas");
        canvasElement.style.height = baseHeight * verticalScale + "px";
      }
      document.documentElement.style.height = null; // for the html tag
      document.body.style.height = null; // for the body tag
      document.getElementById("spinner").style.display = "none";
  
      var canvas = document.getElementById('game-container').querySelector('canvas');
      var computedStyle = window.getComputedStyle(canvas);
    
      window.canvasScaleX = parseInt(computedStyle.width, 10) / baseWidth;
      window.canvasScaleY = parseInt(computedStyle.height, 10) / baseHeight;
  
      
      setupSocketEventListeners(socket);
  
      
      initCalled = true;
      adjustGameSize(game);

    }
  
    this.input.on("pointermove", function (pointer) {
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
}

function initPage(dataArray) {
  // Sort the array based on minWidth for easy comparison.

  dataArray.sort((a, b) => a.minWidth - b.minWidth);

  // Find the suitable size configuration
  dataArray.forEach((data) => {
    if (window.innerWidth >= data.minWidth) {
      updateSizes(data.x, data.y);
    }
  });

  console.log("VISIBLE_WIDTH_CHARACTERS * 8:"+VISIBLE_WIDTH_CHARACTERS * 8);
  console.log("VISIBLE_HEIGHT_CHARACTERS * 16:"+VISIBLE_HEIGHT_CHARACTERS * 16);
  // Initialize config with base dimensions
  config = {
    roundPixels : false,
    title: "Ascii box",
    type: Phaser.AUTO,
    antialias: false,
    width: VISIBLE_WIDTH_CHARACTERS * 8,
    height: VISIBLE_HEIGHT_CHARACTERS * 16,
    pixelArt: true,
    parent: "game-container",
    scene: [MyScene],
    scale: {
      mode: Phaser.Scale.NONE, // Use custom scaling
      autoCenter: Phaser.Scale.CENTER_BOTH, // Center the canvas in both horizontal and vertical
    },
    input: {
      touch: {
          capture: false
      }
    }
  };

   // Create the game instance with initial config
   game = new Phaser.Game(config);
 
   // Remaining setup
   DEFAULT_INSERT = false;
   VISIBLE_HEIGHT = Math.floor(baseHeight / 16);
   VISIBLE_WIDTH = Math.floor(baseWidth / 8);
   setupKeypressListeners();
   
   
 

}

let resizeTimeout = null;
const horizontal = 1920;
const vertical = 960;

const referenceHeight = 1320;
const referenceWidth = 960;
const proportionalityConstant = referenceWidth / referenceHeight;

function adjustGameSize() { 
  
    const dynamicWidth = (window.innerHeight * proportionalityConstant) * 2;

    if  ( (VISIBLE_WIDTH_CHARACTERS >= 79) || (window.innerWidth>800) ) {
      console.log(window.innerWidth + "/" + dynamicWidth);
    const TILE_HEIGHT = 16; // Assuming each character's height is 16 pixels
    const gameContainer = document.getElementById('game-container');
    const viewportWidth = gameContainer.clientWidth* 4; // superscaled by 4
    const viewportHeight = window.innerHeight * 2 ; // superscaled by two

    // Define the aspect ratio of the game
    const aspectRatio = horizontal / vertical;

    // Start by setting the canvas height to the innerHeight
    let finalCanvasHeight = viewportHeight;
    // Calculate the width based on the game's aspect ratio
    let finalCanvasWidth = Math.round(finalCanvasHeight * aspectRatio);

    // If the calculated width exceeds the viewportWidth, adjust both width and height
    if (finalCanvasWidth > viewportWidth / 2) {
        finalCanvasWidth = viewportWidth;
        // Recalculate height to maintain the aspect ratio
        finalCanvasHeight = Math.round(finalCanvasWidth / aspectRatio);
    }

    // Calculate the scale
    let scale = Math.min(finalCanvasWidth / horizontal, finalCanvasHeight / vertical);

    // Update Phaser's internal size
    game.scale.resize(finalCanvasWidth , finalCanvasHeight  * 2); // superscaled
    // Update camera settings
    const scene = game.scene.scenes[0];
    if (scene && scene.cameras && scene.cameras.main) {
        scene.cameras.main.setBounds(0, 0, horizontal, vertical);
        scene.cameras.main.setZoom(scale);
        scene.cameras.main.scrollX = 0;
        scene.cameras.main.scrollY = 0;
    }

    console.log("Canvas resized to:", finalCanvasWidth, finalCanvasHeight);
    console.log("Zoom applied with scale:", scale);

    // Adjust CSS to maintain aspect ratio
    const canvasElement = document.getElementById('game-container').getElementsByTagName('canvas')[0];
    canvasElement.style.width = `${finalCanvasWidth}px`;
    canvasElement.style.height = `${finalCanvasHeight}px`;
    canvasElement.style.maxWidth = '100%';
    canvasElement.style.maxHeight = `${viewportHeight}px`;

} else {
  console.log(2);
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  // Desired canvas dimensions
  const maxCanvasWidth = VISIBLE_WIDTH_CHARACTERS * 8;
  const maxCanvasHeight = VISIBLE_HEIGHT_CHARACTERS * 16;

  // Calculate the scale for both width and height
  let scaleX = viewportWidth / maxCanvasWidth;
  let scaleY = viewportHeight / maxCanvasHeight;

  // Use the smaller of the two scales to ensure the content fits
  let finalScale = Math.min(scaleX, scaleY);

  // Ensure the scale does not go above 1 to avoid enlarging the canvas beyond its intended size
  finalScale = Math.min(finalScale, 1);

  // Set the scale for the scene's main camera
  const scene = game.scene.scenes[0];
  scene.cameras.main.setZoom(finalScale);

  // Calculate the final canvas dimensions
  const finalCanvasWidth = maxCanvasWidth * finalScale;
  const finalCanvasHeight = maxCanvasHeight * finalScale;
 // Set the scale for the scene's main camera

 // Adjust Phaser's world bounds if necessary
 scene.cameras.main.setBounds(0, 0, finalCanvasWidth, finalCanvasHeight);
 //scene.physics.world.setBounds(0, 0, finalCanvasWidth, finalCanvasHeight);

 // Update the canvas element's size
 game.scale.resize(finalCanvasWidth, finalCanvasHeight);

 // Make sure the canvas style matches the new size
 const canvas = game.canvas;
 const canvasStyle = canvas.style;
 canvasStyle.top = '0';
 canvasStyle.left = '0';
 canvasStyle.transform = 'none';
 canvasStyle.imageRendering = 'pixelated';
 canvasStyle.margin = '0';
 canvas.width = finalCanvasWidth;
 canvas.height = finalCanvasHeight;

}
}

window.addEventListener('resize', adjustGameSize);







function keyDownHandler(e) {
  var key = e.key;

  if (e.shiftKey) {
    shiftPressed = true;
  }
  if (e.ctrlKey) {
    ctrlKeyPressed = true;
  }
  if (e.altKey) {
    altgrPressed = true;
  }

  handleKeyCode(key);
  e.preventDefault();
}

function keyUpHandler(e) {
  var key = e.key;

  if (e.shiftKey) {
    shiftPressed = false;
  }
  if (e.ctrlKey) {
    ctrlKeyPressed = false;
  }
  if (e.altKey) {
    altgrPressed = false;
  }
}

function setupKeypressListeners() {
  // Remove existing event listeners if they are already set
  document.body.removeEventListener("keydown", keyDownHandler);
  document.body.removeEventListener("keyup", keyUpHandler);

  // Add new event listeners
  document.body.addEventListener("keydown", keyDownHandler, false);
  document.body.addEventListener("keyup", keyUpHandler, false);
}


function writeString(string, x, y, color, func) {
  for (var i = 0; i < string.length; i++) {
    var index = getCharIndex(color, string.charCodeAt(i));
    layer.putTileAt(index, x + i, y);
  }

  if (typeof func == "function") {
    fields.push({
      startX: x,
      endX: x + string.length,
      startY: y,
      myfunc: func,
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
      if (!drawcanvas[y]) drawcanvas[y] = [];
      drawcanvas[y][x] = 32;
      if (!drawcanvasbg[y]) drawcanvasbg[y] = [];
      drawcanvasbg[y][x] = 0;
    }
  }
}

function drawbg(index, x, y, backgroundColor) {
  y = y - removedYChars;
  layer.putTileAt(index, x, y);
  if (!drawcanvasbg[y]) {
    drawcanvasbg[y] = [];
  }
  drawcanvasbg[y][x] = backgroundColor;
}

function draw(index, x, y, currentColor) {
  y = y - removedYChars;

  try {
  bglayer.putTileAt(index, x, y);
  } catch (e) {
    console.log(e);
  }

  if (!drawcanvas[y]) {
    drawcanvas[y] = [];
  }
  drawcanvas[y][x] = index;
  if (!canvasColor[y]) {
    canvasColor[y] = [];
  }
  canvasColor[y][x] = currentColor;
}



function updateThumbVertical() {
  // Get the camera
  // Calculate the maximum scrollable area
  if (typeof thumbVertical != "undefined") {
    let maxScrollY = TOTAL_HEIGHT_CHARACTERS * 16; // Assuming each character is 16 pixels tall

    // Calculate the thumb position based on the camera's scrollY
    thumbY = (cam.scrollY / maxScrollY) * baseHeight;

    // Clear and redraw the thumb at the new position
    thumbVertical.clear();
    thumbVertical.fillStyle(0xffff00, 1);
    thumbVertical.fillRect(
      cam.scrollX + baseWidth - 5,
      thumbY + cam.scrollY,
      5,
      thumbHeight
    );
  }
}

function updateScrolledChars() {
  scrolledXChars = Math.floor(cam.scrollX / 8);
  scrolledYChars = Math.floor(cam.scrollY / 16);
}

function updateThumbHorizontal() {
  // Get the camera

  if (typeof thumbHorizontal != "undefined") {
    // Calculate the maximum scrollable area horizontally
    let maxScrollX = TOTAL_WIDTH * 8; // Assuming each character is 8 pixels wide

    // Calculate the thumb position based on the camera's scrollX
    thumbX = (cam.scrollX / maxScrollX) * baseWidth;

    // Clear and redraw the thumb at the new position
    thumbHorizontal.clear();
    thumbHorizontal.fillStyle(0xffff00, 1);
    thumbHorizontal.fillRect(
      thumbX + cam.scrollX,
      cam.scrollY + baseHeight - 8,
      thumbWidth,
      8
    );
  }
}

function writeAsciiHTML(string, currentColor, backgroundColor) {
  for (var i = 0; i < string.length; i++) {
    var index = getCharIndex(currentColor, string.charCodeAt(i));

    draw(index, currentX + i, currentY, currentColor);

    var charIndex = getCharIndex(backgroundColor, 219);
    drawbg(charIndex, currentX + i, currentY, backgroundColor);
  }
}

function shiftTilesUp() {
  // Start shifting from the second row to the second-last row
  for (let y = 1; y < TOTAL_HEIGHT_CHARACTERS - 1; y++) {
    for (let x = 0; x < TOTAL_WIDTH; x++) {
      const tile = layer.getTileAt(x, y);
      if (tile) {
        layer.putTileAt(tile.index, x, y - 1);
      }
      const bgtile = bglayer.getTileAt(x, y);
      if (bgtile) {
        bglayer.putTileAt(bgtile.index, x, y - 1);
      }
    }
  }
  // Clear the second-last row
  for (let x = 0; x < TOTAL_WIDTH; x++) {
    layer.removeTileAt(x, TOTAL_HEIGHT_CHARACTERS - 2);
  }
  clearLine(TOTAL_HEIGHT_CHARACTERS-1);
}
function clearLine(y) {

  const defaultChar = 32; // ASCII code for space
  const defaultColor = 15; // Default foreground color
  const defaultBGColor = 0; // Default background color (black)
  if (y === TOTAL_HEIGHT_CHARACTERS - 1) {
    y = TOTAL_HEIGHT_CHARACTERS - 2;
  }
  for (let x = 0; x < TOTAL_WIDTH; x++) {
    // Clear the character layer
    const charIndex = getCharIndex(defaultColor, defaultChar);
    bglayer.putTileAt(charIndex, x, y);
    if (!drawcanvas[y]) drawcanvas[y] = [];
    drawcanvas[y][x] = defaultChar;
    if (!canvasColor[y]) canvasColor[y] = [];
    canvasColor[y][x] = defaultColor;

    // Clear the background layer
    const bgIndex = getCharIndex(defaultBGColor, 219);
    layer.putTileAt(bgIndex, x, y);
    if (!drawcanvasbg[y]) drawcanvasbg[y] = [];
    drawcanvasbg[y][x] = defaultBGColor;
  }
}

//let storedAsciiCommands = [];

/*function storeAsciiHTMLPos(ascii_codes, currentColor, backgroundColor, x, y) {
    // Store the drawing commands instead of executing them
    storedAsciiCommands.push({ ascii_codes, currentColor, backgroundColor, x, y });
}

function flushStoredAsciiHTML() {
    // Execute each stored command using writeAsciiHTMLPos
    storedAsciiCommands.forEach(command => {
        writeAsciiHTMLPos(command.ascii_codes, command.currentColor, command.backgroundColor, command.x, command.y);
    });
    // Clear the buffer after flushing
    storedAsciiCommands = [];
}*/


function writeAsciiHTMLPos(ascii_codes, currentColor, backgroundColor, x, y) {
  return new Promise((resolve, reject) => {
    if (enableScrolling) {
      if (y < TOTAL_HEIGHT_CHARACTERS - 1) {
        maxReachedY = y - 1;
      }
      // Scroll until we've made room for the y-coordinate we're trying to reach
      while (y > maxReachedY + 1 && y >= TOTAL_HEIGHT_CHARACTERS - 1) {
        // Shift all lines up by one
        drawcanvas.shift();
        drawcanvasbg.shift();
        canvasColor.shift();

        shiftTilesUp(); // Shift the tiles up in bglayer
        //shiftTilesUp(layer); // Shift the tiles up in layer

        removedYChars++;
        maxReachedY++;

        // Optionally clear the line at the new bottom of the canvas
        clearLine(y - removedYChars);
      }
    }
    if (ascii_codes.length == 0) {
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
  if (typeof bglayer == "undefined") return;
  return new Promise((resolve, reject) => {
    let y = VISIBLE_HEIGHT_CHARACTERS - 1 + removedYChars;
   

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
  removedYChars = 0;
  maxReachedY = 0;
  var index = getCharIndex(0, 32);
  for (var x = 0; x < TOTAL_WIDTH; x++) {
    for (var y = 0; y < TOTAL_HEIGHT_CHARACTERS; y++) {
      bglayer.putTileAt(index, x, y);
      layer.putTileAt(index, x, y);
    }
  }
}


function moveVerticalThumb(newY) {
  // Clamp the new Y position within the scrollbar track
  newY = Phaser.Math.Clamp(newY, 0, baseHeight - thumbHeight);

  // Update the thumb position
  thumbVertical.clear();
  thumbVertical.fillStyle(0xffff00, 1);
  thumbVertical.fillRect(baseWidth - 8, newY, 8, thumbHeight);

  // Update camera scrollY based on thumb position
  cam.scrollY =
    (newY / (baseHeight - thumbHeight)) *
    (TOTAL_HEIGHT_CHARACTERS * 16 - baseHeight);

  updateThumbHorizontal();
  updateThumbVertical();
  updateScrolledChars();
}

function moveHorizontalThumb(newX) {
  // Clamp the new X position within the scrollbar track
  newX = Phaser.Math.Clamp(newX, 0, baseWidth - thumbWidth);

  // Update the thumb position
  thumbHorizontal.clear();
  thumbHorizontal.fillStyle(0xffff00, 1);
  thumbHorizontal.fillRect(newX, baseHeight - 16, thumbWidth, 16);

  // Update camera scrollX based on thumb position
  cam.scrollX =
    (newX / (baseWidth - thumbWidth)) * (TOTAL_WIDTH * 8 - baseWidth);
  updateThumbHorizontal();
  updateThumbVertical();
  updateScrolledChars();
}

function getCharIndex(foreground, asciiCode) {
  var xpos = foreground;
  while (xpos >= 16) xpos = xpos - 16;
  var ypos = Math.floor(foreground / 16);
  var myx = (asciiCode % 32) * 8 + xpos * 256;
  var myy = Math.floor(asciiCode / 32) * 16 + ypos * 128;
  myx = myx / 8;
  myy = myy / 16;
  return myx + myy * 16 * 32;
}


function emitKeyPress(keyCode) {
  socket.emit("input_keypress", { key: keyCode, shiftPressed: shiftPressed, ctrlKeyPressed: ctrlKeyPressed, altgrPressed: altgrPressed });
}


function handleKeyCode(keyCode) {
  if (keyboardPressAllowed == false) {
    // Store the key press information
    storedKeyPresses.push({ key: keyCode, shiftPressed: shiftPressed, ctrlKeyPressed: ctrlKeyPressed, altgrPressed: altgrPressed });
    return;
  }
  emitKeyPress(keyCode);
}

function redrawCursor() {
  if (currentY > VISIBLE_HEIGHT_CHARACTERS - 3)
    currentY = VISIBLE_HEIGHT_CHARACTERS - 2;
  window.sprite.x = currentX * 8 + 4;
  window.sprite.y = currentY * 16 + 4;
  window.sprite.visible = true;
  clearInterval(window.cursorInterval);
  window.cursorInterval = setInterval(function () {
    if (!isColorPalette) {
      window.sprite.visible = !window.sprite.visible;
    } else {
      window.sprite.visible = false;
    }
  }, 600);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


function setCookie(name, value, daysToExpire) {
  var expires = "";
  if (daysToExpire) {
      var date = new Date();
      date.setTime(date.getTime() + (daysToExpire * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/; Secure";

}