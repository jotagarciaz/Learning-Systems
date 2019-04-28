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
    
    
    real=deepcopy(nodes)

    for k,n in nodes.items():
        for destiny in n:
            n[destiny]=n[destiny]+n[destiny] #Comprobar esto
        n = sorted(n.items(), key=lambda x:x[1])
        nodes[k]=n

    for origin in nodes:
        result=aStar(origin,nodes,real)
        print(result,result[1][-1])


def aStar(origin,nodes,real):
    if origin!=DESTINY:
        path=[[origin],[]]
        last_visited=path[0][-1]
        total=0
        while last_visited != DESTINY:
            map(lambda x:x[1]+total,nodes[last_visited])
            nodes[last_visited]=sorted(nodes[last_visited], key=lambda x:x[1])
            all_visited=True
            for city,distance in nodes[last_visited]: # Se queda atascado porque W solo puede ir a A y si vienes de A no le quedan ciudades por visitar
                if city not in path[0]:
                    total=total+real[last_visited][city]
                    path[0].append(city)
                    path[1].append(total)
                    all_visited=False
                    break
            if all_visited:
                path[0].pop()
                path[1].pop()
                nodes[path[0][-1]].pop(0)       
                
            last_visited=path[0][-1]
    else:
        path=[[origin],[0]]
    return path 

read_files("/Users/jgarcia/Documents/Learning Systems/assignment 4/minixample")        

end = time.time()
print(end - start)

print(proccess.memory_info().rss)