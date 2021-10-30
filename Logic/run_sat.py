# Spencer Bertsch
# October 2021
# Assignment 5
# CS 276 @ Dartmouth College

from pathlib import Path
import random
from random import randrange

from display import display_sudoku_solution
from SAT import Solution, SAT

def run_sat(write_solution: bool, algorithm: str, threshold: float, max_tries: int, max_flips: int, puzzle_name: str,
            problem_type: str = 'sudoku'):
    """
    run_sat is a driver function that gives us an easy way to run the WalkSAT and GSAT
    algorithms on different puzzle CNF files.

    :param write_solution: bool - True if you want to write the assignment to a .sol file in the solutions directory
    :param algorithm: str - the algorithm you want to solver to use (GSAT or WalkSAT)
    :param threshold: float - the (p) value that is used to randomly walk as the algorithm searches
    :param max_tries: int - number of total tries the algorithm uses for each run
    :param max_flips: int - the maximum number of flips used in each search before a new try is initiated
    :param puzzle_name: str - the name of the puzzle CNF file that you want to solve. 'puzzle1' for example
    :param problem_type: str - either 'sudoku' or 'map_coloring', tells the solver what problem to solve
    :return:
    """
    # for testing, always initialize the pseudorandom number generator to output the same sequence of values:
    random.seed(2)
    # define paths to files
    PATH_TO_THIS_FILE: Path = Path(__file__).resolve()
    ABSPATH_TO_CNF_DIR: Path = PATH_TO_THIS_FILE.parent / 'puzzles'
    ABSPATH_TO_SOL_DIR: Path = PATH_TO_THIS_FILE.parent / 'solutions'
    # define the name of the solution file that we will write once the solver is finished
    sol_filename = puzzle_name + ".sol"
    cnf_name = puzzle_name + ".cnf"
    ABSPATH_TO_CNF: Path = ABSPATH_TO_CNF_DIR / cnf_name
    ABSPATH_TO_SOL: Path = ABSPATH_TO_SOL_DIR / sol_filename

    # instantiate an empty solution object that will get updated during search
    sol = Solution(algorithm=algorithm)

    # instantiate the SAT object
    sat = SAT(path_to_puzzle=str(ABSPATH_TO_CNF), path_to_sol=str(ABSPATH_TO_SOL),
              threshold=threshold, max_tries=max_tries, max_flips=max_flips, verbose=True, solution=sol,
              random_initialization=True, problem_type=problem_type)

    # run the solver on the chosen puzzle and return the result
    if algorithm == 'walksat':
        s = sat.walksat()
        print(s)
    elif algorithm == 'gsat':
        s = sat.gsat()
        print(s)
    else:
        raise Exception(f'The \'algorithm\' parameter should be either \'walksat\' or \'gsat\', not {algorithm}.')

    if write_solution:
        # write and display the solution file
        sat.write_solution()
        display_sudoku_solution(str(ABSPATH_TO_SOL))


if __name__ == "__main__":
    # --- Choose parameters to test the solver --- #
    algorithm: str = 'walksat'  # <-- 'gsat' or 'walksat'
    threshold: float = 0.85  # <-- 0.85 for walksat puzzle1, 0.8 for walksat puzzle2, 0.9 for all others
    max_tries: int = 100_000
    max_flips: int = 100_000
    puzzle_name: str = 'puzzle1'  # <-- try 'puzzle1' or 'puzzle2'/ 'map_coloring' for map coloring problems
    write_solution: bool = False
    problem_type: str = 'sudoku'  # <-- 'sudoku' or 'map_coloring'

    # run the solver on the chosen puzzle
    run_sat(algorithm=algorithm, threshold=threshold, max_tries=max_tries, max_flips=max_flips,
            puzzle_name=puzzle_name, write_solution=write_solution, problem_type=problem_type)
