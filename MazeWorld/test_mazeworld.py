from MazeworldProblem import MazeworldProblem
from Maze import Maze
import math

import os

from uninformed_search import bfs_search
from astar_search import astar_search


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(current_state, goal_state):
    return 0


def manhattan_heuristic(current_state, goal_state):
    """
    Function to return the manhattan distance (X1 - X2) + (Y1 - Y2) given two points [X1, Y1] and [X2, Y2]
    :param current_state:
    :param goal_state:
    :return:
    """
    # TODO once this working, clean this up so it's only 3 lines (one line per if/else)
    if len(current_state) == 3:
        x1 = current_state[1]
        y1 = current_state[2]
        x2 = goal_state[0]
        y2 = goal_state[1]

        return abs(x1 - x2) + abs(y1 - y2)

    elif len(current_state) == 5:
        x1 = current_state[1]
        y1 = current_state[2]
        x2 = goal_state[0]
        y2 = goal_state[1]

        x3 = current_state[3]
        y3 = current_state[4]
        x4 = goal_state[2]
        y4 = goal_state[3]

        return ((abs(x1 - x2) + abs(y1 - y2)) + (abs(x3 - x4) + abs(y3 - y4)))/2

    elif len(current_state) == 7:
        x1 = current_state[1]
        y1 = current_state[2]
        x2 = goal_state[0]
        y2 = goal_state[1]

        x3 = current_state[3]
        y3 = current_state[4]
        x4 = goal_state[2]
        y4 = goal_state[3]

        x5 = current_state[5]
        y5 = current_state[6]
        x6 = goal_state[4]
        y6 = goal_state[5]

        return ((abs(x1 - x2) + abs(y1 - y2)) + (abs(x3 - x4) + abs(y3 - y4)) + (abs(x5 - x6) + abs(y5 - y6)))/3


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

maze_test = Maze("mazes/maze3.maz")
print(maze_test)
test_maze_problem = MazeworldProblem(maze_test, goal_locations=(1,2,1,3,1,4), start_states=(1,0,1,1,2,1))

# uncomment the next line to test BFS Search
# path: list = bfs_search(search_problem=test_maze_problem)

# uncomment the next line to test the A* Search
path: list = astar_search(search_problem=test_maze_problem, heuristic_fn=null_heuristic)

# uncomment the next line to print the animated path that was found using the search method above
test_maze_problem.animate_path(path=path)


# * multi robot test *
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
