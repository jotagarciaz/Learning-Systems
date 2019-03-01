"""
    Source code created for DVA427 - Lärande System.
    Code writers:
        - Joaquín García Benítez.
        - Clara Torre García-Barredo.
    Code created on February 2019.
"""

import numpy as np
import random
import math

f = open("assigment 1/data", 'r')
f.seek(0)
n_lines_to_read = len(f.readlines())

number_neurons = 10
weights = [] #type: list
dout = 0 #delta of output neuron
#delta of neurons from hidden layer
dhidden = [] #type: list
l_rate = 0.01
epoch = 30


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def read_training_set():
    global f, n_lines_to_read
    n_lines_training = int(0.75 * n_lines_to_read)
    training_set = []  # type: list
    f.seek(0)
    for i in range(0, n_lines_training):
        aux = f.readline()
        training_set.append(aux.split(",", 19))

    for i in range(0, len(training_set)):
        training_set[i] = list(map(lambda x: num(x), training_set[i]))

    return np.array(training_set)


def read_validation_set():
    global f, n_lines_to_read
    n_lines_validation = int(0.10 * n_lines_to_read)
    validation_set = []  # type: list
    for i in range(0, n_lines_validation):
        aux = f.readline()
        validation_set.append(aux.split(",", 19))

    for i in range(0, len(validation_set)):
        validation_set[i] = list(map(lambda x: num(x), validation_set[i]))

    return np.array(validation_set)


def read_testing_set():
    global f, n_lines_to_read
    n_lines_testing = int(0.15 * n_lines_to_read + 1)
    testing_set = []  # type: list
    for i in range(0, n_lines_testing):
        aux = f.readline()
        testing_set.append(aux.split(",", 19))

    for i in range(0, len(testing_set)):
        testing_set[i] = list(map(lambda x: num(x), testing_set[i]))

    return np.array(testing_set)

def generate_random_weights(range_given):
    random_weights = []  # type: list
    for x in range(range_given):
        random_weights.append(random.uniform(-1.0,1.0))  
    return random_weights


def calc_output_neuron(input, neuron):
    global weights
    sum = weights[(len(input)-1)+neuron][0] #The starter weight for the neuron itself
    #We calculate net.
    for i in range(len(input)-1):
        sum += weights[i][neuron]*input[i]
    #Next we calculate the sigmoid function.
    net = -sum
    output = 1/(1+math.exp(net))
    return output

#Input is the array that contains the outputs of the hidden layer.
def calc_output_neuron_output(input):
    global weights
    sum = weights[len(input)-1+number_neurons][0] #The starter weight for the neuron itself
    #We calculate net.
    for i in range(number_neurons):
        sum += weights[i][1]*input[i]
    #Next we calculate the sigmoid function.
    net = -sum
    output = 1/(1+math.exp(net))
    return output

#Output is the output of the last layer and expected is the target output.
def error_output_layer(output, expected):
    return output*(1-output)*(expected - output)

def error_hidden_layer(error_output, output_hidden, expected):
    global weights
    errors = [] #type: list
    for k in range(len(output_hidden)):
        errors.append(output_hidden[k]*(1-output_hidden[k])*weights[19+k][1]*error_output)
    return errors

def update_weights(deltas, input, outputs):
    global weights
    global l_rate
    for i in range(0, len(input)-1):
        for neuron in range(0, number_neurons):
            weights[i][neuron] += l_rate*deltas[neuron]*input[i]
    for i in range(len(input)-1, number_neurons+len(input)-1):
        weights[i][0] += l_rate*deltas[i-len(input)-1]
        weights[i][1] += l_rate*outputs[i-len(input)-1]*outputs[number_neurons]
    weights[len(weights)-1][0] += l_rate*deltas[number_neurons]

def ann():
    for input in training_set:
        for iteration in range(epoch):
            outputs = [] #type: list
            for neuron in range(number_neurons):
                outputs.append(calc_output_neuron(input, neuron))
            out = calc_output_neuron_output(outputs)
            dout = error_output_layer(out, input[-1])
            dhidden = error_hidden_layer(dout, outputs, input[-1])
            dhidden.append(dout)
            outputs.append(out)
            update_weights(dhidden, input, outputs)
        
    for row in validation_set:
        outputs = [] #type: list
        for neuron in range(number_neurons):
            outputs.append(calc_output_neuron(row, neuron))
        out = calc_output_neuron_output(outputs)
        print("Expected = %d, Predicted = %d"%(row[-1],round(out)))

    hit = 0
    for row in testing_set:
        outputs = [] #type: list
        for neuron in range(number_neurons):
            outputs.append(calc_output_neuron(row, neuron))
        out = calc_output_neuron_output(outputs)
        if out >= 0.5:
            out = 1
        else:
            out = 0
        if row[-1] == out:
            hit += 1

    print(hit/len(testing_set))

# Main.

# First we get the data from the data.txt file.
training_set = read_training_set()
validation_set = read_validation_set()
testing_set = read_testing_set()

for i in range(len(training_set[0])-1):
    weights.append(generate_random_weights(number_neurons))
for i in range(number_neurons):
    weights.append(generate_random_weights(2))
weights.append(generate_random_weights(1))

ann()
