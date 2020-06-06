from argparse import ArgumentParser
import numpy as np

def iterative_policy_evaluation():
	return

def bellman_backup():
	return

def value_iteration():
	return
	
if __name__ == '__main__':

	parser = ArgumentParser()
	parser.add_argument("-f", "--file", dest="filename", help="file to be read", metavar="FILE")
	args = parser.parse_args()
	
	with open(args.filename) as file:
		content = file.readlines()
		print(content)

	## Proximo passo: checar a melhor estrutura de dados para armazenar os estados e gerar a matriz
	## Primeiras hipoteses: numpy e pandas
	## Numpy eh mais eficiente, porem nao estou conseguindo encontrar uma maneira de registrar o titulo das colunas (que seriam correspondentes aos estados).
	## Pandas eh para trabalhar com operacoes aplicadas aos indices, e nao eh isso que queremos.