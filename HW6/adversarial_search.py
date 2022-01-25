# ----------------------------------------------------------------------
# Name:     adversarial_search
# Purpose:  Homework 6 - Implement adversarial search algorithms
#
# Author: Shayanna Gatchalian, Lin Zhu
#
# ----------------------------------------------------------------------
"""
Adversarial search algorithms implementation

Your task for homework 6 is to implement:
1.  minimax
2.  alphabeta
3.  abdl (alpha beta depth limited)
"""
import random
import math  # You can use math.inf to initialize to infinity

def rand(game_state):
    """
    Generate a random move.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the random move
    """
    done = False
    while not done:
        row = random.randint(0, game_state.size - 1)
        col = random.randint(0, game_state.size - 1)
        if game_state.available(row,col):
            done = True
    return row, col


def minimax(game_state):
    """
    Find the best move for our AI agent using the minimax algorithm.
    (searching the entire tree from the current game state)
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # for each possible move for AI, choose maximum of user's minimum next move
    return max(game_state.possible_moves(), key = lambda m: value(game_state.successor(m, "AI"), "user"))


def value(game_state, agent):
    """
    Calculate the minimax value for any state under the given agent's
    control.
    :param game_state: GameState object - state may be terminal or
    non-terminal
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    if game_state.is_win("AI"): # AI wins game
        return 1
    elif game_state.is_win("user"): # user wins game
        return -1
    elif game_state.is_tie():   # game ends in tie
        return 0
    elif agent == "AI": # if agent is AI
        return max_value(game_state)    # return max_value of successor state
    else:   # if agent is user
        return min_value(game_state)    # return min_value of successor state

def max_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent)
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    possible_moves = game_state.possible_moves()    # get list of all empty squares in tic-tac-toe board
    successor_states = []   # create list of successor_states
    for possible_move in possible_moves:    # for each possible_move
        successor_states.append(value(game_state.successor(possible_move, "AI"), "user"))    # get successor_state and add to successor_states
    return max(successor_states)  # return max of these successor_states

def min_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user)
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    possible_moves = game_state.possible_moves()    # get list of all empty squares in tic-tac-toe board
    successor_states = []   # create list of successor_states
    for possible_move in possible_moves:    # for each possible_move
        successor_states.append(value(game_state.successor(possible_move, "user"), "AI"))    # get successor_state and add to successor_states
    return min(successor_states)  # return min of these successor_states

def alphabeta(game_state):
    """
    Find the best move for our AI agent using the minimax algorithm
    with alpha beta pruning.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # for each possible move for AI, choose maximum of user's minimum next move
    return max(game_state.possible_moves(), key = lambda m: ab_value(game_state.successor(m, "AI"), "user", -math.inf, math.inf))

def ab_value(game_state, agent, alpha, beta):
    """
    Calculate the minimax value for any state under the given agent's
    control using alpha beta pruning
    :param game_state: GameState object - state may be terminal or
    non-terminal.
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    if game_state.is_win("AI"):  # AI wins game
        return 1
    elif game_state.is_win("user"):  # user wins game
        return -1
    elif game_state.is_tie():  # game ends in tie
        return 0
    elif agent == "AI":  # if agent is AI
        return abmax_value(game_state, alpha, beta)  # return abmax_value of successor state
    else:  # if agent is user
        return abmin_value(game_state, alpha, beta)  # return abmin_value of successor state

def abmax_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent) using alpha beta pruning
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    v = -math.inf   # initialize with max integer
    possible_moves = game_state.possible_moves()    # get list of all empty squares in tic-tac-toe board
    for possible_move in possible_moves:    # for each possible_move
        v = max(v, ab_value(game_state.successor(possible_move, "AI"), "user", alpha, beta))    # calculate v
        if v >= beta:
            return v    # return v if it is more than or equal to beta
        alpha = max(alpha, v)   # assign new alpha value
    return v    # return v

def abmin_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user) using alpha beta pruning
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    v = math.inf   # initialize with min integer
    possible_moves = game_state.possible_moves()    # get list of all empty squares in tic-tac-toe board
    for possible_move in possible_moves:    # for each possible_move
        v = min(v, ab_value(game_state.successor(possible_move, "user"), "AI", alpha, beta))    # calculate v
        if v <= alpha:
            return v    # return v if it is more than or equal to beta
        beta = min(beta, v)   # assign new alpha value
    return v    # return v


def abdl(game_state, depth):
    """
    Find the best move for our AI agent by limiting the alpha beta
    search the given depth and using the evaluation function
    game_state.eval()
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    return max(game_state.possible_moves(), key = lambda m: abdl_value(game_state.successor(m, "AI"), "user", -math.inf, math.inf, depth))

def abdl_value(game_state, agent, alpha, beta, depth):
    """
    Calculate the utility for any state under the given agent's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: GameState object - state may be terminal or
    non-terminal
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) utility of that state
    """
    size = game_state.size * 2 - 1  # number of rows/columns max can win + number of rows/columns max can win - 1 (for row/column already taken by playwer with current turn)
    if game_state.is_win("AI"):  # AI wins game
        return size
    elif game_state.is_win("user"):  # user wins game
        return -size
    elif game_state.is_tie():  # game ends in tie
        return 0
    elif depth == 0:    # return utility on max depth
        return game_state.eval()
    elif agent == "AI":  # if agent is AI
        return abdlmax_value(game_state, alpha, beta, depth)  # return abdlmax_value of successor state
    else:  # if agent is user
        return abdlmin_value(game_state, alpha, beta, depth)  # return abdlmin_value of successor state


def abdlmax_value(game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Max's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    v = -math.inf  # initialize with max integer
    possible_moves = game_state.possible_moves()    # get list of all empty squares in tic-tac-toe board
    for possible_move in possible_moves:    # for each possible_move
        v = max(v, abdl_value(game_state.successor(possible_move, "AI"), "user", alpha, beta, depth - 1))  # calculate v
        if v >= beta:
            return v    # return v if it is more than or equal to beta
        alpha = max(alpha, v)   # assign new alpha value
    return v    # return v


def abdlmin_value(game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Min's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    v = math.inf   # initialize with max integer
    possible_moves = game_state.possible_moves()    # get list of all empty squares in tic-tac-toe board
    for possible_move in possible_moves:    # for each possible_move
        v = min(v, abdl_value(game_state.successor(possible_move, "user"), "AI", alpha, beta, depth - 1))   # calculate v
        if v <= alpha:
            return v    # return v if it is more than or equal to beta
        beta = min(beta, v)   # assign new alpha value
    return v    # return v

