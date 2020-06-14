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

	return (actions)

def iterative_policy_evaluation():
	return

def bellman_backup():
	return

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
	print(states)
	
	# Calling the method responsible to create the dict of actions
	actions = create_actions(content_list)
	print(actions)

	# Temporary file to store the actions (for validation purpose only)
	file2 = open("MyFile2.txt", "w+")
	file2.write(str(actions))



	#df = pd.DataFrame(content)
	#print(df.head())



	## Proximo passo: checar a melhor estrutura de dados para armazenar os estados e gerar a matriz
	## O que pretendo fazer: criar um dataframe e converter para numpy array depois.
	## https://stackoverflow.com/questions/26173486/create-matrix-with-column-names-and-row-names-in-python/28380345