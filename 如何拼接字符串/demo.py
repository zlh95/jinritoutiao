#使用‘+’可以拼接字符串，推荐使用str.join()方法
#S.join(iterable) -> str返回字符串，该字符串是可迭代对象之间字符串的连接，连接符是S

l = ['abc',123,45,'xyz']
print(''.join([str(x) for x in l]))
