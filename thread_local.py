from threading import Thread,get_ident

class Local(object):
    ident = get_ident()
    def __init__(self):
        object.__setattr__(self,'storage',{})

    def __setattr__(self, key, value):
        if self.ident in self.storage:
            self.storage[self.ident][key] = value
        else:
            self.storage[self.ident] = {key:value}

    def __getattr__(self, item):
        return self.storage[self.ident][item]
