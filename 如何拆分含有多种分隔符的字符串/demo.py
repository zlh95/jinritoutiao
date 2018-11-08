import re

s = 'ab;cd|efg|hi,jkl|mn\topq;rst,uvw\txyz'

#1连续使用str.split()方法，每次处理一种分隔符
def mysplit(s,ds):
    res = [s]

    for d in ds:
        t = []
        list(map(lambda x : t.extend(x.split(d)),res))
        #L.extend(iterable) -> None -- extend list by appending elements from the iterable
        res = t
    return res

print(mysplit(s,';|,\t'))
#2使用正则表达式的re.split()方法，它第一个参数接受一个正则表达式，一次性拆分
res = re.split(r'[;,|\t]+',s) 
print(res)
