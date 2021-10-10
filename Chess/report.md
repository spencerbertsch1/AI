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

Depth-limited Minimax, Alpha Beta pruning, and Minimax with depth-limited search all perform as expected.


### Depth-limited Minimax

Testing the performance of the different implementations of minimax and alpha beta pruning was initially a difficult task, but by examining factors such as
the number of nodes visited along with doing timed performance tests, it was easy to see how well each algorithm performed.

When the MAX_DEPTH is set to 1, the Minimax player can clearly see a single turn ahead, but no more. It will trade a queen for a pawn if that looks like the 
best move in that position, even if that places the queen in a very vulnerable position later on. When MAX_DEPTH is set to 2, Depth-limited Minimax displays much better 
performance. It plays more defensively, keeping most important players back until there is a clear opportunity to take an opponent's piece without sacrificing anything. 

### Alpha Beta Pruning

Alpha Beta performs the same as Minimax under identical conditions, but Alpha Beta is much faster visiting far fewer nodes and requiring 
much less time to run. In order to ensure the algorithm performs the same as Minimax (makes the same decisions in the same situations), I ran 
a series of manual tests by playing games between a human_player (me) and either Minimax or Alpha Beta. See the appendix for a few of the decisions 
that were made by Minimax and by Alpha Beta, showing that they made the same decisions in the same environment. 



TODO performance test with timings (table)
TODO performance test with number of nodes visited (table)

One thing that took me a while to figure out, that I initially mistook for a bug, was that the Minimax or Alpha Beta algorithm seemed to make
misplays in the late game. After most of the opposing player's pieces were taken, the Minimax or Alpha Beta algorithm would miss the opportunity
to take a high value piece from the opposing team and move a rook or pawn on the other side of the board instead. The reason for this behavior is that the
utility function values putting the opponent in check above all else, so later in the game when the opposing player's king is exposed more often, the
Minimax or Alpha Beta player would ignore all opportunities to take knights, rooks, bishops, or even queens if it meant they could put the other
player in check.

Although this was generally an acceptable way to play, it allowed the opponent to make much more aggressive plays, putting their
queen in danger in order to take an important piece as long as they could protect their king from check mate. In order to counteract this, I experimentally
changed the utility associated with putting the opponent in check until other plays such as taking their queen were more valuable. This strategy
worked somewhat well, but each methodology has trade-offs. Ultimately a better solution would be to have a dynamic utility function that is
better at representing the state of the board. The textbook describes other pitfalls of the simplistic approach that we have
implemented including the horizon problem, and I can see that using an algorithm with learned parameters that are updated through repeated simulation
might be better equipped to deal with difficult utility calculations. 

# Appendix

This is an example of how the Minimax and Alpha Beta algorithms make the same decision with identical board states. In this case white is a human player, 
and black is Minimax or Alpha Beta. For this first move (white d2d4), the Minimax or Alpha Beta chooses the first of many moves with max utility, pushing 
their knight into the board. 

<p align="center">
    <img src="https://github.com/spencerbertsch1/AI/blob/main/Chess/docs/1.png?raw=true" alt="sensorless_diagram" width="50%"/>
</p>

Similar to the first move, white advances the pawn and the Minimax / Alpha Beta algorithm chooses one of the many max utility moves which happens to 
be to continue to advance their knight. 

<p align="center">
    <img src="https://github.com/spencerbertsch1/AI/blob/main/Chess/docs/2.png?raw=true" alt="sensorless_diagram" width="50%"/>
</p>

This is where things start to get interesting, now that there is a clear move that increases the utility for black, the Minimax / Alpha Beta algorithms 
take the white pawn with no drawbacks. 

<p align="center">
    <img src="https://github.com/spencerbertsch1/AI/blob/main/Chess/docs/3.png?raw=true" alt="sensorless_diagram" width="50%"/>
</p>

Lastly, after a very foolish move by white leaving the queen exposed, the Minimax / Alpha Beta algorithms move in and take the queen with the bishop, 
largely increasing the relative utility for black. 

<p align="center">
    <img src="https://github.com/spencerbertsch1/AI/blob/main/Chess/docs/4.png?raw=true" alt="sensorless_diagram" width="50%"/>
</p>