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

    def get_path_cost(self):
        # TODO how do we get the path cost from an AStarNode? We need it! Can we use backchain?
        pass

    def priority(self):
        # TODO should we backchoin here and sum the costs for all the transitions to get path cost?
        return self.path_cost

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


def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AStarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0

    # you write the rest:


def get_states_from_frontier(frontier):
    states = [x.state for x in frontier]
    print(f'States currently in the frontier: {states}')
    return states

def uniform_cost_search(search_problem, heuristic_fn):
    # define the starting node as an AStarNode
    start_node = AStarNode(state=search_problem.start_state, heuristic=heuristic_fn())
    frontier = []  # <-- priority queue ordered by path cost, for us it is a heap.
    heappush(frontier, start_node)
    # our frontier needs to be a heap, so we can use heapify here to transform it
    heapify(frontier)
    explored = set()

    # we would usually use a heap for this, but we can just use a dict as it's laid out in the assignment
    visited_cost: dict = {}
    visited_cost[start_node.state] = 0

    while len(frontier) != 0:
        # TODO how does this know what the minimum node is?? What metric is it using here?
        current_node = heappop(frontier)

        # test to see if we're at the solution
        if current_node.state == search_problem.goal_state:
            solution_path: list = backchain(node=current_node)
            solution_path.reverse()
            print(f'Solution found! Path to solution: {solution_path}')
            return solution_path  # <-- optionally we can return the solution path here

        explored.add(current_node.state)

        for child_state in search_problem.get_successors(state=current_node.state):
            # we now need to create a new node!
            new_node = AStarNode(state=child_state,
                                 parent=current_node,
                                 heuristic=heuristic_fn(),
                                 transition_cost=1,
                                 path_cost=len(backchain(current_node)))  # TODO <-- is this right?? Should path_cost be an instance variable for AStarNode?
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
