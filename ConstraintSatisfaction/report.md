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

### AC-3 Algorithm 

### MRV Heuristic

### Degree Heursitic

### LCV Heuristic 

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

The optimal solution for the map-coloring problem was found after searching 8 nodes, and the optimal solution to the 
circuits' problem was found after searching 26 nodes. The heuristics and inference generally improved or did not change the performance
of the algorithms, and in some cases the heuristics caused the circuits' problem to visit more nodes than vanilla backtracking with no 
heuristics at all. 

Optimal solution for the circuits problem:

```
Constraint Satisfaction Problem: Circuit Design 
Nodes Visited: 26 
Answer: {(2, 3): (0, 0), (3, 2): (2, 0), (7, 1): (2, 2), (5, 2): (5, 0)}
```

From this answer we can see the below solution was found after visiting only 26 nodes in the constraint graph. Although some heuristics improved
the performance in the map-coloring problem by reducing the number of nodes visited, the number of nodes visited in the circuits problem for vanilla backtracking, 
backtracking with inference (AC-3) and backtracking with the degree heuristic all produced an optimal solution in which 26 nodes were visited during the search. 

<p align="center">
    <img src="https://github.com/spencerbertsch1/AI/blob/main/ConstraintSatisfaction/docs/circuit_diagram.png?raw=true" alt="sensorless_diagram" width="55%"/>
</p>

For 


# Responses to Discussion Questions

Responses here 
