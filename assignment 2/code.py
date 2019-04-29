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
ACCURACY_REQUIRED = 0.9
MIDDLE=0.6

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
				middle = (element[i]-MIDDLE)/(1-MIDDLE)
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
		x1 = x_values[0].index(max(x_values[0]))
		x2 = x_values[1].index(max(x_values[1]))
		x3 = x_values[2].index(max(x_values[2]))
		x4 = x_values[3].index(max(x_values[3]))
		truth_values = [] #type: list
		truth1 = 0
		#Rule 1:
		if x1 == 0:
			truth1 += 1 - (element[0]/MIDDLE)
			if x2 == 1 and element[1] <= MIDDLE:
				truth1 += element[1]/MIDDLE
				if x3 == 1 and element[2] <= MIDDLE:
					truth1 += element[2]/MIDDLE
					if x4 == 1 and element[3] <= MIDDLE:
						truth1 += element[3]/MIDDLE
					elif x4 == 1:
						truth1 += (element[3]-MIDDLE)/(1-MIDDLE)
				elif x3 == 1 or x3 == 2:
					truth1 += (element[2]-MIDDLE)/(1-MIDDLE)
			elif x2 == 1 or x2 == 2:
				truth1 +=(element[1]-MIDDLE)/(1-MIDDLE)
		elif x1 == 2:
			truth1 += (element[0]-MIDDLE)/(1-MIDDLE)

		truth_values.append(truth1/4)
		
		truth2 = 0
		#Rule 2:
		if x3 == 0:
			truth2 += 1 - (element[2]/MIDDLE)
			if x4 == 0:
				truth2 += element[3]/MIDDLE
		elif x3 == 1 and element[2] <= MIDDLE:
			truth2 += element[2]/MIDDLE
			if x4 == 0:
				truth2 += element[3]/MIDDLE
		elif x3 == 1:
			truth2 += (element[2]-MIDDLE)/(1-MIDDLE)
		
		truth_values.append(truth2/2)

		truth3 = 0
		#Rule 3:
		if x2 == 0:
			truth3 += 1 - (element[1]/MIDDLE)
			if x3 == 2:
				truth3 += (element[2]-MIDDLE)/(1-MIDDLE)
				if x4 == 2:
					truth3 += (element[3]-MIDDLE)/(1-MIDDLE)
		elif x2 == 1 and element[1] <= MIDDLE:
			truth3 += element[1]/MIDDLE
			if x3 == 2:
				truth3 += (element[2]-MIDDLE)/(1-MIDDLE)
				if x4 == 2:
					truth3 += (element[3]-MIDDLE)/(1-MIDDLE)	
		elif x2 == 1:
			truth3 +=(element[1]-MIDDLE)/(1-MIDDLE)

		truth_values.append(truth3/3)

		truth4 = 0
		#Rule 4:
		if x1 == 1 and element[0] <= MIDDLE:
			truth4 += element[0]/MIDDLE
			if x2 == 0:
				truth4 += 1 - (element[1]/MIDDLE)
				if x3 == 0:
					truth4 += 1 - (element[2]/MIDDLE)
					if x4 == 2:
						truth4 += (element[3]-MIDDLE)/(1-MIDDLE)
			elif x2 == 1 and element[1] <= MIDDLE:
				truth4 += element[1]/MIDDLE
				if x3 == 0:
					truth4 += 1 - (element[2]/MIDDLE)
					if x4 == 2:
						truth4 += (element[3]-MIDDLE)/(1-MIDDLE)
			elif x2 == 1:
				truth4 +=(element[1]-MIDDLE)/(1-MIDDLE)
		elif x1 == 1:
			truth4 += (element[0]-MIDDLE)/(1-MIDDLE)
			
		truth_values.append(truth4/4)

		rule = truth_values.index(max(truth_values))
		if rule == 0 or rule == 3:
			output = 2
			if result_e == output:
				hits[1] += 1
			counter[1] += 1
		if rule == 1:
			output = 1
			if result_e == output:
				hits[0] += 1
			counter[0] += 1
		if rule == 2: 
			output = 3
			if result_e == output:
				hits[2] += 1
			counter[2] += 1  

	print("contadores:",sum(counter))
	print(hits/50)
	print("Total hits:", sum(hits))
	print("Accuracy:", (sum(hits)/150)*100, "%")
main()