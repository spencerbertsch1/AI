from MazeworldProblem import MazeworldProblem
from Maze import Maze
from SensorlessProblem import SensorlessProblem
import math

import os

from uninformed_search import bfs_search
from astar_search import astar_search


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(current_state, goal_state):
    return 0

# * SENSORLESS SEARCH *
test_maze3 = Maze("mazes/maze2.maz")
test_problem = SensorlessProblem(test_maze3, start_state=(1, 0))
start_state = test_problem.generate_initial_state()
all_successors = test_problem.get_successors(start_state)
print(all_successors)

# uncomment the next line to test the A* Search
path: list = sensorless_astar_search(search_problem=test_problem, heuristic_fn=null_heuristic)
print(f'SOLUTION PATH LENGTH: {len(path)}')

# uncomment the next line to print the animated path that was found using the search method above
test_problem.animate_path(path=path)