# Spencer Bertsch
# October 2021
# Assignment 5
# CS 276 @ Dartmouth College

# native imports
from pathlib import Path
import random
from random import randrange


class Solution:

    def __init__(self):
        self.tries = 0
        self.flips = 0
        self.assignment = None

    def __repr__(self):
        s = f'WALKSAT SOLUTION \n' \
            f'Number of Tries: {self.tries} \n' \
            f'Number of Flips: {self.flips} \n' \
            f'Solved Board: {self.assignment} \n'
        return s


class SAT:

    def __init__(self, path_to_puzzle: str, path_to_sol: str, threshold: float, max_flips: int, max_tries: int,
                 verbose: bool, solution):
        self.path_to_puzzle = path_to_puzzle
        self.path_to_sol = path_to_sol
        self.threshold = threshold
        self.max_flips = max_flips
        self.max_tries = max_tries
        self.verbose = verbose
        self.clauses = self.create_clause_dicts()
        self.assignment = self.create_random_assignment()
        self.solution = solution

    def create_clause_dicts(self):
        f = open(self.path_to_puzzle, "r")
        clauses = []
        for line in f:
            # split the cnf file into lists of strings
            values = line.split()
            if len(values) == 2:
                # we set the negated clauses to False, False
                clause_dict: dict = {int(x): False for x in values}
            else:
                # we set the other clauses to True, True, True, ...
                clause_dict: dict = {int(x): True for x in values}
            clauses.append(clause_dict)
        f.close()

        return clauses

    def create_cnf_list(self):
        """
        Import the CNF file
        :return:
        """
        f = open(self.path_to_puzzle, "r")
        cnf_list = []
        for line in f:
            cnf_list.append(line)
        f.close()

        return cnf_list


    def write_solution(self):
        pass
        # TODO method to write the solved puzzle to the specified output location

    def create_random_assignment(self):
        """
        Returns the initial assignment dictionary read in from the CNF file. If any values are not added (0 in the
        CNF file), then they are filled in randomly.

        :return: dictionary mapping 729 variables to 81 boolean values representing the state of the board
        """
        # first we can start with an assignment where everything is false, then we can randomly fill it in
        assignment = {}
        for row in range(9):
            row += 1
            for col in range(9):
                col += 1
                for value in range(9):
                    value += 1
                    key = int(str(row) + str(col) + str(value))
                    assignment[key] = False

        # We can now update the truth values for the starting points in our board
        cnf_list = self.create_cnf_list()
        cnf_list.reverse()
        current_positions = []
        for position in cnf_list:
            if len(position) < 5:
                current_positions.append(int(position))
            else:
                break

        # update the truth values that the board starts with
        for position, value in assignment.items():
            if position in current_positions:
                assignment[position] = True

        # TODO this could become a more generic method for randomizing the assignment - could be useful later on
        counter = 0
        assignment_values = []
        assignment_positions = []
        for position, value in assignment.items():
            counter += 1
            assignment_positions.append(position)
            assignment_values.append(value)

            if counter == 9:
                if not any(assignment_values):
                    position_to_update: int = random.choice(assignment_positions)  # <-- random choice used here
                    assignment[position_to_update] = True
                # reset after every 9 values in the dict
                counter = 0
                assignment_values = []
                assignment_positions = []

        return assignment

    def get_satisfied_clauses(self, assignment_to_score):
        """
        Returns the number of clauses satisfied by the input assignment.
        A perfect assignment would return a value of 3240.

        :return: int - satisfied_clauses
        """
        satisfied_clauses = 0

        # we can iterate through the clauses and see if we have any that aren't satisfied
        for clause in self.clauses:

            # count number of satisfied clauses
            if any(((clause[key]) == (assignment_to_score[key])) for key in clause.keys()):
                # clause is satisfied!
                satisfied_clauses += 1



            # if len(clause) == 2:
            #     # this is a clause that restricts a value from being both 1 and 2
            #     keys = [int(str(x)[-3:]) for x in clause.keys()]
            #
            #     if (assignment_to_score[keys[0]] is True) & (assignment_to_score[keys[1]] is True):
            #         # TODO how does this happen??
            #         score += 1
            #
            # else:
            #     # determine if this clause is satisfied:
            #     satisfied = False
            #     for cell, truth_value in clause.items():
            #         if truth_value == assignment_to_score[cell]:
            #             satisfied = True
            #
            #     # if the constraint was not satisfied, then we add one value to the violations counter
            #     if not satisfied:
            #         score += 1

        # This might be a cleaner implementation of the above code - more pythonic
        # for clause in self.clauses:
        #     if (any((clause[x]) == (assignment[x])) for x, y in clause.items()):
        #         pass
        #     else:
        #         violations += 1

        return satisfied_clauses

    def gsat_rewrite(self):

        for i in range(self.max_tries):
            self.solution.tries += 1
            # randomly fill the assignment
            random.seed(i + 1)
            self.assignment = self.create_random_assignment()

            for j in range(self.max_flips):
                self.solution.flips += 1

                # if the assignment is legal, we update the solution object and return it
                if self.get_satisfied_clauses(assignment_to_score=self.assignment) == 3240:
                    self.solution.assignment = self.assignment
                    return self.solution

                # generate a random number between 0 and 1
                p: float = random.uniform(0, 1)

                if p > self.threshold:
                    # flip a random variable in the assignment
                    random_key = random.choice(list(self.assignment.keys()))
                    if self.assignment[random_key] is True:
                        self.assignment[random_key] = False
                    else:
                        self.assignment[random_key] = True

                else:
                    # we now want to create a score dict which will hold the score improvement for each flip
                    score_dict = {}
                    for variable, truth_val in self.assignment.items():
                        # flip each truth value and see how that changes the score
                        test_assignment = self.assignment.copy()

                        # flip the variable
                        if test_assignment[variable] is True:
                            test_assignment[variable] = False
                        else:
                            test_assignment[variable] = True

                        # get the new score with the flipped variable
                        satisfied_clauses: int = self.get_satisfied_clauses(assignment_to_score=test_assignment)

                        if self.verbose:
                            # suppress print statements
                            if j % 10 == 1:
                                print(f'Remaining Clauses: {3240 - satisfied_clauses}')

                        # add the satisfied_clauses to the score dictionary
                        score_dict[variable] = satisfied_clauses

                    # now that we have the score dict, we can take a min value and make that change to the assignment
                    best_move = max(score_dict.items(), key=lambda x: x[1])[1]
                    best_moves = []
                    # Iterate over all the values in dictionary to find moves with min values
                    for key, value in score_dict.items():
                        if value == best_move:
                            best_moves.append(key)

                    # now we can flip the chosen variable in the assignment and continue with the search
                    chosen_var = random.choice(best_moves)

                    # flip the variable
                    if self.assignment[chosen_var] is True:
                        self.assignment[chosen_var] = False
                    else:
                        self.assignment[chosen_var] = True

    def walksat(self):
        pass
        # TODO


# some test code - this code can be safely ignored or removed
if __name__ == "__main__":

    # define puzzle name
    puzzle_name = 'puzzle2'
    # define paths to files
    PATH_TO_THIS_FILE: Path = Path(__file__).resolve()
    ABSPATH_TO_CNF_DIR: Path = PATH_TO_THIS_FILE.parent / 'puzzles'
    # for testing, always initialize the pseudorandom number generator to output the same sequence of values:
    random.seed(1)

    # define the name of the solution file that we will write once the solver is finished
    sol_filename = puzzle_name + ".sol"
    cnf_name = puzzle_name + ".cnf"
    ABSPATH_TO_CNF: Path = ABSPATH_TO_CNF_DIR / cnf_name
    ABSPATH_TO_SOL: Path = ABSPATH_TO_CNF_DIR / sol_filename

    # instantiate an empty solution object that will get updated during search
    sol = Solution()

    # instantiate the SAT object
    sat = SAT(path_to_puzzle=str(ABSPATH_TO_CNF), path_to_sol=str(ABSPATH_TO_SOL),
              threshold=0.99, max_tries=100_000, max_flips=10_000, verbose=True, solution=sol)

    sat.create_random_assignment()

    sat.gsat_rewrite()

