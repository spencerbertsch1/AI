# LOGIC

Assignment 5  
CS 276, Artificial Intelligence  
Fall 2021, Dartmouth College  
Spencer Bertsch

## To run the code:

1. Clone [this github repository](https://github.com/spencerbertsch1/AI.git) locally and `cd` into the `AI` directory.
   Alternatively, if you acquired this code from a zip file, simply unzip the file locally, `cd` into the `AI` directory, and continue to Step 2.
   In order to run any of the test scripts in this repository, you will need python 3.
    1. If you don't have python 3 installed, you can install Anaconda and create a new Conda environment using the following command:
        1. `$ conda create -n CS-276 python=3.8`
    2. Then activate the new environment by running the following command:
        1. `$ conda activate CS-276`
    3. Then proceed to the following step.


2. `cd` to the Logic directory by running the following command:
    1. `$ cd Logic`

### To Run GSAT Search for Map Coloring:
3. Ensure that the 'algorithm' variable is set to 'gsat', as noted on line 64. 
   1. `algorithm: str = 'gsat'`

4. Run the following command to run the run_sat.py file.
    1. `$ python3 run_sat.py`

### To Run WalkSAT Search for Map Coloring:
3. Ensure that the 'algorithm' variable is set to 'walksat', as noted on line 64.
    1. `algorithm: str = 'walksat'`

4. Run the following command to run the run_sat.py file.
    1. `$ python3 run_sat.py`

### To Run WalkSAT Search for Map Coloring:
5. Ensure that the 'algorithm' variable is set to 'walksat', as noted on line 64. Also ensure that the **puzzle_name** and **problem_type** variables are both set to 
'map_coloring' on lines 69 and 71.
   ```
   algorithm: str = 'walksat'
   ...
   puzzle_name: str = 'map_coloring'
   ...
   problem_type: str = 'map_coloring'
   ```
6. Run the following command to run the run_sat.py file.
   1. `$ python3 run_sat.py`

Feel free to change the configuration in the run_sat.py to experiment with different *p* values or test the algorithms
on different .cnf puzzle files. 