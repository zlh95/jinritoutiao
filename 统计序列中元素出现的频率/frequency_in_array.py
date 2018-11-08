from collections import Counter
from random import randint

data = [randint(0,30) for _ in range(20)]
d = dict.fromkeys(data,0)

for i in data:
    d[i] += 1
print(d)

c = Counter(data)   #将序列传入Counter的构造器，得到Counter对象是元素频度的字典
print(c)
print(c.most_common(3))  #该方法得到频度最高的n个元素的列表
