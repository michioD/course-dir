import math
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
    n = int(input())
    a = int(input())
    b = int(input())
    c = int(input())
    print(coins(n, a, b, c))

if __name__ == '__main__':
    main()
