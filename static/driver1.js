var numToChar = ["a", "b", "c", "d", "e", "f", "g", "h"];
var charToNum = {
  a: 0,
  b: 1,
  c: 2,
  d: 3,
  e: 4,
  f: 5,
  g: 6,
  h: 7
}

var displayBoard = function () {
  var column = [0, 1, 2, 3, 4, 5, 6, 7];
  console.log("  | " + column.join("   "));
  console.log("-----------------------------------");
  for (var i = 0; i < board.length; i++) {
    console.log(numToChar[i] + " |" + board[i].join(" "));
  }
};

$(document).on('boardChange', function() {
  displayBoard();
});

$(document).on('pieceTaken', function(e,currentPlayer,row,col) {
  alert("The " + currentPlayer + " player lost a piece at " + numToChar[row] + "" + col);

});

$(document).on('invalidMove', function(e, error_message) {
  alert(error_message);
});

$(document).on('updateRound', function(e, round) {
  console.log('The round is ' + round);
});

$(document).on('winnerNamed', function(e, winner) {
  alert(winner +' won');
  endGame();
});

// var play = function() {
//   resetBoard();
//   while (winner===null) {
//     getMove();
//   }
// };

//var getMove = function() {

  //var starting = prompt(currentPlayer + ", what piece would you like to move? Row, column (e.g., A2).").trim();
  //quit(starting);
  //var startingParsed = parseAnswer(starting);
  //var ending = prompt(currentPlayer + ", to what spot would you like to move? Row, column (e.g., A2).").trim();
 // quit(ending);
  //var endingParsed = parseAnswer(ending);
 // var move_object = {
    //startingRow: startingParsed[0],
   // startingCol: startingParsed[1],
    //endingRow: endingParsed[0],
    //endingCol: endingParsed[1]
 // }
  //return move_object;
//}

var getMoveAI = function() {
  if(currentPlayer === 'wht'){
    var starting = prompt("It's the AI's turn").trim();
    
    //trigger to views.py for variables 


    //end of trigger to views.py
    var startingParsed; 
    var endingParsed;
    //need to get the starting row and column & ending row and column 
    var move_object = { //translates the moves
      startingRow: startingParsed[0],
      startingCol: startingParsed[1],
      endingRow: endingParsed[0],
      endingCol: endingParsed[1]
    }
    return move_object; //returns so moves can be executed 

  }else{
    var starting = prompt(currentPlayer + ", what piece would you like to move? Row, column (e.g., A2).").trim();
    quit(starting); //see if player wants to quit
    var startingParsed = parseAnswer(starting); //gets the piece to move
    var ending = prompt(currentPlayer + ", to what spot would you like to move? Row, column (e.g., A2).").trim();
    quit(ending); //see if player wants to quit
    var endingParsed = parseAnswer(ending); //gets where the piece should go to 
    var move_object = { //translates the moves
      startingRow: startingParsed[0],
      startingCol: startingParsed[1],
      endingRow: endingParsed[0],
      endingCol: endingParsed[1]
    }
    return move_object; //returns so moves can be executed 
  }
}

var quit = function(string) {
  if (string[0] === 'q') {
      endGame();
    }
};

var endGame = function() {
  alert('Thanks for playing');
  play();
};

var parseAnswer = function(string) { //gets which square to move to 
  answer = []
  if (string.length===2) {
    answer.push(charToNum[string[0].toLowerCase()]); //goes to charToNum array
    answer.push(parseInt(string[1]));
  } else {
    alert("Invalid entry for start point");
    getMove();
  }
  return answer;
};

var play = function() {
  resetBoard();
  displayBoard();
  var move
  while (winner===null) {
    move = getMove();
    attemptMove(move.startingRow,move.startingCol,move.endingRow,move.endingCol);
  }
};