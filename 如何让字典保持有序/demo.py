from collections import OrderedDict

#能记住插入顺序的字典
d = OrderedDict()
d['Jim'] = (1,32)
d['Rick'] = (2,43)
d['Jack'] = (3,45)
d['Tony'] = (4,54)
for i in d:
    print(i)
