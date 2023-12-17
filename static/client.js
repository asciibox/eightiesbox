var persistentID = "";
var chosen_bbs = 0;
const protocol = window.location.protocol;
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
    } else {
      const canvasElements = document.getElementsByTagName("canvas");
      for (let i = 0; i < canvasElements.length; i++) {
        canvasElements[i].parentNode.removeChild(canvasElements[i]);
      }
      initPage(data);
    }
  });

  socket.on("connect", function () {
    console.log("Connected with SID:", window.socket.id);
  });

  socket.on("draw", async (data) => {
    await writeAsciiHTMLPos(
      data.ascii_codes,
      data.currentColor,
      data.backgroundColor,
      data.x,
      data.y
    );
  });

  socket.on("draw_to_status_bar", async (data) => {
    await writeAsciiToStatusBar(
      data.ascii_codes,
      data.currentColor,
      data.backgroundColor
    );
  });

  socket.on("clear", (data) => {
    clearScreen();
  });

  socket.on("ansi_mod_editor", (data) => {
    clearScreen();
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
  });

  socket.on("uploadFile", (data) => {
    // Hide all canvas elements
    const canvasElements = document.getElementsByTagName("canvas");
    for (let i = 0; i < canvasElements.length; i++) {
      canvasElements[i].style.display = "none";
    }

    // Display the fileUploadDiv
    const uploadDiv = document.getElementById("fileUploadDiv");
    uploadDiv.style.display = "inline";
    uploadToken = data.uploadToken;
    current_file_area = data.current_file_area;
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
        canvasElements[i].style.display = "inline";
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