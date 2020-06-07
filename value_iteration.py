from argparse import ArgumentParser
import numpy as np
import pandas as pd

def create_states(content_list):
	states = []

	for pos in range(len(content_list)):
		if(content_list[pos] == "states"):
			states.append(content_list[pos+1].split(', '))
	
	return (states)

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
	
	#df = pd.DataFrame(content)
	#print(df.head())



	## Proximo passo: checar a melhor estrutura de dados para armazenar os estados e gerar a matriz
	## O que pretendo fazer: criar um dataframe e converter para numpy array depois.
	## https://stackoverflow.com/questions/26173486/create-matrix-with-column-names-and-row-names-in-python/28380345