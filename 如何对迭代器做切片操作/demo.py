from itertools import islice

'''
islice(iterable, start, stop[, step]) --> islice object
返回一个迭代器，其next（）方法从iterable返回选定的值。 如果指定了start，
则将跳过所有前面的元素;否则，将默认值设置为零。 步骤默认为1。 如果指定为另一个值，
则step确定连续调用之间跳过的值数。 像列表中的slice（）一样工作但返回一个迭代器。
'''

l = list(range(20))
t = iter(l)

for i in islice(t,5,10):
	print(i)

for x in t:
	print(x)