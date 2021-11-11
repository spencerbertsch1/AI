
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
            maze[row][col] = '*'
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

            next = [[0 for x in range(4)] for x in range(4)]
            for row in range(4):
                for col in range(4):

                    # # define m
                    # # I think this section is the problem area... How do we use the
                    # counter = 0
                    # current_transition_model: np.array = np.array(transition_model[counter])
                    # print(current_transition_model)
                    # current_location = current_state[row][col]
                    # m = current_transition_model * current_state
                    # counter += 1
                    # m_total: float = float(np.sum(m))
                    # next[row][col] = m_total


                    # define update vector (my update vector - next - is always a matrix of only ones!!)
                    counter = 0
                    m = [[0 for x in range(4)] for x in range(4)]
                    for sub_row in range(4):
                        for sub_col in range(4):
                            current_transition_model: np.array = np.array(transition_model[counter])
                            m[sub_row][sub_col] = current_transition_model * current_state[sub_row][sub_col]
                            counter += 1

                    # we then add the sum to the next matrix
                    m_total: float = float(np.sum(m))
                    next[row][col] = m_total

            next_array = np.array(next)
            prediction_vector_array = np.array(prediction_vector)
            prediction_vector = prediction_vector_array + next_array  # <-- (+) or (*)

            current_state = self.normalize_matrix(prediction_vector)

            if self.verbose:
                self.pretty_print_maze(matrix=self.ground_truth_states[i], maze_name=f'Ground Truth: X{i}')
                self.pretty_print_maze(matrix=current_state, maze_name='Current State')
            print('\n\n')

        return current_state


if __name__ == "__main__":
    h = HMM(starting_state=(0, 0), path_length=25, verbose=True)
    h.pretty_print_maze(matrix=h.maze, maze_name='Maze')
    h.filtering()
