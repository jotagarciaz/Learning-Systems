"""
    Source code created for DVA427 - Lärande System.
    Code writers:
        - Joaquín García Benítez.
        - Clara Torre García-Barredo.
    Code created on February 2019.
"""

import numpy as np

f = open("assigment 1/data",'r')
f.seek(0)
n_lines_to_read = len(f.readlines())

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
    
def read_training_set():
    global f, n_lines_to_read
    n_lines_training = int(0.75 * n_lines_to_read)
    training_set = [] #type: list
    f.seek(0)
    for i in range(0,n_lines_training):
        aux = f.readline()
        training_set.append(aux.split(",",19))

    for i in range(0,len(training_set)):
        training_set[i] = list(map(lambda x: num(x), training_set[i]))
   
    return np.array(training_set)

def read_validation_set():
    global f, n_lines_to_read
    n_lines_validation = int(0.10 * n_lines_to_read)
    validation_set = [] #type: list
    for i in range(0, n_lines_validation):
        aux = f.readline()
        validation_set.append(aux.split(",", 19))
    
    for i in range(0, len(validation_set)):
        validation_set[i] = list(map(lambda x: num(x), validation_set[i]))
    
    return np.array(validation_set)

def read_testing_set():
    global f, n_lines_to_read
    n_lines_testing = int(0.15 * n_lines_to_read + 1)
    testing_set = [] #type: list
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

np.random.seed(1)

random = [] #type: list
for i in range (0,len(training_set[0])):
    random.append(2 * np.random.random_sample() -1)

#for iteration in range(10000):
 #   output = output_neuron(random)
    #synaptic_weights += np.dot(training_set.T, (training_set_outputs - output) * output * (1 - output))

def output_neuron(random):
    random = np.array(random)
    sum = 0
    for i in range (0, len(training_set)):
        sum += training_set[i] * random[i]
    sum = -sum
    return 1 / (1 + np.exp(sum))

# Make a prediction with weights
# row = data?
def predict(row, weights):
	activation = weights[0]
	for i in range(len(row)-1):
		activation += weights[i + 1] * row[i]
	return 1.0 if activation >= 0.0 else 0.0

# Estimate Perceptron weights using stochastic gradient descent
def train_weights(train, l_rate, n_epoch):
	weights = [0.0 for i in range(len(train[0]))]
	for epoch in range(n_epoch):
		sum_error = 0.0
		for row in train:
			prediction = predict(row, weights)
			error = row[-1] - prediction
			sum_error += error**2
			weights[0] = weights[0] + l_rate * error
			for i in range(len(row)-1):
				weights[i + 1] = weights[i + 1] + l_rate * error * row[i]
		print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))
	return weights

l_rate = 0.1
n_epoch = 200
weights = train_weights(training_set, l_rate, n_epoch)
print(weights)

for row in training_set:
	prediction = predict(row, random)
	print("Expected=%d, Predicted=%d" % (row[-1], prediction))