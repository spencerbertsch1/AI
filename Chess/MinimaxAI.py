# Spencer Bertsch
# October 2021
# Code adapted from Assignment 3
# CS 276 @ Dartmouth College

import chess
import math
import random
import sys


class MinimaxAI:

    def __init__(self, max_depth, use_ids_search, player1):
        self.max_depth = max_depth
        self.nodes_visited = 0
        self.use_ids_search = use_ids_search
        self.player1 = player1

    def choose_move(self, board, random_best: bool = False):
        """
        Outer function for the minimix framework.
        This function calls the min_value function which cycles back and forth between min_value and max_value
        until either the game ends or until the max depth is reached. Realistically, because chess is such a complex
        game with a huge state space, the minimax algorithm will almost always end by reaching the max depth limit.

        :param board:
        :param random_best: True if you want the function to return a random move with max weight
        :return:
        """
        if self.use_ids_search:
            return self.minimax_ids(board=board, depth_limit=self.max_depth)
        else:
            moves = list(board.legal_moves)
            print(f'Searching through {len(moves)} moves!')
            actions_dict: dict = {}
            for move in moves:
                board.push(move)
                move_weight = self.min_value(board=board, depth=0)
                board.pop()
                actions_dict[move] = move_weight

            # print(actions_dict)
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


    def cutoff_test(self, board, depth):
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

    def max_value(self, board, depth):
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
        moves = list(board.legal_moves)
        for move in moves:
            # Make the move
            board.push(move)
            # call min_value on the new state after we made the move
            v = max(v, self.min_value(board=board, depth=depth+1))

            # after we exit the recursive step we want to pop the last move off of the board
            # print('popping')
            board.pop()

        return v

    def min_value(self, board, depth):
        """
        Min_value function for depth-limited minimax.
        :param board:
        :param depth:
        :return:
        """
        self.nodes_visited = self.nodes_visited + 1

        # check to see if we need to stop searching if the depth > max depth
        if depth >= self.max_depth:
            return self.cutoff_test(board, depth)

        v = math.inf
        moves = list(board.legal_moves)
        for move in moves:
            # Make the move
            board.push(move)
            # call max_value on the state after we make the move
            v = min(v, self.max_value(board=board, depth=depth+1))

            # after we exit the recursive step we want to pop the last move off of the board
            # print('popping')
            board.pop()

        return v


    def minimax_ids(self, board, depth_limit):
        """
        Depth limited minimax

        Loop through each depth and run limited Minimax for that depth,
        breaking if Minimax returns True OR if depth > max_limit

        :param board:
        :param depth_limit:
        :return:
        """

        best_moves_all_depths = {}

        i = 0
        while i < depth_limit:
            i += 1
            # set max depth to i so that we can run the minimax search for this depth first
            self.max_depth = i
            print(f'--- MAX DEPTH = {self.max_depth} ---')

            # run minimax for depth = i
            moves = list(board.legal_moves)
            print(f'Searching through {len(moves)} moves!')
            actions_dict: dict = {}
            for move in moves:
                board.push(move)
                move_value = self.min_value(board=board, depth=0)
                board.pop()
                actions_dict[move] = move_value

            # print(actions_dict)
            print(f'NODES VISITED: {self.nodes_visited}')
            self.nodes_visited = 0

            # find the best move overall (for all depths)
            best_move = max(actions_dict, key=actions_dict.get)
            max_move_val = max(actions_dict.items(), key=lambda x: x[1])[1]
            best_moves_all_depths[best_move] = max_move_val

        best_move_all_depths = max(best_moves_all_depths, key=best_moves_all_depths.get)
        return best_move_all_depths
