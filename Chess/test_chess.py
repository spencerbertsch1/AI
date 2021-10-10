# Spencer Bertsch
# October 2021
# Code adapted from Assignment 3
# CS 276 @ Dartmouth College

# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
import time


import sys

# DEFINE MAX DEPTH
MAX_DEPTH = 3
DISPLAY_TIME = False

# PLAYER 1
player1 = HumanPlayer()
# player1 = RandomAI()
# player1 = MinimaxAI(max_depth=MAX_DEPTH, use_ids_search=False)
# player1 = AlphaBetaAI(max_depth=2)

# PLAYER 2
# player2 = HumanPlayer()
# player2 = RandomAI()
player2 = MinimaxAI(max_depth=MAX_DEPTH, use_ids_search=False)
# player2 = AlphaBetaAI(max_depth=MAX_DEPTH)

game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    tic = time.time()
    game.make_move()
    toc = time.time()
    if DISPLAY_TIME:
        print(f'TIME TAKEN: {round(toc-tic, 3)} seconds.')


#print(hash(str(game.board)))
