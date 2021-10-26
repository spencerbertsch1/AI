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
        self.board = None

    def __repr__(self):
        s = f'WALKSAT SOLUTION \n' \
            f'Number of Tries: {self.tries} \n' \
            f'Number of Flips: {self.flips} \n' \
            f'Solved Board: {self.board} \n'
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
        self.assignment = self.create_initial_assignment()
        self.solution = solution

    def create_clause_dicts(self):
        f = open(self.path_to_puzzle, "r")
        clauses = []
        for line in f:
            # split the cnf file into lists of strings
            values = line.split()
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
            # split the cnf file into lists of strings
            values = line.split()
            if self.verbose:
                print(f'Values: {values}')
            cnf_list.append(line)
        f.close()

        return cnf_list


    def write_solution(self):
        pass
        # TODO method to write the solved puzzle to the specified output location

    def create_initial_assignment(self):
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
                    position_to_update: int = random.choice(assignment_positions)
                    assignment[position_to_update] = True
                # reset after every 9 values in the dict
                counter = 0
                assignment_values = []
                assignment_positions = []

        return assignment

    def is_assignment_legal(self):
        """

        :return:
        """
        violations = 0

        # we can iterate through the clauses and see if we have any that aren't satisfied
        for clause in self.clauses:

            # determine if this clause is satisfied:
            satisfied = False
            for cell, truth_value in clause.items():
                if truth_value == self.assignment[cell]:
                    satisfied = True

            # if the constraint was not satisfied, then we add one value to the violations counter
            if not satisfied:
                violations += 1

        # This might be a cleaner implementation of the above code - more pythonic
        # for clause in self.clauses:
        #     if (any((clause[x]) == (self.assignment[x])) for x, y in clause.items()):
        #         pass
        #     else:
        #         violations += 1

        return violations

    def gsat(self):

        # TODO rework this guy so that it works with the CNF implementation

        # define the parameters we will use for search
        max_tries = self.max_tries
        max_flips = self.max_flips
        threshold: float = self.threshold

        # run the search 'max_tries' times
        for i in range(max_tries):
            board = self.randomly_fill_board(puzzle=self.puzzle)
            self.solution.tries = self.solution.tries + 1
            print(f'on try {i}!')

            # perform at most 'max_flips' flips during the search
            for j in range(max_flips):
                self.solution.flips = self.solution.flips + 1

                # if the board state has no violations, add it to the solution and return the solution
                if self.is_legal(board_state=board) == 0:
                    self.solution.board = board
                    return self.solution

                # generate a random number between 0 and 1
                p: float = random.uniform(0, 1)

                if p > threshold:
                    # define the value that's going to get flipped
                    v1, v2 = (randrange(9) + 1), (randrange(9) + 1)
                    val_to_flip = int(str(v1) + str(v2))

                    # what does "flip it" mean? Just assign it a new value between 1 and 9?
                    board, new_value = self.flip_single_variable(board=board, val_to_flip=val_to_flip)
                    continue

                else:
                    # for each variable, see how the object changes if that variable gets flipped
                    board_copy = board.copy()
                    objective_val_dict = {}
                    initial_objective: int = self.is_legal(board_state=board)
                    for row in range(9):
                        row += 1
                        for col in range(9):
                            col += 1

                            # here we flip a variable and get the new objective score
                            val_to_flip: int = int(str(row) + str(col))

                            # get the new board with a new value
                            new_board, new_value = self.flip_single_variable(board=board, val_to_flip=val_to_flip)

                            # score the new board with our objective function
                            new_objective: int = self.is_legal(board_state=new_board)

                            if self.verbose:
                                # suppress print statements
                                if j % 5 == 1:
                                    print(f'REMAINING BOARD VIOLATIONS: {new_objective}')

                            # find the difference between our initial objective and the new one & add it to the dict
                            objective_diff: int = new_objective - initial_objective
                            objective_val_dict[new_value] = objective_diff

                            # we need to remember to reset the board after each change we make to it
                            board = board_copy  # <-- we may not need this if we are just creating new boards every time

                    # now we find the change that maximized the objective (or minimized the cost function)
                    # instead of picking the first min value (argmin) we choose a random min value
                    min_move_val = min(objective_val_dict.items(), key=lambda x: x[1])[1]
                    best_moves = []
                    # Iterate over all the values in dictionary to find moves with max value
                    for key, value in objective_val_dict.items():
                        if value == min_move_val:
                            best_moves.append(key)

                    # now we can make the move and continue with our search
                    new_value = random.choice(best_moves)
                    old_value = self.get_val_from_position(b=board, search_index=int(str(new_value)[0] + str(new_value)[1]))
                    board = self.update_board_value(b1=board, old_value=old_value, new_value=new_value)

        return f'Could not find a solution after {max_tries} tries and {max_flips} flips.'

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
              threshold=0.3, max_tries=100_000, max_flips=1000, verbose=False, solution=sol)

    sat.create_initial_assignment()

    sat.is_assignment_legal()

    print('something')
