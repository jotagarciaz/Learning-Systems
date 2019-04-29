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
PERCENTAGE_TRAINING=0.75
PERCENTAGE_VALIDATION=0.1
PERCENTAGE_TEST=0.15
ACCURACY_REQUIRED = 0.9

HIDDEN_LAYER_1 = 4 
HIDDEN_LAYER_2 = 3
OUTPUT_NEURONS = 3

LEARNING_RATE=0.1

MIDDLE_LOW=0.3
MIDDLE_HIGH=0.8

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

""" First we need to extract values from the file"""
def read_training_set():
    n_lines_training = int(PERCENTAGE_TRAINING * n_lines_to_read) 

    f.seek(0)
    training_result=np.zeros(n_lines_training)
    training_set=np.zeros((n_lines_training,LINE_LEN-1))
    for i in range(0, n_lines_training): 
        aux = f.readline()
        aux=aux.split(" ", LINE_LEN)
        line=np.zeros(len(aux)-1)
        for j in range(0,len(aux)-1):
            line[j]=(num(aux[j]))
            
        training_set[i]=line.copy()
        training_result[i]=int(aux[-1])
             
    return training_set,training_result

def read_validation_set():
    n_lines_validation = int(PERCENTAGE_VALIDATION * n_lines_to_read) 



    validation_result =np.zeros(n_lines_validation)
    validation_set=np.zeros((n_lines_validation,LINE_LEN-1))
    for i in range(0, n_lines_validation): 
        aux = f.readline()
        aux=aux.split(" ", LINE_LEN)
        line=np.zeros(len(aux)-1)
        for j in range(0,len(aux)-1):
            line[j]=(num(aux[j]))
            
        validation_set[i]=line.copy()
        validation_result[i]=int(aux[-1])
             
    return validation_set,validation_result

def read_testing_set():
    n_lines_testing = int(PERCENTAGE_TEST * n_lines_to_read) 



    testing_result =np.zeros(n_lines_testing)
    testing_set=np.zeros((n_lines_testing,LINE_LEN-1))
    for i in range(0, n_lines_testing): 
        aux = f.readline()
        aux=aux.split(" ", LINE_LEN)
        line=np.zeros(len(aux)-1)
        for j in range(0,len(aux)-1):
            line[j]=(num(aux[j]))
            
        testing_set[i]=line.copy()
        testing_result[i]=int(aux[-1])
             
    return testing_set,testing_result


def sigmoid(net):
  return 1/(1+np.exp(-net)) 

def softmax(output):

    softmax = np.exp(output)
    summation=np.sum(softmax)
    softmax=softmax[0]/summation
    output=softmax.argmax(axis=0)
    return output,softmax

def normalize(training_data,validation_data,testing_data):
    set=np.vstack((training_data,validation_data,testing_data))
    for i in range(len(set[0])):
        minimum=min(set[:,i])
        maximum=max(set[:,i])
        training_data[:,i]=(training_data[:,i]-minimum)/(maximum-minimum)
        validation_data[:,i]=(validation_data[:,i]-minimum)/(maximum-minimum)
        testing_data[:,i]=(testing_data[:,i]-minimum)/(maximum-minimum)

    return training_data,validation_data,testing_data

def main():
    target_error = np.zeros((OUTPUT_NEURONS,OUTPUT_NEURONS))
    np.fill_diagonal(target_error,1)
    

    training_data,training_result=read_training_set()
    validation_data,validation_result=read_validation_set()
    testing_data,testing_result=read_testing_set()

    training_data,validation_data,testing_data=normalize(training_data,validation_data,testing_data)

    hits=np.zeros(3)
    counter = np.zeros(3)
    for e in range(len(training_data)):
        element=training_data[e]
        result=training_result[e]
        if (element[0]<=MIDDLE_LOW or element[0]>=MIDDLE_HIGH) and (element[1]>=MIDDLE_LOW) and (element[2]>=MIDDLE_LOW) and (element[3]>=MIDDLE_LOW and element[3]<=MIDDLE_HIGH):
            if result==2:
                hits[1]+=1
            counter[1]+=1
        elif (element[2]<=MIDDLE_HIGH) and (element[3] <= MIDDLE_LOW):
            if result==1:
                hits[0]+=1
            counter[0]+=1  
        elif (element[1]<=MIDDLE_HIGH) and (element[2] >= MIDDLE_HIGH) and (element[3] >= MIDDLE_HIGH):
            if result==3:
                hits[2]+=1
            counter[2]+=1
        elif (element[0]>=MIDDLE_LOW and element[0]<=MIDDLE_HIGH) and (element[1]<=MIDDLE_HIGH) and (element[2]<=MIDDLE_LOW) and (element[3]>=MIDDLE_HIGH):
            if result==2:
                hits[1]+=1
            counter[1]+=1   
    for e in range(len(validation_data)):
        element=validation_data[e]
        result=validation_result[e]
        if (element[0]<=MIDDLE_LOW or element[0]>=MIDDLE_HIGH) and (element[1]>=MIDDLE_LOW) and (element[2]>=MIDDLE_LOW) and (element[3]>=MIDDLE_LOW and element[3]<=MIDDLE_HIGH):
            if result==2:
                hits[1]+=1
            counter[1]+=1
        elif (element[2]<=MIDDLE_HIGH) and (element[3] <= MIDDLE_LOW):
            if result==1:
                hits[0]+=1
            counter[0]+=1  
        elif (element[1]<=MIDDLE_HIGH) and (element[2] >= MIDDLE_HIGH) and (element[3] >= MIDDLE_HIGH):
            if result==3:
                hits[2]+=1
            counter[2]+=1
        elif (element[0]>=MIDDLE_LOW and element[0]<=MIDDLE_HIGH) and (element[1]<=MIDDLE_HIGH) and (element[2]<=MIDDLE_LOW) and (element[3]>=MIDDLE_HIGH):
            if result==2:
                hits[1]+=1
            counter[1]+=1 
    for e in range(len(testing_data)):
        element=testing_data[e]
        result=testing_result[e]
        if (element[0]<=MIDDLE_LOW or element[0]>=MIDDLE_HIGH) and (element[1]>=MIDDLE_LOW) and (element[2]>=MIDDLE_LOW) and (element[3]>=MIDDLE_LOW and element[3]<=MIDDLE_HIGH):
            if result==2:
                hits[1]+=1
            counter[1]+=1
        elif (element[2]<=MIDDLE_HIGH) and (element[3] <= MIDDLE_LOW):
            if result==1:
                hits[0]+=1
            counter[0]+=1  
        elif (element[1]<=MIDDLE_HIGH) and (element[2] >= MIDDLE_HIGH) and (element[3] >= MIDDLE_HIGH):
            if result==3:
                hits[2]+=1
            counter[2]+=1
        elif (element[0]>=MIDDLE_LOW and element[0]<=MIDDLE_HIGH) and (element[1]<=MIDDLE_HIGH) and (element[2]<=MIDDLE_LOW) and (element[3]>=MIDDLE_HIGH):
            if result==2:
                hits[1]+=1
            counter[1]+=1 

    print("contadores: ",sum(counter))
    print(hits/counter)
main()