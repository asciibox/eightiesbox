var fs = require('fs');

   var ansicolors = [
      '000000', 'aa0000', '00aa00', 'aa5500', '0000aa', 'aa00aa', '00aaaa', 'aaaaaa', '555555', 'ff5555', // 10
      '55ff55', 'ffff55', '5555ff', 'ff55ff', '55ffff', 'ffffff', '000000', '00005f', '000087', '0000af', // 20
      '0000D7', '0000FF', '005F00', '005F5F', '005f87', '005faf', '005fd7', '005fff', '008700', '00875f', // 30
      '008787', '0087af', '0087d7', '0087ff', '00af00', '00af5f', '00af87', '00afaf', '00afd7', '00afff', // 40
      '00d700', '00d787', '00d787', '00d7af', '00d7af', '00d7ff', '00ff00', '00ff5f', '00ff87', '00ffaf', // 50
      '00ffd7', '00ffff', '5f0000', '5f5fff', '5f0087', '5f00af', '5f00d7', '5f00ff', '5f5f00', '5f5f5f', // 60
      '5f5f87', '5f5faf', '5f5fd7', '5f5fff', '5f8700', '5f875f', '5f8787', '5f87af', '5f87d7', '5f87ff', // 70
      '5faf00', '5faf5f', '5faf87', '5fafaf', '5fafd7', '5fafff', '5fd700', '5fd75f', '5fd787', '5fd7af', // 80
      '5fd7d7', '5fd7ff', '5fff00', '3399cc', '5fff87', '5fffaf', '5fffd7', '5fffff', '870000', '87005f', // 90
      '870087', '8700af', '8700af', '8700ff', '875f00', '875f5f', '875f87', '875faf', '875fd7', '875fff', // 100 
      '878700', '87875f', '878787', '8787af', '8787d7', '8787ff', '87af00', '87af5f', '87af87', '87afaf', // 110
      '87afd7', '87afff', '87d700', '87d75f', '87d787', '87d7af', '87d7d7', '87d7ff', '87ff00', '87ff5f', // 120
      '87ff87', '87ffaf', '87ffd7', '87ffff', 'af0000', 'af005f', 'af0087', 'af00af', 'af00d7', 'af00ff', // 130
      'af5f00', 'af5f5f', 'af5f87', 'af5faf', 'af5fd7', 'af5fff', 'af8700', 'af875f', 'af8787', 'af87af', // 140
      'af87d7', 'af87ff', 'afaf00', 'afd7af', 'afaf87', 'afafaf', 'afafd7', 'afafff', 'afd700', 'afd75f', // 150
      'afd787', 'afd7af', 'afd7d7', 'afd7ff', 'afff00', 'afff5f', 'afff87', 'afffaf', 'afffd7', 'afffff', // 160
      'd70000', 'd7005f', 'dd2699', 'd700af', 'd700d7', 'd700ff', 'd75f00', 'd75f5f', 'd75f87', 'd75faf', // 170
      'd75fd7', 'd75fff', 'd78700', 'd7875f', 'd78787', 'd787af', 'd787d7', 'd787ff', 'd7af00', 'd7af5f', // 180
      'd7af87', 'd7afaf', 'd7afd7', 'd7afff', 'd7d75f', 'd7d75f', 'd7d787', 'd7d7af', 'd7d7d7', 'd7d7ff', // 190
      'd7ff00', 'd7ff5f', 'd7ff87', 'd7ffaf', 'd7ffd7', 'd7ffff', 'ff0000', 'ff005f', 'ff0087', 'ff00af', // 200
      'ff00d7', 'ff00ff', 'ff5f00', 'ff5f5f', 'ff5f87', 'ff5faf', 'ff5fd7', 'ff5fff', 'ff8700', 'ff875f', // 210
      'ff8787', 'ff87af', 'ff87d7', 'ffaf00', 'ffaf00', 'ffaf5f', 'ffaf87', 'ffafaf', 'ffafd7', 'ffafff', // 220
      'ffd700', 'ffd75f', 'ffd787', 'ffd7af', 'ffd7d7', 'ffd7ff', 'ffff00', 'ffff5f', 'ffff87', 'ffffaf', // 230
      'ffffd7', 'ffffff', '080808', '121212', '1c1c1c', '262626', '303030', '3a3a3a', '444444', '4e4e4e', // 240
      '585858', '626262', '6c6c6c', '767676', '808080', '8a8a8a', '949494', '9e9e9e', 'a8a8a8', 'b2b2b2', // 250
      'bcbcbc', 'c6c6c6', 'd0d0d0', 'e4e4e4', 'e4e4e4', 'eeeeee', 'ffffff'
    ];

var Canvas = require('canvas')
  , Image = Canvas.Image;
  
fs.readFile(__dirname + '/../images/CO_437_8x16.png', function(err, squid){
  if (err) throw err;
  img = new Image;
  img.src = squid;
  
  var i, background;
            characterWidth = img.width / 32;
            
            characterHeight = img.height / 8;
            codepageImgs = [];
            backgroundImgs = [];
            console.log("Creating w:"+characterWidth+" h: "+characterHeight);
            background = createCanvas(characterWidth, characterHeight);
            for (i = 0; i < ansicolors.length; i++) {
            	console.log("color "+i);
                codepageImgs[i] = colorCanvas(img, i, true);
                backgroundImgs[i] = colorCanvas(background, i, false);
            }
  
  
    newCanvas = new Canvas(img.width, img.height)
    console.log("New img w: "+(img.width)+" img.height h: "+(img.height));
    ctx = newCanvas.getContext('2d');
          
            console.log("Merging");
            for (var i = 0; i < codepageImgs.length; i++) 
            {
                console.log("Merging "+i);
                var x = i;
                while (x >= 16) x=x-16;
                var y = Math.floor(i/16);
                
    
                ctx.drawImage(codepageImgs[i], 0, 0, 256, 128, x*256, y*128, 256, 128);
            }
            
            

			var fs2 = require('fs')
			  , out = fs2.createWriteStream(__dirname + '/text.png')
			  , stream = newCanvas.pngStream();
	
			stream.on('data', function(chunk){
			  out.write(chunk);
			});

			stream.on('end', function(){
			  console.log('saved png');
			});
        
});

        function createCanvas(width, height) {
            var newCanvas;
            newCanvas = new Canvas(width, height)
            
            return newCanvas;
        }

        function colorCanvas(source, color, preserveAlpha) {
            var canvas, ctx, imageData, i;
            canvas = createCanvas(source.width, source.height);
            ctx = canvas.getContext("2d");
            ctx.drawImage(source, 0, 0);
            imageData = ctx.getImageData(0, 0, source.width, source.height);
            for (i = 0; i < imageData.data.length; ++i) {
                
                var c1 = h2d(ansicolors[color].substring(0,2));
                var c2 = h2d(ansicolors[color].substring(2,4));
                var c3 = h2d(ansicolors[color].substring(4));
               
                imageData.data[i++] = c1; // COLORS[color][0];
                imageData.data[i++] = c2; // COLORS[color][1];
                imageData.data[i++] = c3; // COLORS[color][2];
                if (!preserveAlpha) { imageData.data[i] = 255; }
            }
            ctx.putImageData(imageData, 0, 0);
            return canvas;
        }

function d2h(d) {return d.toString(16);}
function h2d(h) {return parseInt(h,16);}