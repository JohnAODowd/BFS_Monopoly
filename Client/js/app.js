(function($){
	$(function(){
		// Game Variables
		var gameID;
		var game_turn;
		var figurines;
		var game_status;
		var playersNo;
		// player variables
		// public
		var player_name;
		var player_GOOJF;
		var player_number;
		var player_position;
		var player_properties; // ID's > properties.json
		// private
		var playerID;
		var player_balance;
		// player list object
		var player_list;
		var player_keys;

		$(document).ready(function(){
			/*	=========
				Core Logic
				=========	*/

			hostGame();
			//joinGame();
			if (gameID){
				// check a game has actually been found
				if (game_type === 'LOBBY'){

				}
			}

		});

		/*	=========
			Join Game
			=========	*/	
		function joinGame() {
			console.log("Join Game!");
			// update JSON using returned variable 'init' which is embedded in html return
			updateJSON(init);
		} // end joinGame()

		/*	=========
			Host Game
			=========	*/	
		function hostGame() {
			console.log("Host Game!");
			// update JSON using returned variable 'init' which is embedded in html return
			updateJSON(init);

		} // end hostGame()

		/*	=========
			Init Game State
			=========	*/	
		function initGame(){
			console.log("Game Started!")
			//
			var canvas = document.getElementById("game-board")
			var ctx = canvas.getContext("2d");

			canvas.width = 520;
			canvas.height = 520;

			// draw loading screen to game
			ctx.fillRect(0,0,520,520);
			var img = new Image();
			img.onload = function () {
			    ctx.drawImage(img, 0, 0, 520, 520);
			}
			img.src = "assets/game_assets/lobby/monopoly-test-background.png";
		}
		/*	========= =========
				  HELPERS
			========= =========	*/	
		function parseJSON(json_data) {
			// game variables
			console.log('game_variables');
			// FIRST CHECK FOR 'error'
			// game : player : players : options - req all states
			// board - req when game in playing state
			// alert - !req 
			if (!json_data.hasOwnProperty('error')) {
				if (json_data.hasOwnProperty('game') && 
					json_data.hasOwnProperty('player') && 
					json_data.hasOwnProperty('players') && 
					json_data.hasOwnProperty('options')) {
						// all required fields exist
						game_variables = json_data['game'];
						gameID = game_variables['gID']; 			console.log('GID:' + gameID);
						game_turn = game_variables['turn']; 		console.log('turn:' + game_turn);
						figurines = game_variables['figurines']; 	console.log('figurines:'+figurines);			
						game_status = game_variables['status']; 	console.log('status:'+game_status);
						playersNo = game_variables['playersNo']; 	console.log('playersNo:'+playersNo);
						// player variables
						console.log('player variables');
						playerOBJ = json_data['player'];
						//public
						player_name = playerOBJ['public']['name']; 				console.log('player_name:'+player_name);
						player_GOOJF = playerOBJ['public']['GOOJF']; 			console.log('player_GOOJF:'+player_GOOJF);
						player_number = playerOBJ['public']['number']; 			console.log('player_number:'+player_number);
						player_position = playerOBJ['public']['position']; 		console.log('player_position:'+player_position);
						player_properties = playerOBJ['public']['properties']; 	console.log('player_properties:'+player_position);
						// private
						playerID = playerOBJ['uID']; console.log('playerID:'+playerID);
						player_balance = playerOBJ['money']; console.log('player_balance:'+playerID);
						// dictionary of players (inclds this player data, we'll check for that later)

						// player list 
						console.log('Player list');
						player_list = json_data['players'];
						player_keys = [];
						$.each(player_list, function(key, value) {
							player_keys.push(key);
						});
						for (var x=0; x < player_keys.length; x++){
							console.log(player_keys[x]);
							$.each(player_list[player_keys[x]], function(key, value){
								console.log(key + ':' + value);
							});
						} // End for
			} // End error check for req
			console.log('Something went wrong');
		}

		/*	========= =========
				  HELPERS
			========= =========	*/		
		/*	=========
			PING RQST
			Updates game and player state throughout game
			=========	*/
		function ping() {
			var data = {};
			data['request'] = 'PING';
			data['uID'] = playerID;
			data['gID'] = gameID;

			var json = JSON.stringify(data);
			var ping_url = "http://leela.netsoc.co:8080/game";
			$.getJSON(url, json, function(result){
				json = result;
			});
			parseJSON(json);

		}

		/*	=========
			Display figurines to lobby
			=========	*/	
		function displayFigurines(json) {
			console.log('displayFigurines');
			$.each(json, function(key){
				console.log(key);
			});
		}

		/*	============	============	============
			Core logic will go in a loop in the main() func
			============	============	============	*/
		function main() {

			setInterval(ping, 300);
			displayFigurines(figurines);

		}

  	}); // end of document ready
})(jQuery); // end of jQuery name space