# Spencer Bertsch
# November 2021
# Assignment 6
# CS 276 @ Dartmouth College

from copy import deepcopy
import random
import seaborn as sns
from pathlib import Path
import matplotlib.pylab as plt
from matplotlib.colors import LogNorm
import numpy as np
np.random.seed(1)
random.seed(4)


# define paths to save heatmap files of solutions
PATH_TO_THIS_FILE: Path = Path(__file__).resolve()
ABSPATH_TO_DOCS: Path = PATH_TO_THIS_FILE.parent / 'docs'


def heatmap(ground_truth_array: np.array, curr_state_array: np.array, i: int):
    """
    Simple utility function to generate some nice heatmaps of the outputs.
    This let's us make sure that the probability distribution found in the state X(t)
    really represents the location of the robot.
    :return: NA
    """

    # round the probability matrix for better annotation in plotting
    curr_state_array = np.around(curr_state_array, decimals=4)

    fig, ax = plt.subplots(1, 2)

    # plot the ground truth
    sns.heatmap(ground_truth_array, ax=ax[0], linewidths=.5,
                cmap="YlGnBu", square=True, annot=True, cbar=False).set(title='Ground Truth (Robot Position)')

    # plot the current state
    sns.heatmap(curr_state_array, ax=ax[1], linewidths=.5,
                cmap="YlGnBu", square=True, annot=True, cbar=False,
                norm=LogNorm()).set(title=f'Current State X(time={i})')

    # save the figure to the /docs directory
    plot_name: str = f'solution_iteration_{i}_random.svg'
    save_path: Path = ABSPATH_TO_DOCS / plot_name
    plt.savefig(str(save_path))

    plt.show()


class HMM:

    # define a mapping for each color
    maze_map: dict = {
        'R': 0,
        'G': 1,
        'B': 2,
        'Y': 3
    }
    # define the colors of the board
    colors = ['R', 'B', 'G', 'Y']

    def __init__(self, path_length: int, starting_state: tuple, verbose: bool, show_heatmaps: bool):
        self.verbose = verbose
        self.show_heatmaps = show_heatmaps
        self.maze = self.generate_maze()
        self.path_length = path_length
        self.starting_state = starting_state
        self.robot_path = self.generate_path()
        self.ground_truth_states = self.generate_robot_path()
        self.sensor_readings = self.make_sensor_readings()
        self.transition_model = self.generate_transition_model()

    @staticmethod
    def pretty_print_maze(matrix: list, maze_name: str):
        """
        Print the maze or the probability matrix in a nice format
        :param matrix: list of lists representing the maze or the probability matix
        :return: N/A
        """
        print(f'----- {maze_name} -----')
        for row in matrix:
            print(f'{row}')

    def generate_maze(self) -> list:
        maze = []
        for i in range(4):
            row = []
            for j in range(4):
                color = random.choice(self.colors)
                encoded_color = self.maze_map[color]  # <- use encoded color if ints are more useful than strings
                row.append(color)
            maze.append(row)
        return maze

    def generate_moves(self):
        """
        Helper function that returns a list of moves 'N', 'E', 'S', or 'W'
        :return:
        """
        moves = []
        for i in range(self.path_length):
            direction = random.choice(['N', 'E', 'S', 'W'])
            moves.append(direction)
        return moves

    def generate_path(self) -> list:
        """
        Starting in cell [0, 0], get a list of random locations in a path of length self.path_length
        :return:
        """
        moves = self.generate_moves()
        starting_state = self.starting_state

        # we start by appending the starting state to the path
        path = [deepcopy(starting_state)]

        current_state = deepcopy(starting_state)
        for move in moves:

            state = deepcopy(current_state)

            # --- NORTH ---
            if move == 'N':
                if state[1] == 3:
                    # we're at the top wall, so we return the same state
                    path.append(state)
                else:
                    # the robot moves up one cell
                    state = (state[0], state[1]+1)
                    path.append(state)

            # --- EAST ---
            elif move == 'E':
                if state[0] == 3:
                    # we're at the right wall, so we return the same state
                    path.append(state)
                else:
                    # the robot moves to the right one cell
                    state = (state[0]+1, state[1])
                    path.append(state)

            # --- SOUTH ---
            elif move == 'S':
                if state[1] == 0:
                    # we're at the bottom wall, so we return the same state
                    path.append(state)
                else:
                    # the robot moves down one cell
                    state = (state[0], state[1]-1)
                    path.append(state)

            # --- WEST ---
            elif move == 'W':
                if state[0] == 0:
                    # we're at the right wall, so we return the same state
                    path.append(state)
                else:
                    # the robot moves down one cell
                    state = (state[0]-1, state[1])
                    path.append(state)

            current_state = deepcopy(state)

        if self.verbose:
            print(f'Robot Path: {path}')

        return path

    def make_sensor_readings(self):
        """
        returns the list of sensor readings

        returns a list of color readings, for example ['R', 'B', 'R', 'R', 'Y']
        This gets passed to the filter algorithm

        :return: a list of sensor readings
        """

        sensor_readings = []
        for cell in self.robot_path:
            # find the ground truth at the current cell
            ground_truth: str = self.maze[cell[0]][cell[1]]
            # define the other colors that the sensor could pick up
            other_colors = set(self.colors) - set(ground_truth)

            # build the list so that the ground truth is at the front and the rest are unordered behind it
            choices = [ground_truth]
            for other_color in other_colors:
                choices.append(other_color)

            # here we simulate the sensor reading (88% chance of getting it right, and 12% chance of getting it wrong)
            sensor_reading_array: str = np.random.choice(a=choices, size=1, p=[0.88, 0.04, 0.04, 0.04])

            # we can use the below line to test the optimal ability of the system (given a perfectly performing sensor)
            # sensor_reading_array: str = np.random.choice(a=choices, size=1, p=[1, 0, 0, 0])
            sensor_reading = sensor_reading_array[0]
            if self.verbose:
                if ground_truth != sensor_reading:
                    print(f'Ground Truth: {ground_truth}, Incorrect Sensor Reading: {sensor_reading}')

            sensor_readings.append(sensor_reading)

        return sensor_readings

    def generate_transition_model(self, maze_size: int = 4) -> list:
        """
        Generate the update vector
        :param: length of one side of the square maze
        :return:
        """
        transition_model = []

        empty_matrix = [[0 for x in range(4)] for x in range(4)]

        # here we iterate through each cell in the maze and find the probability of moving in each direction
        for row in range(4):
            for col in range(4):

                current_matrix = deepcopy(empty_matrix)

                # get the cell north - if it's open, then make it 0.25, if not then add 0.25 to the existing cell
                north_cell = (row-1, col)
                if north_cell[0] >= 0:
                    current_matrix[row-1][col] = 0.25
                else:
                    # the robot is against the north wall
                    current_matrix[row][col] = current_matrix[row][col] + 0.25

                # get the cell east - if it's open, then make it 0.25, if not then add 0.25 to the existing cell
                east_cell = (row, col+1)
                if east_cell[1] <= 3:
                    current_matrix[row][col+1] = 0.25
                else:
                    # the robot is against the right wall
                    current_matrix[row][col] = current_matrix[row][col] + 0.25

                # get the cell south - if it's open, then make it 0.25, if not then add 0.25 to the existing cell
                south_cell = (row+1, col)
                if south_cell[0] <= 3:
                    current_matrix[row+1][col] = 0.25
                else:
                    # the robot is against the north wall
                    current_matrix[row][col] = current_matrix[row][col] + 0.25

                # get the cell west - if it's open, then make it 0.25, if not then add 0.25 to the existing cell
                west_cell = (row, col-1)
                if west_cell[1] >= 0:
                    current_matrix[row][col-1] = 0.25
                else:
                    # the robot is against the right wall
                    current_matrix[row][col] = current_matrix[row][col] + 0.25

                transition_model.append(current_matrix)

        return transition_model

    def normalize_matrix(self, matrix):
        """
        Sum everything in the array and divide by the sum
        :param matrix:
        :return:
        """
        sum = 0
        for i in range(4):
            for j in range(4):
                sum = sum + matrix[i][j]

        for i in range(4):
            for j in range(4):
                matrix[i][j] = matrix[i][j] / sum

        return matrix

    def generate_robot_path(self):
        """
        Generates a list of matrices in which the robot's position is updated for each move in the move list
        Note that sometimes the robot runs into a wall and doesn't actually move - this still uses a turn
        :return:
        """
        robot_path = []

        for position in self.robot_path:
            maze = [[0 for x in range(4)] for x in range(4)]
            row = position[0]
            col = position[1]
            maze[row][col] = 1
            robot_path.append(maze)

        return robot_path

    def filtering(self):
        """
        Implement the filtering algorithm

        initialize probability matrix as matrix of 0.0625 probabilities
            loop through readings:
                p_v = generate prediction vector
                u_v = generate update vector
                probability_matrix = prediction_vector * update_vector
            return probability_matrix
        :return:
        """

        color_matrix: list = self.maze
        transition_model: list = self.transition_model

        sensor_readings = self.sensor_readings
        if self.verbose:
            print(f'SENSOR READINGS: \n {sensor_readings}')

        # define the initial probability matrix with values of 0.0625 in each cell
        current_state_list = [[0.0625 for x in range(4)] for x in range(4)]
        current_state = np.array(current_state_list)
        if self.verbose:
            self.pretty_print_maze(matrix=current_state_list, maze_name='Initial Probability Matrix')

        for i, sensor_reading in enumerate(sensor_readings):
            if self.verbose:
                print(f'\n\n\n Output for Time t={i}')

            # initialize prediction vector
            prediction_vector = [[0 for x in range(4)] for x in range(4)]
            # if the color of the ground truth matches the current sensor reading, then set the probability to 0.88
            for row in range(4):
                for col in range(4):
                    if color_matrix[row][col] == sensor_reading:
                        prediction_vector[row][col] = 0.88
            # if the color of the ground truth doesn't match the current sensor reading, set the probability to 0.04
            for row in range(4):
                for col in range(4):
                    if prediction_vector[row][col] == 0:
                        prediction_vector[row][col] = 0.04

            if self.verbose:
                self.pretty_print_maze(matrix=prediction_vector, maze_name='Prediction Vector')

            # create the transition array
            transition = np.array([[0 for x in range(4)] for x in range(4)])
            counter = 0
            for row in range(4):
                for col in range(4):
                    # multiply the transition vector by the current_state
                    current_transition_model: np.array = np.array(transition_model[counter])
                    transition = transition + np.multiply(current_transition_model, current_state[row][col])
                    counter += 1

            transition_array = np.array(transition)
            prediction_vector_array = np.array(prediction_vector)

            prediction_vector = np.multiply(prediction_vector_array, transition_array)  # <-- (+) or (*)

            current_state = self.normalize_matrix(prediction_vector)

            if self.verbose:
                self.pretty_print_maze(matrix=self.ground_truth_states[i], maze_name=f'Ground Truth: X{i}')
                self.pretty_print_maze(matrix=current_state, maze_name='Current State')

            if self.show_heatmaps:
                # we need to suppress output even more here so we don't end up with 100 solution heatmaps
                if i % 3 == 0:
                    heatmap(ground_truth_array=np.array(self.ground_truth_states[i]), curr_state_array=current_state,
                            i=i)

        return current_state


# test code
if __name__ == "__main__":
    h = HMM(starting_state=(0, 0),
            path_length=12,
            verbose=True,
            show_heatmaps=False)  # <-- heatmaps require matplotlib and seaborn to be installed! See requirements.txt
    h.pretty_print_maze(matrix=h.maze, maze_name='Maze')
    h.filtering()
