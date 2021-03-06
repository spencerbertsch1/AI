# Spencer Bertsch
# September 2021
# Code adapted from Assignment 1
# CS 276 @ Dartmouth College

class SearchSolution:
    def __init__(self, problem, search_method):
        self.problem_name = str(problem)
        self.search_method = search_method
        self.path = []  # <-- This is the FIFO queue that will get updates as we search
        self.nodes_visited = 0
        self.solved = False  # <-- had to add this so I could write a test to break out of the

    def __repr__(self):
        string = "----\n"
        string += "{:s}\n"
        string += "attempted with search method {:s}\n"

        if len(self.path) > 0:

            string += "number of nodes visited: {:d}\n"
            string += "solution length: {:d}\n"
            string += "path: {:s}\n"

            string = string.format(self.problem_name, self.search_method,
                self.nodes_visited, len(self.path), str(self.path))
        else:
            string += "no solution found after visiting {:d} nodes\n"
            string = string.format(self.problem_name, self.search_method, self.nodes_visited)

        return string
