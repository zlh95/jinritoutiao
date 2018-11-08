def fib(n,cache=None):
    '''
    斐波那契数列的运算涉及到许多重复的运算，所以导致程序运行很慢，
    加快他的速度采用了缓存的机制，如果n被计算过，把n的值以键值对的
    方式存入字典中。
    '''
    if cache is None:
        cache = {}
    if n<2:
        return 1
    if n in cache:
        return cache[n]

    else:
        cache[n] = fib(n-1,cache) + fib(n-2,cache)
        return cache[n]

print(fib(50))
