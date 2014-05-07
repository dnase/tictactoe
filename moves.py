import random
from itertools import permutations

WINNING_COMBINATIONS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8)]

#helper functions
def _available_moves(game_state):
    #return a list of available moves on the board.
    return [i for i, j in enumerate(game_state) if j != 'X' and j != 'O']

def _computer_moves(game_state):
    #return a list of previous computer (O) moves.
    return [i for i, j in enumerate(game_state) if j == 'O']

def _human_moves(game_state):
    #return a list of previous human (X) moves.
    return [i for i, j in enumerate(game_state) if j == 'X']

def _opponent(player):
    #return the opponent of "player"
    return 'X' if player == 'O' else 'O'

def _minimax(game_state, player, alpha, beta):
    '''
    _minimax - implements Minimax with alpha-beta
    pruning.
    This algorithm is described here: http://en.wikipedia.org/wiki/Alpha-beta_pruning
    '''
    has_won = winning_state(game_state)
    if has_won:
        if has_won == 1:
            return -1
        elif has_won == 2:
            return 1
        elif has_won == 3:
            return 0
    for move in _available_moves(game_state):
        game_state[move] = player
        v = _minimax(game_state, _opponent(player), alpha, beta)
        game_state[move] = False
        if player == 'O':
            if v > alpha:
                alpha = v
            if alpha >= beta:
                return beta
        else:
            if v < beta:
                beta = v
            if beta <= alpha:
                return alpha
    if player == 'O':
        return alpha
    else:
        return beta

def best_move(game_state):
    '''
    best_move attempts to find the best move
    for the computer to take next.
    Returns an integer from 0-8 representing
    a game square.
    '''
    a = -2
    choices = []
    if  4 in _available_moves(game_state):
        return 4
    for move in _available_moves(game_state):
        game_state[move] = 'O'
        v = _minimax(game_state, 'X', -2, 2)
        game_state[move] = False
        if v > a:
            a = v
            choices = [move]
        elif v == a:
            choices.append(move)
    return random.choice(choices)

def winning_state(game_state):
    '''
    winning_state - given game_state list,
    checks if the game board has a win or tie.
    Returns:
        1 for human (X) win
        2 for computer (O) win
        3 for tie
        False if game is not over
    '''
    #use permutations to check if there exists a winning combination on the board.
    for combo in WINNING_COMBINATIONS:
        if combo in list(permutations(_human_moves(game_state), 3)):
            return 1
        elif combo in list(permutations(_computer_moves(game_state), 3)):
            return 2
    #if there are no available moves left, the game is over.
    if len(_available_moves(game_state)) == 0:
        return 3
    else:
       return False