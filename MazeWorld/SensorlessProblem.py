from Maze import Maze
from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
    # TODO should we include start state or goal here? We don't know either if I'm correct...
    def __init__(self, maze, start_state):
        self.maze = maze
        self.width = self.maze.width
        self.height = self.maze.height
        self.start_state = start_state

    def __str__(self):
        string = "Blind robot problem: "
        print(self.maze)
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def generate_initial_state(self):
        # create a list of all the possible states in the entire maze
        state = []
        for i in range(self.width):
            for j in range(self.height):
                tuple_to_add: tuple = (i, j)
                state.append(tuple_to_add)

        # remove all the illegal states
        legal_states = self.get_legal_states(state_list=state)

        # convert to a set and return
        s = set(legal_states)
        return s

    def get_legal_states(self, state_list: list) -> list:
        legal_states: list = []
        # given a list of states, remove the illegal ones
        for state in state_list:
            # run checks to ensure the possible move is floor and not covered by another robot
            if self.maze.is_floor(x=state[0], y=state[1]):
                if not self.maze.has_robot(x=state[0], y=state[1]):
                    legal_states.append(state)

        return legal_states

    def heuristic(self):
        pass

    def max_distance(self):
        pass

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))


## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("mazes/maze2.maz")
    test_problem = SensorlessProblem(test_maze3, start_state=(1, 0))
    start_state = test_problem.generate_initial_state()
    print(test_problem)
