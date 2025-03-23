"""
Tic Tac Toe Player
"""

import numpy as np
from copy import deepcopy

class InvalidActionError(Exception):
	"""
	Exception raised for invalid attempt.
	"""
	def __init__(self, action, board, message="Invalid action attempted."):
		super().__init__(f"{message} Action: {action}, Board: {board}")

X = "X"
O = "O"
EMPTY = None

def initial_state():
	"""
	Returns starting state of the board.
	"""
	return [[EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY]]

def player(board):
	"""
	Returns player who has the next turn on a board.
	"""
	return O if sum(row.count(X) for row in board) > sum(row.count(O) for row in board) else X

def actions(board):
	"""
	Returns set of all possible actions (i, j) available on the board.
	"""
	return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
	"""
	Returns the board that results from making move (i, j) on the board.
	"""
	if not (0 <= action[0] < 3 and 0 <= action[1] < 3) or board[action[0]][action[1]] != EMPTY:
		raise InvalidActionError(action, board, "Invalid move.")
	board_copy = deepcopy(board)
	board_copy[action[0]][action[1]] = player(board)
	return board_copy

def winner(board):
	"""
	Returns the winner of the game, if there is one.
	"""
	values = {"X": 1, "O": -1, None: 0}
	state = np.array([values[cell] for row in board for cell in row])
    # rows 0, 1, 2 -> win in rows 1, 2, 3;
	# rows 3, 4, 5 -> wins in cols 1, 2, 3;
	# rows 6, 7, 8 -> wins in diagonal / anti-diagonal;
	sums = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0],
				  	[0, 0, 0, 1, 1, 1, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 1, 1, 1],
					[1, 0, 0, 1, 0, 0, 1, 0, 0],
					[0, 1, 0, 0, 1, 0, 0, 1, 0],
					[0, 0, 1, 0, 0, 1, 0, 0, 1],
					[1, 0, 0, 0, 1, 0, 0, 0, 1],
					[0, 0, 1, 0, 1, 0, 1, 0, 0]]) @ state # Matrix product: winning positions, board
	return X if 3 in sums else O if -3 in sums else None

def terminal(board):
	"""
	Returns True if game is over (win / tie), False otherwise.
	"""
	return True if winner(board) or not actions(board) else False

def utility(board):
	"""
	Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
	"""
	return {X: 1, O: -1}.get(winner(board), 0)

# With alpha-beta pruning:
def max_value(board, alpha, beta):
	"""
	Returns the best utility value for the max player with alpha-beta pruning.
	(Helper function)
	"""
	if terminal(board):
		return utility(board), None
	v, best_move = float('-inf'), None
	for action in actions(board):
		min_val, move = min_value(result(board, action), alpha, beta)
		if min_val > v:
			v, best_move = min_val, action
		if v >= beta:
			return v, best_move
		alpha = max(alpha, v)
	return v, best_move

def min_value(board, alpha, beta):
	"""
	Returns the best utility value for the min player with alpha-beta pruning.
	(Helper function)
	"""
	if terminal(board):
		return utility(board), None
	v, best_move = float('inf'), None
	for action in actions(board):
		max_val, move = max_value(result(board, action), alpha, beta)
		if max_val < v:
			v, best_move = max_val, action
		if v <= alpha:
			return v, best_move
		beta = min(beta, v)
	return v, best_move

def minimax(board):
	"""
	Returns the optimal action for the current player on the board.
	"""
	if player(board) == X:
		return max_value(board, float('-inf'), float('inf'))[1]
	elif player(board) == O:
		return min_value(board, float('-inf'), float('inf'))[1]
	else: # Terminal
		return None

# Without alpha-beta pruning:
"""
def max_value(board):
    # Returns the best utility value for the max player.
    # (Helper function)
    if terminal(board):
        return utility(board), None
    v, best_move = float('-inf'), None
    for action in actions(board):
        min_val, move = min_value(result(board, action))
        if min_val > v:
            v, best_move = min_val, action
    return v, best_move

def min_value(board):
    # Returns the best utility value for the min player.
    # (Helper function)
    if terminal(board):
        return utility(board), None
    v, best_move = float('inf'), None
    for action in actions(board):
        max_val, move = max_value(result(board, action))
        if max_val < v:
            v, best_move = max_val, action
    return v, best_move

def minimax(board):
    # Returns the optimal action for the current player on the board.
    if terminal(board):
        return None
    if player(board) == X:
        return max_value(board)[1]
    elif player(board) == O:
        return min_value(board)[1]
"""