from threading import Thread,get_ident

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


    
#类似实现ThreadLocal结构，通过字典的方式，让每个线程保存的数据独立，互不影响。
