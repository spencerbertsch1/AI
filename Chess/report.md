# Chess

Assignment 3  
CS 276, Artificial Intelligence  
Fall 2021, Dartmouth College  
Spencer Bertsch

This report contains three sections, as seen below:
* Description
* Evaluation
* Responses to Discussion Questions

# Description

1. How do your implemented algorithms work? 

### Minimax 

The minimax algorithm works by taking some current state of a graph (in this case a board object) and iterating over all the possible moves
that one of the players could make. For each iteration, it calls *min_value()*, one of the two recursive parts of the Minimax algorithm. 
For each move, the *min_value()* function makes recursive calls to *max_value()* which calls *min_value()*, etc. until the game is complete, or a depth limit has been reached. 
Once a base case is reached, a utility value *u* gets passed back up through the recursive calls to the outer function, and that *u* value is then 
associated with the initial, given move. 

This is how vanilla minimax works! The time complexity of MiniMax is O(b^m) where b is the branching factor (number of legal moves in our case), and 
m is the max depth of the tree, or in our depth limited search, the MAX_DEPTH parameter. The space complexity is only O(b*m) because as each space is searched, 
we don't need to keep all old nodes in memory because that part of the game has already been played and we no longer need the information stored in that part of the tree. 
As we can see, the time complexity is clearly the limiting constraint for the MiniMax algorithm. We can see this empirically later on when time tests are 
run for different MAX_DEPTH values for depth-limited minimax. 

### Depth-Limited Minimax

Same as above, but we just make sure to add the MAX_DEPTH to the minimax so that we don't have to search the entire tree. For a game such as chess where 
b=35 and m~=100, so the time needed to explore the entire space would be incredibly large, making the problem intractable. 

### Alpha Beta Pruning

Same as MiniMax but with a few added constraints that gave a significant performance increase to the run time of the algorithm.
(See imperical time tests for examples of increased performance)

Note that node ordering would increase the performance even more to O(b^(m/2)), but with random ordering I acheived performance closer to 
O(b^(3m/4)), which is still much better than the vanilla Minimax's O(b^m). 

### Iterative Deepening Minimax 

Same as minimax, but we run for multiple depths and choose the best utility for all depths. 


2. What design decisions did you make?

For Minimax IDS-Search, I stored all the 'best_moves' in an outer dictionary so that I could keep track of if/how they changed. Doing this allowed me to 
look at how the utility function was calculating the relative utility of different moves on the same board because it had the capability to explore to different 
depths. I know the assignment mentioned that it would also be a good idea to create an instance variable *self.best_move*, and although this would also be a perfectly 
reasonable implementation, using a dictionary instead allowed me to easily keep track of how the best move changes as MAX_DEPTH changes. 



# Evaluation

1. Do your implemented algorithms actually work? How well? 

Testing the performance of the different implementations of minimax and alpha beta pruning was initially a difficult task, but by examining factors such as 
the number of nodes visited along with doing timed performance tests, it was easy to see how well each algorithm performed. 

Depth-limited Minimax performs as expected.

When the MAX_DEPTH is set to 1, the Minimax player can clearly see a single turn ahead, but no more. It will trade a queen for a pawn if that looks like the 
best move in that position, even if that places the queen in a very vulnerable position later on. When MAX_DEPTH is set to 2, Depth-limited Minimax displays much better 
performance. It plays more definsively, keeping most important players back until there is a clear opportunity to take an opponent's piece without sacrificing anything. 

Alpha Beta performs the same as Minimax under identical conditions, but Alpha Beta is much faster. 

TODO show that they play the same (screenshots) 

TODO performance test with timings (table)
TODO performance test with number of nodes visited (table)