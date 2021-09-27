from MazeworldProblem import MazeworldProblem
from Maze import Maze
import math

import os

from uninformed_search import bfs_search
from astar_search import astar_search


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


def euclidian_heuristic(current_state, goal_state):
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

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


# Test problems
# maze_test = Maze("mazes/maze_test3.maz")
# test_maze_problem = MazeworldProblem(maze_test, goal_locations=(32, 9), start_states=(0, 0))

# maze_test = Maze("mazes/maze_test2.maz")
# test_maze_problem = MazeworldProblem(maze_test, goal_locations=(28, 8), start_states=(0, 0))

maze_test = Maze("mazes/maze_test.maz")
test_maze_problem = MazeworldProblem(maze_test, goal_locations=(16, 3), start_states=(0, 0))

# uncomment the next line to test BFS Search
# path: list = bfs_search(search_problem=test_maze_problem)

# uncomment the next line to test the A* Search
path: list = astar_search(search_problem=test_maze_problem, heuristic_fn=manhattan_heuristic)

# uncomment the next line to print the animated path that was found using the search method above
test_maze_problem.print_path(path=path)



# maze_test = Maze("mazes/maze_test3.maz")
# test_mp = MazeworldProblem(maze_test, goal_locations=(1, 4, 1, 3, 1, 2), start_states=(0, 0))

# test_maze = Maze("mazes/multirobot_maze1.maz")
# test_mp = MazeworldProblem(test_maze, goal_locations=(0, 3, 3, 6, 6, 4), start_states=(0, 0, 1, 6, 4, 5))
#
# print(test_mp.get_successors((1, 6)))

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
