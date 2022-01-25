# ----------------------------------------------------------------------
# Name:     sudoku
# Purpose:  Homework5
#
# Author(s): Shayanna Gatchalian, Lin Zhu
#
# ----------------------------------------------------------------------
"""
Sudoku puzzle solver implementation

q1:  Basic Backtracking Search
q2:  Backtracking Search with AC-3
q3:  Backtracking Search with MRV Ordering and AC-3
"""
import csp


def build_domain(puzzle):
    """
    Create a dictionary representing the initial domains at each index of the sudoku puzzle.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: dictionary representing the initial domains at each index of the sudoku puzzle.
    """
    domain = {}
    for row in range(9):
        for column in range(9):
            if (row, column) in puzzle.keys():  # if puzzle(row, column) has given value,
                domain[(row, column)] = {puzzle[(row, column)]}  # assign given value to domain
            else:  # if puzzle(row, column) has no value
                domain[(row, column)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # assign initial domain of 1-9
    # print(domain)
    return domain


def fetch_neighbors(row, column):
    """
    Fetch the neighbors (same row, same column, same 3x3 square) for variable at (row, column)
    :param row: row value of variable
    :param column: column value of variable
    :return: set of neighbors of variable at (row, column).
    """
    neighbors = set()

    # row, column neighbors
    for i in range(9):  # add neighbors of same row
        if i != column:
            neighbors.add((row, i))
    for j in range(9):  # add neighbors of same column
        if j != row:
            neighbors.add((j, column))

    # 3x3 neighbors
    square_row = int(row / 3)  # return 0, 1, 2
    square_column = int(column / 3)  # return 0, 1, 2
    for i in range(square_row * 3, (square_row * 3) + 3):  # for each row value in 3x3
        for j in range(square_column * 3, (square_column * 3) + 3):  # for each column value in 3x3
            if i != row and j != column and (i, j) not in neighbors:  # if not index we are getting neighbors for +
                # not neighbors already in set
                neighbors.add((i, j))  # add neighbor
    # print(neighbors)
    return neighbors


def build_neighbors(puzzle):
    """
    Create a dictionary representing the neighbors of an index.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: dictionary representing the neighbors of an index.
    """
    neighbors = {}
    for row in range(9):
        for column in range(9):
            neighbors[(row, column)] = fetch_neighbors(row, column)

    # print(neighbors)
    return neighbors

def check_constraint(var1, val1, var2, val2):
    """
    Constraint = val1 cannot equal val2, where var1 and var2 are neighbors in the sudoku puzzle
    :param var1: a variable in the CSP ((row, column) tuple)
    :param val1: the value of var1
    :param var2: a variable in the CSP ((row, column) tuple)
    :param val2: the value of var2
    :return: true if constraint holds true, false if arguments do not
    """
    return val1 != val2


def build_csp(puzzle):
    """
    Create a CSP object representing the puzzle.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: CSP object
    """
    # domains, neighbors, constraints
    # take puzzle variable (dictionary) and turn it into a CSP object

    return csp.CSP(build_domain(puzzle), build_neighbors(puzzle), check_constraint)


def q1(puzzle):
    """
    Solve the given puzzle with basic backtracking search
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    q1csp = build_csp(puzzle)
    return q1csp.backtracking_search(), q1csp

def q2(puzzle):
    """
    Solve the given puzzle with backtracking search and AC-3 as
    a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    q2csp = build_csp(puzzle)
    q2csp.ac3_algorithm()
    return q2csp.backtracking_search(), q2csp


def q3(puzzle):
    """
    Solve the given puzzle with backtracking search and MRV ordering and
    AC-3 as a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    q3csp = build_csp(puzzle)
    q3csp.ac3_algorithm()
    return q3csp.backtracking_search("MRV"), q3csp
