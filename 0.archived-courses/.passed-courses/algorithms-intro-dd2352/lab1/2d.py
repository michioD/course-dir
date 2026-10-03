import time
import matplotlib.pyplot as plt
import sys
from labtask2c import g

sys.setrecursionlimit(10**9)


def main():
    p = 0.99
    time_list = []
    n_list = [n for n in range(1,200,2)]
    #_list = [2**n for n in range(1,11)]
        
    for n in n_list:
        start = time.perf_counter()
        g(n, int(n/2), p)
        end = time.perf_counter()
        time_list.append(end - start)

    plt.plot(n_list, time_list)
    plt.xlabel('Size of N')
    plt.ylabel('Running time (s)')
    plt.show()

if __name__ == '__main__':
    main()
