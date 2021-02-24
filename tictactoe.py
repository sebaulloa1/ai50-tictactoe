"""
Tic Tac Toe Player
"""

import math
import copy

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
    x_counter = 0
    o_counter = 0
    for row in board:
        for column in row:
            if column == X:
                x_counter += 1
            elif column == O:
                o_counter += 1
    if x_counter > o_counter and x_counter + o_counter < 9:
        return O
    elif x_counter <= o_counter and x_counter + o_counter < 9:
        return X
    else:
        return False


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    if terminal(board):
        return False
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                move = (row, column)
                moves.add(move)
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board = copy.deepcopy(board)
    row, column = action
    if board[row][column] is not EMPTY:
        raise Exception('Not a valid action.')
    board[row][column] = player(board)
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    x = 0
    while x < 3:
        # Check horizontal
        if board[x][0] is not EMPTY and board[x][0] == board[x][1] and board[x][1] == board[x][2]:
            return board[x][0]

        # Check vertical
        if board[0][x] is not EMPTY and board[0][x] == board[1][x] and board[1][x] == board[2][x]:
            return board[0][x]
        x += 1

    # Check diagonal win
    if board[0][0] is not EMPTY and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] is not EMPTY and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[1][1]

    # If tie or still in progress
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    else:
        for row in board:
            for column in row:
                if column == EMPTY:
                    return False
        return True 

    

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    elif not result:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    best_move = None
    alpha = -math.inf
    beta = math.inf
    if player(board) == X:
        best = -math.inf
        for action in actions(board):
            v = max_value(result(board, action), alpha, beta)
            if v > best:
                best = v
                best_move = action
        return best_move
    elif player(board) == O:
        best = math.inf
        for action in actions(board):
            v = min_value(result(board, action), alpha, beta)
            if v < best:
                best = v
                best_move = action
        return best_move
    else:
        return None


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v