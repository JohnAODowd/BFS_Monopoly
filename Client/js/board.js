// Load JSON File
var loadFile = function (filePath, done) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function () { console.log('2');return done(this.responseText) }
    xhr.open("GET", filePath, true);
    xhr.send();

}
// paths to all of your files
var myFiles = [ "../Server/monopoly/board.json",
				"../Server/monopoly/properties.json",
				"../Server/monopoly/cards.json"
			  ];
// where you want to store the data
var jsonData 	= [];
var jboard;
var jcards;
var jproperties;
// loop through each file
myFiles.forEach(function (file, i) {
    // and call loadFile
    // note how a function is passed as the second parameter
    // that's the callback function
    loadFile(file, function (responseText) {
        // we set jsonData[i] to the parse data since the requests
        // will not necessarily come in order
        // so we can't use JSONdata.push(JSON.parse(responseText));
        // if the order doesn't matter, you can use push
        jsonData[i] = JSON.parse(responseText);
        // or you could choose not to store it in an array.
        // whatever you decide to do with it, it is available as
        // responseText within this scope (unparsed!)
	    jboard 		= jsonData[0];
	    jproperties	= jsonData[1];
	    jcards 		= jsonData[2];

		/* ----------------------------------- */

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

		function getPropertyColour(index){
			var path = getAttribute(index, "property");
			return jproperties.properties[path]["colourHex"];
		} // returns (eg.) "#ffffff"

		function getTaxAmount(index){
			return getAttribute(index, "amount");
		} // returns 100, 200

		/* ----------------------------------- */

		var _width = 250;
		var _height = 250;

		var wanchor = _width / 13;
		var hanchor = _height / 13;

		function Square(i) {
		  //this.index  = Integer.parseInt(i);
		  this.width  = 2*wanchor;
		  this.height = 2*hanchor;

		  _drawRect( _width-this.width,
		            _height-this.width,
		            this.width,
		            this.height);
		}

		function Tile(i, o) {
		  //this.index  = Integer.parseInt(i);
		  this.width  = wanchor;
		  this.height = 2*hanchor;
		  this.orient = o;
		  this.n = i % 10;
		  
		  var windent = (2*wanchor) + this.n * this.width;
		  var hindent = this.height;

		  _drawRect(_width-windent,
		            _height-hindent,
		            this.width,
		            this.height);
		}

		/* ----------------------------------- */

		function _drawRect(x1,y1,w,h) {
		  console.log("Drawing at \n x     : ".concat(x1)
		              .concat("\n y     : ".concat(y1))
		              .concat("\n width : ".concat(w))
		              .concat("\n height: ".concat(h))
		             );
		  ctx.rect(x1,y1,w,h);
		  ctx.stroke();
		}

		function _fillRect(x1,y1,colourHex) {
		  ctx.beginPath();
		  ctx.fillStyle = colourHex;
		  var w = wanchor;
		  var h = hanchor/4; // thanks hassan
		  ctx.fillRect(x1,y1,(x1 + w) ,(y1 + h));
		  ctx.closePath();
		}

		function rotate_point(pointX, pointY, originX, originY, angle) {
		    angle = angle * Math.PI / 180.0;
		    return {
		        x: Math.cos(angle) * (pointX-originX) - Math.sin(angle) * (pointY-originY) + originX,
		        y: Math.sin(angle) * (pointX-originX) + Math.cos(angle) * (pointY-originY) + originY
    		};
		}

		/* ----------------------
		------------- */

		var c = document.getElementById("boardCanvas");
		var ctx = c.getContext("2d");

		function draw(){
		  //test draw
		  _drawRect(0,0,2*wanchor,2*hanchor);
		  
		  var orient = 0;
		  var type;
		  var tile;
		  for(var i = 0; i < 40; i++){
		  	switch(getCategory(i)){
		  		case "special":
		  			//make a side
		  			//make a square
		  			type = getSpecialType(i);
		  			if (type == "Go"){
		  				// make the Go tile
		  			} else if (type == "jail"){
		  				// make jail tile
		  			} else if (type == "FreeParking"){
		  				// make Free Parking tile
		  			} else {
		  				// make the goToJail tile
		  			}
		  			//increment orient
		  			break;
		  		case "property":
		  			type = getPropertyType(i);
		  			if (type == "street") {
		  				// make a street tile
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
		  			} else {
		  				// make a community tile
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

		  /*
		  var corner = new Square(0);
		  var tile;
		  for(var i = 1; i < 10; i++){
		    tile = new Tile(i);
		  }
		*/
		}
		draw();
    })
})