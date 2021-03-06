// functions for interaction between checkers.js and DOM

var displayBoard = function(board) {
	for (var row = 0; row < board.length; row++) {
		for (var col = 0; col < board[row].length; col++) {
			if (board[row][col] === 'wht') {
				$($('.row')[row].children[col]).html('<span class="wht piece"></span>');
			} else if (board[row][col] === 'red') {
				$($('.row')[row].children[col]).html('<span class="red piece"></span>');
			} else {
				$($('.row')[row].children[col]).empty();
			}
		}
	}
};

var numToChar = ["a", "b", "c", "d", "e", "f", "g", "h"];

var moveObject = {};

var getMove = function(chosen) {
	var row = $('.row').index(chosen.parent());
	var col = chosen.parent().children().index(chosen);
	if ( Object.keys(moveObject).length == 0 ) {
		moveObject.startingRow = row;
		moveObject.startingCol = col;
	} else if ( Object.keys(moveObject).length == 2 ) {
		moveObject.endingRow = row;
		moveObject.endingCol = col;
		attemptMove(moveObject.startingRow,moveObject.startingCol,moveObject.endingRow,moveObject.endingCol);
		moveObject = {};
	}
};

//DOM interaction event handlers starts here
//Wait till document ready to hook clicks to DOM objects

$(document).on('ready', function(){
  
	$('.start').on('click', function(){
	  resetBoard();
	  displayBoard(board);
	  $('.round').text("Round:" + round);
	  $('.playerUp').text("Please move " + currentPlayer + " player");
	});

	$('.col').on('click', function (e) {
		$('.playerUp').text("Please move " + currentPlayer + " player");
		var helper = $(this);
		getMove(helper);
	});

	$(document).on('boardChange', function() {
	  displayBoard(board);
	});

	$(document).on('pieceTaken', function(e,currentPlayer,row,col) {
	  $('.takenTaunt').text("The " + currentPlayer + " player lost a piece at " + numToChar[row] + "" + col);
	});

	$(document).on('invalidMove', function(e, error_message) {
		console.log(error_message);
	  $('.playerUp').text("Invalid move: " + error_message);
	});

	$(document).on('updateRound', function(e, round) {
	  $('.round').text("Round:" + round);
	  $('.playerUp').text("Please move " + currentPlayer + " player");
	});

	$(document).on('winnerNamed', function(e, winner) {
	  $('.takenTaunt').text("Game over! The " + winner + "player won");
	  setTimeout( function() {
		  $('.round').empty();
			$('.playerUp').empty();
			$('.takenTaunt').empty();
		}, 5000);
	});

});
