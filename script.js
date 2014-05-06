/*
* getGameState - checks the state of the game to 
* see if the player initiated a legal move.
* If so, it calls updateGameState.
*/
function getGameState(squareNumber, key) {
    //ajax request for gamestate from server
    req = $.ajax({
        url: "/getgamestate",
        type: "post",
        data: "key=" + key
    });
    req.done(function (response, textStatus, jqXHR) {
        gameState = JSON.parse(response);
        //if the space is unoccupied
        if(gameState[squareNumber] == false) {
            //it is a valid move
            gameState[squareNumber] = 'X';
            updateGameState(gameState, key);
        } else {
            //it is an invalid move. Do nothing.
            drawBoard(gameState);
        }
    });
}

/*
* updateGameState - sends an updated gameState array
* to the server, which then updates its internal
* representation of the game board and returns
* the gameState array with its next move. The board
* is then redrawn by drawBoard.
*/
function updateGameState(gameState, key) {
    //ajax request to update gamestate - check for legality serverside
    //afterwards, return the server's move and draw the board
    jsonGameState = JSON.stringify(gameState);
    req = $.ajax({
        url: "/updategamestate",
        type: "post",
        data: "key=" + key + "&game_state=" + jsonGameState
    });
    req.done(function (response, textStatus, jqXHR) {
        newGameState = JSON.parse(response);
        drawBoard(gameState);
    });
}

//wrapper to pass the square that was clicked
function squareClicked(squareNumber, key) {
    //ajax request to mark square with an "X"
    getGameState(squareNumber, key);
}

/*
* drawBoard - draws the game board based on the
* gameState array.
*/
function drawBoard(gameState) {
    for(var i = 0; i < 9; i++) {
        if(gameState[i] == 'X') {
            c = document.getElementById("square" + i);
            cxt = c.getContext('2d');
            cxt.lineWidth = 5;
            cxt.beginPath();
            cxt.moveTo(0,0);
            cxt.lineTo(c.width, c.height);
            cxt.moveTo(c.width, 0);
            cxt.lineTo(0, c.height);
            cxt.stroke();
            cxt.closePath();
        } else if(gameState[i] == 'O') {
            c = document.getElementById("square" + i);
            cxt = c.getContext('2d');
            cxt.lineWidth = 5;
            cxt.beginPath();
            cxt.arc(c.width / 2, c.height / 2, c.width / 4, 0, Math.PI * 2, true);
            cxt.stroke();
            cxt.closePath();
        }
    }
}

function playAgain() {
    //simple page refresh
    location.reload(true);
}