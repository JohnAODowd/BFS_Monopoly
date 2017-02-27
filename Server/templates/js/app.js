(function($){
	$(function(){

		// game state variables: "form", "lobby", "play"
		var game_state = "form";


		$(document).ready(function(){
			loadGame();
			//initGame();

		});

		function joinGame() {
			console.log("Join Game!")

		}

		function hostGame() {
			console.log("Host Game!");
			// change game state // will replace with cookie or similar
			game_state = "lobby";
			// clear html from game page
			var board = $(".board");

			// send ajax request for JSON file
			// some of this data will be permanent
			console.log(init);
		}

		function initGame(){
			console.log("Game Started!")
			
			var board = $('.board');
			board.append('<canvas id="canvas"></canvas>');
			var canvas = document.getElementById("canvas")
			var ctx = canvas.getContext("2d");

			canvas.width = 140;
			canvas.height = 180;

			ctx.beginPath();
			ctx.rect(20, 20, 140, 180);
			ctx.fillStyle = "white";
			ctx.fill();

			// // draw loading screen to game
			// ctx.fillRect(0,0,530,530);
			// var img = new Image();
			// img.onload = function () {
			//     ctx.drawImage(img, 0, 0, 530, 530);
			// }
			// img.src = "assets/game_assets/lobby/monopoly-test-background.png";

			

			

		}

  }); // end of document ready
})(jQuery); // end of jQuery name space