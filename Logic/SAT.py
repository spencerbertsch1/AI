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
        # self.puzzle = self.import_cnf()
        self.solution = solution


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


    @ staticmethod
    def get_board_state_from_cnf(puzzle):
        """
        Helper function that returns a list of 3 digit integers representing the current board state from
        a starting CNF file.

        The list might be [115, 127], indicating a 5 in the [1,1] position, and a 7 in the [1,2] position
        :param puzzle:
        :return:
        """
        puzzle.reverse()
        # get the current state of the board (what numbers have already been assigned)
        current_positions = []
        for position in puzzle:
            if len(position) < 5:
                current_positions.append(int(position))
            else:
                break

        return current_positions

    def is_legal(self, board_state: list) -> int:
        """
        The function find the number of illegal board states and returns that number. If the board is completely
        legal, it returns a 0.

        If the board is illegal by only 2 positions, then a change is made the board is illegal by 4 positions
        then we know that was a bad change. Our hope is that as we make changes, or "flips" as they're called
        in the Walksat pseudocode, this function will return smaller and smaller numbers until we reach 0.

        :param board_state:
        :return:
        """
        assert(len(board_state) == 81), f'Please only call \'is_legal()\' on complete boards!'

        violations: int = 0

        # ----- STEP 1 ----- make sure the rows don't have any repeating values
        for row in range(9):
            row += 1
            values_in_row = []
            for col in range(9):
                col += 1
                # get the value of the current position
                for position in board_state:
                    if (int(str(position)[0]) == row) & (int(str(position)[1]) == col):
                        # get the value from the current position
                        value = int(str(position)[2])
                        values_in_row.append(value)

            # now we can just find the difference between 9 and the num_unique values in the row
            v = 9 - len(set(values_in_row))
            violations = violations + v

        # ----- STEP 2 ----- make sure the columns dont have any repeating values
        for col in range(9):
            col += 1
            values_in_col = []
            for row in range(9):
                row += 1
                # get the value of the current position
                for position in board_state:
                    if (int(str(position)[0]) == row) & (int(str(position)[1]) == col):
                        # get the value from the current position
                        value = int(str(position)[2])
                        values_in_col.append(value)

            # now we can just find the difference between 9 and the num_unique values in the row
            v = 9 - len(set(values_in_col))
            violations = violations + v

        # ----- STEP 3 ----- make sure the 9x9 squares don't have any repeating numbers
        # search each sub-block
        i = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for block_i in i:
            for block_j in i:

                # here we will store the values for each sub_block
                values_in_sub_block = []

                # we can now iterate through each sub-block and find any violations
                for row in block_i:
                    for col in block_j:
                        for position in board_state:
                            if (int(str(position)[0]) == row) & (int(str(position)[1]) == col):
                                # get the value from the current position
                                value = int(str(position)[2])
                                values_in_sub_block.append(value)

                # now we can just find the difference between 9 and the num_unique values in the row
                v = 9 - len(set(values_in_sub_block))
                violations = violations + v

        return violations

    def randomly_fill_board(self, puzzle):
        """
        Take an incomplete board and fill the missing spaces with random values between 1 and 9

        :param puzzle: unfinished puzzle (list of ints of length < 81)
        :return: filled puzzle (list of ints of length 81)
        """
        # generate the initial board state from the cnf file
        board_state: list = self.get_board_state_from_cnf(puzzle=puzzle)

        for row in range(9):
            row += 1
            for col in range(9):
                col += 1
                # if the board doesn't already have an assignment for [row, col], add a random one
                position_exists = False
                for position in board_state:
                    # check through the current row/col and see if we have any positions in that row/col
                    if (int(str(position)[0]) == row) & (int(str(position)[1]) == col):
                        position_exists = True

                # TODO fix initialization!!!
                # now we have all the positions in the row, let's filter those to make sure we're in the right col
                if position_exists:
                    pass
                else:
                    # if we don't have the position filled yet, we will it with a random int between 1 and 9
                    random_entry: int = randrange(9)
                    random_entry += 1
                    new_position = int(str(row) + str(col) + str(random_entry))

                    # add the random entry to the board state
                    board_state.append(new_position)

        return board_state

    @ staticmethod
    def update_board_value(b1: list, old_value: int, new_value: int) -> list:
        """
        Helper function to update a single value on the board given a board (list of ints), an old_value
        (int representing row, col, old_val), and a new_value (int representing row, col, new_val)

        :param board:
        :param old_value:
        :param new_value:
        :return:
        """
        b1.remove(old_value)
        b1.append(new_value)
        return b1

    def get_val_from_position(self, b, search_index: int):
        """
        Takes a board search_index (an int with 2 digits representing row and col) and returns the value at that
        position (an int with 3 digits representing row, col, value)

        :param search_index: int with 2 digits representing position
        :return: int with 3 digits representing position and value
        """
        current_val = 0
        for position in b:
            if (int(str(position)[0]) == (int(str(search_index)[0]))) & \
                    (int(str(position)[1]) == (int(str(search_index)[1]))):
                current_val = (int(str(search_index)[0] + str(search_index)[1] + str(position)[2]))
                break

        return current_val

    def flip_single_variable(self, board: list, val_to_flip: int) -> (list, int):

        # TODO maybe we need to pass in a variable so this isn't quite as random? Not sure...
        b1 = board.copy()
        v1 = val_to_flip

        # we don't want to accidentally flip the value to the same value, so we can add a check for that
        current_val = self.get_val_from_position(b=b1, search_index=val_to_flip)
        current_val = int(str(current_val)[2])

        potential_values = [x+1 for x in range(9)]
        potential_values.remove(current_val)
        new_val = random.choice(potential_values)

        # now that we have a new value, we can update and return our board
        old_value = int(str(val_to_flip) + str(current_val))
        new_value = int(str(val_to_flip) + str(new_val))
        updated_board = self.update_board_value(b1=b1, old_value=old_value, new_value=new_value)

        return updated_board, new_value

    def gsat(self):
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
              threshold=0.3, max_tries=100_000, max_flips=1000, verbose=True, solution=sol)

    sat.create_initial_assignment()
