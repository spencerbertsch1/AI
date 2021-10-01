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

1. You would need 2 * k numbers, or (2 * number_of_robots) numbers to represent the robot state of the system. Each robot has an [X,Y] coordinate
and each robot is free to move in any direction as long as it's not being blocked by another robot or by a wall. We need to store the original map
in addition to the [X,Y] positions of all robots at any given time during their exploration. 


2. An upper bound on the number of states in the system can be found by thinking about the way we represented the state. We represent the state
with a tuple (k, m, m, ...) for a square maze of length m and k robots where the first robot is represented by 0. 
The upper bound on the size of the state would be m\*m\*(k+1) if k starts with 0 as represented in my implementation, or (m\*m\*k). 




6. The 8-puzzle in the book is a special case of this problem because each numbered square in the 8-puzze can be treated as a robot! Each numbered square 
has a starting state and a goal state and each needs to work together to get into the goal state. I think that A* and our implementation could be used to 
implement the 8-puzzle. As discussed in class, a good heuristic to use would be the overall manhattan distance for the all game pieces and all goal states. 

7. The 8-puzzle can be represented by two mutually disjoint sets which can be represented by solvable start states and unsolvable start states. XXXXX TODO 


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