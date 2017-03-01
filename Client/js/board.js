

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
	    jproperties = jsonData[1];
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
		} // board.["property"], otherwise board.["name"]

		function getAttribute(index, attr){
			return jboard.board[index.toString()][attr];
		}

		function getCategory(index){
			return getAttribute(index, "category");
		} // returns "property"

		function getCardType(index){
			return getAttribute(index, "name");
		} // returns "CommunityChesy", "Chance"

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


		var Board = {
		}

		var Side = {
		}

		var Line = {
		}

		var Square = {
		  width: 2*wanchor,
		  height: 2*hanchor
		}

		var Tile = {
		  width: wanchor,
		  height: 2*hanchor
		}

		var PropertyTile = {
		}

		var UtilityTile = {
		}

		var TransportTile = {
		}

		var ChanceTile = {
		}

		var CommunityTile = {
		}

		/* ----------------------------------- */

		var c = document.getElementById("boardCanvas");
		var ctx = c.getContext("2d");

		function draw(){

		}

    })
})