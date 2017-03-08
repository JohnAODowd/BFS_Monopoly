	var d = document.getElementById("dynamicCanvas");
		var dtx = d.getContext("2d");

dtx.font = "10px Arial";
dtx.textAlign="center";
var player1 = {id: 1, token :String.fromCharCode(0xD83D, 0xDE87)};
var player2 = {id: 2, token:String.fromCharCode(0xD83D, 0xDC18)};
var players = [player1, player2];
var locations = [[1,11], [2,13]];
function getPlayer(playerID){
	for (i =0; i<players.length;i++){
		if (playerID-1 == i){
			return players[i]}
	}
}

function drawPiece(playerID, pos){
	var pieceSize = 10;
	var x = tiles[pos].left + (tiles[pos].width/2) - (pieceSize/2);
	
	var y = tiles[pos].top + (tiles[pos].height/2) - (pieceSize/2);
	var player = getPlayer(playerID);
	
	dtx.fillText(player.token, x +10,y -10);
	return tiles[pos].top + " " + tiles[pos].left + "\n" +x + " " + y}

function shuffleTiles(){
	var newTiles =[];
	for (j =0; j<tiles.length;j++){
		var pos = tiles[j].i;
		newTiles[pos] = tiles[j];
	}
	tiles = newTiles;
	}
	
function drawPieces(){
	dtx.clearRect(0,0,d.width,d.height);
	for (var i = 0; i<locations.length;i++){
	
		console.log(loc);
		var loc = locations[i];
		console.log(loc);
		drawPiece(loc[0], loc[1]);
	}

}

function updateLocation(playerID, position){
	locations[playerID-1] = [playerID, position];
}
function start(){
	shuffleTiles();
	drawPieces();
}
dtx.textAlign="center";
function drawRotatedText(r,x,y){
	var word1="The Brog";
	var word1Width=ctx.measureText(word1).width;
	var rotation
	switch(r){
		  		case 1:
		  			rotation = 0;
					break;
				case 0:
		  			rotation = 90;
					break;
				case 2:
		  			rotation = 180;
					break;
				case 3:
					rotation = 270;
				}
	dtx.save();
	dtx.translate(x,y);
	dtx.rotate(rotation*Math.PI/180); 
	
	dtx.fillText(word1,-word1Width/2,4);
	dtx.restore();
 
}
function test(){
shuffleTiles();
var x = tiles[6].left + (tiles[6].width/2);
var y = tiles[6].top + (tiles[6].height/1.5);
drawRotatedText(0,x,y);
}
