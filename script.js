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
            drawBoard(key);
        }
    });
}

/*
* updateGameState - sends an updated gameState array
* to the server, which then updates its internal
* representation of the game board and returns
* an integer representing whether or not the game
* is over, and who won. The board is then redrawn.
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
        //if response is 0, game is still in play
        if(response == 0) {
            drawBoard(key);
        } else {
        //otherwise, it is in an ending state
            //nullify onClick function wrapper
            squareClicked = function () {};
            a = document.getElementById("announce");
            if(response == 1) {
                a.innerHTML = "Human player wins! Refresh page to play again.";
            } else if(response == 2) {
                a.innerHTML = "Computer player wins! Refresh page to play again.";
            } else if(response == 3) { 
                a.innerHTML = "The game is a tie! Refresh page to play again.";
            }
            drawBoard(key);
        }
    });
}

//wrapper to pass the square that was clicked
function squareClicked(squareNumber, key) {
    getGameState(squareNumber, key);
}

/*
* drawBoard - draws the game board based on the
* game state retrieved from the server.
*/
function drawBoard(key) {
    req = $.ajax({
        url: "/getgamestate",
        type: "post",
        data: "key=" + key
    });
    req.done(function (response, textStatus, jqXHR) {
        gameState = JSON.parse(response);
        //iterate through each square
        for(var i = 0; i < 9; i++) {
            c = document.getElementById("square" + i);
            ctx = c.getContext('2d');
            ctx.clearRect(0, 0, c.width, c.height);
            ctx.lineWidth = 5;
            //draw an X on each square the human has selected
            if(gameState[i] == 'X') {
                ctx.beginPath();
                ctx.moveTo(0,0);
                ctx.lineTo(c.width, c.height);
                ctx.moveTo(c.width, 0);
                ctx.lineTo(0, c.height);
                ctx.stroke();
                ctx.closePath();
            //draw an O on each square the computer has selected
            } else if(gameState[i] == 'O') {
                ctx.beginPath();
                ctx.arc(c.width / 2, c.height / 2, c.width / 4, 0, Math.PI * 2, true);
                ctx.stroke();
                ctx.closePath();
            }
        } 
    });
}