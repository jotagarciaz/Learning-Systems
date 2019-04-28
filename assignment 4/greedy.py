import time
start = time.time()
from copy import deepcopy 
import os
import psutil
proccess = psutil.Process(os.getpid())

DESTINY='E'

""" First we need to extract values from the file"""
def read_files(file1):

    f = open(file1, "r") #city_1
    f.seek(0)
    nodes={}
    for line in f:
        line_split=line.split(" ", 3)
        origin=line_split[0]
        destiny= line_split[1]
        distance=int(line_split[2])
        route= {destiny:distance}
        route_inverse={origin:distance}
        if destiny not in nodes:
            nodes.update({destiny:route_inverse})
        else:
            nodes[destiny].update(route_inverse)
        if origin not in nodes:
            nodes.update({origin:route})
        else:
            nodes[origin].update(route)
    
    
    real_distances=deepcopy(nodes)

    for origin in nodes:
        result=bfs(origin,nodes)
        sum=0
        for n in range(1,len(result[0])):
            sum=sum+real_distances[result[0][n-1]][result[0][n]]
        print(result,sum)


def bfs(origin,nodes):
    path=[[origin],[]]
    last_visited=path[0][-1]
    while last_visited != DESTINY:
        for city in nodes[last_visited]:
            if city not in path[0]:
                path[0].append(city)
                path[1].append(nodes[last_visited][city])
                break
        last_visited=path[0][-1]
    return path 
        
read_files("/Users/jgarcia/Documents/Learning Systems/assignment 4/minixample")        

end = time.time()
print(end - start)

print(proccess.memory_info().rss)