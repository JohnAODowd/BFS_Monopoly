var c = document.getElementById("boardCanvas");

		var ctx = c.getContext("2d");
		var tiles = [];
				var _width = c.width;
		var _height = c.height;

		var wanchor = _width / 13;
		var hanchor = _height / 13;

		var cLeft = c.offsetLeft;
		var cTop = c.offsetTop;
var background = new Image();
background.src = "loading.gif";

background.onload = function(){
    ctx.drawImage(background,100,200);   
}

// Load JSON File
var loadFile = function (filePath, done) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function () { console.log('2');return done(this.responseText) }
    xhr.open("GET", filePath, true);
    xhr.send();
}

// directory paths to all JSON files
var myFiles = [ "../js/monopolyJSON/board.json",
				"../js/monopolyJSON/properties.json",
				"../js/monopolyJSON/cards.json"
			  ];

// where JSON data is stored
var jsonData 	= [];
var jboard;
var jcards;
var jproperties;

// loop through each file
myFiles.forEach(function (file, i) {
    // and call loadFile
    // note how a function is passed as the second parameter
    loadFile(file, function (responseText) {
        // set jsonData[i] to the parse data since the requests
        // will not necessarily come in order
		//alert("adfasd!");
        jsonData[i] = JSON.parse(responseText);
        // all JSON obj's are available in this scope.
	    jboard 		= jsonData[0];
	    jproperties	= jsonData[1];
	    jcards 		= jsonData[2];

		/* ----------------------------------- */


		
    })
})

		function getAttribute(index, attr){
			var str = index.toString(); //force type string
			return jboard.board[str][attr];
		}

		function getCategory(index){
			return getAttribute(index, "category");
		} // returns "property", "special", "card", "tax"

		function getCardType(index){
			return getAttribute(index, "name");
		} // returns "CommunityChest", "Chance"

		function getSpecialType(index){
			return getAttribute(index, "name");
		} // returns "Go", "jail", "goToJail", "FreeParking"
		
		function getTaxType(index){
			return getAttribute(index, "name");
		} // returns "LuxuryTax", "tax"

		function getPropertyType(index){
			return getAttribute(index, "type");
		} // returns "street", "railroad", "utility"

		function getStreetColour(index){
			var path = getAttribute(index, "pID");
			return jproperties[path]["colourHex"];
		} // returns (eg.) "#ffffff"

		function getPropertyName(index){
			var path = getAttribute(index, "pID");
			return jproperties[path]["name"];
		}  

		function getPropertyPrice(index){
			var path = getAttribute(index, "pID");
			return jproperties[path]["price"];
		} 

		function getTaxAmount(index){
			return getAttribute(index, "amount");
		} // returns 100, 200

		/* ----------------------------------- */

		



		
		c.addEventListener('mousemove', function(event) {
		    var x = event.pageX - cLeft,
		        y = event.pageY - cTop;
		    //console.log(x, y)
		    tiles.forEach(function(tile) {
		        if (y > tile.top && y < tile.top + tile.width &&
		        	x > tile.left && x < tile.left + tile.height) {
					
					var category = getCategory(tile.i);
					if (category == "property"){
		                 document.getElementById("blaze").innerHTML = tile.i + " " + getPropertyName(tile.i);}
		        }
		    });

		}, false);
		
		
		
		ctx.textAlign="center";
		
		function switchOrientation(o){
		switch(o){
						case 1:
							ctx.textAlign = "right";
							textX =20;
							textY = -14;
							
							rotation = 0;
							break;
						case 0:
						ctx.textAlign = "left";
							textX = -33;
							textY = -8;
							rotation = 90;
							break;
						case 3:
						ctx.textAlign = "left";
							textX = -20;
							textY = -14;
							rotation = 0;
							break;
						case 2:
							ctx.textAlign = "left";
							textX = -4;
							textY = -8;
							rotation = 270;
						}
						
						return [textX, textY, rotation];
		}
		
		function drawRotatedText(text,price, o,x,y){
			console.log("|||||||||||zzzz|||||||||");
			var twoWords = text.includes(" ");
			var word2;
			if (twoWords){
			var words = text.split(" ");
			word2 = words[1];
			text = words[0];
			}
			var namewidth=ctx.measureText(text).width;
			var rotation;
			var textX =0;			
			var textY = -12;
			
			[textX, textY, rotation] = switchOrientation(o);
			
						
			
			ctx.save();
			ctx.translate(x,y);
			ctx.rotate(rotation*Math.PI/180); 
			ctx.fillStyle = "black";
			
			 
			if (twoWords){ctx.fillText(text,textX,textY);
			ctx.fillText(word2,textX,textY +10)}else{
			
			ctx.fillText(text,textX,textY);}
			ctx.fillText("$" +price,textX,textY +24)
			ctx.restore();
			
			console.log(text + " " + textX);
		 
		}
		
		function drawRailroad(text,price, o,x,y){
			var twoWords = text.includes(" ");
			var word2;
			if (twoWords){
			var words = text.split(" ");
			word2 = words[1];
			text = words[0];
			}
			var symbol = String.fromCharCode(0xD83D, 0xDE87);
			var rotation;
			var textX =0;			
			var textY = -12;
			
			[textX, textY, rotation] = switchOrientation(o);
			
						
			
			ctx.save();
			ctx.translate(x,y);
			ctx.rotate(rotation*Math.PI/180); 
			ctx.fillStyle = "black";
			
			 
			
			
			if (twoWords){ctx.fillText(text,textX,textY+5);
			ctx.fillText(word2,textX,textY +15)}else{
			
			ctx.fillText(text,textX,textY+5);}
			ctx.font = "15px Arial";
			ctx.fillText(symbol,textX+20,textY+12)
			ctx.restore();
		 
		}
		
		function drawName(text, price, i){
		//shuffleTiles();
		coords = orientTile(i);
		var x = coords.x + (coords.w/2);
		var y = coords.y + (coords.h/1.5);
		var o = Math.floor(i / 10);
		
		console.log("****************************");
		drawRotatedText(text, price, o,x,y);
		
		console.log("<><><><><><><><");
}

		function drawRailroadName(text, price, i){
		//shuffleTiles();
		coords = orientTile(i);
		var x = coords.x + (coords.w/2);
		var y = coords.y + (coords.h/1.5);
		var o = Math.floor(i / 10);
		drawRailroad(text, price, o,x,y);
}

		

		function Square(i) {
		  coords = orientSquare(i);
		  this.width  = 2*wanchor;
		  this.height = 2*hanchor;
		  this.x = coords.x;
		  this.y = coords.y;
		  if (i != 0){
		  i = 40-i;}
		  _drawRect(this.x, this.y, this.width, this.height);
		  tiles.push({ top : this.x, left : this.y, width : this.width, height: this.height, i : i});
		}

		
		function Tile(i) {
		  coords = orientTile(i);
		  this.width = coords.w;
		  this.height = coords.h;
		  this.x = coords.x;
		  this.y = coords.y;
		  _drawRect(this.x, this.y, this.width, this.height);
		  if (i != 0){
		  i = 40-i;}
		  tiles.push({ top : this.x, left : this.y, width : this.width, height: this.height, i : i});
		}

		function ColourTile(i, colourHex) {
		  coords = orientColourTile(i);
		  this.width = coords.w;
		  this.height = coords.h;
		  this.x = coords.x;
		  this.y = coords.y;
		  _fillRect(this.x, this.y, this.width, this.height, colourHex);
		}

		function ImageTile(i, image){
		  coords = orientImageTile(i);
		  this.width = coords.w;
		  this.height = coords.h;
		  this.x = coords.x;
		  this.y = coords.y;
		  _drawImage(this.x, this.y, this.width, this.height, image);
		}

		/* ----------------------------------- */
		// ?? ?? ?? warning ?? ?? ?? much wisdom below ?? ?? ??
		function orientTile(i) {
			var o = Math.floor(i / 10);
			var n;
			if (i < 10){
				n = i;
			} else {
				n = i % 10;
			}
			switch(o){
		  		case 0:
		  			return {
		  				x : _width - 2*wanchor - n*wanchor,
		  				y : _height - 2*hanchor,
		  				w : wanchor,
		  				h : 2*hanchor
		  			}
		  			break;
		  		case 1:
		  			return {
		  				x : 0,
		  				y : _height - 2*hanchor - (n*hanchor),
		  				w : 2*hanchor,
		  				h : wanchor
		  			}
		  			break;
				case 2:
		  			return {
						x : wanchor + n*wanchor,
						y : 0, 
						w : wanchor, 
						h : 2*hanchor
		  			}
		  			break;
				case 3:
		  			return {
						x : _width - 2*wanchor, 
						y : hanchor + n*hanchor, 
						w : 2*hanchor, 
						h : wanchor
		  			}
			}
		}

		function orientImageTile(i) {
			var o = Math.floor(i / 10);
			var n;
			if (i < 10){
				n = i;
			} else {
				n = i % 10;
			}
			switch(o){
		  		case 0:
		  			return {
		  				x : _width - 2*wanchor - n*wanchor,
		  				y : _height - 2*hanchor,
		  				w : wanchor,
		  				h : 2*hanchor - hanchor/4
		  			}
		  			break;
		  		case 1:
		  			return {
		  				x : 0,
		  				y : _height - 2*hanchor - (n*hanchor),
		  				w : 2*hanchor - hanchor/4,
		  				h : wanchor
		  			}
		  			break;
				case 2:
		  			return {
						x : wanchor + n*wanchor,
						y : wanchor/4, 
						w : wanchor, 
						h : 2*hanchor - hanchor/4
		  			}
		  			break;
				case 3:
		  			return {
						x : _width - 2*wanchor, 
						y : hanchor + n*hanchor, 
						w : 2*hanchor - hanchor/4, 
						h : wanchor
		  			}
			}
		}

		function orientColourTile(i) {
			var o = Math.floor(i / 10);
			if (i < 10){
				n = i;
			} else {
				n = i % 10;
			}
			switch(o){
		  		case 0:
		  			return {
		  				x : _width - 2*wanchor - n*wanchor,
		  				y : _height - 2*hanchor,
		  				w : wanchor,
		  				h : hanchor/2
		  			}
		  			break;
		  		case 1:
		  			return {
		  				x : 2*wanchor - wanchor/2,
		  				y : _height - 2*hanchor - (n*hanchor),
		  				w : wanchor/2,
		  				h : hanchor
		  			}
		  			break;
				case 2:
		  			return {
						x : wanchor + n*wanchor,
						y : 2*hanchor - hanchor/2, 
						w : wanchor, 
						h : hanchor/2
		  			}
		  			break;
				case 3:
		  			return {
						x : _width - 2*wanchor, 
						y : hanchor + n*hanchor, 
						w : wanchor/2, 
						h : hanchor
		  			}
			}
		}


		function orientSquare(i) {
			var o = Math.floor(i / 10);
			var n = i % 10;
			switch(o){
				case 0:
		  			return {
		  				x : _width  - 2*wanchor,
		  				y : _height - 2*hanchor
		  			}
		  			break;
		  		case 1:
		  			return {
		  				x : 0,
		  				y : _height - 2*hanchor
		  			}
		  			break;
				case 2:
		  			return {
						x : 0,
						y : 0
		  			}
		  			break;
				case 3:
		  			return {
						x : _width - 2*wanchor, 
						y : 0
		  			}
			}
		}

		/* ----------------------------------- */


		function _drawRect(x,y,w,h) {
		  console.log("Drawing at \n x     : ".concat(x)
		              .concat("\n y     : ".concat(y))
		              .concat("\n width : ".concat(w))
		              .concat("\n height: ".concat(h))
		             );
		  ctx.rect(x,y,w,h);
		  ctx.stroke();

		}

		function _fillRect(x,y,w,h, colourHex) {
		  ctx.beginPath();
		  ctx.fillStyle = colourHex;
		  ctx.fillRect(x,y,w,h);
		  ctx.closePath();
		}

		function _drawImage(x,y,w,h, img) {
			ctx.drawImage(img, x, y, w, h);
		}

		function _drawRotatedText(x,y,angle,str) {
			 ctx.save();
			 ctx.translate(x+2*wanchor, y+2*hanchor);
			 ctx.rotate(angle * (Math.PI / 180));
			 ctx.textAlign = "center";
			 var fontsize = Math.floor(wanchor/1.75).toString();
			 ctx.font = fontsize.concat("px Impact, Charcoal, sans-serif");
			 ctx.fillText(str, 0, -1.5*hanchor);
			 ctx.restore();
		}

		function rotate_point(pointX, pointY, originX, originY, angle) {
		    angle = angle * Math.PI / 180.0;
		    return {
		        x: Math.cos(angle) * (pointX-originX) - Math.sin(angle) * (pointY-originY) + originX,
		        y: Math.sin(angle) * (pointX-originX) + Math.cos(angle) * (pointY-originY) + originY
    		};
		}

		/* ----------------------------------- */
		function _createImage(src, alt, title) {
 	    var img = new Image();
		    img.src = src;
 		    if ( alt != null ) img.alt = alt;
 		    if ( title != null ) img.title = title;
 		    return img;
 		}
		function draw(){
		  ctx.clearRect(0,0,d.width,d.height);
 		  // tile imgs
		  var _path = "./assets/game_assets/board/"
 		  var chance1_img 		= _createImage(_path.concat("chance.png"));
 		  var chance2_img 		= _createImage(_path.concat("chance2.png"));
 		  var chance3_img 		= _createImage(_path.concat("chance3.png"));
 
 		  var community_img 	= _createImage(_path.concat("community-chest.png"));
 		  var luxury_img 		= _createImage(_path.concat("luxury-tax.png"));
 		  var income_img		= _createImage(_path.concat("income-tax.png"));
 		  var water_img 		= _createImage(_path.concat("water.png"));
 		  var electric_img		= _createImage(_path.concat("electric.png"));
 		  var railroad_img		= _createImage(_path.concat("railroad.png"));

		  //corner imgs
		  var go_img 			= _createImage(_path.concat("go.png"));
 		  var jail_img 			= _createImage(_path.concat("jail.png"));
 		  var free_parking_img 		= _createImage(_path.concat("free-parking.png"));
 		  var go_to_jail_img 		= _createImage(_path.concat("go-to-jail.png"));
		  var type;
		  var tile;


		  for(var i = 0; i < 40; i++){
		  	switch(getCategory(i)){
		  		case "special":
		  			//make a square
		  			type = getSpecialType(i);
		  			if (type == "Go"){
		  				// make the Go tile
		  				tile = new Square(i);
						ctx.drawImage(go_img, Object.values(tile)[2], Object.values(tile)[3], Object.values(tile)[0], Object.values(tile)[1]);
		  			} else if (type == "jail"){
		  				tile = new Square(i);
						ctx.drawImage(jail_img, Object.values(tile)[2], Object.values(tile)[3], Object.values(tile)[0], Object.values(tile)[1]);
		  			} else if (type == "FreeParking"){
		  				// make Free Parking tile
		  			  	tile = new Square(i);
						ctx.drawImage(free_parking_img, Object.values(tile)[2], Object.values(tile)[3], Object.values(tile)[0], Object.values(tile)[1]);
		  			} else {
		  				// make the goToJail tile
		  				tile = new Square(i);
						ctx.drawImage(go_to_jail_img, Object.values(tile)[2], Object.values(tile)[3], Object.values(tile)[0], Object.values(tile)[1]);
		  			}
		  			break;

		  		case "property":
		  			type = getPropertyType(i);
		  			if (type == "street") {
		  				// make a street tile
		  				tile = new Tile(i);
						var name = getPropertyName(i);
						var price = getPropertyPrice(i)
						tile = drawName(name, price, i);
		  				tile = new ColourTile(i, getStreetColour(i));
		  			} else if (type == "railroad") {
		  				// make a railroad tile
		  				tile = new Tile(i);
						var name = getPropertyName(i);
						var price = getPropertyPrice(i)
						tile = drawRailroadName(name, price, i);
		  				//tile = new ImageTile(i, railroad_img);
		  			} else {
		  				// make a utility tile
		  				if (getPropertyName(i) == "Water Works"){
		  					tile = new Tile(i);
							tile = new ImageTile(i, water_img);
		  				} else {
		  					tile = new Tile(i);
							tile = new ImageTile(i, electric_img);
						}
		  			}
		  			break;

	  		case "card":
		  			type = getCardType(i);
		  			if (type == "Chance"){
		  				// make a chance tile
		  				tile = new Tile(i);
		  				var chance_img;
		  				if (i == 7) chance_img = chance1_img;
		  				if (i == 22) chance_img =chance2_img;
		  				if (i == 36) chance_img = chance3_img;
						tile = new ImageTile(i, chance_img);		  			
					} else {
		  				// make a community tile
		  				tile = new Tile(i);
						tile = new ImageTile(i, community_img);
		  			}
		  			break;


		  		case "tax":
		  			type = getTaxType(i);
		  			if (type == "LuxuryTax"){
		  				// make the LuxuryTax tile
		  				tile = new Tile(i);
						tile = new ImageTile(i, luxury_img);

		  			} else {
		  				// make the IncomeTax tile

		  				tile = new Tile(i);
						tile = new ImageTile(i, income_img);
		  			}
		  		}
		  }
		  
		  console.log(tiles);
		  draw = function(){}; // Google "js noop" 
		  
		}
		
		// init once
	setTimeout(draw, 1500
	);
