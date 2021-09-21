# Spencer Bertsch
# September 2021
# Code adapted from Assignment 1
# CS 276 @ Dartmouth College

from collections import deque
from SearchSolution import SearchSolution

# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes


def back_chaining(SearchNode, chain=None) -> list:
    """
    Function that takes a SearchNode object and returns a list of tuples representing all states from that node
    back to the starting point in the graph.

    :param SearchNode: object wrapper for a state in the graph. holds state and data such as parent, etc.
    :param chain: list of tuples representing the path from SearchNode's current state back to the stat node
    :return: list of tuples
    """

    # python doesn't like it when the default arg in a function is mutable, so we can do the following check
    if chain is None:
        chain = []

    # use recursion to create a list called chain which shows the path from the current node back to the starting node
    if SearchNode.state == SearchNode.starting_state:
        chain.append(SearchNode.state)
        return chain
    else:
        chain.append(SearchNode.state)
        return back_chaining(SearchNode.parent, chain=chain)


class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state: tuple, starting_state: tuple, parent=None):
        self.state = state
        self.starting_state = starting_state
        self.parent = parent

    # you might write other helper functions, too. For example,
    #  I like to separate out backchaining, and the dfs path checking functions


def bfs_search(search_problem) -> bool:

    print(f'BFS Search Initiated! Starting State: {search_problem.start_state}')
    # define the frontier as an empty FIFO queue
    frontier: deque = deque()
    # define the start node based on the starting state
    start_node = SearchNode(state=search_problem.start_state, starting_state=search_problem.start_state)
    # append the starting node to the frontier
    frontier.appendleft(start_node)

    # define the explored set and add the starting state to the new set
    explored: set = set()
    explored.add(search_problem.start_state)

    while len(frontier) != 0:
        # get the current node from the frontier and the current state from that node
        current_node = frontier.pop()
        current_state = current_node.state

        # test to see if we have found the solution
        if current_state == search_problem.goal_state:
            solution_path: list = back_chaining(SearchNode=current_node)
            solution_path.reverse()
            print(f'Solution found! Path to solution: {solution_path}')
            return True

        # goal not found, so we need to search the children of the current node.
        for child_state in search_problem.get_successors(state=current_state):
            # if the child_node is new and unexplored
            if child_state not in explored:
                # add this state to the set of explored states
                explored.add(child_state)
                # we now need to create a new node! We pack the current_state into the node and point to the
                # current_node as the parent for the new node
                new_node = SearchNode(state=child_state,
                                      starting_state=search_problem.start_state,
                                      parent=current_node)
                # we now add the node to the frontier so it will get popped and used for continued searching
                frontier.appendleft(new_node)

    print(f'No solution found.')
    return False


def dfs_search(search_problem, depth_limit: int = 100, node=None, solution=None):
    # if no node object given, create a new search from starting state

    # Don't forget that your dfs function should be recursive and do path checking,
    #  rather than memorizing (no visited set!) to be memory efficient

    # We pass the solution along to each new recursive call to dfs_search
    #  so that statistics like number of nodes visited or recursion depth
    #  might be recorded

    if node is None:
        node = SearchNode(state=search_problem.start_state, starting_state=search_problem.start_state)
        solution = SearchSolution(problem=search_problem, search_method="DFS")
        # the next line isn't strictly necessary, but it makes the output more readable in my opinion.
        solution.path.append(node.state)

    # base case for when we exceed the depth_limit
    if len(solution.path) >= depth_limit:
        print(f'node state: {node.state}')
        print(f'length of solution path: {len(solution.path)}, solution path: {solution.path}')
        print(f'Depth limit has been reached! depth_limit={depth_limit}. \n')
        return False
    # base case for when we are at the solution:
    elif node.state == search_problem.goal_state:
        solution_path: list = solution.path
        # solution_path.reverse()
        print(f'Solution found! Path to solution: {solution_path}')
        print(f'{solution}')
        return True
    else:
        # look at the next state:
        for child_state in search_problem.get_successors(state=node.state):
            # if the child_node is new and unexplored
            if child_state not in solution.path:
                # we now need to create a new node! We pack the current_state into the node and point to the
                # current_node as the parent for the new node
                new_node = SearchNode(state=child_state,
                                      starting_state=search_problem.start_state,
                                      parent=node)
                # increment the solution nodes_visited
                solution.nodes_visited = solution.nodes_visited + 1
                # add the node to the solution path
                solution.path.append(new_node.state)  # <-- node or new node?
                dfs_search(search_problem=search_problem, depth_limit=depth_limit, node=new_node, solution=solution)


def ids_search(search_problem, depth_limit=100):

    for depth in range(depth_limit):
        s = dfs_search(search_problem=search_problem, depth_limit=depth)
        if s:
            break

    print('ids_search complete.')


# __main__ is just here for testing - it can be safely ignored or removed
if __name__ == "__main__":
    s = SearchNode(state=(3, 3, 1), starting_state=(3, 3, 1))
    s2 = SearchNode(state=(0, 0, 0), parent=s, starting_state=(3, 3, 1))
    s3 = SearchNode(state=(1, 1, 1), parent=s2, starting_state=(3, 3, 1))
    s4 = SearchNode(state=(2, 2, 2), parent=s3, starting_state=(3, 3, 1))
    s5 = SearchNode(state=(3, 3, 3), parent=s4, starting_state=(3, 3, 1))
    print(back_chaining(SearchNode=s5))
