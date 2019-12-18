# Paolo Takagi-Atilano: COSC 76, September 20 2017
from CannibalProblem import CannibalProblem
from uninformed_search import bfs_search, dfs_search, ids_search, wfs_search, bds_search

# Create a few test problems:
problem331 = CannibalProblem((3, 3, 1))
problem541 = CannibalProblem((5, 4, 1))
problem551 = CannibalProblem((5, 5, 1))

# Run the searches.
#  Each of the search algorithms should return a SearchSolution object,
#  even if the goal was not found. If goal not found, len() of the path
#  in the solution object should be 0.

print(bfs_search(problem331))
print(dfs_search(problem331))
print(ids_search(problem331))
print(bds_search(problem331))

print(bfs_search(problem551))
print(dfs_search(problem551))
print(ids_search(problem551))
print(bds_search(problem551))

print(bfs_search(problem541))
print(dfs_search(problem541))
print(ids_search(problem541))
print(bds_search(problem541))

print(wfs_search(problem331, 11))

