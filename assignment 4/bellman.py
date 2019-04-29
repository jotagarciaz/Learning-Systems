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

	return nodes 

def main():
	nodes = read_files("/Users/jgarcia/Documents/Learning Systems/assignment 4/city_1")

	result = bellman(nodes)
	print(result)  

main()      



#print(proccess.memory_info().rss)