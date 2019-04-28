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

f = open("data", 'r')
f.seek(0)
n_lines_to_read = len(f.readlines())
LINE_LEN=20
PERCENTAGE_TRAINING=0.75
PERCENTAGE_VALIDATION=0.1
PERCENTAGE_TEST=0.15
ACCURACY_REQUIRED = 0.76

HIDDEN_LAYER_1 = 15 
HIDDEN_LAYER_2 = 10
OUTPUT_NEURONS = 2

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
    resultado_training=np.zeros(n_lines_training)
    training_set=np.zeros((n_lines_training,LINE_LEN-1))
    for i in range(0, n_lines_training): 
        aux = f.readline()
        aux=aux.split(",", LINE_LEN)
        line=np.zeros(len(aux)-1)
        for j in range(0,len(aux)-1):
            line[j-1]=(num(aux[j])/255)
            
        training_set[i]=line.copy()
        resultado_training[i]=int(aux[-1])
             
    return training_set,resultado_training

def read_validation_set():
    n_lines_validation = int(PERCENTAGE_VALIDATION * n_lines_to_read) 
  
    f.seek(0)
    resultado_validation =np.zeros(n_lines_validation)
    validation_set=np.zeros((n_lines_validation,LINE_LEN-1))
    for i in range(0, n_lines_validation): 
        aux = f.readline()
        aux=aux.split(",", LINE_LEN)
        line=np.zeros(len(aux)-1)
        for j in range(0,len(aux)-1):
            line[j-1]=(num(aux[j])/255)
            
        validation_set[i]=line.copy()
        resultado_validation[i]=int(aux[-1])
             
    return validation_set,resultado_validation

def read_testing_set():
    n_lines_testing = int(PERCENTAGE_TEST * n_lines_to_read) 
  
    f.seek(0)
    resultado_testing =np.zeros(n_lines_testing)
    testing_set=np.zeros((n_lines_testing,LINE_LEN-1))
    for i in range(0, n_lines_testing): 
        aux = f.readline()
        aux=aux.split(",", LINE_LEN)
        line=np.zeros(len(aux)-1)
        for j in range(0,len(aux)-1):
            line[j-1]=(num(aux[j])/255)
            
        testing_set[i]=line.copy()
        resultado_testing[i]=int(aux[-1])
             
    return testing_set,resultado_testing


def sigmoid(net):
  return 1/(1+np.exp(-net)) 

def softmax(output):

    softmax = np.exp(output)
    suma=np.sum(softmax)
    softmax=softmax[0]/suma
    output=softmax.argmax(axis=0)
    return output,softmax


def main():
    target_error = np.zeros((OUTPUT_NEURONS,OUTPUT_NEURONS))
    np.fill_diagonal(target_error,1)
    

    datos_training,resultado_training=read_training_set()
    datos_validation,resultado_validation=read_validation_set()

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
    while hits/len(datos_validation) <ACCURACY_REQUIRED:
        hits=0

        #TRAINING
        for x in range(len(datos_training)):
            inputlayer_neurons = datos_training[x]

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
            E = target_error[int(resultado_training[x])]-output_softmax

            d_output = E*output_softmax * (1- output_softmax)
            
            Error_at_hidden_layer_2 = d_output.dot(weights_output_layer.T)
            d_hidden_layer_2 = (Error_at_hidden_layer_2 * hidden_layer_2_activations)*(1-hidden_layer_2_activations)
        
            Error_at_hidden_layer_1 = d_hidden_layer_2.dot(weights_hidden_layer_2.T)
            d_hidden_layer_1 = (Error_at_hidden_layer_1 * hidden_layer_1_activations)*(1-hidden_layer_1_activations)

            weights_output_layer = weights_output_layer + hidden_layer_2_activations.T.dot(np.reshape(d_output,(1,OUTPUT_NEURONS))) *LEARNING_RATE
            bias_out = bias_out + np.sum(d_output, axis=0,keepdims=True) * LEARNING_RATE
            
            weights_hidden_layer_2 = weights_hidden_layer_2 + hidden_layer_1_activations.T.dot(d_hidden_layer_2) *LEARNING_RATE
            bias_hidden_layer_2 = bias_hidden_layer_2 + np.sum(d_hidden_layer_2, axis=0,keepdims=True) *LEARNING_RATE

            weights_hidden_layer_1 = weights_hidden_layer_1 + np.reshape(datos_training[x],(1,LINE_LEN-1)).T.dot(d_hidden_layer_1) *LEARNING_RATE
            bias_hidden_layer_1 += np.sum(d_hidden_layer_1, axis=0,keepdims=True) *LEARNING_RATE
            
            
        
        #VALIDATION
        for x in range(len(datos_validation)):
            inputlayer_neurons = datos_validation[x]

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
            
            if result_output== int(resultado_validation[x]):
                hits=hits+1
        
        print("porcentaje de acierto Validation= ",(hits/len(datos_validation))*100," ronda= ",counter)
        counter=counter+1
        graph_accuracy.append((hits/len(datos_validation))*100)
        graph_round.append(counter)

    #TESTING
    print("Leyendo datos de testing")
    datos_testing,resultado_testing=read_testing_set()
    hits=0
    hitsEntity=np.zeros(OUTPUT_NEURONS)
    datosEntity=np.zeros(OUTPUT_NEURONS)

    for x in range(len(datos_testing)):
        inputlayer_neurons = datos_testing[x]

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
        if result_output== int(resultado_testing[x]):
            hits=hits+1
            hitsEntity[result_output]+=1

    print("porcentaje de acierto Testing= ",(hits/len(datos_testing))*100)
    print("porcentaje de cada entidad= ",hitsEntity/datosEntity*100)

    plt.plot(graph_round,graph_accuracy)
    plt.xlabel('Round')
    plt.ylabel('Accuracy')
    plt.show()
main()