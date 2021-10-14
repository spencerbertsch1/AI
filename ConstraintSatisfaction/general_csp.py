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

    def is_complete(self, assignment, csp) -> bool:
        """
        TODO determine whether or not the current assignment is a solution to the CSP
        :param assignment:
        :param csp:
        :return:
        """
        return False

    @ staticmethod
    def select_unassigned_variable(csp):
        # maybe we should remove var from the unassigned variables here
        val = list(csp.unassigned_variables)[1]
        return val

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

    def test_consistency(self):
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
        # if assignment is complete, then we return the assignment
        if self.is_complete(assignment=assignment, csp=csp):
            return assignment

        var = self.select_unassigned_variable(csp=csp)
        print(var)

        for value in self.order_domain_values(var=var, assignment=assignment, csp=csp):
            # test whether or not the value is consistent with the assignment
            pass
                # add value to assignment

                # see if any constraints are violated


# some test code - this section can be safely ignored or removed.
if __name__ == "__main__":

    # define the variables
    x = {'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T'}

    # define the domains
    d = {'WA': {'red', 'green', 'blue'},
         'NT': {'red', 'green', 'blue'},
         'Q': {'red', 'green', 'blue'},
         'NSW': {'red', 'green', 'blue'},
         'V': {'red', 'green', 'blue'},
         'SA': {'red', 'green', 'blue'},
         'T': {'red', 'green', 'blue'}
         }

    # define the constraints
    # write a function that takes 2 countries and their colors and returns True if that is ok, False if it's illegal
    c = [('SA', 'WA'), ('SA', 'NT'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'WA'),
         ('SA', 'V'), ('WA', 'NT'), ('NT', 'Q'), ('Q', 'NSW'), ('NSW', 'V')]

    # could also define c as a dictionary... TODO
    C = {'SA': ['WA', 'NT', 'Q', 'NSW', 'WA', 'V'],
         'WA': ['NT']}

    m_csp = CSP(x=x, d=d, c=c)
    print(m_csp.backtracking_search(csp=m_csp))
