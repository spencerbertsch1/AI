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


import sys

# DEFINE MAX DEPTH
MAX_DEPTH = 2

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
    game.make_move()


#print(hash(str(game.board)))
