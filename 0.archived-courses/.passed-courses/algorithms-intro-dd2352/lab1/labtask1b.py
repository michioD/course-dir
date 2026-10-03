'''
Trying to analyse the complexity of the algorithm.
'''


import math
import time
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10**4)

def coins(n, a, b, c):
    if n < 0:
        return math.inf
    elif n == 0:
        return 0
    else:
        return min(n, 1 + coins(n-a, a, b, c), 1 + coins(n-b, a, b, c), 1 + coins(n-c, a, b, c))


def main():
    a = 5
    b = 6
    c = 7
    time_list = []
    n_list = [n for n in range(1,90)]
    # n_list = [2**n for n in range(1,10)]
        
    for n in n_list:
        start = time.perf_counter()
        coins(n, a, b, c)
        end = time.perf_counter()
        time_list.append(end - start)

    plt.plot(n_list, time_list)
    plt.xlabel('Size of N')
    plt.ylabel('Running time (s)')
    plt.show()



    print(n_list)

if __name__ == '__main__':
    main()