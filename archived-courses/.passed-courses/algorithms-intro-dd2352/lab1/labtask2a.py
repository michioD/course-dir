import math

import sys

sys.setrecursionlimit(10**6)

# def f(x, y, p, k):
#     if y == 0:
#         return float(1.0) 
#     elif x== 0 and y >0:
#         return float(0.0)
#     elif 1 <= x and 1 <= y:
#         return p * f(x-1, y-1,p, k) + (1-p)*f(x-1,k,p, k) 

def f(x, y, p, k):

    cache = {}
    answer = _f(x, y, p, k, cache)
    return answer
    
def _f(x, y, p, k, cache):
    '''
    recursive helper function, does the actual recursion. 
    '''
    if (x,y) in cache:
        return cache[(x,y)]
    elif y == 0:
        return float(1.0) 
    elif x== 0 and y >0:
        return float(0.0)




    cache[(x,y)] = p * _f(x-1,y-1,p,k,cache) + (1-p) * _f(x-1,k, p,k, cache)
    return cache[(x,y)]

asdasdawgd

def main():
    x = int(input())
    k = int(input())
    y = k
    p = float(input())
    print(f(x, y, p, k))

if __name__ == '__main__':
    main()
