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
