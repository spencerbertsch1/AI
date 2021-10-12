# Spencer Bertsch
# October 2021
# Assignment 4
# CS 276 @ Dartmouth College


def is_complete(assignment, csp) -> bool:
    """
    TODO determine whether or not the current assignment is a solution to the CSP
    :param assignment:
    :param csp:
    :return:
    """
    return False


def AC3(csp):
    """
    TODO implement AC-3

    :param csp:
    :return:
    """
    pass


def backtracking_search(csp):
    return backtrack(assignment={}, csp=csp)


def backtrack(assignment, csp):
    """
    Implement recursive backtracking search

    :param assignment:
    :param csp:
    :return: either a valid assignment or False if none exists
    """
    # if assignment is complete, then we return the assignment
    if is_complete(assignment=assignment, csp=csp):
        return assignment



