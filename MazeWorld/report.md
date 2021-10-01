# MazeWorld

Assignment 2  
CS 276, Artificial Intelligence  
Fall 2021, Dartmouth College  
Spencer Bertsch

# Description


# Evaluation

## Multi-Robot Coordination Problem
The multi-robot coordination proboem is working as expected. The robots seem to work together, moving out of tunnels and reorienting themselves 
in the correct way before re-entering tight spaces so that they can all reach their intended targets. See below for a somewhat long example of how 
three robots (A, B, and C) coordinate to orient themselves so that they can enter the tunnel in the correct allignment. 

```
#######
#.#####
#.#####
#C#####
#B....#
#A#####

...

#######
#A#####
#B#####
#C#####
#.....#
#.#####
```

There were two real keys to this problem: understanding that the heuristic should apply to the robots as a whole, and the get_successors function should 
store the information regarding which robot's turn it is to move. 

## Blind Robot Evaluation
After many hours of changing the heuristic function and implementation, the blind robot functionality essentially works as expected. 

Lets imagine a trivial maze with no blocks and only floor space. The robot could reduce the state space by either a row or column by simply 
moving either north or south, then moving either east or west until there is only one remaining space left. That is the result we
see when running test_sensorless.py on the trivial sensorless maze: 
```
....
....
....
```

And we can see that we get the expected output below. Note that the solution length is one larger than it should be because the initial 
SensorlessNode was initialized with a direction of None. 

```
Solution found! Path to solution: [None, 'North', 'North', 'East', 'East', 'East']
SOLUTION PATH LENGTH: 6
```

The solutions for nontivial sensorless problems always seem to be missing the last direction in the path. (See below). It looks like the sensorless A* search always 
converges on the correct solution, but it doesn't print the last move (direction) in the path. I'm still trying to figure out why! 

```
...#
.#..
```

This input, as seen from our quiz a few days ago, renders the following output: 

```
Solution found! Path to solution: [None, 'North', 'East']
SOLUTION PATH LENGTH: 3
```

We all know the real answer is North, East, East, so where is that last 'East'? If I had a little more time I'm sure I could fix the bug!  

# Discussion Questions

## Multi-robot coordination problem

1. Representing the state of the system correctly is one of the most important aspects of getting this problem right. The state of the system 
requires (2 * k robots) + 1 integers, or (2 * k robots) + 1 pieces of information about the state. This is clearly an odd number, so the smallest 
state would consist of 3 integers: (robot_to_move, X_position, Y_position). In this case there is only a single robot, so the first integer would
always be zero. As the number of robots in the game increases, then we would increase the number of ints in the state from 3 to 5, then to 7, then to 9
and so on. Each robot adds an additional X, Y coordinate to the state and an additional increment to the first int in the state telling the A* algorithm 
which robot's turn it is to move next. Structuring the state in this way is one of the keys of setting up the multi-robot coordination problem correctly.


2. An upper bound on the number of states in the system can be found by thinking about the way we represented the state. We represent the state
with a tuple (k, m, m, ...) for a square maze of length m and k robots where the first robot is represented by 0. 
The upper bound on the size of the state would be m\*m\*(k+1) if k starts with 0 as represented in my implementation, or (m\*m\*k). 


3. As the number of wall squares increases, collisions will increase as well. Boxing the robots in so that they are stuck in hallways or paths will force robots to 
collide and potentially back out of a hallway in order to reorient themselves to reach the desired goal. In terms of an expression, I 
would probably need to run a simulation in which I generate random, large mazes with differing wall densities and measure the number of 
robot-robot collisions that take place during the search for each maze. Without doing this, I could say that the number of collisions can 
be expressed by *collisions = (alpha(w)/n) + epsilon* for some small constant epsilon and a scaling factor alpha. Epsilon and alpha in this case would 
depend on *n*, and the larger *n* is the smaller epsilon would be. Similarly, we include an *n* term when we consider *w* so that we can get the relative density 
of the maze instead of simple the number of walls.


4. Good question, I think that BFS would probably not be a good solution here because it would likely cause the machine to run out of memory. 
We know that if n is 100, there are very few walls, and k=10, then each iteration will likely present a very large state space. We know that BFS
holds all previous states in memory, giving it a space complexity of O(b^d). With 10 robots capable of moving North, South, East, or West, the 
branching factor could be as large as 40, and the depth of the shallowest solution (in the worst case) would be 99 moves north or south, and 99 moves east or west
for a single robot, which makes depth = 198. This means that the space complexity for this problem would be on the order of 1.6*10^317 bytes assuming 1000 bytes per node in the BFS graph.


5. In addition to understanding how to represent the state space for the problem, understanding the right way to represent the heuristic is for multi-robot search
is a key to success. There are many admissible or consistent heuristic that can be used for a simple two-dimensional puzzle such as this, but 
an example of a monotonic (consistent) heuristic that I used was the mean manhattan distance for all robots to all goals. Remember that monotonicity or 
consistency just means that the heuristic at any node *n* is not greater than the heuristic at the next node *n'* plus the cost of reaching *n'*.

<p align="center">
    h(n) ≤ h(n') + c
</p>

5. (Continued) The mean manhattan distance for all robots is monotonic because the fuel needed to move one square is 1. In the worst case, even if the 
robot is moving in the exact opposite direction from its goal (which does sometimes happen), consistency is held because the cost would be 1
and the new heuristic *h(n') would increase by 1, allowing the inequality to hold strongly. For the mean manhattan heuristic, and the manhattan, heuristic in general,
moving laterally also yields the same result in which the cost increase is added to the additional heuristic, allowing the inequality to strongly hold. In the case where the robot is 
moving directly towards its goal, then the *h(n')* term would be one less than *h(n)*, but the cost *c* in this case would be exactly 1, allowing the 
inequality to hold.


5. The 8-puzzle in the book is a special case of this problem because each numbered square in the 8-puzze can be treated as a robot! Each numbered square 
has a starting state and a goal state and each needs to work together to get into the goal state. I think that A* and our implementation could be used to 
implement the 8-puzzle. As discussed in class, a good heuristic to use would be the overall manhattan distance for the all game pieces and all goal states. 

6. The 8-puzzle can be represented by two mutually disjoint sets which can be represented by solvable start states and unsolvable start states. XXXXX TODO 


# APPENDIX

### Multi-Robot Search Complete Example 
Please see below for a complete example of a multi-robot search problem whereall three robots needed to shift their orientation in order to achieve the goal state. 

```
#######
#.#####
#.#####
#C#####
#B....#
#A#####

MazeWorld problem:

#######
#.#####
#.#####
#C#####
#B....#
#A#####

MazeWorld problem:

#######
#.#####
#.#####
#C#####
#.B...#
#A#####

MazeWorld problem:

#######
#.#####
#.#####
#C#####
#.B...#
#A#####

MazeWorld problem:

#######
#.#####
#.#####
#C#####
#AB...#
#.#####

MazeWorld problem:

#######
#.#####
#.#####
#C#####
#A.B..#
#.#####

MazeWorld problem:

#######
#.#####
#.#####
#C#####
#A.B..#
#.#####

MazeWorld problem:

#######
#.#####
#.#####
#C#####
#.AB..#
#.#####

MazeWorld problem:

#######
#.#####
#.#####
#C#####
#.AB..#
#.#####

MazeWorld problem:

#######
#.#####
#.#####
#.#####
#CAB..#
#.#####

MazeWorld problem:

#######
#.#####
#.#####
#.#####
#CAB..#
#.#####

MazeWorld problem:

#######
#.#####
#.#####
#.#####
#CAB..#
#.#####

MazeWorld problem:

#######
#.#####
#.#####
#.#####
#.AB..#
#C#####

MazeWorld problem:

#######
#.#####
#.#####
#.#####
#A.B..#
#C#####

MazeWorld problem:

#######
#.#####
#.#####
#.#####
#AB...#
#C#####

MazeWorld problem:

#######
#.#####
#.#####
#.#####
#AB...#
#C#####

MazeWorld problem:

#######
#.#####
#.#####
#A#####
#.B...#
#C#####

MazeWorld problem:

#######
#.#####
#.#####
#A#####
#B....#
#C#####

MazeWorld problem:

#######
#.#####
#.#####
#A#####
#B....#
#C#####

MazeWorld problem:

#######
#.#####
#A#####
#.#####
#B....#
#C#####

MazeWorld problem:

#######
#.#####
#A#####
#B#####
#.....#
#C#####

MazeWorld problem:

#######
#.#####
#A#####
#B#####
#C....#
#.#####

MazeWorld problem:

#######
#A#####
#.#####
#B#####
#C....#
#.#####

MazeWorld problem:

#######
#A#####
#B#####
#.#####
#C....#
#.#####

MazeWorld problem:

#######
#A#####
#B#####
#C#####
#.....#
#.#####
```