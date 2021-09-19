# Chickens and Foxes

Assignment 1  
Artificial Intelligence - Fall 2021  
Dartmouth College  
Spencer Bertsch

## Problem Definition & Discussion

The problem definition was adapted from the assignment on [gradescope.](https://www.gradescope.com/courses/297527/assignments/1483539/submissions/new)

There are three chickens and three foxes that have found themselves on one side of a river with a single boat.
Our job is to model this situation as a graph, then use uninformed search algorithms to find a solution that gets all chickens and foxes safely to the other side of the river.

Starting State:
* (3, 3, 1) - (3 chickens, 3 foxes, and 1 boat)

Constraints:
* Only two animals can fit in the boat at one time.
* In order for the boat to move from bank to bank, one animal must be in the boat to row.
* If there are ever more foxes than chickens on either bank of the river, then the chickens will get eaten.

### Upper Bound on States

The upper bound on the number of states, given that the starting state is (3, 3, 1) is 20 states including the start state.
The number of all possible states -- legal or illegal -- can be thought of as the combinatorial set of all integers with
maximum values of 3, 3, and 1. Ignoring the boat/not boat and simply examining the chickens and foxes, we can see that the set of available states
is: {(3,3), (2, 3), (3, 2), (2, 2), (2, 1), (1, 2), (1, 1), (1, 0), (0, 1), (0, 0)}.

From this we can conclude that adding a binary variable to the state definition (boat or not boat) would double the number of possible states.
See the below figure for a look at each of the 20 unique states.

![all_vertices](/Users/spencerbertsch/Desktop/dev/CS/AI/ChickensAndFoxes/docs/all_vertices.png)

* **Note:** I also have PDF copies of all figures under the `docs` directory in the ChickenAndFoxes assignment. I couldn't figure out 
how to embed local PDF files into markdown docs, but if the TAs have some example code for that I will surely use that method
in the future. For now please refer to the PNG files in the markdown and the PDF copies with the same names in the `docs` directory if more clarity is needed. 
