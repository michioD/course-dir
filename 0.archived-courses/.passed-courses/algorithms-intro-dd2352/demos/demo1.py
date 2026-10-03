import math
import numpy as np
import matplotlib.pyplot as plt
x = -math.inf

s = sorted(np.random.randint(0, 10, 20))

t = [np.random.randint(s_i,10,1) for s_i in s]
intervals = (list(zip(s,t)))

sol = list()
for i in intervals:
    s_i = i[0]
    t_i = i[1]
    if x<s_i:
        sol.append(i)
        x = t_i

print(sol)

