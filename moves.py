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

def _next_move(previous, available):
	#given a list of previous moves and available moves, return the first winning move if any exist
	for avail in available:
        #if we don't use list(), python will just make p_buf point to the memory address of previous
		p_buf = list(previous)
		p_buf.append(avail)
		for combo in WINNING_COMBINATIONS:
			if combo in list(permutations(p_buf, 3)):
				return avail
	return None

def best_move(game_state):
    '''
    best_move attempts to find the best move
    for the computer to take next.
    Returns an integer from 0-8 representing
    a game square.
    '''
    available = _available_moves(game_state)
    if 4 in available:
    	return 4
    else:
    	human_win = _next_move(_human_moves(game_state), available)
    	computer_win = _next_move(_computer_moves(game_state), available)
    	if human_win != None:
    		return human_win
    	elif computer_win != None:
    		return computer_win
    	else:
    		return min(available)

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
	#if there are no available moves left, the game is over.
	if len(_available_moves(game_state)) == 0:
		return 3
	#use permutations to check if there exists a winning combination on the board.
	for combo in WINNING_COMBINATIONS:
		if combo in list(permutations(_human_moves(game_state), 3)):
			return 1
		elif combo in list(permutations(_computer_moves(game_state), 3)):
			return 2
	return False