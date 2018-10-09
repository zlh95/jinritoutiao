def deco(func):
    cache = {}
    def warp(n):
        if n not in cache:
            cache[n] = func(n)
            return cache[n]
        return cache[n]
    return warp



@deco
def fib(n):
    if n < 2 :
        return 1
    return fib(n-1) + fib(n-2)

print(fib(50))
