
import numpy as np
from copy import deepcopy
import random
random.seed(5)


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

    def __init__(self, path_length: int, starting_state: tuple, verbose: bool):
        self.verbose = verbose
        self.maze = self.generate_maze()
        self.path_length = path_length
        self.starting_state = starting_state
        self.robot_path = self.generate_path()
        self.sensor_readings = self.make_sensor_readings()

    @staticmethod
    def pretty_print_maze(matrix: list, maze: bool):
        """
        Print the maze or the probability matrix in a nice format
        :param matrix: list of lists representing the maze or the probability matix
        :return: N/A
        """
        if maze:
            print(f'----- MAZE -----')
        else:
            print(f'----- Probability Matrix -----')
        for row in matrix:
            print(f'{row}')

    def generate_maze(self) -> list:
        maze = []
        for i in range(4):
            row = []
            for j in range(4):
                color = random.choice(self.colors)
                encoded_color = self.maze_map[color]  # <- use encoded color if strings are'nt a good implementation
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
            sensor_reading = sensor_reading_array[0]
            if self.verbose:
                if ground_truth != sensor_reading:
                    print(f'Ground Truth: {ground_truth}, Incorrect Sensor Reading: {sensor_reading}')

            sensor_readings.append(sensor_reading)

        return sensor_readings

    def filtering(self) -> list:
        """

        :return:
        """
        sensor_readings = self.sensor_readings
        if self.verbose:
            print(f'SENSOR READINGS: \n {sensor_readings}')

        # define the initial probability matrix with values of 0.0625 in each cell
        initial_matrix = [[0.0625 for x in range(4)] for x in range(4)]
        if self.verbose:
            self.pretty_print_maze(matrix=initial_matrix, maze=False)

        for sensor_reading in sensor_readings:
            # p_v = generate prediction vector

            # u_v = generate update vector

            # probability_matrix = prediction_vector * update_vector
            pass

        # takes an initial probability matrix of
        # [0.0625, 0.0625, 0.0625, 0.0625]
        # [0.0625, 0.0625, 0.0625, 0.0625]
        # [0.0625, 0.0625, 0.0625, 0.0625]
        # [0.0625, 0.0625, 0.0625, 0.0625]

        # as it explores, it updates the probability matrix, then returns the resulting matrix

        """
        def filter(sensor_readings):
            initialize probability matrix as matrix of 0.0625 probabilities 
            
            loop through readings:
                p_v = generate prediction vector
                
                u_v = generate update vector
                
                probability_matrix = prediction_vector * update_vector
                
            return probability_matrix
        """
        return []

if __name__ == "__main__":
    h = HMM(starting_state=(0, 0), path_length=20, verbose=True)
    h.pretty_print_maze(matrix=h.maze, maze=True)
    h.filtering()
