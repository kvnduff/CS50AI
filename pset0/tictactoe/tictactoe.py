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

    # Initialize x and o counters
    x_count = 0
    o_count = 0

    # Determine number of X and O on the board
    for row in board:
        x_count += row.count(X)
        o_count += row.count(O)

    # If number of X and O are equal then X turn
    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Initialize empty action set
    actions = set()

    # Iterate over rows
    for row in range(len(board)):
        # Iterate over columns
        for col in range(len(board[0])):
            # If board space is Empty then is available action
            if board[row][col] == EMPTY:
                actions.add((row, col))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Return exception if move invalid
    if action not in actions(board):
        raise Exception("Not a valid move!")

    # Return result if move valid
    newboard = copy.deepcopy(board)
    if player(board) == X:
        newboard[action[0]][action[1]] = X
        return newboard
    elif player(board) == O:
        newboard[action[0]][action[1]] = O
        return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Initialize win variable
    win = None

    # Horizontal winner
    if win is None:
        for i in range(3):
            # Horizontal win
            if board[i].count(X) == 3:
                return X
            if board[i].count(O) == 3:
                return O

    # Vertical winner
    if win is None:
        for i in range(3):
            count_x = 0
            count_y = 0
            for j in range(3):
                if board[j][i] == X:
                    count_x += 1
                    if count_x == 3:
                        return X
                if board[j][i] == O:
                    count_y += 1
                    if count_y == 3:
                        return O

    # Diagonal winner
    if win is None:
        if (board[0][0] == X and board[1][1] == X and board[2][2] == X) \
                or (board[0][2] == X and board[1][1] == X and board[2][0] == X):
            return X
        if (board[0][0] == O and board[1][1] == O and board[2][2] == O) \
                or (board[0][2] == O and board[1][1] == O and board[2][0] == O):
            return O

    # No winner
    if win is None:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Number of occupied board spaces
    num = 0
    for row in board:
        num += row.count(X) + row.count(O)

    # Return True if winner or all board spaces occupied, otherwise False
    if winner(board) is not None or num == 9:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # Use winner function to return numeric utility values
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Initialize variable
    optimal = ""

    # Determine current player
    cplayer = player(board)

    # Determine best move if current player is X (max score)
    if cplayer == X:
        # Set maxscore to negative infinity
        maxscore = -math.inf
        # maxscore = -2
        # Iterate through possible actions
        for action in actions(board):
            score = min_score(result(board, action))
            # Update maxscore and optimal action
            if score > maxscore:
                maxscore = score
                optimal = action

    # Determine best move if current player is 0 (min score)
    else:
        # Set minscore to positive infinity
        minscore = math.inf
        # minscore = 2
        # Iterate through possible actions
        for action in actions(board):
            score = max_score(result(board, action))
            # Update minscore and optimal action
            if score < minscore:
                minscore = score
                optimal = action

    # Return optimal move
    return optimal


def max_score(board):
    """
    Returns the maximal score.
    """

    # If action leads to terminal state then return score
    if terminal(board):
        return utility(board)

    # If no terminal state then return maxscore
    maxscore = -math.inf
    # maxscore = -2
    for action in actions(board):
        maxscore = max(maxscore, min_score(result(board, action)))
    return maxscore


def min_score(board):
    """
    Returns the minimal score.
    """

    # If action leads to terminal state then return score
    if terminal(board):
        return utility(board)

    # If no terminal state then return minscore
    minscore = math.inf
    # minscore = 2
    for action in actions(board):
        minscore = min(minscore, max_score(result(board, action)))
    return minscore
