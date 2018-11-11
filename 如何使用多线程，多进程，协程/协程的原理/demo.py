#首先看一下yield from的使用方法
#手动实现itertools.chain生成器
def chain(*iterables):
	for it in iterables:
		for i in it:
			yield i
>> s = 'ABC'
>> t = tuple(range(3))
>> list(chain(s,t))  #list() ->new empty list ;list(iterable) -> new list initialized from iterable's items 
['A','B','C',0,1,2]

#yield from的使用方法
def chain(*iterables):
	for i in iterables:
		yield from i
#1.yield from i 替代内层的for循环
#2.还有一个重要的特性，yield from还会创建通道，把内层生成器直接与外层生成器的客户端联系起来。把生成器当成协程使用时，
#这个通道十分重要，不仅能为客户端代码生成值，还能使用客户端代码提供的值。

#yield字面意思,产出和让步，yield item这行代码会产出一个值，提供給next(...)的调用方，此外还会做出让步，暂停执行生成器
#让调用方继续工作，知道需要另一个值时再调用next()。调用方会从中拉取值。