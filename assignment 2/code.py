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
#import matplotlib.pyplot as plt

f = open("/Users/clara/Documents/GitHub/Learning-Systems/assignment 2/iris", 'r')
f.seek(0)
n_lines_to_read = len(f.readlines())
LINE_LEN=5

MIDDLE=0.25
s = 0
m = 1
l = 2
SETOSA = 1
VERSICOLOR = 2
VIRGINICA = 3

def num(s):
	try:
		return int(s)
	except ValueError:
		return float(s)

""" First we need to extract values from the file"""
def read_file():
	f.seek(0)
	result=np.zeros(n_lines_to_read)
	data_set=np.zeros((n_lines_to_read,LINE_LEN-1))
	for i in range(0, n_lines_to_read): 
		aux = f.readline()
		aux=aux.split(" ", LINE_LEN)
		line=np.zeros(len(aux)-1)
		for j in range(0,len(aux)-1):
			line[j]=(num(aux[j]))
			
		data_set[i]=line.copy()
		result[i]=int(aux[-1])
			 
	return data_set,result


def normalize(data):
	set=np.vstack(data)
	for i in range(len(set[0])):
		minimum=min(set[:,i])
		maximum=max(set[:,i])
		data[:,i]=(data[:,i]-minimum)/(maximum-minimum)

	return data

def main():
	data,result=read_file()

	data=normalize(data)

	hits=np.zeros(3)
	counter = np.zeros(3)
	for e in range(len(data)):
		x_values = [] #type: list
		element=data[e]
		result_e=result[e]
		for i in range(4):
			x_values_row = [] #type: list
			#Short:
			short = 1 - element[i]/MIDDLE
			if short < 0:
				short = 0
			x_values_row.append(short)
			#Middle:
			if element[i] <= MIDDLE:
				middle = element[i]/MIDDLE
			else:
				middle = 1 - (element[i]-MIDDLE)/(1-MIDDLE)
			if middle < 0:
				middle = 0
			x_values_row.append(middle)
			#Long:
			long = (element[i]-MIDDLE)/(1-MIDDLE)
			if long < 0:
				long = 0
			x_values_row.append(long)
			x_values.append(x_values_row)

		#Calculate the truth values of the rules.
		truth_values = [] #type: list
		#Rule 1:
		truth_values.append((x_values[0][s] + x_values[0][l])*(x_values[1][m] + x_values[1][l])*(x_values[2][m] + x_values[2][l])*x_values[3][m])
		truth_values.append((x_values[2][s] + x_values[2][m])*x_values[3][s])
		truth_values.append((x_values[1][s] + x_values[1][m])*x_values[2][l]*x_values[3][l])
		truth_values.append(x_values[0][m]*(x_values[1][s] + x_values[1][m])*x_values[2][s]*x_values[3][l])

		rule = truth_values.index(max(truth_values))

		if rule == 0 or rule == 3:
			output = VERSICOLOR
			if result_e == output:
				hits[1] += 1
			counter[1] += 1
		elif rule == 1:
			output = SETOSA
			if result_e == output:
				hits[0] += 1
			counter[0] += 1
		elif rule == 2: 
			output = VIRGINICA
			if result_e == output:
				hits[2] += 1
			counter[2] += 1  

	print("contadores:",sum(counter))
	print(hits/50)
	print("Total hits:", sum(hits))
	print("Accuracy:", (sum(hits)/150)*100, "%")
main()