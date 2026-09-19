import math
import time
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10**6)

def coins(n, a, b, c):
    '''
    Same thing as in part a), but with memoization.
    Parameters:
    n (int): value expressed in number of copper coins
    a (int): silver
    b (int): gold
    c (int): platinum
    '''
    cache = {}
    answer = _coins(n, a, b, c, cache)
    return answer
    
    
    
def _coins(n, a, b, c, cache):
    '''
    Recursive helper function, does the actual recursion. 
    '''

    if n < 0:
        return math.inf
    if n == 0:
        return 0
    if n in cache:
        return cache[n]
    
    cache[n] = min(n, 1 + _coins(n-a, a, b, c, cache), 1 + _coins(n-b, a, b, c, cache), 1 + _coins(n-c, a, b, c, cache))

    return cache[n]

def main():
    a = 5
    b = 6
    c = 7
    
    runtime = 0
    n = 1
    runtime_list = []

    while True:
        start = time.perf_counter()
        coins(n, a, b, c)
        end = time.perf_counter()
        runtime = end - start
        runtime_list.append(runtime)
        if runtime >= 1:
            print(f'The largest n that could run under 1 sec was for n = {n-1}, whose runtime was {runtime_list[-2]}')
            break
        n += 1


if __name__ == '__main__':
    main()