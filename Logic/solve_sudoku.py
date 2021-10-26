# Spencer Bertsch
# October 2021
# Assignment 5
# CS 276 @ Dartmouth College

from Logic.display import display_sudoku_solution
import random, sys
from pathlib import Path
from SAT import SAT, Solution

# define paths to files
PATH_TO_THIS_FILE: Path = Path(__file__).resolve()
ABSPATH_TO_CNF_DIR: Path = PATH_TO_THIS_FILE.parent / 'puzzles'


def solve(puzzle_name: str):
    # for testing, always initialize the pseudorandom number generator to output the same sequence of values:
    random.seed(1)

    # create an instance of the SAT object
    sol_filename = puzzle_name + ".sol"
    cnf_name = puzzle_name + ".cnf"
    ABSPATH_TO_CNF: Path = ABSPATH_TO_CNF_DIR / cnf_name
    ABSPATH_TO_SOL: Path = ABSPATH_TO_CNF_DIR / sol_filename

    # instantiate an empty solution object that will get updated during search
    sol = Solution()

    # instantiate the SAT object
    sat = SAT(path_to_puzzle=str(ABSPATH_TO_CNF), path_to_sol=str(ABSPATH_TO_SOL),
              threshold=0.3, max_tries=100_000, max_flips=1000, verbose=False, solution=sol)

    # run the walksat algorithm on the puzzle
    result = sat.walksat()

    if result:
        print(f'Walksat Successful! Writing solved {puzzle_name} to the following location: \n {sol_filename}')
        sat.write_solution()
        display_sudoku_solution(sol_filename)


if __name__ == "__main__":
    puzzle_name = 'puzzle2'
    solve(puzzle_name=puzzle_name)


