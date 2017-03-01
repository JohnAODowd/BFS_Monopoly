

// Load JSON File
var loadFile = function (filePath, done) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function () { console.log('2');return done(this.responseText) }
    xhr.open("GET", filePath, true);
    xhr.send();

}
// paths to all of your files
var myFiles = [ "../Server/monopoly/board.json","../Server/monopoly/properties.json","../Server/monopoly/cards.json"
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
			return jboard.board[index.toString()][attr];
		}

		function getCategory(index){
			return getAttribute(index, "category");
		} // returns "property", "special", "card", "tax"

		function getCardType(index){
			return getAttribute(index, "name");
		} // returns "CommunityChest", "Chance"

		function getPropertyType(index){
			return getAttribute(index, "type");
		} // returns "street", "railroad", "utility"

		function getColour(index){
			var path = getAttribute(index, "property");
			return jproperties.properties[path]["colourHex"];
		} // returns (eg.) "#ffffff"

		/* ----------------------------------- */

		var _width = 500;
		var _height = 500;

		var wanchor = _width / 13;
		var hanchor = _height / 13;

		function Square(i) {
		  this.index  = Integer.parseInt(i);
		  this.name   = getName(i);
		  this.width  = 2*wanchor;
		  this.height = 2*hanchor;

		  _drawRect( _width-this.width, _height-this.width, this.width, this.height);
		}

		function Tile(i) {
		  this.index  = Integer.parseInt(i);
		  this.cat    = getCategory(i);
		  this.name   = getName(i);
		  this.width  = wanchor;
		  this.height = 2*hanchor;
		  this.n = (index % 10);
		  
		  _drawRect( (_width - 2*this.width - this.n*this.width ), _height - 2*this.width - (this.n-1)*this.width); 
		}

		/* ----------------------------------- */

		function _drawRect(x1,y1,w,h) {
		  ctx.beginPath();
		  ctx.rect(x1,y1,(x1 + w) ,(y1 + h));
		  ctx.stroke();
		  ctx.closePath();
		}

		function _fillRect(x1,y1,colourHex) {
		  ctx.beginPath();
		  ctx.fillStyle = colourHex;
		  var w = wanchor/4;
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

		/* ----------------------------------- */

		var c = document.getElementById("boardCanvas");
		var ctx = c.getContext("2d");

		function draw(){
			for(var i in jboard){
				switch(getCategory(i)) {
					case "special":
						var sq = new Square(i);
						break;
					case "property":
						var tile = new Tile(i);
						break;
					case "card":
						// get more info, then
						// draw tile
						break;
					case "tax" :
						// get more info, then
						// draw tile
				}
			}
		}

		draw();

    })
})