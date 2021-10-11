# Spencer Bertsch
# October 2021
# Code adapted from Assignment 3
# CS 276 @ Dartmouth College

import chess
import math
import random
import sys


class AlphaBetaAI:

    def __init__(self, max_depth, move_ordering, player1):
        self.max_depth = max_depth
        self.nodes_visited = 0
        self.move_ordering = move_ordering
        self.player1 = player1

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

        moves = list(board.legal_moves)
        # we can also call the simple method for node reordering to test how much quicker we can make Alpha Beta
        # moves = self.node_reorder(board=board)

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
            print('Minimax AI has been defeated!!!')
            print(board)
            sys.exit(0)

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
        Function to calculate the utility of a board from the perspective of a certain player
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

        # AI is the white player
        if self.player1:
            return white_total - black_total
        else:
            return black_total - white_total

    def cutoff_test(self, board):
        """
        Helper function for MiniMax that determines if the chess game has been won by either party or we have reached
        the maximum depth in our search tree.

        :param board:
        :param depth:
        :return:
        """

        if board.is_checkmate():
            # if player and turn are the same value then we lose
            if board.turn == self.player1:  # True and True represent white and white
                # AI loses
                return -1000

            # if player and turn are different values we win
            if board.turn != self.player1:
                # AI wins
                return 1000

        elif board.is_stalemate():
            return 0

        else:
            return self.evaluate_board(board=board)

    def max_value(self, board, depth, alpha, beta):
        """
        Max_value function for depth-limited minimax.
        :param board:
        :param depth:
        :return:
        """
        self.nodes_visited = self.nodes_visited + 1

        # check to see if we need to stop searching if the depth > max depth
        if depth >= self.max_depth:
            return self.cutoff_test(board, depth)

        v = -math.inf

        if self.move_ordering:
            # add move reordering
            moves = self.node_reorder(board=board, is_max=True)
        else:
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

        # check to see if we need to stop searching if the depth > max depth
        if depth >= self.max_depth:
            return self.cutoff_test(board)

        v = math.inf

        if self.move_ordering:
            # add move reordering
            moves = self.node_reorder(board=board, is_max=False)
        else:
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

    def node_reorder(self, board, is_max: bool) -> list:
        """
        Function to order the next moves based on their utility so we search the best moves first, and the
        worst moves last

        :param board:
        :param is_max:
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

        if is_max:
            sorted_moves_list.reverse()

        return sorted_moves_list
