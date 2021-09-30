from Maze import Maze
from time import sleep
from heapq import heappush, heappop, heapify
from astar_search import backchain, get_states_from_frontier
from SearchSolution import SearchSolution


class SensorlessAStarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0, path_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost
        self.path_cost = path_cost

    def goal_test(self) -> bool:
        if len(self.state) == 1:
            return True
        else:
            return False

    def priority(self):
        return self.path_cost + self.heuristic

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# use the sensorless AStarNode
def sensorless_astar_search(search_problem, heuristic_fn):

    # TODO
    # create a long tuple (...) from the set of tuples {(...), (...), ...} that's returned by the
    # sensorless_get_successors function

    # define the starting node as an AStarNode
    start_node = SensorlessAStarNode(state=search_problem.start_states,
                                     heuristic=heuristic_fn(current_state=search_problem.start_states,
                                                  goal_state=search_problem.goal_states))
    frontier = []  # <-- priority queue ordered by path cost, for us it is a heap.
    heappush(frontier, start_node)
    # our frontier needs to be a heap, so we can use heapify here to transform it
    heapify(frontier)
    explored = set()  # <-- we could also remove the explored set and just reference the keys in the visited_cost dict

    # define a solution object that we will modify as we search
    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    # we would usually use a heap for this, but we can just use a dict as it's laid out in the assignment
    visited_cost: dict = {}
    visited_cost[start_node.state] = 0

    while len(frontier) != 0:
        current_node = heappop(frontier)

        # test to see if we're at the solution
        if current_node.goal_test:
            solution_path: list = backchain(node=current_node)
            print(f'Solution found! Path to solution: {solution_path}')
            solution.solved = True
            return solution_path

        explored.add(current_node.state)

        for child_state in search_problem.get_successors(states=current_node.state, search_problem=search_problem):
            # we now need to create a new node!
            transition_cost = 1
            new_node = SensorlessAStarNode(state=child_state,
                                           parent=current_node,
                                           heuristic=heuristic_fn(current_state=child_state,
                                                                  goal_state=search_problem.goal_states),
                                           transition_cost=transition_cost,
                                           path_cost=current_node.path_cost + transition_cost)
            visited_cost[new_node.state] = new_node.path_cost

            frontier_states = get_states_from_frontier(frontier=frontier)
            if (new_node.state not in explored) & (new_node.state not in frontier_states):
                # if the new child node is not the solution, we add it to the frontier for further exploring
                heappush(frontier, new_node)

            # elif the new state is in the frontier and the node in the frontier has a cheaper path cost, swap them
            elif (new_node.state in frontier_states) & (visited_cost[new_node.state] > new_node.path_cost):
                # update the visited_cost dict to represent the new, cheaper path_cost
                visited_cost[new_node.state] = new_node.path_cost
                # and add the node to the frontier
                heappush(frontier, new_node)

    print('no solution found.')
    return False

class SensorlessProblem:

    ## You write the good stuff here:
    # TODO should we include start state or goal here? We don't know either if I'm correct...
    def __init__(self, maze, start_state):
        self.maze = maze
        self.width = self.maze.width
        self.height = self.maze.height
        self.start_state = start_state

    def __str__(self):
        string = "Blind robot problem: "
        print(self.maze)
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def generate_initial_state(self):
        # create a list of all the possible states in the entire maze
        state = []
        for i in range(self.width):
            for j in range(self.height):
                tuple_to_add: tuple = (i, j)
                state.append(tuple_to_add)

        # remove all the illegal states
        legal_states = self.get_legal_states(state_list=state)

        # convert to a set and return
        s = set(legal_states)
        return s

    def get_legal_states(self, state_list: list) -> list:
        legal_states: list = []
        # given a list of states, remove the illegal ones
        for state in state_list:
            # run checks to ensure the possible move is floor and not covered by another robot
            if self.maze.is_floor(x=state[0], y=state[1]):
                if not self.maze.has_robot(x=state[0], y=state[1]):
                    legal_states.append(state)

        return legal_states

    def heuristic(self):
        return 0

    def max_distance(self):
        pass

    def get_successors(self, states):
        all_successors: set = set()
        for state in states:
            successors: list = [(state[0]+1, state[1]), (state[0]-1, state[1]), (state[0], state[1]+1),
                                    (state[0], state[1]-1), (state[0], state[1])]
            legal_successors: list = self.get_legal_states(state_list=successors)
            all_successors.update(legal_successors)

        return all_successors


    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))


## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("mazes/maze2.maz")
    test_problem = SensorlessProblem(test_maze3, start_state=(1, 0))
    # start_state = test_problem.generate_initial_state()
    # all_successors = test_problem.get_successors(start_state)

    path: list = sensorless_astar_search(search_problem=test_problem, heuristic_fn=test_problem.heuristic)
    print(f'SOLUTION PATH LENGTH: {len(path)}')

    # print(all_successors)
