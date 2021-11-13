# Hidden Markov Models

Assignment 6  
CS 276, Artificial Intelligence  
Fall 2021, Dartmouth College  
Spencer Bertsch

This report contains two sections:
1. Description
2. Evaluation

# Description

1. How do your implemented algorithms work?  

### Filtering 


### Filtering Part 1


### Filtering Part 2


### Filtering Part 3

As we can see the ground truth state of the robot is (1, 3), and the highest probability 
in the current state probability matrix is also at (1, 3) followed closely by the other 
likely position of the robot: (0, 2). 


<p align="center">
    <img src="https://github.com/spencerbertsch1/AI/blob/main/HiddenMarkovModels/docs/solution_iteration_0.svg?raw=true" alt="sensorless_diagram" width="60%"/>
</p>

*Figure 1: Ground truth function of the starting state with the robot in cell (0, 0). The state refelcts an equal probability of the robot 
in any of the states that it sees are blue.*

<p align="center">
    <img src="https://github.com/spencerbertsch1/AI/blob/main/HiddenMarkovModels/docs/solution_iteration_3.svg?raw=true" alt="sensorless_diagram" width="60%"/>
</p>

*Figure 2: Ground truth function of state at time t=3 with the robot in cell (1, 0). After only three moves, we can already see
that the Current state lists the true location as the most probable, but we can get better!*

<p align="center">
    <img src="https://github.com/spencerbertsch1/AI/blob/main/HiddenMarkovModels/docs/solution_iteration_9.svg?raw=true" alt="sensorless_diagram" width="60%"/>
</p>

*Figure 3: Ground truth function of state at time t=9 with the robot in cell (3, 0). Here we can see that after 9 iterations we 
get a better result in which the state matrix shows a probability of the ground truth is 0.75*
