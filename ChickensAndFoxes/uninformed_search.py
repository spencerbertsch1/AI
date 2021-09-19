
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
        # you write this part

    # you might write other helper functions, too. For example,
    #  I like to separate out backchaining, and the dfs path checking functions


def bfs_search(search_problem):
    print(f'BFS Search Initiated. Starting State: {search_problem.start_state}')
    # TODO



def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state

    # Don't forget that your dfs function should be recursive and do path checking,
    #  rather than memoizing (no visited set!) to be memory efficient

    # We pass the solution along to each new recursive call to dfs_search
    #  so that statistics like number of nodes visited or recursion depth
    #  might be recorded

    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    # you write this part



def ids_search(search_problem, depth_limit=100):
    pass
    # you write this part


# __main__ is just here for testing - it can be safely ignored or removed
if __name__ == "__main__":
    s = SearchNode(state=(3, 3, 1), starting_state=(3, 3, 1))
    s2 = SearchNode(state=(0, 0, 0), parent=s, starting_state=(3, 3, 1))
    s3 = SearchNode(state=(1, 1, 1), parent=s2, starting_state=(3, 3, 1))
    s4 = SearchNode(state=(2, 2, 2), parent=s3, starting_state=(3, 3, 1))
    s5 = SearchNode(state=(3, 3, 3), parent=s4, starting_state=(3, 3, 1))
    print(back_chaining(SearchNode=s5))
