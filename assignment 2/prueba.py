from copy import deepcopy 
import math
import random
import numpy as np

def normalize(set):
	for i in range(len(set[0])):
		minimum=min(set[:,i])
		maximum=max(set[:,i])
		set[:,i]=(set[:,i]-minimum)/(maximum-minimum)

	return set

res=normalize(np.array([[1.0, 4], [5, 2],[2,2]]))

print(res)