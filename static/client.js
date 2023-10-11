const socket = io.connect('http://' + document.domain + ':' + location.port);


let drawing = false;

// Listen for 'draw' events from the server
socket.on('draw', async (data) => {
    //console.log(data);
    

    // console.log(data.ascii_codes+" currentColor:"+data.currentColor+" data.backgroundColor: "+data.backgroundColor+" data.x:"+data.x+" data.y:"+data.y);
    await writeAsciiHTMLPos(data.ascii_codes, data.currentColor, data.backgroundColor, data.x, data.y);
});

socket.on('initPage', (data) => {
    initPage(data);
});

socket.on('clear', (data) => {
    clearScreen();
});
