import math

import sys

sys.setrecursionlimit(10**6)
# Naive recursion
# def g(x, k, p):
#     if x < k:
#         return float(0.0) 
#     elif x == k:
#         return float(p**k)
#     elif k+1 <= x:
#         return g(x-1, k, p) + (p**k)*(1-p)*(1-g(x-k-1,k,p))


# memoization
def g(x,k,p):
    cache = {}
    answer = _g(x,k,p,cache)
    return answer

def _g(x,k,p,cache):
    if x in cache:
        return cache[x]
    elif x < k:
        return 0.0
    elif x == k:
        return p**k
    cache[x] =  _g(x-1, k, p, cache) + (p**k)*(1-p)*(1-_g(x-k-1,k,p, cache))
    return cache[x]




def main():
    x = int(input())
    k = int(input())
    y = k
    p = float(input())
    print(g(x, y, p))

if __name__ == '__main__':
    main()
