(function($){
	$(function(){
		var ping_url = "";
		// Game Variables
		var gameID;
		var game_turn;
		var figurines;
		var game_state;
		var playersNo;
		//options
		var options;
		// player variables
		// public
		var player_name;
		var player_GOOJF;
		var player_number;
		var player_position;
		var player_properties; // ID's > properties.json
		var player_figurine;
		// private
		var playerID;
		var player_balance;
		// player list object
		var player_list;
		var player_keys;

		var first_pass = true;

		$(document).ready(function(){
			initGame();
			main();

		});

		/*	=========	=========
			Init Game State
			=========	=========  */	

		//	Read in initial data from HTML and parse it
		//	Update player icons and meta data
		//
		function initGame(){
			console.log("Game Started!")
		
			// Grab data from HTML
			parseJSON(init);
		}

		/*	========= =========
				  HELPERS
			========= =========	*/	
		function parseJSON(json_data) {
			// game variables
			console.log('');
			console.log('- - - - - - - - - - - - - - - - ');
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
					playersNo = game_variables['playersNo']; 	console.log('playersNo:'+ playersNo);
					// OPTIONS 
					options = json_data['player']['options'];	console.log('Options:'+ options);

					console.log("\n");
					console.log("Checking for game state change...");
					if (game_variables['state'] != game_state) {
						// GAMES STATE HAS CHANGED
						console.log("CHANGED GAME STATE");
						// THIS WILL BE USED FOR END OF GAME WINNER/PAUSE ETC

						if (game_variables['state'] === 'PLAYING') {
							// check if has changed to playing
							console.log("DRAWING BOARD");
							$('.board').empty();


							var canvas_html = '<div id="blaze">'+
												'</div>'+
												'<canvas id="boardCanvas" width="520" height="520">'+
												'</canvas>'+
												'<canvas id="dynamicCanvas" width="520" height="520"'+
												'</canvas>';
							$('.board').append(canvas_html);
							setTimeout(draw, 1400);
							setTimeout(start, 1400);
							//sleep(1400);
							//draw();
							//tart();
						}
			
					}
					// now that we've checked for game changes we can do more general code
					game_state = game_variables['state'];

					/* 	-------	-------
						Check if button should be enabled or disabled
						-------	-------	*/
						// this does not count as secure so check again later during request gen
					if (options.length > 0) {
						$.each(options, function(opt){
							if (options[opt] === "START" || options[opt] === "ROLL") {
								console.log('START ENABLED');
								$('#action-button').removeClass('disabled');
							} 
						})//foreach
					} else {
						$('#action-button').addClass('disabled');
						console.log('START DISABLED');
					}

					console.log('Player list');
					player_list = json_data['players'];

					if (game_state === 'PLAYING' && first_pass != true){

						// GAME IS BEING PLAYED - RENDER GAME + OPTIONS
						// Set control buttons
						// The game's state has not changed so we should not redraw canvas etc to board
						console.log('playing: ' + game_state);
						// cycle through each player and render them to the board
						$.each(player_list, function(plyr){
							var pnum = player_list[plyr]['number'];
							// var psquare = player_list[plyr]['position'];
							move(pnum,player_position);
						});

					}
					// PRINT LOBBY SCREEN FIRST - OVERWRITTEN WHEN NEEDED
					
					
					if (game_state === 'LOBBY'){
						console.log('GAME STATE: ' + game_state);
						
						// GAME IS IN LOBBY - RENDER BOARD OR OPTIONS
						//disable control buttons
						if (options.length > 0) {
							// if there are options
							console.log('Options are present:' + options);
							$.each(options, function(opt){
								if (options[opt] === "FIGURINE") {
									displayFigurines();		// tere should only ever be this option or none in LOBBY
								}
							})//foreach
						} // END IF LOBBY
	//
						
					}

						// paused

						// over / winner

					
					/* 	==========
						PLAYER VARS
						========== */
					console.log('\n');
					console.log('Player Variables');
					playerOBJ = json_data['player'];
					/* 	==========
						  PUBLIC
						========== */
					player_name = playerOBJ['public']['name']; 				console.log('player_name:'+player_name);
					$('#player-name').html(player_name);
					player_GOOJF = playerOBJ['public']['GOOJF']; 			console.log('player_GOOJF:'+player_GOOJF);
					player_number = playerOBJ['public']['number']; 			console.log('player_number:'+player_number);
					player_position = playerOBJ['public']['position']; 		console.log('player_position:'+player_position);
					player_properties = playerOBJ['public']['properties']; 	console.log('player_properties:'+player_position);
					player_figurine = playerOBJ['public']['figurine'];		console.log('player_figurine:'+player_figurine);
					// display player figurine to screen
					if (player_figurine != null) {
						console.log('Setting player_figurine:'+player_figurine);
						$("#player-image").attr("src", initFig[player_figurine]);
					} else {
						// replace server uncomment
						$("#player-image").attr("src", "assets/game_assets/lobby/Avatars/unknown.png");
					}
					/* 	==========
						  PRIVATE
						========== */
					playerID = playerOBJ['uID']; console.log('playerID:'+playerID);
					player_balance = playerOBJ['money']; console.log('player_balance:'+playerID);
					$('#player-balance').html('&#36;'+player_balance);

				}

				// Check if can buy
				if (playerOBJ['canBuy'] != null) {
					console.log('PLAYER CAN BUY');
					$('.options').removeClass('disabled');
					$('#buy').click(function(){
						buyProperty();
					})
				 } else {
				 	$('.options').addClass('disabled');
				 }
				

				if (json_data.hasOwnProperty('alert')) {
					// IMPLEMENT
				}

				// FUNCTIONS FOR AFTER PARSE
				displayPlayers();
				first_pass = false;
				return 1;
			} // End error check for req
			console.log('Something went wrong');
			return 0;
		}

		/*	========= =========
				  HELPERS
			========= =========	*/		
		/*	=========
			BUY PROPERTY RQST
			Send JSON BUY request to server
			=========	*/
		function buyProperty() {
			var data = {};
			data['request'] = 'BUY';
			data['pID'] = playerOBJ['canBuy'];
			data['uID'] = playerID;
			data['gID'] = gameID;

			var json = JSON.stringify(data);
			
			// *******
			// Uncomment for server
			// *******

			$.ajax({
				type: 'post',
	            url: ping_url,
	            data: json,
	            contentType: "application/json; charset=utf-8",
	            traditional: true,
	            success: function (data) {
                	parseJSON(data);
                	console.log(data);
                }
			});
			parseJSON(json);
		}
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
			
			// *******
			// Uncomment for server
			// *******

			$.ajax({
				type: 'post',
	            url: ping_url,
	            data: json,
	            contentType: "application/json; charset=utf-8",
	            traditional: true,
	            success: function (data) {
                	parseJSON(data);
                	console.log(data);
                }
			});
			parseJSON(json);

		}
		/* 	=========	=========
			Draw players to screen
			=========	=========  */
			// 
			//	Embeds players in Header
			//
		function displayPlayers() {
			$('.player-icons').empty();
			for (_player in player_list) {
				if (_player != player_name) {
					console.log("Player ----");
					console.log(_player);
					console.log(player_list[_player]['figurine']);
					var player_img = initFig[player_list[_player]['figurine']];
					$('.player-icons').append('<li><img src="'+ player_img +'" class="player-icon circle valign" id="'+_player+'"></li>');
					
				/* 	========= 	=========
					Add Event Listeners using _player 
					=========	========= */
				}
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
			var figurines_html = 	'<div class="figurines z-depth-2">'+
									'	<h2>Choose a firuine below:</h2>'+
									'</div>';
									
			$('.board').append(figurines_html);
			for (fig in figurines) {
				$('.figurines').append('<img src="' + initFig[figurines[fig]] + '" id="' + figurines[fig] + '" class="hoverable"/>');
			}

		}
		/*  ============
			Functions for figurines
			============ */

        function figurineRequest(data) {

          var json = JSON.stringify(data);
          

          // *** Uncomment when pushing to server
          $.ajax({
              type: 'post',
              url: ping_url,
              data: json,
              contentType: "application/json; charset=utf-8",
              traditional: true,
              success: function (data) {
                  console.log(data);
                }
            });
        }
		/*  ============
			Functions for Start Button and Roll
			============ */
		// Function to be used for either rolling or starting game from lobby
		function sendMainAction() {
			var data = {};
			data['gID'] = gameID;
			data['uID'] = playerID;
			// to implement
			$.each(options, function(opt){
				if (options[opt] === 'START') {
					console.log('START GAME REQUEST');
					data['request'] = 'START';
				} else if (options[opt] === "ROLL") {
					console.log('ROLL DICE REQUEST');
					data['request'] = 'ROLL';
				} else {
					console.log('ERROR SENDING REQUEST TO SERVER - NO PERMISSION FOUND');
					return 0;
				}
				var json = JSON.stringify(data);
				$.ajax({
		          type: 'post',
		          url: ping_url,
		          data: json,
		          contentType: "application/json; charset=utf-8",
		          traditional: true,
		          success: function (data) {
		              console.log(data);
		            }
		        });

			});

		}
		function sleep(milliseconds) {

}

		/*	============	============	============
			Core logic will go in a loop in the main() func
			============	============	============	*/
		function main() {
			//ping();
			// console.log('PING 1');
			// wait(3000);
			// //var ping_interval = setInterval(ping, 4000);
			// wait(3000);

			$('#action-button').click(function(){
				sendMainAction();
			});

			$('#HAT').click(function()
			{
				//delete figurines["HAT"];
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "HAT";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log('HAT');
	          sendRequest(data);
			});
	        $('#CAR').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "CAR";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("CAR");
	          sendRequest(data);
	        });
	        $('#THIMBLE').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "THIMBLE";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("THIMBLE");
	          sendRequest(data);
	        });
	        $('#IRON').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "IRON";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("IRON");
	          sendRequest(data);
	        });
	        $('#BOOT').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "BOOT";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("BOOT");
	          sendRequest(data);
	        });
	        $('#SHIP').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "SHIP";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("SHIP");
	          sendRequest(data);
	        });
	        $('#DOG').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "DOG";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("DOG");
	          sendRequest(data);
	        });
	        $('#WHEELBARROW').click(function() {
	          var data = {};
	          data['request'] = 'FIGURINE';
	          data["figurine"] = "WHEELBARROW";
	          data['gID'] = gameID;
	          data['uID'] = playerID;
	          console.log("WHEELBARROW");
	          sendRequest(data);
	        });

		}

  	}); // end of document ready
})(jQuery); // end of jQuery name space