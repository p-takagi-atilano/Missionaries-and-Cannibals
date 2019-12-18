# Paolo Takagi-Atilano: COSC 76, September 20 2017

from collections import deque
from SearchSolution import SearchSolution

# SearchNode class wraps state objects (not states)
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

# breadth-first search algorithm
def bfs_search(search_problem):
    start_node = SearchNode(search_problem.start_state)  # assumes search_problem has start_state
    visited_from = {start_node.state}
    queue = deque([start_node])
    count = 0

    while queue: # while there are items in queue
        count += 1
        curr_node = queue.pop()
        #print(curr_node.state)

        # if goal is found, we are done!
        if search_problem.goal_test(curr_node.state): # assumes search_problem has goal_test(state)
            return backchain(search_problem, curr_node, "BFS", count)

        for successor in search_problem.get_successors(curr_node.state):
            # ^assumes search_problem has get_successors(state)
            if successor not in visited_from:
                visited_from.add(successor)
                queue.insert(0, SearchNode(successor, curr_node))
                #count += 1

    # no solution found if control reaches this point
    return no_solution(search_problem, "BFS", count)


# path-checking recursive dfs algorithm
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    solution.nodes_visited += 1  # increment nodes visited count
    # base case: test to see if goal is current node
    if search_problem.goal_test(node.state):
        return backchain(search_problem, node, "DFS", solution.nodes_visited)
    else:
        # base case: depth limit has been exceeded, handle accordingly
        if depth_limit-1 <= 0:  # -1 for logic purposes
            if node.state == search_problem.start_state:
                return no_solution(search_problem, "DFS", solution.nodes_visited)
            else:
                return None

        # recursive case: continue recursing down successors, searching for goal node
        for successor in search_problem.get_successors(node.state):
            if not_in(node, successor):
                result = dfs_search(search_problem, depth_limit-1, SearchNode(successor, node), solution)
                if result:  # ensure that result is not none
                    if not len(result.path) == 0:  # ensure that result is not no_result
                        return result
        # none of the successors had any promise, return no_solution
        return no_solution(search_problem, "DFS", solution.nodes_visited)


# iterative depth search algorithm implementation
def ids_search(search_problem, depth_limit=100):
    count = 0 # keep track of nodes that were visited in failed depths
    for depth in range(depth_limit):
        solution = dfs_search(search_problem, depth)
        if not len(solution.path) == 0:  # actual solution found
            solution.search_method = "IDS" # this is IDS, not DFS
            solution.nodes_visited += count  # adding dfs searches of earlier depths
            return solution
        count += solution.nodes_visited  # solution was no good, add nodes visited to count
    return no_solution(search_problem, "IDS", count) # no solution found in given depth_limit


# wavefront search algorithm implementation
def wfs_search(search_problem, depth_level):
    string = "----\nWFS search\ngoal state: "
    string += str(search_problem.goal_state)
    string += "\ndepth level: "
    string += str(depth_level)
    string += "\npossible start states: "
    depth = 0
    start_nodes = {search_problem.goal_state}

    while depth < depth_level:
        temp = set()
        for start_node in start_nodes:
            for predecessor in search_problem.get_predecessors(start_node):
                temp.add(predecessor)

        start_nodes = set()
        for state in temp:
            start_nodes.add(state)

        depth += 1

    string += str(start_nodes)
    return string


# bidirectional search implementation
def bds_search(search_problem):
    start_node = SearchNode(search_problem.start_state)  # assumes search_problem has start_state
    goal_node = SearchNode(search_problem.goal_state)    # assumes search_problem has goal_state
    start_visited_from = {start_node.state}
    goal_visited_from = {goal_node.state}
    start_queue = deque([start_node])
    goal_queue = deque([goal_node])

    count = 0
    nodes_dict = {goal_node.state: goal_node}

    while start_queue and goal_queue: # while there are items in queues
        start_curr_node = start_queue.pop()
        goal_curr_node = goal_queue.pop()
        count += 2

        # add to dictionary if necessary
        if goal_curr_node.state not in nodes_dict:
            nodes_dict[goal_curr_node.state] = goal_curr_node

        # checking to see if there are any matches
        for goals_state in goal_visited_from:
            if start_curr_node.state == goals_state:
                start_backchain = backchain(search_problem, start_curr_node, "BDS", count)
                possible = nodes_dict.get(goals_state, None)
                if possible:
                    goal_backchain = backchain(search_problem, possible, "BDS", count)
                    goal_backchain.path.pop()
                    chain_len = len(start_backchain.path)
                    for state in goal_backchain.path:
                        start_backchain.path.insert(chain_len, state)
                    start_backchain.search_method = "BDS"
                    return start_backchain

        # find successors from start node end
        for successor in search_problem.get_successors(start_curr_node.state):
            # ^assumes search_problem has get_successors(state)
            if successor not in start_visited_from:
                start_visited_from.add(successor)
                start_queue.insert(0, SearchNode(successor, start_curr_node))
                #count += 1

        # find predecessors from goal node end
        for predecessor in search_problem.get_predecessors(goal_curr_node.state):
            if predecessor not in goal_visited_from:
                goal_visited_from.add(predecessor)
                goal_queue.insert(0, SearchNode(predecessor, goal_curr_node))
                #count += 1

    # no solution found if control reaches this point
    return no_solution(search_problem, "DFS", count)


# *************************** #
# **** HELPER FUNCTIONS: **** #
# *************************** #


# returns a SearchSolution object with given search_problem, search_method, and count and empty path
def no_solution(search_problem, search_method, count):
    solution = SearchSolution(search_problem, search_method)
    solution.nodes_visited = count
    return solution


# given search problem, found goal node, search method and count, returns corresponding SearchSolution object
# (constructs the path using backpointers from goal node)
def backchain(search_problem, goal_node, search_method, count):
    solution = SearchSolution(search_problem, search_method)
    solution.nodes_visited = count

    temp = goal_node
    solution.path.append(temp.state)
    while temp.parent is not None:
        solution.path.insert(0, temp.parent.state) # insert before child
        temp = temp.parent

    return solution


# returns true if test state is not equal to given node's state, or any of its (extended) predecessors, false otherwise
def not_in(given, test):
    temp = given
    while temp.parent is not None:
        if temp.state == test:
            return False
        temp = temp.parent
    if temp.state == test:
        return False
    return True
