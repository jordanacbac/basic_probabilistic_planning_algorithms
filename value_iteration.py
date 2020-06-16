from argparse import ArgumentParser
import numpy as np
import pandas as pd
import re

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

def iterative_policy_evaluation():
	return

def bellman_backup(states, states_view):

	# Creating dataframe from states
	df = pd.DataFrame(states)
	# Giving the only column a name (states)
	df.columns = ['states']

	# Setting states as dataframe index
	df.set_index('states', inplace=True)
	print(df)

	# Transposing the dataframe
	df_t = df.T
	print(df_t)

	# Next steps: Calculate Q*(state, action) and V*(state)
	
	return (0)

def value_iteration():
	return
	
if __name__ == '__main__':

	# Creating script argument to indicate the problem file that must be read
	parser = ArgumentParser()
	parser.add_argument("-f", "--file", dest="filename", help="file to be read", metavar="FILE")
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
	#print(states)
	
	# Calling the method responsible to create the dict of actions
	actions = create_actions(content_list)
	#print(actions)

	# Calling the method responsible to create the list of costs
	costs = create_costs(content_list)
	#print(costs)
	
	# Calling the method responsible to read the initial and the goal state
	initial, goal = create_initial_and_goal_states(content_list)
	#print(initial, goal)

	# Generating states view to run value iteration algorithm
	# states_view is a dictionary in which states are keys and their values are lists containing applicable actions and their costs. It does not contain the resulting state from the action.
	states_view = create_states_view(costs)

	teste = bellman_backup(states, states_view)

	'''# Temporary file to store the actions (for validation purpose only)
	file2 = open("MyFile2.txt", "w+")
	file2.write(str(actions))'''

	#df = pd.DataFrame(content)
	#print(df.head())

	## Proximo passo: checar a melhor estrutura de dados para armazenar os estados e gerar a matriz
	## O que pretendo fazer: criar um dataframe e converter para numpy array depois.
	## https://stackoverflow.com/questions/26173486/create-matrix-with-column-names-and-row-names-in-python/28380345