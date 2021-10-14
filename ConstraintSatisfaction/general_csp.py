# Spencer Bertsch
# October 2021
# Assignment 4
# CS 276 @ Dartmouth College


class CSP:

    def __init__(self, x, d, c):
        self.x = x
        self.d = d
        self.c = c
        self.assigned_variables = set()
        self.unassigned_variables = set(self.x) - self.assigned_variables

    def __repr__(self):
        return '\n'.join([
            f'Variables: {self.x}',
            f'Domains: {self.d}',
            f'Constraints: {self.c}'
        ])

    @ staticmethod
    def select_unassigned_variable(csp):
        # maybe we should remove var from the unassigned variables here
        # TODO wouldn't it be easier to just pass the assignment into this function instead of keeping track in the CSP?

        val = list(csp.unassigned_variables)[1]
        return val

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

    def order_domain_values(self, var, assignment, csp):
        """
        Order domain values method - similar to the get_successors method in DFS
        :param csp:
        :return:
        """
        # get all the possible values that can belong to that variable
        domains = csp.d[var]
        # TODO is this right?? Where do we use the assignment here?
        return domains

    def test_consistency(self, assignment, csp) -> bool:
        """
        returns True if the assignment is consistent and doesn't violate any constraints.
        returns False otherwise.

        :param assignment:
        :param csp:
        :return: bool
        """
        # TODO how should we do this? We could iterate over each k-v pair in the assignment dict and then
        # TODO iterate over all the constraints to ensure they never match, seems costly but maybe that's the best move
        answer = True
        for var, value in assignment.items():
            for constraint in csp.c:
                if ((var == constraint[0]) & (value == constraint[1])) | \
                   ((var == constraint[1]) & (value == constraint[0])):
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

    def backtracking_search(self, csp):
        return self.backtrack(assignment={}, csp=csp)

    def backtrack(self, assignment, csp):
        """
        Implement recursive backtracking search

        :param assignment: dictionary of variables to values
        :param csp:
        :return: either a valid assignment or False if none exists
        """
        # if assignment is complete, then we return the assignment here
        if set(assignment) == set(csp.x):  # TODO <-- double check that this works
            return assignment

        var = self.select_unassigned_variable(csp=csp)
        print(var)

        for value in self.order_domain_values(var=var, assignment=assignment, csp=csp):
            # test whether or not the value is consistent with the assignment
            print(f'Testing whether or not {value} is consistent with the assignment: {assignment}')

            # add value to test assignment
            test_assignment = assignment
            test_assignment[var] = value

            # see if any constraints are violated
            if self.test_consistency(assignment=test_assignment, csp=csp):

                # add value to assignment
                assignment[var] = value

                # # TODO add inference code later...
                # inferences = self.inference(csp=csp, var=var, value=value)
                # if inferences:
                result = self.backtrack(assignment, csp)

                if result is not False:
                    return result

            del assignment[var]  # <-- TODO maybe this shouldn't be here?... but maybe it should...

        return False


# some test code - this section can be safely ignored or removed.
if __name__ == "__main__":

    # define the variables
    x = {'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T'}

    # define the domains
    doms = ['red', 'green', 'blue']
    # we might need something like this in the future vvv
    d = {'WA': doms, 'NT': doms, 'Q': doms, 'NSW': doms, 'V': doms, 'SA': doms, 'T': doms}

    # define the constraints
    # write a function that takes 2 countries and their colors and returns True if that is ok, False if it's illegal
    c = [('SA', 'WA'), ('SA', 'NT'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'WA'),
         ('SA', 'V'), ('WA', 'NT'), ('NT', 'Q'), ('Q', 'NSW'), ('NSW', 'V')]

    m_csp = CSP(x=x, d=d, c=c)
    print(m_csp.backtracking_search(csp=m_csp))
