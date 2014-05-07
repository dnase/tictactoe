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

def best_move(game_state):
    #if the middle spot is available, always take it.
    if 4 in _available_moves(game_state):
    	return 4
    else:
    	return min(_available_moves(game_state))

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