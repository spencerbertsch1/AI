# Spencer Bertsch
# October 2021
# Assignment 4
# CS 276 @ Dartmouth College


class Solution:

    def __init__(self, problem_type: str):
        self.problem_type = problem_type
        self.nodes_visited = 0
        self.answer = None

    def __repr__(self):
        s = f'Constraint Satisfaction Problem: {self.problem_type} \n' \
            f'Nodes Visited: {self.nodes_visited} \n' \
            f'Answer: {self.answer}'
        return s


class CSP:

    def __init__(self, x, d, c, verbose: bool, csp_problem: str, solution):
        self.x = x
        self.d = d
        self.c = c
        self.verbose = verbose
        self.csp_problem = csp_problem
        self.solution = solution

    def __repr__(self):
        return '\n'.join([
            f'Variables: {self.x}',
            f'Domains: {self.d}',
            f'Constraints: {self.c}'
        ])

    def select_unassigned_variable(self, assignment):
        # maybe we should remove var from the unassigned variables here
        # TODO this is where we can implement heuristic to improve performance !
        unassigned_vars = set(self.x) - set(assignment.keys())
        var = list(unassigned_vars)[0]
        return var

    def revise(self, csp, X, Y):
        """
        Helper function for AC-3 function

        TODO implement revise
        :param csp:
        :param X:
        :param Y:
        :return:
        """
        pass

    def AC3(self, csp):
        """
        TODO implement AC-3

        :param csp:
        :return:
        """
        pass

    def order_domain_values(self, var, assignment):
        """
        Order domain values method - similar to the get_successors method in DFS
        :param csp:
        :return:
        """
        # get all the possible values that can belong to that variable
        domains = self.d[var]
        # TODO is this right?? Where do we use the assignment here?
        return domains

    @ staticmethod
    def pretty_print_board(board):
        """
        Small helper function to help us visualize the board
        :param board:
        :return:
        """
        for row in reversed(board):
            print(row, '\n')

    def test_consistency(self, assignment) -> bool:
        """
        returns True if the assignment is consistent and doesn't violate any constraints.
        returns False otherwise.

        :param assignment:
        :param csp:
        :return: bool
        """
        if self.csp_problem == 'map_coloring':
            answer = True
            for constraint in self.c:
                # here we use .get() with the assignment to provide a default value for the lookup (avoiding key errors)
                val1 = assignment.get(constraint[0], float('nan'))  # <-- use float('nan') because [nan != nan]
                val2 = assignment.get(constraint[1], float('nan'))
                if val1 == val2:
                    answer = False
        else:
            # circuit problem
            answer = True
            piece_names: dict = {0: 'a', 1: 'b', 2: 'c', 3: 'e'}
            ll, ul, lr, ur = [], [], [], []
            # first step, find all the corners of each piece!
            for piece, lower_left in assignment.items():
                upper_left = (lower_left[0], (lower_left[1] + piece[1]-1))
                lower_right = ((lower_left[0] + piece[0] - 1), lower_left[1])
                upper_right = ((lower_left[0] + piece[0] - 1), (lower_left[1] + piece[1]-1))

                # save the corners of each piece outside the loop
                ll.append(lower_left)
                ul.append(upper_left)
                lr.append(lower_right)
                ur.append(upper_right)
                if self.verbose:
                    print(f'PIECE: {piece}, Lower left position: {lower_left} \n upper_left: {upper_left} '
                          f'\n lower_right: {lower_right} \n upper_right: {upper_right}')

            if len(ll) < 2:
                # only one shape can't overlap with itself
                return True
            else:
                # we need to check every combination of shapes and make sure each one doesn't overlap
                for i in range(len(ll)-1):
                    for j in range(i+1, len(ll), 1):
                        ll_1, ll_2 = ll[i], ll[j]
                        ul_1, ul_2 = ul[i], ul[j]
                        lr_1, lr_2 = lr[i], lr[j]
                        ur_1, ur_2 = ur[i], ur[j]
                        # I think I could have done this with only 2 points on each piece, oh well.

                        # NOTE logic in this if-statement was adapted from stackoverflow.com: bit.ly/3p8pKgQ
                        # if piece 1 is on the right or left of piece 2
                        if (lr_2[0] < ll_1[0]) | (lr_1[0] < ll_2[0]):
                            pass
                        # if piece 1 is above or below piece 2
                        elif (ur_1[1] < ll_2[1]) | (ul_2[1] < lr_1[1]):
                            pass
                        else:
                            answer = False

        return answer

    def inference(self, csp, var, value):
        """
        TODO
        :param csp:
        :param var:
        :param value:
        :return:
        """
        pass

    def backtracking_search(self):
        """
        Wrapper function for backtracking
        :return: either False, or a feasible solution to the CSP
        """
        return self.backtrack(assignment={})

    def backtrack(self, assignment):
        """
        Implement recursive backtracking search

        :param assignment: dictionary of variables to values
        :param csp:
        :return: either a valid assignment or False if none exists
        """
        # if assignment is complete, then we return the assignment here
        if set(assignment) == set(self.x):
            self.solution.answer = assignment
            return self.solution

        var = self.select_unassigned_variable(assignment=assignment)

        for value in self.order_domain_values(var=var, assignment=assignment):
            # increment nodes visited in the solution object
            self.solution.nodes_visited += 1

            # test whether or not the value is consistent with the assignment
            if self.verbose:
                print(f'Testing whether or not {var, value} is consistent with the current assignment: {assignment}')

            # add value to test assignment
            test_assignment = assignment
            test_assignment[var] = value

            # see if any constraints are violated
            if self.test_consistency(assignment=test_assignment):

                # add value to assignment
                assignment[var] = value

                # # TODO add inference code later...
                # inferences = self.inference(csp=csp, var=var, value=value)
                # if inferences:
                result = self.backtrack(assignment=assignment)

                if result is not False:
                    return result

            del assignment[var]

        return False
