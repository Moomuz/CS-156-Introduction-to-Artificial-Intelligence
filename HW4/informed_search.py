# ----------------------------------------------------------------------
# Name:     informed_search
# Purpose:  Homework 4 - Implement astar and some heuristics
#
# Author(s): Shayanna Gatchalian, Lin Zhu
# ----------------------------------------------------------------------
"""
A* Algorithm and heuristics implementation

Your task for homework 4 is to implement:
1.  astar
2.  single_heuristic
3.  better_heuristic
4.  gen_heuristic
"""
import data_structures


def astar(problem, heuristic):
    """
    A* graph search algorithm
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py
    heuristic (a function) the heuristic function to be used
    :return: list of actions representing the solution to the quest
                or None if there is no solution
    """
    closed = set()  # keep track of our explored states
    fringe = data_structures.PriorityQueue()  # for a*, the fringe is a priority queue
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    fringe.push(root, 0)
    while not fringe.is_empty():
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()  # we found a solution
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node, action, node.cumulative_cost + action_cost)
                fringe.push(child_node, child_node.cumulative_cost + heuristic(child_state, problem))
    return None  # Failure -  no solution was found


def null_heuristic(state, problem):
    """
    Trivial heuristic to be used with A*.
    Running A* with this null heuristic, gives us uniform cost search
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: 0
    """
    return 0


def single_heuristic(state, problem):
    """
    Single heuristic based on Manhattan distance to be used with A*, since we use the
    manhattan distance the actual cost will be greater the heuristic value
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest

    :return: integer representing heuristic value from Sammy's current position to last medal (using Manhattan
    """
    if not problem.is_goal(state):
        return abs(state[0][0] - state[1][0][0]) + abs(
            state[0][1] - state[1][0][1])  # get Manhattan distance from Sammy's current position to last medal
    else:
        return 0


def better_heuristic(state, problem):
    """
    Calculates heuristic using pathfinder helper function,
    since we use the manhattan distance the actual cost will be greater the heuristic value
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: integer representing a better heuristic estimation
    """
    if not problem.is_goal(state):  # if the state is not the goal state, calculate heuristic using Manhattan distance
        sammy, medals = state       # unpack state tuple into sammy (current position), medals (tuple of remaining medals)
        medal = medals[0]
        return pathfinder(sammy, medal, problem)
    else:
        return 0


def gen_heuristic(state, problem):
    """
    Calculates heuristic value for one or more medals using Manhattan distance with consideration of carrot cost,
    since we use the manhattan distance the actual cost will be greater the heuristic value
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: integer indicating the closest least cost heuristic
    """
    if not problem.is_goal(state):  # if the state is not the goal state, calculate heuristic using Manhattan distance
        sammy, medals = state   
        return max(pathfinder(sammy, medal, problem) for medal in medals)  # get the front of the queue
    else:
        return 0


def pathfinder(sammy, medal, problem):
    """
    Calculates heuristic value for one medal using Manhattan distance with consideration of carrot cost
    :param
    sammy: tuple indicating x,y position of sammy
    medal: tuple indicating x,y position of medal
    problem: (a Problem object) representing the quest
    :return: integer value of calculated heuristic
    """
    if sammy[0] <= medal[0]:
        if sammy[1] <= medal[1]:
            return (problem.cost['E'] * (medal[0] - sammy[0])) + (
                    problem.cost['S'] * (medal[1] - sammy[1]))  # sammy is above and to the left of medal
        else:
            return (problem.cost['E'] * (medal[0] - sammy[0])) + (
                    problem.cost['N'] * (sammy[1] - medal[1]))  # sammy is below and to the left of medal
    else:
        if sammy[1] <= medal[1]:
            return (problem.cost['W'] * (sammy[0] - medal[0])) + (
                    problem.cost['S'] * (medal[1] - sammy[1]))  # sammy is above and to the right of medal
        else:
            return (problem.cost['W'] * (sammy[0] - medal[0])) + (
                    problem.cost['N'] * (sammy[1] - medal[1]))  # sammy is below and to the right of medal
