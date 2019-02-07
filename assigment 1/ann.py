"""
    Source code created for DVA427 - Lärande System.
    Code writers:
        - Joaquín García Benítez.
        - Clara Torre García-Barredo.
    Code created on February 2019.
"""

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
   
    return training_set

def read_validation_set():
    global f, n_lines_to_read
    n_lines_validation = int(0.10 * n_lines_to_read)
    validation_set = [] #type: list
    for i in range(0, n_lines_validation):
        aux = f.readline()
        validation_set.append(aux.split(",", 19))
    
    for i in range(0, len(validation_set)):
        validation_set[i] = list(map(lambda x: num(x), validation_set[i]))
    
    return validation_set

def read_testing_set():
    global f, n_lines_to_read
    n_lines_testing = int(0.15 * n_lines_to_read + 1)
    testing_set = [] #type: list
    for i in range(0, n_lines_testing):
        aux = f.readline()
        testing_set.append(aux.split(",", 19))
    
    for i in range(0, len(testing_set)):
        testing_set[i] = list(map(lambda x: num(x), testing_set[i]))
    
    return testing_set
    
# First we get the data from the data.txt file.
training_set = read_training_set()
validation_set = read_validation_set()
testing_set = read_testing_set()