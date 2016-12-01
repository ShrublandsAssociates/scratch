from math import factorial as fac

def choose(n,r):
    return fac(n) / fac(r) / fac(n-r)

choose(100, 2)
