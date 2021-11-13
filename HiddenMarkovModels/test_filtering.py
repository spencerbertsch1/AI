# Spencer Bertsch
# November 2021
# Assignment 6
# CS 276 @ Dartmouth College

from Filtering import HMM
import random
random.seed(4)


def test_filtering(starting_state: tuple, path_length: int, verbose: bool, show_heatmaps: bool):
    """
    Function to test the filtering algorithm

    :param starting_state: the (x, y) position of the starting state of the robot
    :param path_length: the number of steps that the robot will take on it's path
    :param verbose: True if you want to see lots of printed output showing the robot's journey
    :param show_heatmaps: True if you want to see heatmaps generated showing the ground truth vs the Current State
    :return: NA
    """
    h = HMM(starting_state=starting_state,
            path_length=path_length,
            verbose=verbose,
            show_heatmaps=show_heatmaps)  # <-- heatmaps require matplotlib and seaborn to be installed!
    h.pretty_print_maze(matrix=h.maze, maze_name='Maze')
    h.filtering()


if __name__ == "__main__":
    test_filtering(starting_state=(0, 0),
                   path_length=12,
                   verbose=True,
                   show_heatmaps=False)
