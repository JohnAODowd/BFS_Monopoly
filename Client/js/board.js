// Load JSON File
var loadFile = function (filePath, done) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function () { console.log('2');return done(this.responseText) }
    xhr.open("GET", filePath, true);
    xhr.send();

}

// directory paths to all JSON files
var myFiles = [ "../Server/monopoly/board.json",
				"../Server/monopoly/properties.json",
				"../Server/monopoly/cards.json"
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
        jsonData[i] = JSON.parse(responseText);
        // all JSON obj's are available in this scope.
	    jboard 		= jsonData[0];
	    jproperties	= jsonData[1];
	    jcards 		= jsonData[2];

		/* ----------------------------------- */

		// un-used due to lack of readability
		function getName(index){
			var name;
			switch(getCategory(index)) {
				case "property":
					name = getAttribute(index,"property");
					break;
				default:
					name = getAttribute(index, "name");
			} 
			return name;
		} // board[index]["property"], otherwise board[index]["name"]

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
			var path = getAttribute(index, "property");
			return jproperties.properties[path]["colourHex"];
		} // returns (eg.) "#ffffff"

		function getPropertyName(index){
			var path = getAttribute(index, "property");
			return jproperties.properties[path]["name"];
		} // returns (eg.) "#ffffff"

		function getPropertyPrice(index){
			var path = getAttribute(index, "property");
			return jproperties.properties[path]["name"];
		} // returns (eg.) "#ffffff"

		function getTaxAmount(index){
			return getAttribute(index, "amount");
		} // returns 100, 200

		/* ----------------------------------- */

		var c = document.getElementById("boardCanvas");
		var ctx = c.getContext("2d");

		var _width = c.width;
		var _height = c.height;

		var wanchor = _width / 13;
		var hanchor = _height / 13;

		function Square(i) {
		  coords = orientSquare(i);
		  this.width  = 2*wanchor;
		  this.height = 2*hanchor;
		  this.x = coords.x;
		  this.y = coords.y;
		  _drawRect(this.x, this.y, this.width, this.height);
		}

		function Tile(i) {
		  coords = orientTile(i);
		  this.width = coords.w;
		  this.height = coords.h;
		  this.x = coords.x;
		  this.y = coords.y;
		  _drawRect(this.x, this.y, this.width, this.height);
		}

		function ColourTile(i, colourHex) {
		  coords = orientColourTile(i);
		  this.width = coords.w;
		  this.height = coords.h;
		  this.x = coords.x;
		  this.y = coords.y;
		  _fillRect(this.x, this.y, this.width, this.height, colourHex);
		}

		/* ----------------------------------- */
		// 🐘 🐘 🐘 warning 🐘 🐘 🐘 much wisdom below 🐘 🐘 🐘
		function orientTile(i) {
			var o = Math.floor(i / 10);
			var n = i % 10;
			switch(o){
		  		case 0:
		  			return {
		  				x : wanchor + n*wanchor,
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

		function orientColourTile(i) {
			var o = Math.floor(i / 10);
			var n = i % 10;
			switch(o){
		  		case 0:
		  			return {
		  				x : wanchor + n*wanchor,
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

		function draw(){
		  //test draw
		  //_drawRect(0,0,2*wanchor,2*hanchor);
		  
		  // tile imgs
		  var chance_img 		= document.getElementById("chance");
		  var community_img 	= document.getElementById("community");
		  var luxury_img 		= document.getElementById("luxury_tax");

		  //corner imgs
		  var go_img 			= document.getElementById("go");
		  var jail_img 			= document.getElementById("jail");
		  var free_parking_img 	= document.getElementById("free_parking");
		  var go_to_jail_img 	= document.getElementById("go_to_jail");

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
		  				tile = new ColourTile(i, getStreetColour(i));
		  			} else if (type == "railroad") {
		  				// make a railroad tile
		  			} else {
		  				// make a utility tile
		  			}
		  			break;
		  		case "card":
		  			type = getCardType(i);
		  			if (type == "Chance"){
		  				// make a chance tile
		  				tile = new Tile(i);
		  				ctx.drawImage(chance_img, Object.values(tile)[2], Object.values(tile)[3], Object.values(tile)[0], Object.values(tile)[1]);
		  			} else {
		  				// make a community tile
		  				tile = new Tile(i);
		  				ctx.drawImage(community_img, Object.values(tile)[2], Object.values(tile)[3], Object.values(tile)[0], Object.values(tile)[1]);

		  			}
		  			break;
		  		case "tax":
		  			type = getTaxType(i);
		  			if (type == "LuxuryTax"){
		  				// make the LuxuryTax tile
		  			} else {
		  				// make the IncomeTax tile
		  			}
		  	}
		  }
		  draw = function(){}; // Google "js noop" 
		}
		// init once
		draw();
    })
})