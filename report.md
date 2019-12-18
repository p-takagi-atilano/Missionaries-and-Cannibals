# COSC 76: Missionaries and Cannibals Assignment Report
## Paolo Takagi-Atilano
### Introduction:
The rules of the Missionaries and Cannibals problem are as follows: There are 3 missionaries and 3 cannibals on one side of the river, and would like to reach the other side.  They have a boat that carries two people accross, and there cannot be fewer missionaries than cannibals on either side, at risk of the missionaries being eaten.

In order to represnt a state for this problem, we are using a tuple of integers in this form `(m, c, b)`, where `m` is the number of missionaries on the original side, `c` is the number of cannibals on the original side, and `b` is which side the boat is on (`0` if on the desired side, `1` if on the original side)

Without considering their legality, and upper bound on the number of states is 36.  I reached this number by the following reasoning: There are 4 possible options for both the number of missionaries and cannibals (0, 1, 2, or 3).  Next, there are 2 possible options for the number of boats (0 or 1).  By the Product Principle, we have 
`4 x 4 x 2 = 32`
classes. Hence, we see that a general Missionaries and Cannibals Problem with 
m missionaries and c cannibals will have an upper bound of 
`2(m+1)(c+1)`
 states (without considering their legality).

##### Diagram
A graphical representation of the first couple depths of states is shown below:
![](missionaries and cannibals diagram.pdf)

### Code Design:
There are 4 different modules in the code: CannibalProblem.py, SearchSolution.py, cannibals.py, and uninformed_search.py.  

##### CannibalProblem.py
This file contains the definition for the `CannibalProblem` object, meant to model a Missionaries and Cannibals problem.  It has the following information:

*Data*

`start_state` - a tuple of the form `(int, int ,int)`, which reflects the starting state of the current Missionaries and Cannibals problem, stored a `CannibalProblem` object.

`goal_state` - a tuple of the form `(int, int, int)`, which reflects the goal state of the Missionaries and Cannibals problem, stored in a `CannibalProblem` object.

`total_missionaries` - an integer that is the total number of missionaries in the Missionaries and Cannibals problem at any time (assuming none are eaten).  It is the same as `start_state[0]`.

`total_cannibals` - an integer that is the total number of cannibals in the Missionaries and Cannibals problem at any time. It is the same as `start_state[1]`.

*Functions*

`__init__(self, start_state=(3, 3, 1))` - constructor function that sets its corresponding `start_state` to given state (default `(3, 3, 1)`, `goal_state` to `(0, 0, 0)`, `total_missionaries` to `start_state[0]`, and `total_cannibals` to `start_state[1]`.

`get_successors(self, state)` - a function where given any state of the form `(int, int, int)` returns a set containing all legal successor states (in the given Missionaries and Cannibals problem).  If there are no legal successor states, it returns an empty set.

`is_legal(self, state)` - returns true if a given state is legal according to the given Missionaries and Cannibals problem, and false otherwise.

`goal_test(self, state)` - returns true if a given state is the same as the set `goal_state` in the `CannibalProblem` object.

`def __str__(self)` - returns information about current `CannibalProblem` object in string format.

##### SearchSolution.py
This file contains the definition for the `SearchSolution` object, meant to model a solution to some sort of problem (in this case, it is used for a Missionaries and Cannibals problem).  It has the following information;

*Data*

`problem_name` - the name of the problem, in string format.

`search_method` - the type of search used, in string format.

`path` - an array of states that start at the start state, and end at the goal state.

`nodes_visited` - an integer representing the number of nodes visited to reach the goal state from the start state.

*Functions*

`__init__(self, problem, search_method)` - constructor function that sets its corresponding `problem_name` to given `str(problem)`, `search_method` to given `search_method`, `path` to `[]`, and `nodes_visited` to 0.

`__str__(self)` - returns all data of corresponding `SearchSolution` object in string format, with some syntax to make it more readable.

##### cannibals.py
This file creates a few test `CannibalProblem`'s, and then outputs the results of different search methods (from `uninformed_search.py`) for each `CannibalProblem`

##### uninformed_search.py
This file contains the `SearchNode` object, as well as `bfs_search`, `no_solution`, `backchain`, `dfs_search`, and `ids_search` functions.

*SearchNode Data*

`state` - state object
`parent` - pointer to parent SearchNode

*SearchNode Functions*

`__init__(self, state, parent=None)` - constructor function that sets its corresponding `state` to given `state`, and `parent` to given `parent` (defaut value of `None`)

*Search Functions*

`bfs_search(search_problem)` - conducts a breadth-first search on given search problem, returns `SearchSolution` object

`dfs_search(search_problem, depth_limit=100, node=None, solution=None)` - conducts a path-checking, recursive depth-first search on given search problem, up to given `depth_limit` (default of 100).  

`ids_search(search_problem, depth_limit=100)` - conducts an iterative depth search, using `dfs_search` algorithm, up to and including given `depth_limit` (default of 100).

### Building the Model:

This model was built with the goal the keep the specific aspects of how the Missionaries and Cannibal problem works away from the search algorithms.  This was the case because if performed correctly, then it would be relatively easy to plug in other problems and use the same code as search algorithm implementations.  In other words, the intent of the code was to be modular.  In order for this to happen, some assumptions had to be made about the search problem that was passed to the algorithms.  The search algorithms assumed that the passed `search_problem` object had the following information: `start_state`, `goal_test(state)`, `get_successors(state)`.  Where `start_state` was some sort of representation of the search problem's start state, `goal_test(state)` returned true if the given state was the goal state of the search problem (false otherwise), and `get_successors(state)` returned a set of all legal successor states to a given state.

With these assumptions, the model could be built modularly, in a way that the search algorithm implementations should be able to work for other problems as well (has not been tested on other problems).

### Breadth-First Search:
I implemented my BFS search algorithm iteratively, using queue and set data structures.  As the queue is First In First Out, a path can be built by enqueueing the root node, and then constantly dequeueing each node from the queue, while enqueueing their successors.  The set is used to keep track of which nodes have already been visited in order to prevent infinite loops from occuring.  After the goal is found, the backchain function creates a corresponding `SearchSolution` object.  This function works by starting at the goal, and then putting the goal's predecessoror at the beginning of the path, and then putting that node's predecessor at the beginning of the path, and so on, until the start node is reached.

**Testing:**

In order to test my BFS algorithm, I ran it on a `CannibalProblem` with a `start_state` of `(3, 3, 1)`.  While doing so, I printed out each SearchNode's state after it was dequeued.  Below is the order in which they were printed out, with dashed lines to better discern each depth.  We can see that this corresponds to the nodes and depths shows in the initial diagram. (Note: illegal nodes were never returned by the `CannibalProblem` and repeat nodes were never added to the queue, so all that are shows are the legal nodes of each depth.

	(3, 3, 1)
	---------
	(3, 2, 0)
	(3, 1, 0)
	(2, 2, 0)
	---------
	(3, 2, 1)
	---------
	(3, 0, 0)
	---------
	(3, 1, 1)
	---------
	(1, 1, 0)
	---------
	(2, 2, 1)
	---------
	(0, 2, 0)
	---------
	(0, 3, 1)
	---------
	(0, 1, 0)
	---------
	(1, 1, 1)
	(0, 2, 1)
	---------
	(0, 0, 0)
	
To further conduct testing, I looked at the results of passing the `bfs_search` method a `CannibalProblem` object with `start_state = (3, 3, 1)`.  Below is the output:

	Missionaries and cannibals problem: (3, 3, 1)
	attempted with search method BFS
	number of nodes visited: 15
	solution length: 12
	path: [(3, 3, 1), (3, 1, 0), (3, 2, 1), (3, 0, 0), (3, 1, 1), (1, 1, 0), (2, 2, 1), (0, 2, 0), (0, 3, 1), (0, 1, 0), (1, 1, 1), (0, 0, 0)]
	
What is of note is that the solution length is 12.  According to this paper: `https://www.jstor.org/stable/pdf/3619658.pdf?refreqid=excelsior%3A6f3fcf0e4f3abed0a5f8d9f2e39a1355`
The optimal number of boat crossings of the `(3, 3, 1)` Missionaries and Cannibals problem is 11.  This is consistent with my result, because that means the solution length should be 12 if both the `start_state` and `goal_state` are included in the path.

**Discussion**
	
There appear to be multiple advantages to using breadth-first search.  For exampe, there is a guarentee that if there is a solution (assuming the state space is finite), then it will eventually be found by a BFS algorithm.  Also, this solution will be optimal; the path from start state to goal state will be the shortest possible.  

There are also some disadvantages.  It can be slow, as it may spend much time at low depth searches that are nowhere near the goal.  Also, it can use quite a bit of memory, as legal node stored in the queue and the set, which means that it is redundant, and thus requires quite a bit of memory.

### Memoizing Depth-First Search:
This can be implemented easily by using the BFS algorithm and then switching the queue to a stack.

**Memory**

Memoizing does not save significant memory compared to breadth-first search.  This is because it also uses a visited set to keep track of nodes that have have already been visited, making the memory similar to that of Breadth-First Search.  In fact, it is possible for Memoizing Depth-First Search to consume more memory than Breadth-First Search, if it finds the goal after visiting more node sthan Breadth-First Search.

### Path-Checking Depth-First Search:
Another version of depth-first search is the recursive Path-Checking Depth-First Search, which only keeps track of states on the path.

**Memory**

Path-Checking Depth-First Search does save significant memory with respect to Breadth-First Search.  This is because there is no visited set, instead successor nodes are checked to ensure that ecah node has not been visited again.  So, the only item stored in memory must be the path from start to goal (recall BFS stores the path and the visited set).  There are some potential sacrifices that are made in order for such memory advantages.  One is that Path-Checking DFS is not optimal.  In other words, it does not necessarily find the shortest path from start to goal.  Also, there are potential runtime sacrifices, as Path-Checking DFS (or any DFS in fact) may spend much time sarching down nodes that will not lead to the goal, whereas BFS will seach all potential pathways equally as fast, potentially finding the goal faster.  

Here is an example of a diagram where Path-Checking DFS is much slower than BFS:
![](bfs vs dfs.pdf)
In this case, BFS would find the Goal Node after the 3rd iteration and be done, but Path-Checking DFS would iterate through every node in the graph before it found the goal node.

**Testing:**

In order to test my Path-Checking DFS, I ran both BFS and Path-Checking DFS on a `CannibalProblem` object with `(5, 4, 1)` as its starting state.  From there, I compared the results:

BFS:

	Missionaries and cannibals problem: (5, 4, 1)
	attempted with search method BFS
	number of nodes visited: 30
	solution length: 16
	path: [(5, 4, 1), (4, 3, 0), (5, 3, 1), (3, 3, 0), (4, 3, 1), (3, 2, 0), (3, 3, 1), (2, 2, 0), (3, 2, 1), (2, 1, 0), (2, 2, 1), (1, 1, 0), (2, 1, 1), (1, 0, 0), (1, 1, 1), (0, 0, 0)]

DFS (Path-Checking):

	Missionaries and cannibals problem: (5, 4, 1)
	attempted with search method DFS
	number of nodes visited: 19
	solution length: 18
	path: [(5, 4, 1), (4, 3, 0), (5, 3, 1), (3, 3, 0), (4, 3, 1), (3, 2, 0), (3, 3, 1), (2, 2, 0), (3, 2, 1), (2, 1, 0), (2, 2, 1), (1, 1, 0), (2, 1, 1), (1, 0, 0), (1, 1, 1), (0, 1, 0), (0, 2, 1), (0, 0, 0)]
	
We can see that the DFS did indeed find a path longer than the BFS, which makes me inclined to think that it works.  Also of interst is that it it visited quite a few fewer nodes (11 to be precise) than the BFS.  That means that Path-Checking DFS was able to find a (non-optimal) pathway early on, compared to BFS.  (Note: while it may seem very unlikely that the DFS only visited one more node that its solution length, it is important to recall that many potential states down the tree are illegal, which means the the DFS does not have many potential successor states to visit during each recursion.)

### Iterative Deepening Search:
Iterative Deepening Search is a search that runs Depth First-Seach with incrememting depth limits, stopping when the goal is found.  This will hence return an optimal path using DFS-eqsue algorithms.  

**Path-Checking vs Memoizing:**

It appears that Path-Checking DFS should be used.  First from a time-perspective, it seems like there is little difference between Path-Checking and Memoizing DFS.  This is because both select nodes to visit in a similar manner, and both have the same potential run-time advantages/disadvantages compared to BFS.  They can both either get lucky and find the goal early on without visiting much of the graph, but they can also both be unlucky and visit much of the graph before finding a goal node close to the start node.  Since DFS is being ran many times in an IDS algorithm, it makes sense that IDS has to sacrifice run-time compared to BFS.  But, we see that Path-Checking DFS is much more memory efficent than Memoizing DFS.  This is because Memoizing DFS uses a visited set, while Path-Checking only stores the nodes of the path from start to goal.  In fact, there are no memory advantages that Memoizing DFS really has compared to BFS, so if Memoizing DFS was used for IDS, there seems to be little advantage compared to BFS.  Hence, it makes sense that Path-Checking DFS is the best DFS search algorithm to use for the IDS search algorithm.

**Testing:**

In order to test my IDS search algorithm (which used by Path-Checking DFS algorithm), I ran it on the same `CannibalProblem` object that I used for the Path-Checking DFS testing (see above).  Below are the results (I included BFS and DFS results here as well for readability).

BFS:

	Missionaries and cannibals problem: (5, 4, 1)
	attempted with search method BFS
	number of nodes visited: 30
	solution length: 16
	path: [(5, 4, 1), (4, 3, 0), (5, 3, 1), (3, 3, 0), (4, 3, 1), (3, 2, 0), (3, 3, 1), (2, 2, 0), (3, 2, 1), (2, 1, 0), (2, 2, 1), (1, 1, 0), (2, 1, 1), (1, 0, 0), (1, 1, 1), (0, 0, 0)]

DFS (Path-Checking):

	Missionaries and cannibals problem: (5, 4, 1)
	attempted with search method DFS
	number of nodes visited: 19
	solution length: 18
	path: [(5, 4, 1), (4, 3, 0), (5, 3, 1), (3, 3, 0), (4, 3, 1), (3, 2, 0), (3, 3, 1), (2, 2, 0), (3, 2, 1), (2, 1, 0), (2, 2, 1), (1, 1, 0), (2, 1, 1), (1, 0, 0), (1, 1, 1), (0, 1, 0), (0, 2, 1), (0, 0, 0)]

IDS:

	Missionaries and cannibals problem: (5, 4, 1)
	attempted with search method IDS
	number of nodes visited: 1082
	solution length: 16
	path: [(5, 4, 1), (4, 3, 0), (5, 3, 1), (3, 3, 0), (4, 3, 1), (3, 2, 0), (3, 3, 1), (2, 2, 0), (3, 2, 1), (2, 1, 0), (2, 2, 1), (1, 1, 0), (2, 1, 1), (1, 0, 0), (1, 1, 1), (0, 0, 0)]
	
Based off of these results, I am inclined to think that my IDS search algorithm is working properly.  That is beacuse its behavior is what I would expect.  For starters, the number of nodes visited is much larger than both BFS and DFS, which makes sense because IDS is the tally of all the nodes that DFS visited.  Next, the solution length is the same as that of the BFS, and shorter than DFS.  That makes sense, because now the IDS search algorithm has successfully found the optimal path, which BFS also does.  The DFS algorithm is suboptimal, which explains why its solution path is longer.  Finally, the solution path of IDS is similar to that of the DFS path, where at the end it reaches the goal after the `(1, 1, 1)` state, rather than the dillydallying that the DFS algorithm partakes in.  This makes sense, because the DFS that found the goal was limited in depth, so it was essentially forced to recurse to the successor that yielded the goal state.

### Lossy Missionaries and Cannibals:
**Problem State:**

The new state would look like `(m, c, b, e)`, where `m` is the number of missionaries, `c` is the number of cannibals, `b` indicates which side the boat is on, and `e` is the number of missionaries that have already been eaten.

**Code Changes:**

It it would be possible to implement this by changing the `is_legal` function in `CannibalProblem.py`.  The "general" rule return statement (line 42 and 43) could be modified to an if statement instead, where if the general rule is the case, the function returns true, else return `e <= E-1` (-1 because a missionary will get eate, so it is necesary to preserve the state's legality.

Perhaps, it would also be possible to assign different values to states that do and don't kill missionaries, and then change the search algorithms to react accordingly to such value differences.  That way, the algorithms will prioritize not killing missionaries, but is still capable of doing so if it is absolutely necessary.

**Possible States Upper Bound:** 

We see that for all states in the original loss-free Missionaries and Cannibals problem, there are now `(E+1)` states.  So by the product principle, there are `2(m+1)(c+1)(E+1)` states now (without considering legality).

### Further Exploration:
**Wavefront BFS:**

I implemented a Wavefront BFS search from the goal node.  Given a `search_problem` object and a `depth_level` (integer), it outputs some syntax and every possible start node that has a path to the goal node at that depth level.  In order to do this, I had to write a `get_predecessors(self, state)` function for the `CannibalProblem` object, which works very similar to how the `get_successors(self, state)` works, but instead shows states that occured before the given state, instead of after.  Also, in order to check legality, the `get_predecessors(self, state)` function does not consider the `total_missionaries` and `total_cannibal` numebrs, as it is discovering new start states, with new potential totals for missionaries and cannibals.  There is one quirk, where at even depth levels, (where the boat aspect of the state is set to `0`), one would have to increase the `total_missionaries` and `total_cannibals` values by at most 2.  This is because the boat is on the other side, so the first step is going to involve bringing missionaries and cannibals back to the original side, which is going to increase the `m` and `c` values of the next state object.

In order to test, I ran the WFS search with a `CannibalProblem` object with `start_state = (3, 3, 1)`, and `depth_level = 11`.  From previous results, we know that the solution length of the path from `(3, 3, 1)` to `(0, 0, 0)` is 12, so the nodes should be a depth of 11 from each other (because counting depth does not include both the start state and the goal state).  The following was my output:

	WFS search
	goal state: (0, 0, 0)
	depth level: 11
	possible start states: {(0, 1, 1), (6, 0, 1), (1, 0, 1), (3, 3, 1), (5, 2, 1), (0, 2, 1), (0, 5, 1), (4, 0, 1), (4, 3, 1), (5, 1, 1), (2, 0, 1), (0, 6, 1), (6, 1, 1), (3, 1, 1), (3, 2, 1), (7, 0, 1), (0, 3, 1), (4, 1, 1), (1, 1, 1), (5, 0, 1), (2, 2, 1), (0, 4, 1), (2, 1, 1), (0, 7, 1), (4, 2, 1), (3, 0, 1)}

As we can see, `(3, 3, 1)` is a member of the possible start states list, so I am inclined to think that my WFS search algorithm works properly.  This could potentially be used to compile a list of valid starting states that will lead to the goal state.  It could potentially be interesting to know what versions of the Missionaries and Cannibals Problem is not solveable at much higher missionary and cannibals counts.  For example, from BFS search, we discovered that there was no solution to a Missionaries and Cannibal Problem with `start_state = (5, 5, 1)`

**Bi-Directional Search:**

I also attempted to implement a bi-directional search (BDS).  This works by conducting a BFS search at both the start and goal nodes, and ending when the two searches meet eachother.  In theory this should visit fewer nodes than the normal BFS search.  The results of the BDS search that I wrote can be gotten from running the `cannibals.py` file.  But to summarize, I found that my number of nodes visited were higher than that of the BFS search.  So, I essentially achieved the opposite of what the point of BDS is.  Furthermore, my implementation of BDS uses more memory than BFS because it includes a set of visited nodes from the start node, as well as a set of visited nodes from the goal node.  Hence, my implementation of BDS was strictly worse than my implementation of BFS.  I think that had I more time, I would have been able to optimize the BFS to perform better than my BFS search.  I suspect that my implementation of BDS does not stop looping immediately when the two searches meet, and instead at a later point in time, which would explain the larger quantity of nodes visited.  To make it work, I had to use the same `get_predecessors` function that I used in my WFS implementaition.  This was necessary to find the children nodes for the search nodes of the goal state side portion of the search.