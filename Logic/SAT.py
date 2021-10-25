# Spencer Bertsch
# October 2021
# Assignment 5
# CS 276 @ Dartmouth College

from pathlib import Path
import random
from random import randrange


from Sudoku import Sudoku


class SAT(Sudoku):

    def __init__(self, path_to_puzzle: str, path_to_sol: str, threshold: float, iterations: int, verbose: bool):
        super().__init__()
        self.path_to_puzzle = path_to_puzzle
        self.path_to_sol = path_to_sol
        self.threshold = threshold
        self.iterations = iterations
        self.verbose = verbose
        self.puzzle = self.import_cnf()


    def import_cnf(self):
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


    def write_solution(self, sol_filename: str):
        pass
        # TODO method to write the solved puzzle to the specified output location

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

    def is_legal(self, puzzle) -> bool:
        board_state: list = self.get_board_state_from_cnf(puzzle=puzzle)

        # make sure the 9x9 squares don't have any repeating numbers
        # TODO

        print('something')
        return True

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
                if self.verbose:
                    print(f'ROW: {row}, COL: {col}')

                # if the board doesn't already have an assignment for [row, col], add a random one
                position_exists = False
                for position in board_state:
                    # check through the current row/col and see if we have any positions in that row/col
                    if (int(str(position)[0]) == row) & (int(str(position)[1]) == col):
                        position_exists = True

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




    def generate_truth_assignment(self) -> bool:

        return True


    def walksat(self):
        # TODO
        pass


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

    # instantiate the SAT object
    sat = SAT(path_to_puzzle=str(ABSPATH_TO_CNF), path_to_sol=str(ABSPATH_TO_SOL),
              threshold=0.3, iterations=100_000, verbose=False)

    new_board = sat.randomly_fill_board(puzzle=sat.puzzle)
    print(new_board)
