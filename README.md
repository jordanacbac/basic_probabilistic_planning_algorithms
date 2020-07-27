# Basic Probabilistic Planning Algorithms

This project was developed to represent simple (without information) probabilistic planning algorithms. The group used Stochastic Short-Path Markovian Decision Process (SSP MDP), whose characteristic is the lack of information on the number of actions to be taken, but it is known that this quantity is finite, because when a goal state is reached, no further action is taken.

The following algorithms were implemented:

1. Value Iteration
2. Policy iteration

Both should be used to solve problems modeled as Markovian Decision Processes (MDPs) in the gridworld domain.
The outputs include the policy (like in the image below), the number of iterations until convergence and the time in milliseconds spent by the algorithm.


# To execute the script:
Open the terminal and run the following command:

```python value_and_policy_iteration.py -f "domain_file_address" -pp "proper_policy_file_address" -r number_of_grid_lines -c number_of_grid_columns```

To check the help instructions:

```python value_and_policy_iteration.py -h```


# Final comments:
The code was developed for Topics in Planning in Artificial Intelligence subject as part of the Information Systems course from Universidade de São Paulo (USP) in 2020. The group is composed by:
- [dHirabara](https://github.com/dHirabara)
- [jordanacbac](https://github.com/jordanacbac)
- [laurakohatsu](https://github.com/laurakohatsu)
- [Rodrigump](https://github.com/Rodrigump)
