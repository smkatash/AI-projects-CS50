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
    countX = 0
    countO = 0
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == X:
                countX += 1
            if board[row][column] == O:
                countO += 1
    if countX > countO:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()
    for row in range(0, len(board)):
        for column in range(0, len(board[row])):
            if board[row][column] == EMPTY:
                possibleActions.add((row, column))
    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Not a valid action")
    i, j = action
    newBoard = copy.deepcopy(board)
    newBoard[i][j] = player(board)
    return newBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check horizont
    if all(i == board[0][0] for i in board[0]):
        return board[0][0]
    elif all(i == board[1][0] for i in board[1]):
        return board[1][0]
    elif all(i == board[2][0] for i in board[2]):
        return board[2][0]
    # Check vertic
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]
    # Check diagon
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0

def max_val(board):
    if terminal(board):
        return utility(board), None
    value = -math.inf
    move = None
    for action in actions(board):
        x, y = min_val(result(board, action))
        if x > value:
            value = x
            move = action
            if value == 1:
                return value, move
    return value, move

def min_val(board):
    if terminal(board):
        return utility(board), None
    value = math.inf
    move = None
    for action in actions(board):
        x, y = max_val(result(board, action))
        if x < value:
            value = x
            move = action
            if value == -1:
                return value, move
    return value, move

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_val(board)
            return move
        elif player(board) == O:
            value, move = min_val(board)
            return move
