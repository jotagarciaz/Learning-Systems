"""
	Source code created for DVA427 - Lärande System.
	Code writers:
		- Joaquín García Benítez.
		- Clara Torre García-Barredo.
	Code created on April 2019.
"""

from copy import deepcopy 
import math
import random
import numpy as np


GOAL='F'

""" First we need to extract values from the file"""
def read_files(file_name):

	file = open(file_name, "r") #city_1
	file.seek(0)
	nodes={}
	for line in file:
		line_split=line.split(" ", 3)
		origin=line_split[0]
		destiny=line_split[1]
		distance=int(line_split[2])
		route={destiny:distance}
		inverse_route={origin:distance}
		if destiny not in nodes:
			nodes.update({destiny:inverse_route})
		else:
			nodes[destiny].update(inverse_route)
		if origin not in nodes:
			nodes.update({origin:route})
		else:
			nodes[origin].update(route)
	
	for k,n in nodes.items():
		n = sorted(n.items(), key=lambda x:x[1])
		nodes[k]=n

	return nodes

def bellman(nodes):
	visited = [] #type: list
	solutions = [] #type: list
	aux=np.array(([],np.inf))
	bellman_list = np.array([aux for i in range(len(nodes)-1)]) #type: list
	#bellman_list[0] = [[GOAL], 0]
	solutions.append([[GOAL], 0])
	visited.append(GOAL)
	for index, node in enumerate(nodes[GOAL]):
		bellman_list[index] = [[GOAL, node[0]],node[1]]
	
	while len(bellman_list) > 0:
		
		min_value = min(bellman_list[:,1])
		min_index = np.where(bellman_list[:,1]==min_value)[0][0]
		min_node = bellman_list[min_index]
		last_node = nodes[min_node[0][-1]]
		for index, node in enumerate(last_node):
			if node[0] not in visited:
				in_bellman = False
				for el_in, el_v in enumerate(bellman_list[:,0]):
					if node[0] in el_v:
						if (min_value + node[1] < bellman_list[el_in,1]):
							bellman_list[el_in] = [deepcopy(min_node[0]), min_value + node[1]]
							bellman_list[el_in,0].append(node[0])
						in_bellman = True
				if not in_bellman:
					new_ind = np.where(bellman_list[:,1] == np.inf)[0][0]
					bellman_list[new_ind] = [deepcopy(min_node[0]),node[1]+min_value]
					bellman_list[new_ind,0].append(node[0])
		solutions.append(min_node)
		visited.append(min_node[0][-1])
		bellman_list = np.delete(bellman_list,min_index,0)

	#End while

	for element in solutions:
		aux = element[0]
		aux.reverse()
		element[0] = aux
	
	return solutions

def main():
	nodes = read_files("/Users/clara/Documents/GitHub/Learning-Systems/assignment 4/city_1")

	result = bellman(nodes)
	for solution in result:
		print("Path:", solution[0], "Distance:", solution[1])

main()      



#print(proccess.memory_info().rss)