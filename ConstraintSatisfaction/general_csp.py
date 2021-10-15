# Spencer Bertsch
# October 2021
# Assignment 4
# CS 276 @ Dartmouth College


class CSP:

    def __init__(self, x, d, c, verbose: bool, csp_problem: str):
        self.x = x
        self.d = d
        self.c = c
        self.verbose = verbose
        self.csp_problem = csp_problem

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
            # here we loop through the assignment itself and just make sure that nothing is overlapping...
            reset_board = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                           ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                           ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
            board = reset_board.copy()

            piece_names = ['a', 'b', 'c', 'e']

            ii = 0
            for piece, position in assignment.items():
                print(f'Updating the values in the board for piece {piece_names[ii], piece} in position {position}.')
                for x in range(piece[0]):
                    # we are starting from the lower left index, not the upper left, so we loop backwards over [y]
                    for y in range(piece[1]):
                        new_x: int = x + position[0]
                        new_y: int = y + position[1]
                        print(f'CHECKING x:{new_x}, y:{new_y}')
                        if board[new_x][new_y] == '.':
                            # nothing is overlapping so far...
                            board[new_x][new_y] = piece_names[ii]
                            # self.pretty_print_board(board=board)
                        else:
                            # alas something is overlapping...
                            # we could just return False here - it would be much faster
                            return False

                self.pretty_print_board(board=board)
                ii += 1

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
            return assignment

        var = self.select_unassigned_variable(assignment=assignment)

        for value in self.order_domain_values(var=var, assignment=assignment):
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


# some test code - this section can be safely ignored or removed.
if __name__ == "__main__":

    # define the variables
    # length tuple ()
    x = {(3, 2), (5, 2), (2, 3), (7, 1)}

    # define the domains
    a_domain = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1),
                (6, 0), (6, 1), (7, 0), (7, 1)]
    b_domain = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1)]
    c_domain = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
    e_domain = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2)]

    # define domains for each variable in the CSP
    d = {(3, 2): a_domain, (5, 2): b_domain, (2, 3): c_domain, (7, 1): e_domain}

    # define the constraints
    # there would be an incredibly huge number of constraints for this problem... how could we represent them?
    c = []

    # assignment will have the position of the lower left corner of each piece
    # for example: assignment = {(3, 2): (0, 0), (5, 2): (1, 1)}

    m_csp = CSP(x=x, d=d, c=c, verbose=True, csp_problem='circuits')
    print(m_csp.backtracking_search())
