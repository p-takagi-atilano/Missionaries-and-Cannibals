# Paolo Takagi-Atilano: COSC 76, September 20 2017
class CannibalProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.total_missionaries = start_state[0]
        self.total_cannibals = start_state[1]

    # get successor states for the given state
    def get_successors(self, state):
        possible = set()  # all potential successor states
        final = set()     # all final successor states

        if state[2] == 1:  # boat on original side, subtract missionaries/cannibals
            possible.add((state[0]-1, state[1],   0))    # send one missionary on boat
            possible.add((state[0],   state[1]-1, 0))    # send one cannibal on boat
            possible.add((state[0]-1, state[1]-1, 0))    # send one missionary and one cannibal on boat
            possible.add((state[0]-2, state[1],   0))    # send two missionaries on boat
            possible.add((state[0],   state[1]-2, 0))    # send two cannibals on boat

        else:  # boat on other side, add missionaries/cannibals
            possible.add((state[0]+1, state[1],   1))  # bring back one missionary on boat
            possible.add((state[0],   state[1]+1, 1))  # bring back one cannibal on boat
            possible.add((state[0]+1, state[1]+1, 1))  # bring back one missionary and one cannibal on boat
            possible.add((state[0]+2, state[1],   1))  # bring back two missionaries on boat
            possible.add((state[0],   state[1]+2, 1))  # bring back two cannibals on boat

        for successor in possible:  # add all legal states in possible to final
            if self.is_legal(successor):
                final.add(successor)

        return final


    # get predecessors states for the given state
    def get_predecessors(self, state):
        possible = set()
        final = set()

        # pretty much the opposite logic of get_successors, to go up the tree rather than down
        if state[2] == 1:
            possible.add((state[0]-1, state[1],   0))
            possible.add((state[0],   state[1]-1, 0))
            possible.add((state[0]-1, state[1]-1, 0))
            possible.add((state[0]-2, state[1],   0))
            possible.add((state[0],   state[1]-2, 0))
        else:
            possible.add((state[0]+1, state[1],   1))
            possible.add((state[0],   state[1]+1, 1))
            possible.add((state[0]+1, state[1]+1, 1))
            possible.add((state[0]+2, state[1],   1))
            possible.add((state[0],   state[1]+2, 1))

        for state in possible:
            # check to see if it would be a legal start state
            if (state[0] >= 0 and state[1] >= 0) and ((state[0] >= state[1]) or state[0] == 0):
                final.add(state)

        return final

    # returns whether or not given state is legal in current CannibalProblem object
    def is_legal(self, state):
        # make sure that # of given missionaries/cannibals <= total missionaries/cannibals
        # as well as there are no negative quantities of missionaries/cannibals
        if 0 <= state[0] <= self.total_missionaries and 0 <= state[1] <= self.total_cannibals:
            # exception case where there are no missionaries on one side, still a valid state
            if state[0] == 0 or state[0] == self.total_missionaries:
                return True
            # general rule; there must be more missionaries than cannibals on both sides at all times
            return (state[0] >= state[1]) and \
                   ((self.total_missionaries - state[0]) >= (self.total_cannibals - state[1]))
        return False

    # returns whether or not given state is the goal state in current CannibalProblem object
    def goal_test(self, state):
        return state == self.goal_state

    def __str__(self):
        string = "Missionaries and cannibals problem: " + str(self.start_state)
        return string


## A bit of test code

if __name__ == "__main__":
    test_cp = CannibalProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    print(test_cp)
