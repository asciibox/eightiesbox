var persistentID = "";
var chosen_bbs = 0;
const protocol = window.location.protocol;
var uploadFileType = 'ANS';
var uploadToken = '';
var hrefs = [];  // Global array to store hrefs
var loadedImages = [];

let commandQueue = [];


var socket = io.connect(
  protocol + "//" + document.domain + ":" + location.port,
  {
    allowEIO3: true,
    reconnection: true, // Make sure reconnection is enabled
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: Infinity,
  }
);

var inited = false;

let drawing = false;

function toggleKeyboard() {

  var verticalScale;
  if (document.getElementById("simple-keyboard").style.display == "none") {
    document.getElementById("simple-keyboard").style.display = "inline";
    verticalScale = (window.innerHeight - 320) / baseHeight;
  } else {
    document.getElementById("simple-keyboard").style.display = "none";
    verticalScale = window.innerHeight / baseHeight;
  }
  if (verticalScale > 1) verticalScale = 1;
  var canvasElement = document.querySelector("#game-container canvas");
  canvasElement.style.height = baseHeight * verticalScale + "px";

}

window.addEventListener("beforeunload", function (event) {
  socket.emit("disconnect_by_window_listener", {});
});

setupSocketEventListeners(socket);

function setupSocketEventListeners(socket) {
  // Listen for 'draw' events from the server
  socket.on("initPage", (data) => {
    console.error("initPage");
    if (inited == false) {
      initPage(data);
      inited = true;
      const canvasElements = document.getElementsByTagName("canvas");
      for (let i = 0; i < canvasElements.length; i++) {
        if (canvasElements[i].className != "tracker") {
        
          canvasElements[i].addEventListener('mousemove', function(e) {
            const rect = canvasElements[i].getBoundingClientRect();
            const pointer = {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            };
            
            let tileX = Math.floor(pointer.x / canvasScaleX /  8) + 1;
            let tileY = Math.floor(pointer.y / canvasScaleY / 16) + 1;
            let isOverHref = false;
            
            for (let href of hrefs) {

                let hrefLength = 0;
                if (href.length) {
                  hrefLength = href.length;
                }
                /*console.log("hrefLenghth: "+hrefLength);
                console.log(tileX + " >= " + href.x + " && " + tileX + " < " + (Number(href.x) + Number(hrefLength)));
                console.log(tileY + " == " + (Number(href.y) + 1));*/
                if (tileX >= parseInt(href.x) && 
                    tileX < (parseInt(href.x) + parseInt(href.length)) && 
                    tileY > parseInt(href.y) && 
                    tileY <= (parseInt(href.y) + parseInt(href.height))) {
                    isOverHref = true;
                    break;
                }
            }

            canvasElements[i].style.cursor = isOverHref ? 'pointer' : 'default';
        });

        }
      }
    } else {
      const canvasElements = document.getElementsByTagName("canvas");
      for (let i = 0; i < canvasElements.length; i++) {
        canvasElements[i].parentNode.removeChild(canvasElements[i]);
      }
      initPage(data);
    }
  });



socket.on("draw", async (data) => {
    enqueueCommand({ type: "draw", data: data });
    processQueue();
});

socket.on("backgroundimage", async (data) => {
  enqueueCommand({ type: "backgroundimage", data: data });
  processQueue();
});

socket.on("clear", async (data) => {
  enqueueCommand({ type: "clear", data: data });
  processQueue();
});


function enqueueCommand(command) {
  commandQueue.push(command);
}

async function processQueue() {
  if (commandQueue.length > 0) {
      const command = commandQueue.shift(); // Dequeue the next command
      await executeCommand(command);
  }
}

async function executeCommand(command) {
  switch (command.type) {
      case "draw":
        if (command.data.command && command.data.command === 'clear') {
          loadedImages.forEach(image => image.destroy());
          loadedImages=[];
          clearScreen();
          hrefs = [];
        } else {

          await writeAsciiHTMLPos(
              command.data.ascii_codes,
              command.data.currentColor,
              command.data.backgroundColor,
              command.data.x,
              command.data.y
          );
        }
          break;
      case "clear":
          loadedImages.forEach(image => image.destroy());
          loadedImages=[];
          clearScreen();
          hrefs = []
          break;
      case "backgroundimage":
           // Extracting properties from the data object
            const { filename, x, y, width, height, dynamicWidth } = command.data;

            // Constants for tile dimensions in pixels
            const tileWidthInPixels = 8;
            const tileHeightInPixels = 16;

            // Convert tile coordinates and dimensions to pixels
            const pixelX = x * tileWidthInPixels;
            const pixelY = y * tileHeightInPixels;
            const pixelWidth = dynamicWidth ? undefined : width * tileWidthInPixels;
            const pixelHeight = height * tileHeightInPixels;

            // Access the current scene
            let currentScene = game.scene.getScenes(true)[0];

            // Load and display the image
            if (currentScene) {
                console.log("IMAGEURL:" + filename);
                currentScene.load.image(filename, filename);
                currentScene.load.once('complete', () => {
                    let image = currentScene.add.image(pixelX, pixelY, filename);

                    // If dynamicWidth is true, set the height and adjust width to maintain aspect ratio
                    if (dynamicWidth) {
                        image.displayHeight = pixelHeight;
                        image.displayWidth = image.width * (image.displayHeight / image.height);
                    } else {
                        image.setDisplaySize(pixelWidth, pixelHeight);
                    }

                    image.setDepth(IMAGE_LAYER_DEPTH);
                    loadedImages.push(image);

                    // Set image origin to top-left corner
                    image.setOrigin(0, 0);
                });
                currentScene.load.start();
            } else {
                console.error("No active scene found to load the image.");
            }

          break;
      // ... other command types
  }
  processQueue(); // Process the next command in the queue
}



  socket.on("getJWTToken", function(data) {

    let jwtToken = getCookie('jwtToken'+data.chosen_bbs);
    socket.emit("set_user_and_login", { jwtToken : jwtToken, chosen_bbs : data.chosen_bbs });

  })

  socket.on("connect", function () {
    console.log("Connected with SID:", window.socket.id);
  });

  socket.on("a", function (data) {
    // Add the received href data to the global array
    hrefs.push(data);
  });

 

 
  socket.on("draw_to_status_bar", async (data) => {
    await writeAsciiToStatusBar(
      data.ascii_codes,
      data.currentColor,
      data.backgroundColor
    );
  });


  socket.on("ansi_mod_editor", (data) => {
    loadedImages.forEach(image => image.destroy());
    loadedImages=[];
    clearScreen();
    hrefs = []
    enableTrackerKeyboard = true;
  });
  socket.on("graphic_mod_editor", (data) => {
    var canvas = document.getElementsByClassName("tracker");
    console.log(canvas);
    canvas[0].style.display = "inline";
    enableTrackerKeyboard = true;
  });

  socket.on("clearline", (data) => {
    clearLine(data.y);
  });

  socket.on("toggle_keyboard", () => {
    toggleKeyboard();
  });

  socket.on("uploadFile", (data) => {
    uploadToken = data.uploadToken;
    current_file_area = data.current_file_area;
    // Hide all canvas elements
    const canvasElements = document.getElementsByTagName("canvas");
    for (let i = 0; i < canvasElements.length; i++) {
      canvasElements[i].style.display = "none";
    }

    // Display the fileUploadDiv
    const uploadDiv = document.getElementById("fileUploadDiv");
    uploadDiv.style.display = "inline";    
  });

  socket.on("uploadANSI", (data) => {
    // Hide all canvas elements
    const canvasElements = document.getElementsByTagName("canvas");
    for (let i = 0; i < canvasElements.length; i++) {
      canvasElements[i].style.display = "none";
    }

    // Display the fileUploadDiv
    const uploadDiv = document.getElementById("ANSIUploadDiv");
    uploadDiv.style.display = "inline";
    uploadFileType = data.upload_file_type;
    if (data.upload_token) uploadToken = data.upload_token;
        console.error(uploadFileType);
        if (uploadFileType=='Timeline') {
          document.getElementById('toggleButtonANSI').innerHTML='Close Timeline Image Upload';
        } else
        if (uploadFileType=='HTML') {
          document.getElementById('toggleButtonANSI').innerHTML='Close HTML Upload';
        } else {
          document.getElementById('toggleButtonANSI').innerHTML='Close ANSI Upload';
        }
  });

  function removeButtons() {
    if (document.getElementById("download_files")) {
      document
        .getElementById("download_files")
        .parentNode.removeChild(document.getElementById("download_files"));
    }
    if (document.getElementById("exit")) {
      document
        .getElementById("exit")
        .parentNode.removeChild(document.getElementById("exit"));
    }
  }

  socket.on("set_chosen_bbs", function (data) {
    chosen_bbs = data.chosen_bbs;
  });

  socket.on("download_ready", function (data) {
    removeButtons();

    console.log("DOWNLOAD_READY called");
    const canvasElements = document.getElementsByTagName("canvas");
    persistentID = data.sid;
    for (let i = 0; i < canvasElements.length; i++) {
      canvasElements[i].style.display = "none";
    }
    // Function to download all files received in the data parameter
    const downloadAll = () => {
      // Ensure that there are files to download
      hideButtons();
      if (data.files && data.files.length) {
        data.files.forEach((fileInfo, index) => {
          console.log("fileInfo:" + fileInfo);
          // Use a closure to capture the current fileInfo and index
          setTimeout(() => {
            // Add a timeout to space out downloads
            const link = document.createElement("a");
            link.href = fileInfo;
            // Extract filename from fileInfo.path and set it as the download attribute
            link.download = fileInfo.split("/").pop().split("?")[0];
            link.style.display = "none";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }, index * 300); // Increase the timeout for each file to download
        });
        setTimeout(() => {
          // Add a timeout to space out downloads
          setupSocketEventListeners(socket);
          setupKeypressListeners();
          //alert("OK");
        }, (data.files.length + 1) * 300);
      } else {
        console.log("No files to download.");
      }
    };

    const hideButtons = () => {
      removeButtons();
      const canvasElements = document.getElementsByTagName("canvas");
      for (let i = 0; i < canvasElements.length; i++) {
        if (canvasElements[i].className != "tracker") {
        canvasElements[i].style.display = "inline";
        }
      }
    };

    const exit = () => {
      hideButtons();
      socket.emit("download_close", {});
    };

    // Create and append the download button to the page
    const downloadButton = document.createElement("button");
    downloadButton.innerText = "Download Files";
    downloadButton.id = "download_files";
    downloadButton.onclick = downloadAll;
    document.body.appendChild(downloadButton);

    const exitButton = document.createElement("button");
    exitButton.innerText = "Exit without downloading";
    exitButton.id = "exit";
    exitButton.onclick = exit;
    document.body.appendChild(exitButton);

    //socket.emit("custom_disconnect", {});
    //alert("Disconnected");
  });
}

// Event listener for paste event
document.addEventListener('paste', (event) => {
  // Prevent the default paste action
  event.preventDefault();

  // Get the text from the clipboard
  const clipboardData = event.clipboardData || window.clipboardData;
  const pastedText = clipboardData.getData('Text');

  alert(pastedText);
});

socket.on('authentication', function(data) {
  let jwtToken = data.jwt_token;
  let chosen_bbs = data.chosen_bbs;
  // Store the token in cookies or local storage
  setCookie('jwtToken'+chosen_bbs, jwtToken, 30); // Set a bbs-based cookie named 'jwtToken' that expires in 30 days
});


socket.on('clear_cookie', function(data) {
  let chosenBBS = data.chosen_bbs;
  // Store the token in cookies or local storage
  clearCookie('jwtToken'+chosenBBS);
});

function clearCookie(name) {
  document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; Secure";
}