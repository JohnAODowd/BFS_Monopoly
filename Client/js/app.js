(function($){
	$(function(){

		// game state variables: "form", "lobby", "play"
		var game_state = "form";

		// HTML templates for various game states
		// 1st. Form for host game or join game, 2nd. choose avatar, 3rd. game screen
		var form_html = '<div class="form-container row hoverable z-depth-2">'+
				            '<form id="host-form" class="col s12">'+
				            '<h3 class="center-align">Create Game</h3>'+
				              '<div class="row">'+
				                '<div class="input-field col s6">'+
				                  '<input id="first_name" type="text" class="validate">'+
				                  '<label for="first_name">Game Name</label>'+
				                '</div>'+
				                '<div class="input-field col s6">'+
				                  '<input id="last_name" type="text" class="validate">'+
				                  '<label for="last_name">Username</label>'+
				                '</div>'+
				              '</div>'+
				              '<div class="row">'+
				                '<div class="input-field col s6">'+
				                  '<input id="password" type="password" class="validate">'+
				                  '<label for="password">Password</label>'+
				                '</div>'+
				                '<div class="input-field col s6">'+
                  					'<button class="btn waves-effect waves-light red" type="submit" name="action" id="create-submit">Create Game Lobby'+
                    					'<i class="material-icons right">send</i>'+
				                	'</button>'+
				                '</div>'+

				              '</div>'+
				              '<div class="divider white"></div>'+
				            '</form>'+
				        '<!-- JOIN GAME FORM -->'+

				            '<form id="join-form" class="col s12">'+
				              '<h3>Join Game</h3>'+
				              '<div class="row">'+
				                '<div class="input-field col s6">'+
				                  '<input id="random-username" type="text" class="validate">'+
				                  '<label for="random-username">Username</label>'+
				                '</div>'+
				                '<div class="input-field col s6">'+
				           '<input class="btn waves-effect waves-light" type="submit" name="action" id="random-submit" value="Submit">'+
				                '</div>'+
				            '</form>'+
				          '</div>';
		var lobby_html = '<div class="spinner row z-depth-2" data-spin>'+
							'</div>';
		// '<div class="spinner row z-depth-2>'+
		// 					'<h3>test</h3>'+
		// 				'</div>';
		var game_html = '<div class="canvas-container">' +
            			'<canvas id="game-board" width="520" height="520"></canvas>' +
          				'</div>';

		$(document).ready(function(){

			if (game_state === "form"){
				// Firstly load form html
				console.log("form");
				var board = $(".board");
				board.append(form_html);

				// set event listeners
				$('form').on('submit', function(e){
					e.preventDefault();
					hostGame();
				});
			}

		});

		function joinGame() {
			console.log("Join Game!")

		}

		function hostGame() {
			console.log("Host Game!");
			// change game state // will replace with cookie
			game_state = "lobby";
			// clear html from game page
			var board = $(".board");
			$(".form-container").remove();
			// append lobby html
			board.append(lobby_html);

			var opts = {
			  lines: 13 // The number of lines to draw
			, length: 28 // The length of each line
			, width: 14 // The line thickness
			, radius: 42 // The radius of the inner circle
			, scale: 1 // Scales overall size of the spinner
			, corners: 1 // Corner roundness (0..1)
			, color: '#000' // #rgb or #rrggbb or array of colors
			, opacity: 0.25 // Opacity of the lines
			, rotate: 0 // The rotation offset
			, direction: 1 // 1: clockwise, -1: counterclockwise
			, speed: 1.2 // Rounds per second
			, trail: 60 // Afterglow percentage
			, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
			, zIndex: 2e9 // The z-index (defaults to 2000000000)
			, className: 'spinner' // The CSS class to assign to the spinner
			, top: '50%' // Top position relative to parent
			, left: '50%' // Left position relative to parent
			, shadow: false // Whether to render a shadow
			, hwaccel: false // Whether to use hardware acceleration
			, position: 'absolute' // Element positioning
			}
			$('.spinner').spin();
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