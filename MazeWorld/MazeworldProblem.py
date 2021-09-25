from Maze import Maze
from time import sleep

class MazeworldProblem:

    # you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations: tuple, start_states: tuple):
        self.maze = maze
        self.goal_state = goal_locations  # QUESTION!! <-- should we have multiple goal states?
        self.start_state = start_states  # QUESTION!! <-- should we have multiple start states?

    def __repr__(self):
        string = "MazeWorld problem: "
        return string

        # TODO
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
            else:
                print(f'Illegal state found - {state}')

        return legal_states

    def get_successors(self, state: tuple):
        print(f'Finding potential next states for the current state: {state}')
        print(f'Maze information: Width: {self.maze.width}, Height: {self.maze.height}')

        all_successors: list = [(state[0]+1, state[1]), (state[0]-1, state[1]),
                                (state[0], state[1]+1), (state[0], state[1]-1)]

        return self.is_legal(all_possible_states=all_successors)



    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(0.5)

            print(str(self.maze))


# A bit of test code. You might want to add to it to verify that things
#  work as expected.
if __name__ == "__main__":
    test_maze = Maze("maze_test.maz")
    test_mp = MazeworldProblem(test_maze, (19, 2), start_states=(0, 0))

    print(test_mp.get_successors((0, 0)))

    # test_mp = MazeworldProblem(test_maze, (1, 4, 1, 3, 1, 2))  # <-- for testing multi robot, multi goal
    # print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
