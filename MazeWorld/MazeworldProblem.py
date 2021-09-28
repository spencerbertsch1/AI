from Maze import Maze
from time import sleep
import os

class MazeworldProblem:

    # you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations: tuple, start_states: tuple):
        self.maze = maze
        self.goal_states = goal_locations
        self.start_states = start_states

    def print_path(self, path: list):
        # string = "MazeWorld problem: \n"

        # annotate the map with the goal state
        self.maze.map[self.maze.index(self.goal_states[0], self.goal_states[1])] = "$"

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

    def get_legal_states(self, all_successors: list) -> list:
        legal_states: list = []
        stay_in_place = all_successors[-1]
        # given a list of states, remove the illegal ones
        for state in all_successors:
            # run checks to ensure the possible move is floor and not covered by another robot
            if self.maze.is_floor(x=state[0], y=state[1]):
                if not self.maze.has_robot(x=state[0], y=state[1]):
                    legal_states.append(state)

        legal_states.append(stay_in_place)

        return legal_states

    @staticmethod
    def get_full_successors(legal_successors: list, states: tuple, robot_number):

        all_tuples = []
        for single_successor in legal_successors:
            new_state = []
            for i, initial_state_number in enumerate(states):
                if i == 0:
                    if robot_number == 1:
                        new_state.append(1)
                    elif robot_number == 2:
                        new_state.append(2)
                    else:
                        new_state.append(0)
                elif (i == 1) & (robot_number == 1):
                    new_state.append(single_successor[0])
                elif (i == 2) & (robot_number == 1):
                    new_state.append(single_successor[1])
                elif (i == 3) & (robot_number == 2):
                    new_state.append(single_successor[0])
                elif (i == 4) & (robot_number == 2):
                    new_state.append(single_successor[1])
                elif (i == 5) & (robot_number == 3):
                    new_state.append(single_successor[0])
                elif (i == 6) & (robot_number == 3):
                    new_state.append(single_successor[1])
                else:
                    new_state.append(initial_state_number)

            new_state_tuple = tuple(new_state)
            all_tuples.append(new_state_tuple)

        return all_tuples

    def get_successors(self, states: tuple, search_problem):
        """
        Simple get successors function for a robot in a maze

        :param states: tuple of length 7 - (robot_to_move, x1, y1, x2, y2, x3, y3)
        :return:
        """
        # update the robot location in the maze object
        robot_locs = []
        for i, state_num in enumerate(states):
            if i == 0:
                continue
            else:
                robot_locs.append(state_num)
        search_problem.maze.robotloc = robot_locs

        if states[0] == 0:
            state = (states[1], states[2])
            # print('Moving Robot 1...')
            all_successors: list = [(state[0]+1, state[1]), (state[0]-1, state[1]), (state[0], state[1]+1),
                                    (state[0], state[1]-1), (state[0], state[1])]
            legal_successors: list = self.get_legal_states(all_successors=all_successors)

            all_tuples = self.get_full_successors(legal_successors=legal_successors, states=states, robot_number=1)

        elif states[0] == 1:
            state = (states[3], states[4])
            # print('Moving Robot 2...')
            all_successors: list = [(state[0]+1, state[1]), (state[0]-1, state[1]), (state[0], state[1]+1),
                                    (state[0], state[1]-1), (state[0], state[1])]
            legal_successors: list = self.get_legal_states(all_successors=all_successors)

            all_tuples = self.get_full_successors(legal_successors=legal_successors, states=states, robot_number=2)

        else:
            state = (states[5], states[6])
            # print('Moving Robot 3...')
            all_successors: list = [(state[0]+1, state[1]), (state[0]-1, state[1]), (state[0], state[1]+1),
                                    (state[0], state[1]-1), (state[0], state[1])]
            legal_successors: list = self.get_legal_states(all_successors=all_successors)

            all_tuples = self.get_full_successors(legal_successors=legal_successors, states=states, robot_number=3)

        return all_tuples

    def animate_path(self, path: list):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_states[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(0.5)

            print(str(self.maze))


# A bit of test code. You might want to add to it to verify that things
#  work as expected.
if __name__ == "__main__":
    test_maze = Maze("mazes/multirobot_maze1.maz")
    test_mp = MazeworldProblem(test_maze, goal_locations=(0, 3, 3, 6, 6, 4), start_states=(0, 0, 1, 6, 4, 5))
    print(test_mp)

    # print(test_mp.get_successors((1, 6)))

    # test_mp = MazeworldProblem(test_maze, (1, 4, 1, 3, 1, 2))  # <-- for testing multi robot, multi goal
    # print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
    # (robot_to_move, x1, y1, x2, y2, x3, y3)

