
# imports
from Filtering import HMM


if __name__ == "__main__":

    h = HMM(starting_state=(0, 0), path_length=15, verbose=True)
    h.pretty_print_maze(matrix=h.maze, maze=True)
    # h.generate_path()
