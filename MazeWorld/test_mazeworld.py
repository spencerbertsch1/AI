from MazeworldProblem import MazeworldProblem
from Maze import Maze

from uninformed_search import bfs_search
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test problems

maze_test = Maze("maze_test.maz")
test_maze_problem = MazeworldProblem(maze_test, goal_locations=(16, 3), start_states=(0, 0))

print(bfs_search(search_problem=test_maze_problem))

# test_mp = MazeworldProblem(test_maze3, goal_locations=(1, 4, 1, 3, 1, 2), start_states=(0, 0))

print(test_maze_problem.get_successors(test_maze_problem.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_maze_problem, null_heuristic)
print(result)

# this should do a bit better:
result = astar_search(test_maze_problem, test_maze_problem.manhattan_heuristic)
print(result)
test_maze_problem.animate_path(result.path)

# Your additional tests here:
