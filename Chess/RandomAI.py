# Spencer Bertsch
# October 2021
# Code adapted from Assignment 3
# CS 276 @ Dartmouth College

# import chess
import random
from time import sleep
import sys


class RandomAI:
    def __init__(self):
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)
        if len(moves) == 0:
            print('Random AI has been defeated!!!')
            print(board)
            sys.exit(0)
        move = random.choice(moves)
        sleep(0.1)   # I'm thinking so hard.
        print("Random AI recommending move " + str(move))
        return move
