from MazeworldProblem import MazeworldProblem
from Maze import Maze

import os

from uninformed_search import bfs_search
from astar_search import astar_search, uniform_cost_search


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic():
    return 0


def manhattan_heuristic(current_state, goal_state):
    """
    Function to return the manhattan distance (X1 - X2) + (Y1 - Y2) given two points [X1, Y1] and [X2, Y2]
    :param current_state:
    :param goal_state:
    :return:
    """
    x1 = current_state[0]
    y1 = current_state[1]
    x2 = goal_state[0]
    y2 = goal_state[1]

    return (x1 - x2) + (y1 - y2)


# Test problems
# maze_test = Maze("mazes/maze_test3.maz")
# test_maze_problem = MazeworldProblem(maze_test, goal_locations=(32, 9), start_states=(0, 0))

# maze_test = Maze("mazes/maze_test2.maz")
# test_maze_problem = MazeworldProblem(maze_test, goal_locations=(28, 8), start_states=(0, 0))

maze_test = Maze("mazes/maze_test.maz")
test_maze_problem = MazeworldProblem(maze_test, goal_locations=(16, 3), start_states=(0, 0))

# print(test_maze_problem)

# path: list = bfs_search(search_problem=test_maze_problem)
path: list = uniform_cost_search(search_problem=test_maze_problem, heuristic_fn=manhattan_heuristic)

test_maze_problem.print_path(path=path)

# test_maze_problem.animate_path(path=path)







# # test_mp = MazeworldProblem(test_maze3, goal_locations=(1, 4, 1, 3, 1, 2), start_states=(0, 0))
#
# print(test_maze_problem.get_successors(test_maze_problem.start_state))
#
# # this should explore a lot of nodes; it's just uniform-cost search
# result = astar_search(test_maze_problem, null_heuristic)
# print(result)
#
# # this should do a bit better:
# result = astar_search(test_maze_problem, test_maze_problem.manhattan_heuristic)
# print(result)
# test_maze_problem.animate_path(result.path)
#
# # Your additional tests here:
