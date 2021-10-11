# Spencer Bertsch
# October 2021
# Code adapted from Assignment 3
# CS 276 @ Dartmouth College

import chess
import math
import random


class AlphaBetaAI:

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.nodes_visited = 0

    def choose_move(self, board, random_best: bool = False):
        """
        Outer function for the minimix framework.
        This function calls the min_value function which cycles back and forth between min_value and max_value
        until either the game ends or until the max depth is reached. Realistically, because chess is such a complex
        game with a huge state space, the minimax algorithm will almost always end by reaching the max depth limit.

        :param board:
        :param depth:
        :return:
        """

        # moves = list(board.legal_moves)
        # we can also call the simple method for node reordering to test how much quicker we can make Alpha Beta
        moves = self.node_reorder(board=board)

        print(f'Searching through {len(moves)} moves!')
        actions_dict: dict = {}
        for move in moves:
            board.push(move)
            move_weight = self.min_value(board=board, depth=0, alpha=-math.inf, beta=math.inf)
            board.pop()
            actions_dict[move] = move_weight

        print(actions_dict)
        print(f'NODES VISITED: {self.nodes_visited}')
        self.nodes_visited = 0

        if len(moves) == 0:
            print('Looks like we lost...')
            return False

        if random_best:
            # instead of picking the first max value (argmax) lets choose a random max value!
            max_move_val = max(actions_dict.items(), key=lambda x: x[1])
            best_moves = []
            # Iterate over all the values in dictionary to find moves with max value
            for key, value in actions_dict.items():
                if value == max_move_val[1]:
                    best_moves.append(key)

            return random.choice(best_moves)

        else:
            best_move = max(actions_dict, key=actions_dict.get)
            return best_move

    def evaluate_board(self, board):
        """

        :param board:
        :return:
        """
        piece_value_lookup: dict = {
            1: 1,  # Pawn
            2: 3,  # Knight
            3: 3,  # Bishop
            4: 3,  # Rook
            5: 9   # Queen
        }

        white_total: int = 0
        black_total: int = 0
        # find the total board utility for each color based on the lookup table above
        for k, v in piece_value_lookup.items():
            white_total = white_total + (len(board.pieces(piece_type=k, color=True)) * piece_value_lookup[k])
            black_total = black_total + (len(board.pieces(piece_type=k, color=False)) * piece_value_lookup[k])

        # if the utility is equal, we return 0 - the exact center of utility between -1 and 1
        if white_total == black_total:
            return 0

        # if white's utility is greater, we use TanH to get a value between -1 and 0
        elif white_total > black_total:
            return -white_total

        # # if black's utility is greater, we use TanH to get a value between 0 and 1
        else:
            return black_total

    def cutoff_test(self, board, depth, min_or_max: str):
        """
        Helper function for MiniMax that determines if the chess game has been won by either party or we have reached
        the maximum depth in our search tree.

        :param board:
        :param depth:
        :return:
        """
        if board.is_game_over():

            if board.is_checkmate():
                # TODO maybe switch these!
                if min_or_max == 'min':
                    return -100
                elif min_or_max == 'max':
                    return 100
                else:
                    raise Exception(f'min_or_max argument needs to be either \'min\' or \'max\', not {min_or_max}')
            elif board.is_stalemate():
                return 0

            print('WE SHOULDN\'t BE HERE... EVALUATING BOARD...')
            return self.evaluate_board(board=board)

        elif depth >= self.max_depth:
            return self.evaluate_board(board=board)
        else:
            return None

    def max_value(self, board, depth, alpha, beta):
        """
        Max_value function for depth-limited minimax.
        :param board:
        :param depth:
        :return:
        """
        self.nodes_visited = self.nodes_visited + 1

        # check to see if we need to stop searching
        if self.cutoff_test(board, depth, min_or_max='max') is not None:
            return self.cutoff_test(board, depth, min_or_max='max')

        v = -math.inf
        moves = list(board.legal_moves)
        for move in moves:
            # Make the move
            board.push(move)
            # call min_value on the new state after we made the move
            v = max(v, self.min_value(board=board, depth=depth+1, alpha=alpha, beta=beta))
            board.pop()

            # if v is greater than or equal to beta, we can just return v and not keep checking nodes
            if v >= beta:
                return v
            # update alpha
            alpha = max(alpha, v)

        return v

    def min_value(self, board, depth, alpha, beta):
        """
        Min_value function for depth-limited minimax.
        :param board:
        :param depth:
        :return:
        """
        self.nodes_visited = self.nodes_visited + 1

        # check to see if we need to stop searching
        if self.cutoff_test(board=board, depth=depth, min_or_max='min') is not None:
            return self.cutoff_test(board, depth, min_or_max='min')

        v = math.inf
        moves = list(board.legal_moves)
        for move in moves:
            # Make the move
            board.push(move)
            # call max_value on the state after we make the move
            v = min(v, self.max_value(board=board, depth=depth+1, alpha=alpha, beta=beta))
            board.pop()

            # if v is greater than or equal to beta, we can just return v and not keep checking nodes
            if v <= alpha:
                return v
            # update beta
            beta = min(beta, v)

        return v

    def node_reorder(self, board) -> list:
        """
        Function to order the next moves based on their utility so we search the best moves first, and the
        worst moves last

        :param board:
        :return:
        """
        utility_dict = {}
        moves = list(board.legal_moves)
        for move in moves:
            board.push(move)
            move_utility = self.evaluate_board(board=board)
            board.pop()
            utility_dict[move] = move_utility

        # sort the utility dictionary by the utility values associated with each move
        sorted_dict = {k: v for k, v in sorted(utility_dict.items(), key=lambda item: item[1])}

        # create the list of sorted moves that we will search through
        sorted_moves_list = list(sorted_dict.keys())
        sorted_moves_list.reverse()

        return sorted_moves_list
