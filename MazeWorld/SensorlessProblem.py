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
        """
        This is the updated sensorless_goal_test that checks to see if any of the sets in the list only contain a
        single entry.

        Remember that the states in this case are sets of tuples and get_successors returns a list of sets that
        each contain many 2-length state tuples. This function simply takes a set and determines if its length is
        1. If so, it returns true. It returns False otherwise.

        :return: bool - True if the input state is of length 1, False otherwise
        """
        if len(self.state) == 1:
            return True
        else:
            return False

    def priority(self):
        # TODO experiment with this by removing path_cost, might be interesting...
        return self.heuristic + self.path_cost

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# use the sensorless AStarNode
def sensorless_astar_search(search_problem, heuristic_fn):
    """
    A* for the sensorless problem.

    One big change between this construction and the A* that was made for the multirobot search is that we only have
    one robot, and therefore one tuple of even length that represents the state.

    :param search_problem:
    :param heuristic_fn:
    :return:
    """

    # define the starting node as an AStarNode
    start_node = SensorlessAStarNode(state=search_problem.start_state,
                                     heuristic=heuristic_fn(current_state=search_problem.start_state))
    frontier = []  # <-- priority queue ordered by path cost, for us it is a heap.
    heappush(frontier, start_node)
    # our frontier needs to be a heap, so we can use heapify here to transform it
    heapify(frontier)
    explored = set()  # <-- we could also remove the explored set and just reference the keys in the visited_cost dict

    # define a solution object that we will modify as we search
    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    # we would usually use a heap for this, but we can just use a dict as it's laid out in the assignment
    visited_cost: dict = {}
    start_state_tuple = tuple(start_node.state)
    visited_cost[start_state_tuple] = 0

    while len(frontier) != 0:
        current_node = heappop(frontier)

        # test to see if we're at the solution
        if current_node.goal_test():
            solution_path: list = backchain(node=current_node)
            print(f'Solution found! Path to solution: {solution_path}')
            solution.solved = True
            return solution_path

        explored.add(tuple(current_node.state))

        # add check so we make sure we don't iterate through a single tuple of 2 ints
        # This should never happen because we do the goal check above !
        # state_to_search = current_node.state
        # if isinstance(state_to_search, tuple):
        #     print('converting state to set of a single tuple.')
        #     s = set()
        #     s.add(state_to_search)
        #     state_to_search = s
        state_to_search = tuple(current_node.state)

        for child_state in search_problem.get_successors_sensorless(states=state_to_search):
            # we now need to create a new node!
            transition_cost = 1
            new_node = SensorlessAStarNode(state=child_state,
                                           parent=current_node,
                                           heuristic=heuristic_fn(current_state=child_state),
                                           transition_cost=transition_cost,
                                           path_cost=current_node.path_cost + transition_cost)
            tuple_to_add = tuple(new_node.state)
            print(f'ADDING {tuple_to_add} to visited dict!')
            visited_cost[tuple_to_add] = new_node.path_cost

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
    def __init__(self, maze):
        self.maze = maze
        self.width = self.maze.width
        self.height = self.maze.height
        self.start_state = self.generate_initial_state(maze)

    def __str__(self):
        string = "Blind robot problem: "
        # print(self.maze)
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def generate_initial_state(self, maze):
        # create a list of all the possible states in the entire maze
        state = []
        for i in range(maze.width):
            for j in range(maze.height):
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

    def max_distance(self):
        pass

        # north_successors: set = set()
        # for state in states:
        #     print(f'GETTING NORTH SUCCESSOR FOR: {state}')
        #     successors: list = [(state[0]+1, state[1]), (state[0]-1, state[1]), (state[0], state[1]+1),
        #                         (state[0], state[1]-1), (state[0], state[1])]
        #     legal_successors: list = self.get_legal_states(state_list=successors)
        #     all_successors.update(legal_successors)


    def get_successors_sensorless(self, states):
        """

        :param states:
        :return:
        """
        # GET SUCCESSORS
        north_successors: set = set()
        east_successors: set = set()
        south_successors: set = set()
        west_successors: set = set()
        for state in states:
            print(f'GETTING NORTH SUCCESSOR FOR: {state}')
            north_successor: list = [(state[0], state[1]+1)]
            legal_north_successor: list = self.get_legal_states(state_list=north_successor)
            north_successors.update(legal_north_successor)

            print(f'GETTING EAST SUCCESSOR FOR: {state}')
            east_successor: list = [(state[0]+1, state[1])]
            legal_east_successor: list = self.get_legal_states(state_list=east_successor)
            east_successors.update(legal_east_successor)

            print(f'GETTING SOUTH SUCCESSOR FOR: {state}')
            south_successor: list = [(state[0], state[1]-1)]
            legal_south_successor: list = self.get_legal_states(state_list=south_successor)
            south_successors.update(legal_south_successor)

            print(f'GETTING WEST SUCCESSOR FOR: {state}')
            west_successor: list = [(state[0]-1, state[1])]
            legal_west_successor: list = self.get_legal_states(state_list=west_successor)
            west_successors.update(legal_west_successor)

        # generate a list of 4 tuples (N, E, S, W), each of which contain the (X,Y) coordinates of those moves!
        n_successors: tuple = tuple(north_successors)
        e_successors: tuple = tuple(east_successors)
        s_successors: tuple = tuple(south_successors)
        w_successors: tuple = tuple(west_successors)
        return [n_successors, e_successors, s_successors, w_successors]


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
    test_problem = SensorlessProblem(test_maze3)
    start_state = test_problem.generate_initial_state(maze=test_maze3)
    all_successors = test_problem.get_successors_sensorless(start_state)
    for successor in all_successors:
        print(successor)

    # path: list = sensorless_astar_search(search_problem=test_problem, heuristic_fn=test_problem.heuristic)
    # print(f'SOLUTION PATH LENGTH: {len(path)}')

    # print(all_successors)
