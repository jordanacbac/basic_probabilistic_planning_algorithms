from argparse import ArgumentParser
import numpy as np
import pandas as pd
import re
import random
import time
import json

def create_states(content_list):
	# States are represented by a list
	states = []

	for pos in range(len(content_list)):
		# Identifying the line that precedes the states
		if(content_list[pos] == 'states'):
			# Appending all the states
			states.append(content_list[pos+1].split(', '))
	
	return (states[0])

def create_actions(content_list):
	# Actions are represented by a dictionary
	actions = {}
	# Defining regex to catch the action's name
	pattern = '^action .*'
	
	for pos in range(len(content_list)):
		# Identifying the line containing the action's name
		if(re.match(pattern, content_list[pos])):
			# Generating a key with the action's name and receiving an empty list as value 
			actions[str(content_list[pos]).replace('action ', '')] = []
			new_pos = pos + 1
			# Loop responsible for all the action details storage
			while(content_list[new_pos] != 'endaction'):
				actions[str(content_list[pos]).replace('action ', '')].append(content_list[new_pos].split(' '))
				new_pos += 1

	# If necessary, method to clean the actions (remove the discard element)
	actions = clean_actions(actions)
	return (actions)

def create_costs(content_list):
	# Costs are represented by a list
	costs = []

	for pos in range(len(content_list)):
		# Identifying the line that precedes the costs
		if(content_list[pos] == 'cost'):
			pos += 1
			while(content_list[pos] != 'endcost'):
				costs.append(content_list[pos].split(' '))
				pos += 1
			break

	return (costs)

def create_initial_and_goal_states(content_list):
	
	for pos in range(len(content_list)):
		if(content_list[pos] == 'initialstate'):
			init = content_list[pos+1]
		if(content_list[pos] == 'goalstate'):
			goal = content_list[pos+1]
	
	return (init, goal)

def clean_actions(actions):
	for action in actions:
		for item in actions.get(action):
			item.pop(3)
	
	return (actions)

def create_states_view(costs):
	states = []
	states_view = {}
	for element in costs:
		states.append(element[0])
	states = set(states)
	for state in states:
		states_view[state] = []
	
	for element in costs:
		for state in states:
			if (element[0] == state):
				states_view[state].append(element[1:])

	states_view_complete = states_view.copy()
	for state in states_view:
		for pos in range(len(states_view.get(state))):
			action = states_view.get(state)[pos][0]
			for act in actions:
				if (act == action):
					for el in actions.get(act):
						if (el[0] == state):
							states_view_complete.get(state)[pos].extend(el[1:])
	
	return (states_view_complete)

def create_df_states(states):
	# Creating dataframe from states
	df = pd.DataFrame(states)
	# Giving the only column a name (states)
	df.columns = ['states']

	# Setting states as dataframe index
	df.set_index('states', inplace=True)

	# Transposing the dataframe
	df_t = df.T

	return(df_t)

def iterative_policy_evaluation(df, states_view, proper_policy, goal, initial, last_state):
	# Making a copy of first proper_policy
	past_proper_policy = proper_policy.copy()
	
	# Structure to store current proper policy
	current_proper_policy = {}

	# t variable to count the algorithm execution time
	t = time.time()

	# Generating the pseudo random numbers for each state (numbers interval from 0 to 10) - V0 values:
	for col in df.columns:
		df.loc[0, col] = random.randint(0,10)

	# First iteration:
	n = 1
	for state in df.columns:
		# Receiving pi action for each state based on the proper policy first received 
		PIn = proper_policy[state]
		# If the state is not a goal, then it is necessary to:
		if(state != goal):
			# Calculate the approximation evaluation of PIn
			Vpin = policy_evaluation(state, PIn, df, states_view, n)
			# Update value
			df.loc[n, state] = Vpin
		# The cost of the goal to reach itself will always be zero
		else:
			df.loc[n, state] = 0

	# Other necessary iterations
	while(True):
		n += 1
		
		for state in df.columns:
			if(state == goal):
				# The cost of the goal to reach itself will always be zero
				df.loc[n, state] = 0
				current_proper_policy[state] = "-"
				continue

			# Calculates Bellman backup to return the best action (smallest cost)
			PIn = bellman_backup(state, states_view, df, n, 1)
			# Updates current_proper_policy with action returned from Bellman backup
			current_proper_policy[state] = PIn
			# Policy evaluation step
			Vpin = policy_evaluation(state, PIn, df, states_view, n)
			# Updates value
			df.loc[n, state] = Vpin
		
		# Stop condition: pi(n+1) == pi(n)
		if (past_proper_policy == current_proper_policy): 
			break
		
		# Updates past_proper_policy with the current policy
		past_proper_policy = current_proper_policy.copy()
		
		# Clears the current policy
		current_proper_policy.clear()
	
	t = time.time() - t
	print("Policy iteration: " + str(n) + " iterations, runtime: " + str(t) )
	
	# Calling method responsible for the grid visualization
	buildGrid(current_proper_policy, last_state, initial)

	return

# Method responsible for the policy evaluation. It computes V(n+1), the approximation evaluation of PIn
def policy_evaluation(state, action, df_values, states_view, n):
	
	for act in states_view[state]:
		# If the action is found in the list of possible actions for the state, then it is necessary to calculate Vn
		if(action in act[0]):
			# Checks if there is more than 1 resulting state for the action
			if (len(act) == 4):
				return (float(act[1]) + float(df_values.loc[n-1, act[2]]))
			# There is more than 1 resulting state for the action, so it is necessary to compute the probability
			else:
				Q_value = 0
				for num_states in range (2, len(act), 2):
					Q_value += ( float(act[num_states+1]) * float(df.loc[n-1, act[num_states]]) )
				return (float(act[1]) + Q_value) 

# Bellman backup algorithm calculates Qn(s, a) for each iteration (n) and returns the minimum value or best action 
def bellman_backup(state, states_view, df, n, ret):
	# ret = 0: returns value
	# ret = 1: returns action

	# Getting actions
	actions = states_view.get(state)
	
	# Q is used to return smallest value (in other words, best value)
	Q = []

	# best_action is self explanatory 
	best_action = ["none", 1000000]

	if actions is not None:
		for action in actions:
			# Checks if there is more than 1 resulting state for the action
			if (len(action) == 4):
				result = float(action[1]) + float(df.loc[n-1, action[2]])
				# Stores result in Q
				Q.append(result)
			# There is more than 1 resulting state for the action, so it is necessary to compute the probability
			else:
				Q_value = 0
				for num_states in range (2, len(action), 2):
					Q_value += ( float(action[num_states+1]) * float(df.loc[n-1, action[num_states]]) )
				result = float(action[1]) + Q_value
				# Stores result in Q
				Q.append(result)

			if (result < best_action[1]): 
					best_action[0] = action[0]
					best_action[1] = result

		if(ret == 0):
			return (float(min(Q)))	
		else:
			return (best_action[0])

def value_iteration(df, states_view, goal, initial, last_state):
	# Pseudo random numbers generated by the following seed:
	random.seed(324)
	
	# t variable to count the algorithm execution time
	t = time.time()

	# Generating the df responsible to store the best policies:
	df_result = df.copy()

	# Generating the pseudo random numbers for each state (numbers interval from 0 to 10):
	for col in df.columns:
		df.loc[0, col] = random.randint(0,10)

	# Creating dataframe to store residual
	df_residual = df.copy()
	for i in df_residual.columns:
		df_residual.loc[0, i] = 999

	# Both the cost of the goal to reach itself, and its residual will always be zero
	df.loc[0, goal] = 0
	df_residual.loc[0, goal] = 0

	# Defining epsilon as defined by the Professor
	epsilon = 0.1
	n = 0

	while(True):
		n += 1

		for state in df.columns:
			# If we are treating a goal state, then cost and residual are set as 0
			if state == goal:
				df.loc[n, state] = 0
				df_residual.loc[n-1, state] = 0
				continue

			# Computes Bellman backup
			Vn = bellman_backup(state, states_view, df, n, 0)

			# Computes residual
			df_residual.loc[n-1, state] = abs(Vn - df.loc[n-1, state]) 

			# Updates Value
			df.loc[n, state] = Vn

		# Checks epsilon
		df_check = df_residual.loc[n-1]
		
		# Receives max_residual
		max_residual = float(df_check.max())

		# Stop condition: max residual < epsilon
		if max_residual < epsilon:
			break

	t = time.time() - t
	print("Value iteration: " + str(n) + " iterations, runtime: " + str(t) )

	# Storing the best action for each state
	best_action={}
	for state in df_result.columns:
		best_action[state] = bellman_backup(state, states_view, df, n, 1)
	# Setting goal state equals to '-', so this won't be null 
	best_action[goal] = "-"
	
	# Calling method responsible for the grid visualization
	buildGrid(best_action, last_state, initial)

	return

# Method responsible for the grid visualization
def buildGrid(statesANDactions, lastState, initial):

	index = lastState.split("x")[1].split("y")
	grid = [ [ "*" for y in range(int(index[0])+1) ] for x in range(int(index[1])+1) ] 

	sort_states = sorted(statesANDactions.keys())
	action = ""
	for i in statesANDactions:
		if("north" in statesANDactions[i]): action = "↑"
		elif("south" in statesANDactions[i]): action = "↓"
		elif("east" in statesANDactions[i]): action = "→"
		elif("west" in statesANDactions[i]): action = "←"
		else: action = "G"
		index = str(i).split("x")[1].split("y")
		grid[int(index[0])][int(index[1])] = action

	index = initial.split("x")[1].split("y")
	if(grid[int(index[0])][int(index[1])] == "↑"): grid[int(index[0])][int(index[1])] ="▲"
	elif(grid[int(index[0])][int(index[1])] == "↓"): grid[int(index[0])][int(index[1])] ="▼"
	elif(grid[int(index[0])][int(index[1])] == "→"): grid[int(index[0])][int(index[1])] ="▶"
	elif(grid[int(index[0])][int(index[1])] == "←"): grid[int(index[0])][int(index[1])] ="◀"

	for x in reversed(grid):
		print(x)

	return


if __name__ == '__main__':

	# Creating script argument to indicate the problem file that must be read
	parser = ArgumentParser()
	parser.add_argument("-f", dest="filename", help="domain file to be read")
	parser.add_argument("-pp", dest="proper_policy", help="proper policy to start policy iteration")
	args = parser.parse_args()
	
	# Generating a list for the file content and reading it
	content_list = []
	with open(args.filename) as file:
		content = file.readlines()	
	
	# Replacing "\t", spliting the file on line breaks and filling in the list with the file's content
	for element in content:
		content_list.append(element.replace('\t', '').split('\n')[0])

	# Calling the method responsible to create the list of states
	states = create_states(content_list)
	
	# Calling the method responsible to create the dict of actions
	actions = create_actions(content_list)

	# Calling the method responsible to create the list of costs
	costs = create_costs(content_list)
	
	# Calling the method responsible to read the initial and the goal state
	initial, goal = create_initial_and_goal_states(content_list)

	# Generating states view to run value iteration algorithm
	# states_view is a dictionary in which states are keys and their values are lists containing applicable actions and their costs, followed by the resulting states and their probabilities.
	states_view = create_states_view(costs)
	
	# Calling the method responsible to create a dataframe from the list of states
	df = create_df_states(states)
	# To execute the slides example:
	#df.loc[0] = {'robot-at-x0y0': float(3), 'robot-at-x0y1': float(3), 'robot-at-x1y0': float(2), 'robot-at-x2y0': float(0), 'robot-at-x2y1': float(1), 'robot-at-x2y2': float(2)}

	# Calling value iteration method:
	value_iteration(df, states_view, goal, initial, states[-1])

	with open(args.proper_policy) as json_file:
		proper = json.load(json_file)	
	
	# Resetting the variable
	df = create_df_states(states)
	
	# Calling policy iteration method:
	iterative_policy_evaluation(df,states_view,proper,goal,initial,states[-1])