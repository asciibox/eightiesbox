const protocol = window.location.protocol;
const socket = io.connect(
  protocol + "//" + document.domain + ":" + location.port
);

let drawing = false;

// Listen for 'draw' events from the server
socket.on("draw", async (data) => {
  //console.log(data);
  // console.log(data.ascii_codes+" currentColor:"+data.currentColor+" data.backgroundColor: "+data.backgroundColor+" data.x:"+data.x+" data.y:"+data.y);
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

socket.on("initPage", (data) => {
  initPage(data);
});

socket.on("clear", (data) => {
  clearScreen();
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

window.addEventListener("beforeunload", function (event) {
  socket.emit("custom_disconnect", {});
});

socket.on('download_ready', function(data) {    

  const canvasElements = document.getElementsByTagName("canvas");
  for (let i = 0; i < canvasElements.length; i++) {
    canvasElements[i].style.display = "none";
  }
    // Function to download all files received in the data parameter
    const downloadAll = () => {
      console.log(data.files);
      // Ensure that there are files to download
      if (data.files && data.files.length) {
        data.files.forEach((fileInfo, index) => {
        
          console.log("fileInfo:"+fileInfo);
          // Use a closure to capture the current fileInfo and index
          setTimeout(() => { // Add a timeout to space out downloads
            const link = document.createElement('a');
            link.href = fileInfo;
            // Extract filename from fileInfo.path and set it as the download attribute
            link.download = fileInfo.split('/').pop().split('?')[0];
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }, index * 300); // Increase the timeout for each file to download
        });
        setTimeout(() => { // Add a timeout to space out downloads
          hideButtons();
          console.log("ENMITTED CLOSE");        
          socket.emit("download_close", {});
          console.log("ENMITTED CLOSE");        
        }, (data.files.length+1)*300);
      } else {
        console.log('No files to download.');
      }
    };
    
    const hideButtons = () => {
      document.getElementById('download_files').parentNode.removeChild(document.getElementById('download_files'));
      document.getElementById('exit').parentNode.removeChild(document.getElementById('exit'));
      const canvasElements = document.getElementsByTagName("canvas");
      for (let i = 0; i < canvasElements.length; i++) {
        canvasElements[i].style.display = "inline";
      }
    }

    const exit = () => {
      hideButtons();
      socket.emit("download_close", {});
    }
  
    // Create and append the download button to the page
    const downloadButton = document.createElement('button');
    downloadButton.innerText = 'Download Files';
    downloadButton.id = 'download_files';
    downloadButton.onclick = downloadAll;
    document.body.appendChild(downloadButton);

    const exitButton = document.createElement('button');
    exitButton.innerText = 'Exit without downloading';
    exitButton.id = 'exit';
    exitButton.onclick = exit;
    document.body.appendChild(exitButton);

  });