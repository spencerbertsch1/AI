# Spencer Bertsch
# October 2021
# Code adapted from Assignment 3
# CS 276 @ Dartmouth College

# brew install pyqt
from PyQt5 import QtGui, QtSvg
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import QApplication, QWidget
import sys
import chess, chess.svg
from RandomAI import RandomAI
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
from HumanPlayer import HumanPlayer

import random


class ChessGui:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        self.game = ChessGame(player1, player2)

        self.app = QApplication(sys.argv)
        self.svgWidget = QtSvg.QSvgWidget()
        self.svgWidget.setGeometry(50, 50, 400, 400)
        self.svgWidget.show()


    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.make_move)
        self.timer.start(10)

        self.display_board()

    def display_board(self):
        svgboard = chess.svg.board(self.game.board)

        svgbytes = QByteArray()
        svgbytes.append(svgboard)
        self.svgWidget.load(svgbytes)


    def make_move(self):

        print("making move, white turn " + str(self.game.board.turn))

        self.game.make_move()
        self.display_board()


if __name__ == "__main__":

    random.seed(2)

    # DEFINE MAX DEPTH
    MAX_DEPTH = 2

    # PLAYER 1
    # player1 = HumanPlayer()
    player1 = RandomAI()
    # player1 = MinimaxAI(max_depth=MAX_DEPTH, use_ids_search=False)
    # player1 = AlphaBetaAI(max_depth=MAX_DEPTH)

    # PLAYER 2
    # player2 = HumanPlayer()
    # player2 = RandomAI()
    # player2 = MinimaxAI(max_depth=MAX_DEPTH, use_ids_search=False, player1=False)
    player2 = AlphaBetaAI(max_depth=MAX_DEPTH, move_ordering=True, player1=False)

    game = ChessGame(player1, player2)
    gui = ChessGui(player1, player2)

    gui.start()

    sys.exit(gui.app.exec_())
