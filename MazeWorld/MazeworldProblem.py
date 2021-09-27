from Maze import Maze
from time import sleep
import os

class MazeworldProblem:

    # you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations: tuple, start_states: tuple):
        self.maze = maze
        self.goal_state = goal_locations
        self.start_state = start_states

    def print_path(self, path: list):
        # string = "MazeWorld problem: \n"

        # annotate the map with the goal state
        self.maze.map[self.maze.index(self.goal_state[0], self.goal_state[1])] = "$"

        for state in path:
            # store the old state
            old_state = self.maze.robotloc
            # update the location of the robot
            self.maze.robotloc = [state[0], state[1]]

            # update and print the new map
            self.maze.map[self.maze.index(old_state[0], old_state[1])] = "1"

            print(self.maze)
            sleep(0.5)
            clear = "\n" * 20
            print(clear)

    def __str__(self):
        string = "MazeWorld problem: \n"
        # print(self.maze)
        return string

        # TODO  ^^^ this functionality has been implemented above in the print_path method
        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def is_legal(self, all_possible_states: list) -> list:
        legal_states: list = []
        # given a list of states, remove the illegal ones
        for state in all_possible_states:
            # run checks to ensure the possible move is floor and not covered by another robot
            if self.maze.is_floor(x=state[0], y=state[1]):
                if not self.maze.has_robot(x=state[0], y=state[1]):
                    legal_states.append(state)

        return legal_states

    def get_successors(self, state: tuple):
        """
        Simple get successors function for a robot in a maze

        :param state:
        :return:
        """
        all_successors: list = [(state[0]+1, state[1]), (state[0]-1, state[1]),
                                (state[0], state[1]+1), (state[0], state[1]-1),
                                (state[0], state[1])]

        return self.is_legal(all_possible_states=all_successors)


    # def multirobot_get_successors(self, states: tuple):
    #     """
    #     get successors function for multiple robots in a maze. very similar to get_successors, but with the
    #     addition of an option to stay in the same place
    #     :param states:
    #     :return:
    #     """
    #     num_robots = 1
    #     if len(states) == 4:
    #         num_robots = 2
    #     else:
    #         num_robots = 3
    #
    #     all_successors: list = [(states[0] + 1, states[1]), (states[0] - 1, states[1]),
    #                             (states[0], states[1] + 1), (states[0], states[1] - 1),
    #                             (states[0], states[1])]
    #
    #     return self.is_legal(all_possible_states=all_successors)

    # def animate_path(self, path: list):
    #     # reset the robot locations in the maze
    #     self.maze.robotloc = tuple(self.start_state[1:])
    #
    #     for state in path:
    #         print(str(self))
    #         self.maze.robotloc = tuple(state[1:])
    #         sleep(0.5)
    #
    #         print(str(self.maze))


# A bit of test code. You might want to add to it to verify that things
#  work as expected.
if __name__ == "__main__":
    test_maze = Maze("mazes/multirobot_maze1.maz")
    test_mp = MazeworldProblem(test_maze, goal_locations=(0, 3, 3, 6, 6, 4), start_states=(0, 0, 1, 6, 4, 5))

    print(test_mp.get_successors((1, 6)))

    # test_mp = MazeworldProblem(test_maze, (1, 4, 1, 3, 1, 2))  # <-- for testing multi robot, multi goal
    # print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
