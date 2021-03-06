var board, currentPlayer, otherPlayer, enemyPieceJumped, winner, error_message, round, dead;

var resetBoard = function () {
  board = [
    [' X ', 'wht', ' X ', 'wht', ' X ', 'wht', ' X ', 'wht'],
    ['wht', ' X ', 'wht', ' X ', 'wht', ' X ', 'wht', ' X '],
    [' X ', 'wht', ' X ', 'wht', ' X ', 'wht', ' X ', 'wht'],
    [' X ', ' X ', ' X ', ' X ', ' X ', ' X ', ' X ', ' X '],
    [' X ', ' X ', ' X ', ' X ', ' X ', ' X ', ' X ', ' X '],
    ['red', ' X ', 'red', ' X ', 'red', ' X ', 'red', ' X '],
    [' X ', 'red', ' X ', 'red', ' X ', 'red', ' X ', 'red'],
    ['red', ' X ', 'red', ' X ', 'red', ' X ', 'red', ' X ']
  ];

  currentPlayer = 'wht';
  otherPlayer = 'red';
  enemyPieceJumped = [];
  dead = { 
    white: 0,
    red: 0 
  };
  winner = null;
  error_message = null;
  round = "0\u21D1";
};

var attemptMove = function (row1, col1, row2, col2) {
  if ((checkOrigin(row1,col1))
    && (checkDestination(row2,col2))
    && (checkDirection(row1, row2))
    && (checkDistance(row1, col1, row2, col2))) 
  {
    makeMove(row1, col1, row2, col2);
    while ( enemyPieceJumped.length > 0 ) {
      colRemover = enemyPieceJumped.pop()
      rowRemover = enemyPieceJumped.pop()
      removePiece(rowRemover,colRemover);
    }
    round = updateRound(round);
  }
  $(document).trigger('updateRound', round);
  $(document).trigger('boardChange');
};

var checkOrigin = function(row1,col1) {
  if (board[row1][col1] !== currentPlayer) {
    error_message = 'Pick a spot to start where you do have a piece';
    $(document).trigger('invalidMove', 'Pick a spot to start where you do have a piece');
    return false;
  } else {
    return true;
  }
};

var checkDestination = function(row2,col2) {
  if (board[row2][col2] !== ' X ') {
    error_message = 'Pick a spot to end that is empty';
    $(document).trigger('invalidMove', error_message);
    return false;
  } else {
    return true;
  } 
};

var checkDirection = function(row1,row2) {
  if (( currentPlayer === 'red' ) 
    && ( row2 > row1 ))
  {
    error_message = 'Go the other direction';
    $(document).trigger('invalidMove', error_message);
    return false;
  }
  else if (( currentPlayer === 'wht' ) 
    && ( row2 < row1 )) 
  {
    error_message = 'Go the other direction';
    $(document).trigger('invalidMove', error_message);
    return false;
  }
  else {
    return true;
  }
};

var checkDistance = function(row1, col1, row2, col2) {
  rowjump = Math.abs(row1-row2);
  coljump = Math.abs(col1-col2);
  if ((rowjump===1) && (coljump===1)) {
    return true;
  } else if ((rowjump===2) 
    && (coljump===2)
    && (enemyJumped(row1, col1, row2, col2).length > 0 )) {
    return true;
  // } else if ((doubleJump(row1,col1,row2,col2))
  //   && (rowjump===4)
  //   && ((coljump===0) || (coljump===4))) {
  //   return true;
  } else {
    error_message = 'You tried to move too many spaces';
    return false;
  }
};

// var doubleJump = function(row1,col1,row2,col2) {
//   rowjump = Math.abs(row1-row2);
//   coljump = Math.abs(col1-col2);
//   if (coljump == 0) {
//     $(document).trigger('leftOrRight');
//     var holder = leftOrRight();
//     attemptMove(row1,col1, holder[0],holder[1]);
//     attemptMove(holder[0],holder[1],row2,col2);
//     holder = [];
//   } else if (coljump == 4) {
//     attemptMove(row1,col1,(row1+2),(col1+2));
//     attemptMove((row1+2),(col1+2),row2,col2);
//   }
// };

var enemyJumped = function(row1, col1, row2, col2) {
  middleRow = row2 + ((row1-row2)/2);
  middleCol = col2 + ((col1-col2)/2);
  if (board[middleRow][middleCol] === otherPlayer) {
    enemyPieceJumped.push(middleRow);
    enemyPieceJumped.push(middleCol);
  }
  return enemyPieceJumped;
};

var makeMove = function (row1, col1, row2, col2) {
  board[row1][col1] = ' X ';
  board[row2][col2] = currentPlayer;
  swap(currentPlayer,otherPlayer);
};

var swap = function() {
  var temp = currentPlayer;
  currentPlayer = otherPlayer;
  otherPlayer = temp;
};

var removePiece = function (row, col) {
  board[row][col] = ' X ';
  if (currentPlayer === 'red') {
    dead.red++;
  } else if (currentPlayer === 'wht') {
    dead.white++;
  }
  $(document).trigger('pieceTaken', [currentPlayer, row, col]);
  if ((dead.red === 12) || (dead.white === 12)) {
    winner = otherPlayer;
    $(document).trigger('winnerNamed', winner);
  }
};

var updateRound = function(rounded) {
  if (rounded[1]==='\u21D1') {
    rounded = rounded[0] + '\u21D3'
  } else {
    var holder = parseInt(rounded[0]) + 1;
    rounded = holder + '\u21D1';
  }
  return rounded;
};