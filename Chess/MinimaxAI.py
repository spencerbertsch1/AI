import chess
import math


class MinimaxAI:

    def __init__(self, max_depth):
        self.max_depth = max_depth

    def choose_move(self, board):
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
        print(f'Searching through {len(moves)} moves!')
        actions_dict: dict = {}
        for move in moves:
            board.push(move)
            move_weight = self.min_value(board=board, depth=0)
            board.pop()
            actions_dict[move] = move_weight

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

        # if white's utility is greater, we use TanH to get a value between 0 and 1
        elif white_total > black_total:
            return math.tanh(white_total / black_total)

        # # if black's utility is greater, we use TanH to get a value between 0 and 1
        else:
            return math.tanh(black_total / white_total)

    def cutoff_test(self, board, depth):
        """
        Helper function for MiniMax that determines if the chess game has been won by either party or we have reached
        the maximum depth in our search tree.

        :param board:
        :param depth:
        :return:
        """
        if board.is_game_over():
            print(f'Chess game complete!')
            return 1
        elif depth >= self.max_depth:
            # print(f'Max depth reached, evaluating current board state at depth {depth}.')
            return self.evaluate_board(board=board)
        else:
            return None

    def max_value(self, board, depth):
        """
        Max_value function for depth-limited minimax.
        :param board:
        :param depth:
        :return:
        """
        # check to see if we need to stop searching
        if self.cutoff_test(board, depth) is not None:
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
        # check to see if we need to stop searching
        if self.cutoff_test(board, depth) is not None:
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
