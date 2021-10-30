# Logic

Assignment 5  
CS 276, Artificial Intelligence  
Fall 2021, Dartmouth College  
Spencer Bertsch

This report contains two sections: 
1. Description
2. Evaluation

### TODO Add encode/decode to the code after writing the report 

### TODO Add CNF for map coloring (Not state1, Not state 2 if they are touching, etc.)

# Description

1. How do your implemented algorithms work?

### Understanding Propositional Logic & .cnf Files

In order to understand how to solve this problem, we first need to understand the **.cnf** files provided for us to solve. 
The cnf (conjunctive normal form) files are filled with clauses representing the rules of sudoku. By taking an initial board and 
iterating through all the clauses in a **.cnf** file, we can test the board to find how many unsatisfied clauses there are. When the number 
of unsatisfied clauses reaches zero, then the search is finished, and we can return the current assignment. 

In our case, we are working with boolean values that are always separated by an 'or' (∨) symbol. In this way, all we need to do is loop through
our current assignment and compare each bool in each clause to the corresponding element of the assignment. If at least one of the assignment 
values alligns with the clause, then that clause is satisfied and we can continue. If no values in the assignment align with any values in the clause, then 
that clause is unsatisfied. 

For example, a clause might be: 

`~111 ~112`, or `~111 ∨ ~112`

This represents that the value `11`, or row[1], column[1] cannot have the values of both 1 and 2. Assignments such as `{111: True, 112: False}`, 
or `{111: False, 112: False}` would satisfy the clause. However, the assignment `{111: True, 112: True}` would *not* satisfy the clause because neither value in the assignment matches 
the truth values listed in the clause.

Additional information on the formulation of the sudoku problem as a satisfiability problem in conjunctive normal form can be found 
from Ivor Spence [here](http://www.cs.qub.ac.uk/~I.Spence/SuDoku/SuDoku.html).

### GSAT
GSAT is a search algorithm that is designed to solve satisfyability problems given a set of boolean logical expressions. In our case, the 
boolean logic expressions are in the form of **.cnf** files which we iterate through. 

### WALKSAT
TODO

### What design decisions did you make? How you laid out the problems?

All code is in the SAT.py file

Driver script is run_sat.py which can be used to run the solver on any of the **.cnf** files. 

I initially coded the solver using a direct assignment:

```
assignment: dict = {
    111: False, 
    112: True, 
    113: False, 
    ...
}
```

But this forces the solver to only work for this specific Sudoku problem. In order to fix this problem, 
I implemented an *encode/decode* dictionary which is used as a map between the assignment values and the cells in the sudoku board. 
This *encode/decode* mapper is what allowed me to also implement the map coloring problem using GSAT and WalkSAT. 

```
assignment_encode: dict = {
    111: 1, 
    112: 2, 
    113: 3, 
    ...
}

assignment_decode: dict = {
    1: False, 
    2: True, 
    3: False, 
    ...
}
```

This seemingly pedantic step is what allows the solver to become dynamic and applicable to any problem, not just the sudoku problems
in conjunctive normal form. 

TODO 

# Evaluation

1. Do your implemented algorithms actually work? How well? 

The implemented SAT solver works exactly as expected on all puzzles, including the puzzle1.cnf and puzzle2.cnf files. 

|                    | one_cell | all_cells | rows | rows_and_cols     | rules             | puzzle1           | puzzle2           |
|--------------------|----------|-----------|------|-------------------|-------------------|-------------------|-------------------|
| GSAT Iterations    | 5        | 306       | 378  | Unsolved after 2k | Unsolved after 2k | Unsolved after 2k | Unsolved after 2k |
| WalkSAT Iterations | 5        | 282       | 346  | 1,468             | 3,354             | 6,784             | 59,012            |
*Table 1: Results of the GSAT and WalkSAT local search algorithms on different .cnf puzzle files.*


I will say that unlike the solution that the professor posted on slack, I had to vary my **p** value through a large range of values before 
I was able to get my WalkSAT to find solutions to puzzle1 and puzzle2. I ended up using **p=0.85** for puzzle1 and **p=0.8** for puzzle2. 
Using these **p** values along with a value of **p=0.9** for all other puzzles, I was able to achieve the results in *Table 1*. 

Below we can see a solution to one of the sample problems: **puzzle2.cnf**

Puzzle 2 Solution: 
```
4 3 1 | 6 9 7 | 5 2 8
5 7 2 | 1 3 8 | 9 6 4
6 9 8 | 5 2 4 | 3 1 7
---------------------
8 4 9 | 7 6 2 | 1 5 3
2 5 6 | 8 1 3 | 7 4 9
7 1 3 | 9 4 5 | 2 8 6
---------------------
3 2 5 | 4 7 6 | 8 9 1
1 6 7 | 2 8 9 | 4 3 5
9 8 4 | 3 5 1 | 6 7 2
```