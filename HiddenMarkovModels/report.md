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

This problem uses a Hidden Markov Model to approximate the location of a robot as it takes random actions (N, S, E, W) across an n x n board. 
The board squares are each colored either red, yellow, green, or blue, and the robot's only sensor is a color sensor pointing down 
that is not always quite accurate. However! The robot knows what the board looks like before it starts, but it doesn't know where it's starting from. 
The job of the filtering algorithm is to generate a probability distribution that eventually finds the most probable position of the robot simply given its
transitions between colors as the robot moves across the board. 

The implemented algorithm is a filtering algorithm which takes a series of sensor readings - *E(t)* - and produces a probability matrix
representing the distribution representing the likely locations of the robot for a certain time (t). 

There are two important components to this problem: 
1. The Sensor Model
2. The Transition Model 

### The Sensor Model

In this case the sensor model is a little different than the implementation we saw in the textbook because we have a robot that could be 
in any one of *n* positions on a board. In order to generate a correct sensor model, we need to understand the performance of the sensor being used
to detect the colors of the board. At each time step (t), the robot moves (might hit a wall and stay in the same position) and a color is read by the sensor. 
After the color is read, then the sensor model can be generated in the filtering algorithm by giving a 0.88 probability to the colors in the map 
that match the color that was just sensed, and a 0.04 probability to all other colors. This reflects the performance of the sensor attached to the robot. 

For example, if the robot were in the top left position of the following board: 

```
['B', 'G', 'R', 'Y']
['Y', 'B', 'R', 'R']
['R', 'Y', 'G', 'R']
['B', 'G', 'G', 'B']
```

Then the sensor reading would likely be Blue. In that case, the Sensor Model would look like this: 

```
[0.88, 0.04, 0.04, 0.04]
[0.04, 0.88, 0.04, 0.04]
[0.04, 0.04, 0.04, 0.04]
[0.88, 0.04, 0.04, 0.88]
```

The sensor model reflects an equal probability of the robot being in any of the blue cells. 

### The Transition Model


# Evaluation

After much bug fixing, the filtering algorithm is working exactly as expected. In addition to the printed output, I also used 
matplotlib to generate some heatmaps showing how similar the *Current State* is to the actual ground truth location of the robot at time (t). 
In addition to the heatmaps, there is of course also the printed output showing the performance of the filtering algorithm and the current state at each time 
step. Example output can be seen below: 

```
 Output for Time t=12
----- Prediction Vector -----
[0.04, 0.88, 0.04, 0.04]
[0.04, 0.04, 0.04, 0.04]
[0.04, 0.04, 0.88, 0.04]
[0.04, 0.88, 0.88, 0.04]
----- Ground Truth: X12 -----
[0, 0, 0, 0]
[0, 0, 0, 0]
[0, 0, 0, 0]
[0, 1, 0, 0]
----- Current State -----
[0.00191096 0.01706248 0.00039611 0.00021325]
[1.82056894e-03 1.99524254e-02 4.24476130e-04 3.93714434e-05]
[2.08457428e-02 1.27343151e-03 4.25105696e-01 1.11806422e-04]
[0.00297936 0.46610947 0.04080118 0.00095368]
```

We can see from the above output that the *Current State* at time t=12 has a probability of 0.466 for the robot being in location (3, 1) modeled where the origin is 
in the upper left corner. Sometimes the sensor produces a faulty reading, causing the *Current State* to be inaccurate, but after another one or two time steps with accurate sensor readings 
the state reflects the true location of the robot again. 

See below for an example run showing heatmaps for the ground truth and the *Current State* at times t=0, t=3, and t=9. As time progresses, the state becomes more and more accurate, yielding a higher and higher probability for 
where the robot actually exists in the maze. As mentioned before, if the sensor were to produce a faulty reading for a time step, then the distribution of the *Current State* might seem like a poor model for that time step, but the accuracy of the state 
is remedied after one or two accurate sensor readings. 

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
