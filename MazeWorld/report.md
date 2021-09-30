# MazeWorld

Assignment 2  
CS 276, Artificial Intelligence  
Fall 2021, Dartmouth College  
Spencer Bertsch

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
