from threading import Thread,get_ident

'''核心思想就是，用线程的标识符（唯一的）作为键，
这样每个线程都存储了唯一的值，互不干扰
比如说request对象，每个线程中request对象都是不同的，每一个请求进来，request对象都不一样。
'''
class Local(object):

    def __init__(self):
        self.storage = {}
        self.get_ident = get_ident

    def set(self, k, v):
        ident = self.get_ident()
        origin = self.storage.get(ident)
        if not origin:
            origin = {k: v}
        else:
            origin[k] = v
        self.storage[ident] = origin
    def get(self, k):
        ident = self.get_ident()
        origin = self.storage.get(ident)
        print(self.storage)
        if not origin:
            return None
        else:
            return origin.get(k, None)

local_values = Local()


def task(num):
    local_values.set("name", num)  # set方法
    import time
    time.sleep(1)
    print(local_values.get("name"), Thread().name)


if __name__ == '__main__':
    for i in range(20):
        t = Thread(target=task, args=(i,), name="%s" % i)
        t.start()
        
        
#flask源码
try:
    from greenlet import getcurrent as get_ident  # 协程
except ImportError:
    try:
        from thread import get_ident  # 线程
    except ImportError:
        from _thread import get_ident  #获取线程的唯一标识 get_ident()

class Local(object):
    __slots__ = ('__storage__', '__ident_func__')

    def __init__(self):
        object.__setattr__(self, '__storage__', {})
        object.__setattr__(self, '__ident_func__', get_ident)

    def __getattr__(self, name):
        try:
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        ident = self.__ident_func__()
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            storage[ident] = {name: value}

local_values = Local()
import threading


def task(num):
    local_values.name = num
    import time
    time.sleep(1)
    print(local_values.name, threading.Thread().name)


if __name__ == '__main__':
    for i in range(20):
        t = threading.Thread(target=task, args=(i,), name="%s" % i)
        t.start()


    
#类似实现ThreadLocal结构，通过字典的方式，让每个线程保存的数据独立，互不影响。
