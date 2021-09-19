class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)

        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state: tuple) -> list:
        """
        Method to get the legal next states given a state. The boat can either be on the left or right bank and
        can either ferry both a chicken and fox, or just a chicken, or just a fox to the other side of the river.

        :param state: tuple (chicken, fox, boat)
        :return: list of tuples representing the legal next states
        """
        successors: list = []

        # define the number of chickens and foxes on each side of the river
        left_chickens = state[0]
        right_chickens: int = self.start_state[0] - state[0]
        left_foxes: int = state[1]
        right_foxes: int = self.start_state[1] - state[1]

        if state[2] == 0:
            print(f"Boat is on right bank - collecting the possible next states for {state}.")
            if (right_chickens > 0) & (right_foxes > 0):
                successors.append((state[0]+1, state[1]+1, state[2]+1))

            if right_chickens > 0:
                successors.append((state[0]+1, state[1], state[2]+1))

            if right_foxes > 0:
                successors.append((state[0], state[1]+1, state[2]+1))

        elif state[2] == 1:
            print(f"Boat is on left bank - collecting the possible next states for {state}.")
            if(left_chickens > 0) & (left_foxes > 0):
                successors.append((state[0]-1, state[1]-1, state[2]-1))

            if left_chickens > 0:
                successors.append((state[0]-1, state[1], state[2]-1))

            if left_foxes > 0:
                successors.append((state[0], state[1]-1, state[2]-1))

        else:
            raise Exception(f"Something has gone wrong... check state: {state}.")

        # remove the elements of 'successors' that are illegal
        for current_state in successors.copy():
            is_legal = self.is_legal(state=current_state)
            if not is_legal:
                print(f"Illegal state found... Removing: {current_state}.")
                successors.remove(current_state)

        print(f'SUCCESSORS TO {state}: {successors}')
        return successors

    def is_legal(self, state: tuple) -> bool:
        """
        Method to determine whther or not a given state is legal or not based on the number of chickens and foxes
        on each side of the river. If there are more foxes than chickens on either side, then the state is illegal

        :param state: tuple (chickens, foxes, boat)
        :return: True if legal, False otherwise.
        """
        legal: bool = True

        # define the number of chickens and foxes on each side of the river
        left_chickens = state[0]
        right_chickens: int = self.start_state[0] - state[0]
        left_foxes: int = state[1]
        right_foxes: int = self.start_state[1] - state[1]

        # if there are more foxes than chickens on either side, set legal to False
        if (left_foxes > left_chickens) & (left_chickens != 0):
            legal = False
        elif (right_foxes > right_chickens) & (right_chickens != 0):
            legal = False

        return legal

    # I also had a goal test method. You should write one.
    def goal_test(self, state: tuple):
        """
        Simple helper method used to check whether or not the current state satisfies the goal of the game.
        :param state: tuple - current state of the first bank (chickens, foxes, boat)
        :return:
        """
        if state == self.goal_state:
            return True
        else:
            return False

    def __str__(self):
        string = "Chickens and foxes problem: " + str(self.start_state)
        return string


# __main__ here just for testing - can be safely ignored or removed.
if __name__ == "__main__":
    test_cp = FoxProblem(start_state=(3, 3, 1))
    print(test_cp.get_successors(state=(2, 2, 0)))
    print(test_cp)
