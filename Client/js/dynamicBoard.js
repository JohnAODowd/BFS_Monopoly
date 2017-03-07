	var d = document.getElementById("dynamicCanvas");
		var dtx = d.getContext("2d");

dtx.font = "20px Arial";
dtx.textAlign="center";
var player1 = {id: 1, token :String.fromCharCode(0xD83D, 0xDDFF)};
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
