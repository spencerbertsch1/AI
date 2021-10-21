# Constraint Satisfaction Problems

Assignment 4  
CS 276, Artificial Intelligence  
Fall 2021, Dartmouth College  
Spencer Bertsch

This report contains three sections, as seen below:
* Description
* Evaluation
* Responses to Discussion Questions

# Description
* How do your implemented algorithms work? 
### Backtracking Search 

TODO 

### AC-3 Algorithm 

TODO 

### MRV Heuristic

TODO 

### Degree Heursitic

TODO 

### LCV Heuristic 

TODO 

* What design decisions did you make? 

Because this assignment had no skeleton code, I set up the construction of the general CSP problem as a "general" CSP object. The methods 
of the CSP object provide the CSP solver with the backtracking search algorithm, the AC-3 algorithm, as well as each of the heuristics which 
can be enabled or disabled when the CSP object is instantiated. 

In order to instantiate the CSP object, you need to pass in the variables **x**, the domains **d**, and the constraints **c**. 
In addition to the variables, domains, and constraints, the CSP object also takes an instance of the *solution* object which it updates during the search. 
This is very similar to the way that we have been keeping track of performance for the other search methods in earlier assignments. 
Once the CSP instance has been created, you can call the backtracking_search() method which runs backtracking on the problem and returns the solution object, 
providing both the solution and the number of nodes visited during the search.

The CSP object works dynamically to solve 'any' constraint satisfaction problem. The backtracking method, AC-3 method, and all heuristic 
methods work the same way for the map-coloring and circuits problems. 

* How you laid out the problems?

I laid out the two problems by first creating a single, central class called CSP. The CSP class, as mentioned above, is capable of solving any similarly structured constraint satisfaction
problem as long as the constraints are passed in as a list of tuples (in the case of map coloring), or the constraints can be found dynamically during th search (in the case of the circuits problem). 

In order to test each problem, I created two files: *map_coloring.py* and *circuits.py* which each contain the variables, domains, and constraints for 
each problem. You can test each problem by running each of these files as executable scripts.

# Evaluation

### Do your implemented algorithms actually work? How well?

After much tinkering the CSP solver now works as expected for each problem. 

The optimal solution for the map-coloring problem was found after searching 7 nodes, and the optimal solution to the 
circuits' problem was found after searching 19 nodes. The heuristics and inference generally improved or did not change the performance
of the algorithms. In the case of map-coloring, the optimal performance was achieved when all of the heuristics and inference were activated
at the same time. 

### Optimal solution for the map-coloring problem:

```
Constraint Satisfaction Problem: Map Coloring 
Nodes Visited: 7 
Answer: {'WA': 'blue', 'SA': 'green', 'NT': 'red', 'Q': 'blue', 
         'NSW': 'red', 'V': 'blue', 'T': 'blue'}
```

The above result was generated when inference and all heuristics were turned on. See the below table for an overview of the CSP performance 
for the map-coloring problem. 

|               | Backtracking Alone | W/ Inference | W/ LCV | W/ Degree Heuristic | W/ MRV | W/ All Turned On |
|---------------|--------------------|--------------|--------|---------------------|--------|------------------|
| Nodes Visited | 11                 | 10           | 8      | 11                  | 11     | 7                |

*Table showing Map-Coloring performance with different combinations of inference and heuristics*

As seen in the above table, the best performance for the map-coloring problem as achieved when all heuristics and inference 
is turned on. 

<p align="center">
    <img src="https://github.com/spencerbertsch1/AI/blob/main/ConstraintSatisfaction/docs/austraila.png?raw=true" alt="australia" width="55%"/>
</p>

*Graphic showing a feasible map-coloring solution found using the generic CSP solver*

This is one of the many viable solutions to this map coloring problem. Another solution, for example, could easily be found by exchanging all 
green variables with red variables and vice versa. The initialization of the problem - the ordering of the variables and the constraints that 
we pass into the solver - dictate the solution found and returned by the backtracking search. 

### Optimal solution for the circuits problem:

The circuits problem was also solved by the generic CSP solver, yielding different feasible solutions as different combinations of heuristics and 
inference are activated and deactivated. 

```
-------------- CIRCUIT BOARD LAYOUT --------------
 ['c', 'c', '.', 'e', 'e', 'e', 'e', 'e', 'e', 'e'] 
 ['c', 'c', 'b', 'b', 'b', 'b', 'b', 'a', 'a', 'a'] 
 ['c', 'c', 'b', 'b', 'b', 'b', 'b', 'a', 'a', 'a'] 

Constraint Satisfaction Problem: Circuit Design 
Nodes Visited: 19 
Answer: {(3, 2): (7, 1), (5, 2): (2, 1), (2, 3): (0, 0), (7, 1): (3, 0)}
```

Note that the solution to this problem, like the map coloring problem, is not unique. The below diagram and the console log show different solutions produced
by the CSP solver using different heuristics. Each solution is acceptable, but using different heuristics for each problem simply improves performance of the algorithm
by reducing the number of nodes that need to be visited during each search.

<p align="center">
    <img src="https://github.com/spencerbertsch1/AI/blob/main/ConstraintSatisfaction/docs/circuit_diagram.png?raw=true" alt="sensorless_diagram" width="55%"/>
</p>

See below for another board design generated by the CSP solver when different heuristic are activated. 

```
-------------- CIRCUIT BOARD LAYOUT --------------
 ['a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'c', 'c'] 
 ['a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'c', 'c'] 
 ['e', 'e', 'e', 'e', 'e', 'e', 'e', '.', 'c', 'c'] 
```


# Responses to Discussion Questions

1. Describe the results from the test of your solver with and without heuristic, and with and without inference on the map coloring problem.

The map-coloring problem's performance is improved slightly when inference it turned on, and the performance is improved even further when heuristics are turned on as well. 
The optimal solution (in which only 7 nodes are visited before a solution is found) can be achieved when inference and all the heuristics are activated. See the below table for a 
look at how the heuristics and inference impact the performance of backtracking on the map-coloring problem. 

|               | Backtracking Alone | W/ Inference | W/ LCV | W/ Degree Heuristic | W/ MRV | W/ All Turned On |
|---------------|--------------------|--------------|--------|---------------------|--------|------------------|
| Nodes Visited | 11                 | 10           | 8      | 11                  | 11     | 7                |

*Table showing Map-Coloring performance with different combinations of inference and heuristics*

2. Describe the domain of a variable corresponding to a component of width w and height h, on a circuit board of width n and height m.  Make sure the component fits completely on the board.

The size of the domain would be [(n-w)*(m-h)]. The piece can shift to the right until it hits the right wall, leaving (n-w) spaces open from the origin (0,0). 
Similarly, moving the piece up will cause it to run into the top of the board, leaving (m-h) many spaces below the piece. 

The piece will be able to move in a grid which will be a subset of the (n*m) grid created by the board. The domain of the piece will exist as this smaller
grid with height (m-h) and width (n-w). 

More specifically, we could represent the domain as a list of tuples, each of which represents an [x,y] coordinate. We could start at the origin (0,0) and move right, 
adding tuples (1,0), (2,0) until we get to (n-w, 0). We could then move up and cover the next row, then the next, until we reached a height of (m-h). If we were adding values iteratively
from origin upwards, left to right, the last tuple coordinate added would be ((n-w), (m-h)).

3. Consider components a and b above, on a 10x3 board.  In your write-up, write the constraint that enforces the fact that the two components may not overlap.  Write out legal pairs of locations explicitly.



4. Describe how your code converts constraints, etc, to integer values for use by the generic CSP solver.

This is an interesting question; the generic CSP solver uses constraints in different ways based on the type of problem being solved. The 
constraints in the map-coloring problem are hard coded as a list of tuples, each tuple representing two variables (countries) that cannot be adjacent.
The constraints for the circuit design problem on the other hand are found dynamically as the logic in the *test_consistency* method yields legal and illegal
positions for pieces on the board. The conversion to integer values occurs in the *test_consistency* function in which each string value in the input to the 
problem is considered using logic that often converts the constraints, domains, and variables to integers, then returns a bool value. The majority of the generic 
CSP solver uses the exact same methods for each type of CSP problem, treating the inputs from either problem the same way. As mentioned, the *test_consistency* 
method is the main place where the generic CSP solver differs; one part of the function is designed for testing legality of the assignment for 
map-coloring, and the other part is designed to test legality for the layout of the circuit board. 

