(function($){
	$(function(){
		// Game Variables
		var gameID;
		var game_turn;
		var figurines;
		var game_state;
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
			main();

		});

		/*	=========
			Join Game
			=========	*/	
		function joinGame() {
			console.log("Join Game!");
			// update JSON using returned variable 'init' which is embedded in html return
			parseJSON(init);
		} // end joinGame()

		/*	=========
			Host Game
			=========	*/	
		function hostGame() {
			console.log("Host Game!");
			// update JSON using returned variable 'init' which is embedded in html return
			parseJSON(init);

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
				//ensure that there is no error present in the return
				if (json_data.hasOwnProperty('game') && 
					json_data.hasOwnProperty('player') && 
					json_data.hasOwnProperty('players') && 
					json_data.hasOwnProperty('options')) {
					//ensure a 'game', 'player', 'players' and 'options' are set as keys in the json

					/* 	==========
						GAME VARS
						========== */
					game_variables = json_data['game'];
					gameID = game_variables['gID']; 			console.log('GID:' + gameID);
					game_turn = game_variables['turn']; 		console.log('turn:' + game_turn);
					figurines = game_variables['figurines']; 	console.log('figurines:'+ figurines);			
					game_state = game_variables['status']; 	console.log('status:'+ game_state);
					playersNo = game_variables['playersNo']; 	console.log('playersNo:'+ playersNo);
					/* 	==========
						PLAYER VARS
						========== */
					console.log('player variables');
					playerOBJ = json_data['player'];
					/* 	==========
						  PUBLIC
						========== */
					player_name = playerOBJ['public']['name']; 				console.log('player_name:'+player_name);
					player_GOOJF = playerOBJ['public']['GOOJF']; 			console.log('player_GOOJF:'+player_GOOJF);
					player_number = playerOBJ['public']['number']; 			console.log('player_number:'+player_number);
					player_position = playerOBJ['public']['position']; 		console.log('player_position:'+player_position);
					player_properties = playerOBJ['public']['properties']; 	console.log('player_properties:'+player_position);
					/* 	==========
						  PRIVATE
						========== */
					playerID = playerOBJ['uID']; console.log('playerID:'+playerID);
					player_balance = playerOBJ['money']; console.log('player_balance:'+playerID);
					/* 	==========
						PLAYERS
						========== */						
					// player_list contains the json mapping of player_names to their properties
					// player keys is used for processing elsewhere, contains all keys
					console.log('Player list');
					player_list = json_data['players'];
					player_keys = [];
					// populate player_keys
					$.each(player_list, function(key, value) {
						player_keys.push(key);
					});
					// log to console for confirmation
					for (var x=0; x < player_keys.length; x++){
						console.log(player_keys[x]);
						$.each(player_list[player_keys[x]], function(key, value){
							console.log(key + ':' + value);
						});
					} // End for
				}
				if (game_state == 'PLAYING') {
					// check if game is playing
					// in which case 'board' is required
					if (json_data.hasOwnProperty('board')) {
						// make sure 'board' is present

						// NEED TO IMPLEMENT

					}
				} // END PLAYING IF
				if (json_data.hasOwnProperty('alert')) {
					// IMPLEMENT
				}
				return 1;
			} // End error check for req
			console.log('Something went wrong');
			return 0;
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
			
			// *******
			// Uncomment for server
			// *******

			// $.ajax({
			// 	type: 'post',
	  //           url: ping_url,
	  //           data: json,
	  //           contentType: "application/json; charset=utf-8",
	  //           traditional: true,
	  //           success: function (data) {
   //              	parseJSON(data);
   //              	console.log(data);
   //              }
			// });
			parseJSON(init /*json*/);

		}
		/* 	=========	=========
			Draw players to screen
			=========	=========  */
			// 
			//	Embeds players in Header
			//
			function displayPlayers() {
				for (_player in player_list) {
					console.log("Player ----");
					console.log(_player);
					console.log(player_list[_player]['figurine']);
					var player_img = initFig[player_list[_player]['figurine']];
					$('.player-icons').append('<li><img src="'+ player_img +'" class="player-icon circle" id="'+_player+'"></li>');
					
					/* 	========= 	=========
						Add Event Listeners using _player 
						=========	========= */
				}
			}

		/*	=========	=========
			Display figurines to lobby
			=========	========= */
		function displayFigurines() {
			$('.board').empty();
			console.log(figurines);
			var x = 0;
			var row = 1;
			var figurines_html = 	'<div class="figurines">'+
									'</div>';
									
			$('.board').append(figurines_html);
			for (fig in figurines) {
				$('.figurines').append('<img src="' + initFig[figurines[fig]] + '" id="' + figurines[fig] + '" />');
			}

		}
		/*  ============
			Functions for figurines
			============ */

        function figurineRequest(data) {

          var json = JSON.stringify(data);
          var ping_url = "http://leela.netsoc.co:8080/game"

          // *** Uncomment when pushing to server
          // $.ajax({
          //     type: 'post',
          //     url: ping_url,
          //     data: json,
          //     contentType: "application/json; charset=utf-8",
          //     traditional: true,
          //     success: function (data) {
          //         console.log(data);
          //       }
          //   });
        }
        function wait(ms){
		   var start = new Date().getTime();
		   var end = start;
		   while(end < start + ms) {
		     end = new Date().getTime();
		  }
		}
		/*	============	============	============
			Core logic will go in a loop in the main() func
			============	============	============	*/
		function main() {
			ping();
			// console.log('PING 1');
			// wait(3000);
			// //var ping_interval = setInterval(ping, 4000);
			displayFigurines();
			// //var display_fig_interval = setInterval(displayFigurines, 4001);
			// wait(3000);

			displayPlayers();

			$('#HAT').click(function()
			{
				//delete figurines["HAT"];
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "HAT";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log('HAT');
			});
	        $('#CAR').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "CAR";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("CAR");
	          //sendRequest(data);
	        });
	        $('#THIMBLE').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "THIMBLE";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("THIMBLE");
	          //sendRequest(data);
	        });
	        $('#IRON').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "IRON";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("IRON");
	          //sendRequest(data);
	        });
	        $('#BOOT').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "BOOT";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("BOOT");
	          //sendRequest(data);
	        });
	        $('#SHIP').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "SHIP";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("SHIP");
	          //sendRequest(data);
	        });
	        $('#DOG').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "DOG";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("DOG");
	          //sendRequest(data);
	        });
	        $('#WHEELBARROW').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "WHEELBARROW";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("WHEELBARROW");
	          //sendRequest(data);
	        });

		}

  	}); // end of document ready
})(jQuery); // end of jQuery name space