from functools import reduce

#dict.keys()，得到一个字典keys的集合
d1 = {'a':3,'b':2,'c':5}
d2 = {'a':2,'x':2,'y':3}
d3 = {'z':2,'a':2,'y':3}

s = d1.keys() & d2.keys() & d3.keys()  #集合的交集
print(s)

m = map(dict.keys,[d1,d2,d3])
res = reduce(lambda x,y : x & y,m)
print(res)
