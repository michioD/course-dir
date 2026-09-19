import math

def coins(n, a, b, c):
    plat_coins = n // c
    gold_coins = (n - plat_coins * c) // b
    silver_coins = (n - (plat_coins * c + gold_coins * b)) // a
    copper_coins = (n - (plat_coins * c + gold_coins * b + silver_coins * a))
    return plat_coins + gold_coins + silver_coins + copper_coins


def main():
    n = int(input())
    a = int(input())
    b = int(input())
    c = int(input())
    print(coins(n, a, b, c))

if __name__ == '__main__':
    main()