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

def iterative_policy_evaluation(df, states_view, proper_policy, goal):#df iteracao de Vpi
	t = time.time()
	for i in df.columns:
		df.loc[0, i] = random.randint(0,10)
	
	df_residual = df.copy()
	for i in df_residual.columns:
		df_residual.loc[0, i] = 999
	df_residual.loc[0, goal] = 0

	epsilon = 0.1
	n = 1
	for state in df.columns:
		PIn = proper_policy[state]
		if(state != goal):
			Vpin = policy_evaluation(state, PIn, df, states_view, n)
			df_residual.loc[n-1, state] = abs(Vpin - df.loc[n-1, state]) 
			df.loc[n, state] = Vpin
		else:
			df_residual.loc[n-1, state] = 0
			df.loc[n, state] = 0
	# TODO: while max residual < epsilon
	while(True):
		n += 1
		
		for state in df.columns:
			if(state == goal):
				df_residual.loc[n-1, state] = 0
				df.loc[n, state] = 0
				continue
			# calculate bellman backup
			#agr ao inves de receber o melhor valor recebe a melhor acao, acao q tem menor custo
			PIn = bellman_backup(state, states_view, df, n, 1)
			Vpin = policy_evaluation(state, PIn, df, states_view, n)

			#compute residual
			df_residual.loc[n-1, state] = abs(Vpin - df.loc[n-1, state]) 

			# update Value
			df.loc[n, state] = Vpin

		# check epsilon
		df_check = df_residual.loc[n-1]
		#print(df_check)
		max_residual = float(df_check.max())
		#print(max_residual)
		if max_residual < epsilon:
			break
	t = time.time() - t
	print("Policy iteration: " + str(n) + " iterations, runtime: " + str(t) )

	return
def policy_evaluation(state, action, df_values, states_view, n):
	for i in states_view[state]:
		if(action in i[0]):#acao escolhida,calcular Vn
			if len(i) == 4:
				return ( float(i[1]) + float(df_values.loc[n-1, i[2]] ) )
			else:
				# if it has more than 1 result, compute the probability
				Q_value = 0
				for num_states in range (2, len(i), 2):
					Q_value += ( float(i[num_states+1]) * float(df.loc[n-1, i[num_states]]) )
				return (float(i[1]) + Q_value ) 

def bellman_backup(state, states_view, df, n, ret):#devolve Q do estado na iteracao n
	#ret = 0: retorna valor; ret = 1: retorna acao
	# Next steps: Calculate Q*(state, action) and V*(state)
	#df vai ser a tabela com tds valores de cada iteracao n
	#Calc Q*
	# get actions
	actions = states_view.get(state)
	Q = [] #para devolver menor valor
	best_action = "" #para devolver melhor acao
	if actions is not None:
		for action in actions:
			# check if it has more than 1 state for each move
			if len(action) == 4:
				Q.append( float(action[1]) + float(df.loc[n-1, action[2]] ) )
			else:
				# if it has more than 1 result, compute the probability
				Q_value = 0
				for num_states in range (2, len(action), 2):
					Q_value += ( float(action[num_states+1]) * float(df.loc[n-1, action[num_states]]) )
				Q.append(float(action[1]) + Q_value ) 
		if(ret == 0):
			return( min(Q) )	
		else:
			index = Q.index(min(Q))
			if(index==0): return 'south'
			elif(index==1):return 'north'
			elif(index==2): return 'west'
			else: return 'east'

def value_iteration(df, states_view, goal):
	# Pseudo random numbers generated by the following seed:
	random.seed(324)
	
	t = time.time()

	# Generating the pseudo random numbers for each state (numbers interval from 0 to 10):
	for i in df.columns:
		df.loc[0, i] = random.randint(0,10)
	#print(df)

	# df.loc[0, 'robot-at-x1y1'] = 'aaaa' # posicao do valor
	# print(df)
	df_residual = df.copy()
	for i in df_residual.columns:
		df_residual.loc[0, i] = 999
	df_residual.loc[0, goal] = 0

	epsilon = 0.1
	n = 0
	# TODO: while max residual < epsilon
	while(True):
		n += 1

		for state in df.columns:

			#nao sei como tratar
			if state == goal:
				df.loc[n, state] = 0
				df_residual.loc[n-1, state] = 0
				continue

			# calculate bellman backup
			Vn = bellman_backup(state, states_view, df, n, 0)

			#compute residual
			df_residual.loc[n-1, state] = abs(Vn - df.loc[n-1, state]) 

			# update Value
			df.loc[n, state] = Vn

		# check epsilon
		#print(df_residual)
		df_check = df_residual.loc[n-1]
		#print(df_check)
		
		max_residual = float(df_check.max())
		#print(max_residual)
		if max_residual < epsilon:
			break


	t = time.time() - t
	print("Value iteration: " + str(n) + " iterations, runtime: " + str(t) )

	return



if __name__ == '__main__':

	# Creating script argument to indicate the problem file that must be read
	#parser = ArgumentParser()
	#parser.add_argument("-f", "--file", dest="filename", help="file to be read", metavar="FILE")
	#args = parser.parse_args()
	
	# Generating a list for the file content and reading it
	content_list = []
	with open("C:/Users/fmassato/Downloads/TestesGridFixedRandom/TestesGrid/FixedGoalInitialState/navigation_1.net") as file:
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
	# states_view is a dictionary in which states are keys and their values are lists containing applicable actions and their costs, followed by the resulting states and their probabilities.
	states_view = create_states_view(costs)
	# print(states_view)
	
	# Calling the method responsible to create a dataframe from the list of states
	df = create_df_states(states)

	# Next steps:
	value_iteration(df, states_view,goal)

	with open("C:/Users/fmassato/Downloads/PoliticasPropiasFixedRandomParaAlgoritmoIteracaoPolitica/PoliticasFixedRandom/FixedGoalInitialState/navigation_1.net_politicas.json") as json_file:
		proper = json.load(json_file)
	iterative_policy_evaluation(df,states_view,proper,goal)
	## Proximo passo: checar a melhor estrutura de dados para armazenar os estados e gerar a matriz
	## O que pretendo fazer: criar um dataframe e converter para numpy array depois.
	## https://stackoverflow.com/questions/26173486/create-matrix-with-column-names-and-row-names-in-python/28380345