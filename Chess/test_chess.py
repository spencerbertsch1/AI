# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame


import sys

# Set the max depth for depth limited minimax here
MAX_DEPTH: int = 2

player1 = HumanPlayer()
# player1 = MinimaxAI(max_depth=MAX_DEPTH, use_ids_search=False)
player2 = AlphaBetaAI(max_depth=MAX_DEPTH)

game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()


#print(hash(str(game.board)))
