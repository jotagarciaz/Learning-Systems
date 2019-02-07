"""
    Source code created for DVA427 - Lärande System.
    Code writers:
        - Joaquín García Benítez.
        - Clara Torre García-Barredo.
    Code created on February 2019.
"""
def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
    
def read_training_set(file):
    f = open(file,'r')
    f.seek(0)
    n_lines_to_read = len(f.readlines())
    n_lines_to_read = int(0.75 * n_lines_to_read)
    training_set = []
    f.seek(0)
    for i in range(0,n_lines_to_read):
        aux = f.readline()
        training_set.append(aux.split(",",19))

    for i in range(0,len(training_set)):
        training_set[i] = list(map(lambda x: num(x), training_set[i]))
   
    print(training_set)
    
read_training_set("assigment 1/data")