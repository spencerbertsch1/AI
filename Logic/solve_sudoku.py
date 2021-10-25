# Spencer Bertsch
# October 2021
# Assignment 5
# CS 276 @ Dartmouth College

from Logic.display import display_sudoku_solution
import random, sys
from pathlib import Path
from SAT import SAT

# define paths to files
PATH_TO_THIS_FILE: Path = Path(__file__).resolve()
ABSPATH_TO_CNF_DIR: Path = PATH_TO_THIS_FILE.parent / 'puzzles'


def solve(puzzle_name: str):
    # for testing, always initialize the pseudorandom number generator to output the same sequence of values:
    random.seed(1)

    # define the name of the solution file that we will write once the solver is finished
    sol_filename = puzzle_name + ".sol"

    # create an instance of the SAT object
    cnf_name = puzzle_name + ".cnf"
    ABSPATH_TO_CNF: Path = ABSPATH_TO_CNF_DIR / cnf_name

    # instantiate the SAT object
    sat = SAT(path_to_puzzle=str(ABSPATH_TO_CNF), threshold=0.3, iterations=100_000, verbose=False)

    # test is_legal()
    sat.is_legal(puzzle=sat.puzzle)

    # run the walksat algorithm on the puzzle
    result = sat.walksat()

    if result:
        print(f'Walksat Successful! Writing solved {puzzle_name} to the following location: \n {sol_filename}')
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)


if __name__ == "__main__":
    puzzle_name = 'puzzle2'
    solve(puzzle_name=puzzle_name)


