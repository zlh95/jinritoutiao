#使用zip函数将多个和迭代对象合并，每次迭代返回一个元组（并行）
#使用标准库的itertools.chain,将多个可迭代对象连接(串行)

from itertools import chain

a1 = [1,2,3,4,5]
a2 = ['a','b','c','d','e']

for t in zip(a1,a2):
	print(t)  #并行，每次迭代每一个可迭代对象的一个元素，组成一个元组

for i in chain(a1,a2):
	print(i) #串行，迭代完一个后接着迭代另一个