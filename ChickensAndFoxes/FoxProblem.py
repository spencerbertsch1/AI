class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)

        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state):
        pass
        # you write this part. I also had a helper function
        # that tested if states were safe before adding to successor list

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


# A bit of test code
if __name__ == "__main__":
    test_cp = FoxProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    print(test_cp)
