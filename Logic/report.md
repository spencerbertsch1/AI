# Logic

Assignment 5  
CS 276, Artificial Intelligence  
Fall 2021, Dartmouth College  
Spencer Bertsch

This report contains two sections: 
1. Description
2. Evaluation

### TODO Add encode/decode to the code after writing the report 

Add CNF for map coloring (Not state1, Not state 2 if they are touching, etc.)

# Description

1. How do your implemented algorithms work?

### Understanding Propositional Logic & .cnf Files

TODO Explain conjunctive normal form files

Ivor Spence, etc. 

### GSAT
TODO

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