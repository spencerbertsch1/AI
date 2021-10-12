# Spencer Bertsch
# October 2021
# Assignment 4
# CS 276 @ Dartmouth College


class CSP:

    def __init__(self, x, d, c):
        self.x = x
        self.d = d
        self.c = c

    def __repr__(self):
        return '\n'.join([
            f'Variables: {self.x}',
            f'Domains: {self.d}',
            f'Constraints: {self.c}'
        ])

    def is_complete(self, assignment, csp) -> bool:
        """
        TODO determine whether or not the current assignment is a solution to the CSP
        :param assignment:
        :param csp:
        :return:
        """
        return False


    def AC3(self, csp):
        """
        TODO implement AC-3

        :param csp:
        :return:
        """
        pass


    def backtracking_search(self, csp):
        return self.backtrack(assignment={}, csp=csp)


    def backtrack(self, assignment, csp):
        """
        Implement recursive backtracking search

        :param assignment:
        :param csp:
        :return: either a valid assignment or False if none exists
        """
        # if assignment is complete, then we return the assignment
        if self.is_complete(assignment=assignment, csp=csp):
            return assignment