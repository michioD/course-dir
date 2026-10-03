import math

def coins(n,a,b,c):
    cache = [0]*(n+1)
    cache[0] = 0
    for i in range(1, n+1):
        coins_ia = math.inf if i<a else 0 if i-a==0 else cache[i-a]
        coins_ib = math.inf if i<b else 0 if i==b else cache[i-b]
        coins_ic = math.inf if i<c else 0 if i==c else cache[i-c]
        cache[i] = min(i, 1 + coins_ia, 1 + coins_ib, 1 + coins_ic)
    return cache

def main():
    n = 10
    a = 1
    b = 2
    c = 1
    print(coins(n,a,b,c))

main()
