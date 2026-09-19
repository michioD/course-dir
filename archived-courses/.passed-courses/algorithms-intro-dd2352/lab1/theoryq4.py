import math

def coins(n, a, b, c):
    if n < 0:
        return math.inf
    elif n == 0:
        return 0
    else:
        # if min(n,1 + coins(n-a, a, b, c), 1 + coins(n-b, a, b, c), 1 + coins(n-c, a, b, c)) == n:
            # return 0
        return min(1 + coins(n-a, a, b, c), 1 + coins(n-b, a, b, c), 1 + coins(n-c, a, b, c))

def main():
    n = int(input())
    a = int(input())
    b = int(input())
    c = int(input())
    print(coins(n, a, b, c))

if __name__ == '__main__':
    main()
