(function($){
	$(function(){
			// Game Variables
			var game_id;
			var last_activity;
			var turn;
			var figurines;
			var type;
			var status;
			var playersNo;
			// player variables
			// public
			var player_name;
			var player_GOOJF
			var player_number
			var player_position
			var player_properties;
			//private
			var playerID;
			var player_balance;


		$(document).ready(function(){

			hostGame();

		});

		function joinGame() {
			console.log("Join Game!")

		}

		function hostGame() {
			console.log("Host Game!");

			// game variables
			 console.log('game_variables');
			game_variables = init['game'];
			game_id = game_variables['gID']; console.log('GID:' + game_id);
			last_activity = game_variables['lastActivity']; console.log('last_activity:'+last_activity);
			turn = game_variables['turn']; console.log('turn:' + turn);
			figurines = game_variables['figurines']; console.log('figurines:'+figurines);
			type = game_variables['type']; console.log('type:'+type);
			status = game_variables['status']; console.log('status:'+status);
			playersNo = game_variables['playersNo']; console.log('playersNo:'+playersNo);
			// player variables
			console.log('player variables');
			playerOBJ = init['player'];
			//public
			player_name = playerOBJ['public']['name']; console.log('player_name:'+player_name);
			player_GOOJF = playerOBJ['public']['GOOJF']; console.log('player_GOOJF:'+player_GOOJF);
			player_number = playerOBJ['public']['number']; console.log('player_number:'+player_number);
			player_position = playerOBJ['public']['position']; console.log('player_position:'+player_position);
			player_properties = playerOBJ['public']['properties']; console.log('player_properties:'+player_position);
			// private
			playerID = playerOBJ['uID']; console.log('playerID:'+playerID);
			player_balance = playerOBJ['money']; console.log('player_balance:'+playerID);
			// dictionary of players (inclds this player data, we'll check for that later)



		}

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

  }); // end of document ready
})(jQuery); // end of jQuery name space