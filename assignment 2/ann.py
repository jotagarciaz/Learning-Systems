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
import matplotlib.pyplot as plt

f = open("/Users/jgarcia/Documents/Learning Systems/assignment 2/iris", 'r')
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

     #weight and bias initialization
    weights_hidden_layer_1=np.random.uniform(-1,1,size=(LINE_LEN-1,HIDDEN_LAYER_1))
    bias_hidden_layer_1=np.random.uniform(-1,1,size=(1,HIDDEN_LAYER_1))
    
    weights_hidden_layer_2=np.random.uniform(-1,1,size=(HIDDEN_LAYER_1,HIDDEN_LAYER_2))
    bias_hidden_layer_2=np.random.uniform(-1,1,size=(1,HIDDEN_LAYER_2))
   
    weights_output_layer=np.random.uniform(-1,1,size=(HIDDEN_LAYER_2,OUTPUT_NEURONS))
    bias_out=np.random.uniform(-1,1,size=(1,OUTPUT_NEURONS))
    hits=0

    counter=0
    graph_round=[]
    graph_accuracy=[]
    while hits/len(validation_data) <ACCURACY_REQUIRED:
        hits=0

        #TRAINING
        for x in range(len(training_data)):
            inputlayer_neurons = training_data[x]

            #Forward Propogation
            hidden_layer_input_net_sum=np.dot(inputlayer_neurons,weights_hidden_layer_1)
            hidden_layer_input=hidden_layer_input_net_sum + bias_hidden_layer_1
            hidden_layer_1_activations = sigmoid(hidden_layer_input)
            
            hidden_layer_2_input_net_sum=np.dot(hidden_layer_1_activations,weights_hidden_layer_2)
            hidden_layer_2_input=hidden_layer_2_input_net_sum + bias_hidden_layer_2
            hidden_layer_2_activations = sigmoid(hidden_layer_2_input)
            
            output_layer_input_net_sum=np.dot(hidden_layer_2_activations ,weights_output_layer)
            output_layer_input= output_layer_input_net_sum+ bias_out
            
            result_output, output_softmax= softmax(output_layer_input)

            #Backpropagation
            E = target_error[int(training_result[x])-1]-output_softmax

            d_output = E*output_softmax * (1- output_softmax)
            
            Error_at_hidden_layer_2 = d_output.dot(weights_output_layer.T)
            d_hidden_layer_2 = (Error_at_hidden_layer_2 * hidden_layer_2_activations)*(1-hidden_layer_2_activations)
        
            Error_at_hidden_layer_1 = d_hidden_layer_2.dot(weights_hidden_layer_2.T)
            d_hidden_layer_1 = (Error_at_hidden_layer_1 * hidden_layer_1_activations)*(1-hidden_layer_1_activations)

            weights_output_layer = weights_output_layer + hidden_layer_2_activations.T.dot(np.reshape(d_output,(1,OUTPUT_NEURONS))) *LEARNING_RATE
            bias_out = bias_out + np.sum(d_output, axis=0,keepdims=True) * LEARNING_RATE
            
            weights_hidden_layer_2 = weights_hidden_layer_2 + hidden_layer_1_activations.T.dot(d_hidden_layer_2) *LEARNING_RATE
            bias_hidden_layer_2 = bias_hidden_layer_2 + np.sum(d_hidden_layer_2, axis=0,keepdims=True) *LEARNING_RATE

            weights_hidden_layer_1 = weights_hidden_layer_1 + np.reshape(training_data[x],(1,LINE_LEN-1)).T.dot(d_hidden_layer_1) *LEARNING_RATE
            bias_hidden_layer_1 += np.sum(d_hidden_layer_1, axis=0,keepdims=True) *LEARNING_RATE
            
            
        
        #VALIDATION
        for x in range(len(validation_data)):
            inputlayer_neurons = validation_data[x]

            #Forward Propogation
            hidden_layer_input_net_sum=np.dot(inputlayer_neurons,weights_hidden_layer_1)
            hidden_layer_input=hidden_layer_input_net_sum + bias_hidden_layer_1
            hidden_layer_1_activations = sigmoid(hidden_layer_input)
            
            hidden_layer_2_input_net_sum=np.dot(hidden_layer_1_activations,weights_hidden_layer_2)
            hidden_layer_2_input=hidden_layer_2_input_net_sum + bias_hidden_layer_2
            hidden_layer_2_activations = sigmoid(hidden_layer_2_input)
            
            output_layer_input_net_sum=np.dot(hidden_layer_2_activations ,weights_output_layer)
            output_layer_input= output_layer_input_net_sum+ bias_out
            
            result_output, output_softmax= softmax(output_layer_input)
            
            if result_output+1== int(validation_result[x]):
                hits=hits+1
        
        print("Hit percentage Validation =",(hits/len(validation_data))*100," Round =",counter)
        counter=counter+1
        graph_accuracy.append((hits/len(validation_data))*100)
        graph_round.append(counter)

    #TESTING
    print("Reading testing data")
    
    hits=0
    hitsEntity=np.zeros(OUTPUT_NEURONS)
    datosEntity=np.zeros(OUTPUT_NEURONS)

    for x in range(len(testing_data)):
        inputlayer_neurons = testing_data[x]

        #Forward Propogation
        hidden_layer_input_net_sum=np.dot(inputlayer_neurons,weights_hidden_layer_1)
        hidden_layer_input=hidden_layer_input_net_sum + bias_hidden_layer_1
        hidden_layer_1_activations = sigmoid(hidden_layer_input)
        
        hidden_layer_2_input_net_sum=np.dot(hidden_layer_1_activations,weights_hidden_layer_2)
        hidden_layer_2_input=hidden_layer_2_input_net_sum + bias_hidden_layer_2
        hidden_layer_2_activations = sigmoid(hidden_layer_2_input)
        
        output_layer_input_net_sum=np.dot(hidden_layer_2_activations ,weights_output_layer)
        output_layer_input= output_layer_input_net_sum+ bias_out
        
        result_output, output_softmax= softmax(output_layer_input)
        
        datosEntity[result_output]+=1
        if result_output+1== int(testing_result[x]):
            hits=hits+1
            hitsEntity[result_output]+=1

    print("Hit percentage testing =",(hits/len(testing_data))*100)
    print("Percentage of each entity =",hitsEntity/datosEntity*100)

    plt.plot(graph_round,graph_accuracy)
    plt.xlabel('Round')
    plt.ylabel('Accuracy')
    plt.show()
main()