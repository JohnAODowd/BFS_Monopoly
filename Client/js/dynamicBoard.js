var d;
		var dtx;


var player1 = {id: 1, token :String.fromCharCode(0xD83D, 0xDE87)};
var player2 = {id: 2, token:String.fromCharCode(0xD83D, 0xDC18)};
var players = [player1, player2];
//<<<<<<< HEAD
var locations = [[1,11], [2,13]];
var tiles;
//=======
var locations = [[1,0],[2,0]];
//>>>>>>> 22e13484cbb4dab74323780159ae4e0439a879a0
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
	//dtx.rotate(Math.PI*2/(i*6));
	
	console.log(x + "  " + y);
	return tiles[pos].top + " " + tiles[pos].left + "\n" +x + " " + y}


function drawPieces(){
	dtx.clearRect(0,0,d.width,d.height);
	for (var i = 0; i<locations.length;i++){
	
		
		var loc = locations[i];
		console.log("aaa");
		drawPiece(loc[0], loc[1]);
	}

}

function shuffleTiles(){
	var newTiles =[];
	for (j =0; j<tiles.length;j++){
		var pos = tiles[j].i;
		newTiles[pos] = tiles[j];
	}
	tiles = newTiles;
	}

function move(player, location){
	updateLocation(player, location);
	drawPieces();
}

	
function updateLocation(playerID, position){
	locations[playerID-1] = [playerID, position];
}
function start(){
	d = document.getElementById("dynamicCanvas");
	dtx = d.getContext("2d");
	dtx.font = "10px Arial";
dtx.textAlign="center";
	shuffleTiles();
	drawPieces();
}


function test(){
shuffleTiles();
var x = tiles[6].left + (tiles[6].width/2);
var y = tiles[6].top + (tiles[6].height/1.5);
drawRotatedText(0,x,y);
}