from MazeworldProblem import MazeworldProblem
from Maze import Maze
from SensorlessProblem import SensorlessProblem, sensorless_astar_search


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(current_state, goal_state):
    """
    Simply returns 0 - this is a placeholder function that allows us to test A* as if it was Uniform Cost search
    :param current_state:
    :param goal_state:
    :return:
    """
    return 0


def sensorless_heuristic(current_state):
    """
    This is the heuristic function for the sensorless problem. This problem is focused on eliminating (X,Y) coordinate
    pairs from our state sets and fewer states are preferred. Therefore our heuristic is calculated by simply
    returning the number of currently available (X,Y) spaces still available in the state space. The more spaces
    available, the more costly the move.

    :param current_state: tuple of unique, 2-length tuples ((X1, Y1), (X2, Y2), ...)
    :return: number of (X,Y) coordinates in the outer tuple
    """
    # return the number of tuples (X,Y spaces) still available in the complete state space.
    return len(current_state)


# * SENSORLESS SEARCH *
test_maze3 = Maze("mazes/sensorless_maze2.maz")
test_problem = SensorlessProblem(test_maze3)
start_state = test_problem.generate_initial_state(maze=test_maze3)
all_successors = test_problem.get_successors_sensorless(start_state)
print(f'ALL SUCCESSORS: {all_successors}')
for state in all_successors:
    print(state)

path: list = sensorless_astar_search(search_problem=test_problem, heuristic_fn=sensorless_heuristic)
print(f'SOLUTION PATH LENGTH: {len(path)}')

