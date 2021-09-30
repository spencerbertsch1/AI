from MazeworldProblem import MazeworldProblem
from Maze import Maze
from SensorlessProblem import SensorlessProblem, sensorless_astar_search


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(current_state, goal_state):
    return 0

# * SENSORLESS SEARCH *
test_maze3 = Maze("mazes/maze2.maz")
test_problem = SensorlessProblem(test_maze3)
start_state = test_problem.generate_initial_state(maze=test_maze3)
all_successors = test_problem.get_successors(start_state)

path: list = sensorless_astar_search(search_problem=test_problem, heuristic_fn=test_problem.heuristic)
print(f'SOLUTION PATH LENGTH: {len(path)}')

# print(all_successors)