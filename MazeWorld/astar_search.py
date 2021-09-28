from SearchSolution import SearchSolution
from heapq import heappush, heappop, heapify


class AStarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0, path_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost
        self.path_cost = path_cost

    def priority(self):
        return self.path_cost + self.heuristic

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search_old(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AStarNode(search_problem.start_states, heuristic_fn(search_problem.start_states))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0

    # you write the rest:


def get_states_from_frontier(frontier) -> list:
    """
    Small helper function that returns a list of states (tuples) given a frontier heap
    :param frontier:
    :return:
    """
    return [x.state for x in frontier]


def astar_search(search_problem, heuristic_fn):
    # we are given a tuple with start states, we need to add robot_turn to the beginning
    start_states: list = [x for x in search_problem.start_states]
    start_states.insert(0, 0)  # <-- insert 0 at the beginning of the tuple
    s_states = tuple(start_states)

    # define the starting node as an AStarNode
    start_node = AStarNode(state=s_states,
                           heuristic=heuristic_fn(current_state=s_states,
                                                  goal_state=search_problem.goal_states))
    frontier = []  # <-- priority queue ordered by path cost, for us it is a heap.
    heappush(frontier, start_node)
    # our frontier needs to be a heap, so we can use heapify here to transform it
    heapify(frontier)  # <-- TODO replace the explored set all together with the visited_cost dict
    explored = set()

    # define a solution object that we will modify as we search
    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    # we would usually use a heap for this, but we can just use a dict as it's laid out in the assignment
    visited_cost: dict = {}
    visited_cost[start_node.state] = 0

    while len(frontier) != 0:
        current_node = heappop(frontier)

        # test to see if we're at the solution
        if list(current_node.state)[1:] == list(search_problem.goal_states):
            solution_path: list = backchain(node=current_node)
            print(f'Solution found! Path to solution: {solution_path}')
            solution.solved = True
            return solution_path

        explored.add(current_node.state)

        for child_state in search_problem.get_successors(states=current_node.state, search_problem=search_problem):
            # define transition cost
            transition_cost = 1
            if list(child_state)[1:] == list(current_node.state)[1:]:
                transition_cost = 0  # <-- if we stay in the same place, we don't use any gas

            # we now need to create a new node!
            new_node = AStarNode(state=child_state,
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
