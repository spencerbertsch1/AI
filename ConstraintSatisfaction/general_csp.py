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

    def __init__(self, x, d, c, verbose: bool, csp_problem: str, solution, use_inference: bool, use_mrv: bool = False,
                 use_degree_heuristic: bool = False, use_lcv: bool = False):
        self.x = x
        self.d = d
        self.c = c
        self.d_copy = self.d.copy()
        self.verbose = verbose
        self.csp_problem = csp_problem
        self.solution = solution
        self.use_inference = use_inference
        self.use_mrv = use_mrv
        self.use_degree_heuristic = use_degree_heuristic
        self.use_lcv = use_lcv


    def __repr__(self):
        return '\n'.join([
            f'Variables: {self.x}',
            f'Domains: {self.d}',
            f'Constraints: {self.c}'
        ])

    def mrv_heuristic(self, assignment):
        """
        Returns the node with the minimum remaining value for connections in the constraint graph
        :return: node (var)
        """
        # we only want to search through the usassigned variables
        unassigned_vars = set(self.x) - set(assignment.keys())

        # initialize the edge dictionary with all worst cases
        edge_dict = {}
        for var in unassigned_vars:
            edge_dict[var] = len(self.d[var])

        for var in unassigned_vars:
            # here we have a variable with an unconstrained domain. we might be able to prune it here
            for neighbor in self.get_neighbors(X=var):
                # testing whether or not [neighbor] is constraining [var]'s domain values
                if len(self.d[neighbor]) == 1:
                    # we have found a constraint! Now we reduce the domain of [var] by the [var] of the neighbor
                    edge_dict[var] = edge_dict[var] - 1

        # now we just return the variable the has the fewest connections
        var = min(edge_dict, key=edge_dict.get)
        return var

    def degree_heuristic(self, assignment):
        # Use the degree heuristic to get the unassigned variables
        unassigned_vars = set(self.x) - set(assignment.keys())
        vars_dict = {}
        for var in unassigned_vars:
            n = self.get_neighbors(X=var)
            vars_dict[var] = len(n)
            # we can now get the variable with the max neighbors
        var = max(vars_dict, key=vars_dict.get)
        return var

    def order_domain_values(self, var, assignment):
        """
        Order domain values method - similar to the get_successors method in DFS
        Here we can use the Least Common Value heuristic to optimize backtracking search and resude the number of
        nodes that the algorithm needs to search through

        :param csp:
        :return:
        """
        if self.use_lcv:
            # We want to choose the value in the domain that rules out the fewest choices for neighbors

            domains = self.d[var]
            neighbors = self.get_neighbors(X=var)

            # initialize neighbor_choices - later we will pick the variable that maximizes neighbor choices
            neighbor_choices = {}
            for value in domains:
                neighbor_choices[value] = 0

            for value in domains:
                for neighbor in neighbors:
                    # find out how many choices there are for the neighbor if we choose this variable from the domain
                    original_domain = self.d[var].copy()
                    self.d[var] = [value]

                    # get the number of new domains when the current variable is set to [var]
                    num_new_domains = len(self.get_domains(var=neighbor))
                    neighbor_choices[value] = neighbor_choices[value] + num_new_domains

                    # after the test, we reset the instance variable back to it's correct domain
                    self.d[var] = original_domain

            # we now have a dict with the number of total neighbor choices for each variable
            # next step is to sort the dictionary ascending, then convert the keys to a list which we return
            sorted_dict: dict = {k: v for k, v in sorted(neighbor_choices.items(), key=lambda item: item[1])}
            sorted_domains: list = list(sorted_dict.keys())
            sorted_domains.reverse()

            return sorted_domains
        else:
            # get all the possible values that can belong to that variable
            domains = self.d[var]
            return domains

    def select_unassigned_variable(self, assignment):
        """
        This is where we implement heuristics to improve performance!
        1. MRV heuristic
        2. Degree heuristic
        3. If we're not using either, we just return an element of the unnassigned_variables set
        :param assignment: current assignment
        :return: an unassigned variable
        """
        # Minimum Remaining Value heuristic returns the variable with the fewest remaining values in its domain
        if self.use_mrv:
            var = self.mrv_heuristic(assignment=assignment)
            return var

        # Degree heuristic returns the variable with the largest number of connections in the constrain graph
        elif self.use_degree_heuristic:
            var = self.degree_heuristic(assignment=assignment)
            return var

        # If we're not using degree heuristic, LCV, or MRV, then we just use all variables not in the assignment
        else:
            unassigned_vars = set(self.x) - set(assignment.keys())
            var = list(unassigned_vars)[0]  # <-- order doesn't matter here so we just grab a value from the set
            return var

    def get_neighbors(self, X):
        """
        Helper function to return all the neighbors of a node X in the constraint graph
        :param X:
        :return:
        """
        neighbors = []
        for c in self.c:
            if X in c:
                if c[0] != X:
                    neighbors.append(c[0])
                if c[1] != X:
                    neighbors.append(c[1])
        return neighbors

    def revise(self, X, Y) -> bool:
        """
        Helper function for AC-3 function

        :param csp:
        :param X:
        :param Y:
        :return:
        """
        revised = True
        # get the updated domain of X
        d_x = self.get_domains(var=X)
        # get the updated domain of Y
        d_y = self.get_domains(var=Y)

        for x in d_x:
            pass
            # TODO add logic here!!

        return revised

    def AC3(self):
        """
        AC-3 implementation for backtracking algorithm

        :param csp:
        :return:
        """

        # create a queue of all the forward and backward arcs
        backwards_arcs = []
        for constraint in self.c:
            backwards_constraint = tuple(reversed(constraint))
            backwards_arcs.append(backwards_constraint)
        # maybe just use forward arcs... vvv
        forward_arcs = self.c.copy()
        all_arcs_queue = forward_arcs + backwards_arcs

        while len(all_arcs_queue) != 0:
            const = all_arcs_queue.pop()
            X = const[0]
            Y = const[1]
            if self.revise(X=X, Y=Y):
                # get current domain here
                d_i = self.d[X]
                if len(d_i) == 0:
                    return False

                all_neighbors: list = self.get_neighbors(X=X)
                neighbors: list = [x for x in all_neighbors if x != Y]
                for new_x in neighbors:
                    new_edge = (new_x, X)
                    # insert the new edge in the graph at the front of the queue to be checked
                    all_arcs_queue.insert(0, new_edge)

        return True

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

                        # logic in this if-statement was adapted from stackoverflow.com: bit.ly/3p8pKgQ
                        # if piece 1 is on the right or left of piece 2
                        if (lr_2[0] < ll_1[0]) | (lr_1[0] < ll_2[0]):
                            pass
                        # if piece 1 is above or below piece 2
                        elif (ur_1[1] < ll_2[1]) | (ul_2[1] < lr_1[1]):
                            pass
                        else:
                            answer = False

        return answer

    def get_domains(self, var):
        """
        Updated function - returns the current (pruned) domains for an input variable

        :return: the new, potentially pruned domain
        """
        domain_copy: list = self.d[var].copy()
        for neighbor in self.get_neighbors(X=var):
            # testing whether or not [neighbor] is constraining [var]'s domain values
            if len(self.d[neighbor]) == 1:
                # we have found a constraint! Now we reduce the domain of [var] by the [var] of the neighbor
                neighbor_var = self.d[neighbor][0]
                # and we update the instance variable to reflect the change
                domain_copy = [x for x in domain_copy if x != neighbor_var]

        # we return the new, potentially pruned domain
        return domain_copy

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
                # update the current domain of (var) here
                self.d[var] = [value]

                if self.use_inference:
                    # use AC-3 with backtracking here
                    inference: bool = self.AC3()
                    # if AC3 returns false, we pass, but if it returns true, we run backtrack and get the result
                    if inference:
                        result = self.backtrack(assignment=assignment)
                        if result is not False:
                            return result
                else:
                    # vanilla backtracking with no inference
                    result = self.backtrack(assignment=assignment)

                    if result is not False:
                        return result

            del assignment[var]
            # update the domains here as well
            self.d[var] = self.d_copy[var]

        return False
