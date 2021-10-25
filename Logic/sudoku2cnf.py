# Spencer Bertsch
# October 2021
# Assignment 5
# CS 276 @ Dartmouth College

from Sudoku import Sudoku
import sys

if __name__ == "__main__":
    """
    Script to take a .sud file and generate a .cnf file that the SAT class can solve 
    """
    test_sudoku = Sudoku()

    test_sudoku.load(sys.argv[1])
    print(test_sudoku)

    puzzle_name = sys.argv[1][:-4]
    cnf_filename = puzzle_name + ".cnf"

    test_sudoku.generate_cnf(cnf_filename)
    print("Output file: " + cnf_filename)

