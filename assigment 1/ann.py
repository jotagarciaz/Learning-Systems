"""
    Source code created for DVA427 - Lärande System.
    Code writers:
        - Joaquín García Benítez.
        - Clara Torre García-Barredo.
    Code created on February 2019.
"""

import numpy as np
import random

f = open("assigment 1/data", 'r')
f.seek(0)
n_lines_to_read = len(f.readlines())

number_neurons = 10


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


# First we get the data from the data.txt file.
training_set = read_training_set()
validation_set = read_validation_set()
testing_set = read_testing_set()


def sigmoid_function(activation):
    sum = -activation
    return 1 / (1 + np.exp(sum))

# Make a prediction with weights
# row = data?


def predict(row, weights):
    activation = weights[0]
    for i in range(len(row) - 1):
        activation += weights[i + 1] * row[i]
    output = sigmoid_function(activation)
    return 1.0 if output >= 0.5 else 0.0


def generate_random_weights(range_given):
    random_weights = []  # type: list
    for x in range(range_given):
        random_weights.append(random.uniform(0.0, 1.0))
    return random_weights

# Estimate Perceptron weights using stochastic gradient descent


def train_weights(train, l_rate, n_epoch):
    global number_neurons
    aux = []  
    for neuron in range(number_neurons):
        weights = generate_random_weights(len(train[0]))
        for epoch in range(n_epoch):
            sum_error = 0.0
            for row in train:
                prediction = predict(row, weights)
                error = row[-1] - prediction
                sum_error += error**2
                weights[0] = weights[0] + l_rate * error
                for i in range(len(row)-1):
                    weights[i + 1] = weights[i + 1] + l_rate * error * row[i]
            print('Epoch = %d, lrate = %.3f, error = %.3f' % (epoch, l_rate, sum_error))
        aux.append(weights)
    return aux

l_rate = 0.01 #¿l_rate esta funcionando correctamente? Learning Rate: Used to limit the amount each weight is corrected each time it is updated.
n_epoch = 150
weights = train_weights(training_set, l_rate, n_epoch)
print(weights)

best_option = 0
for option in range(0,len(weights)):
    maximum_value = 0.0
    hits = 0
    for row in validation_set:
        prediction = predict(row,weights[option])
        if row[-1] == prediction:
            hits += 1
    value = hits/len(validation_set)
    if value >= maximum_value:
        maximum_value = value
        best_option = option

for row in validation_set:
    prediction = predict(row,weights[best_option])
    print("Expected = %d, Predicted = %d"%(row[-1],prediction))

hit = 0
for row in testing_set:
    prediction = predict(row,weights[best_option])
    if row[-1] == prediction:
        hit += 1

print(hit/len(testing_set))
