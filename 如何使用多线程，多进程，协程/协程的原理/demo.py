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

#1.yield字面意思,产出和让步，yield item这行代码会产出一个值，提供給next(...)的调用方，此外还会做出让步，暂停执行生成器
#让调用方继续工作，直到需要另一个值时再调用next()。调用方会从中拉取值。
#2.在协程中yield通常出现在表达式的右边（例如 data = yield）,可以产出值，也可以不产出，如果yield关键字后面没有表达式，那么生成器产出None.
#从根本上把yield视作控制流程的方式，这样就很好理解协程了。

#生成器如何进化成协程
1.生成器的调用方可以使用.send(...)方法发送数据，发送的数据会成为生成器函数中yield表达式中的值，因此生成器可以作为协程使用。协程是指一个过程，这个过程与调用方协作，产出又调用方提供的值。

#可能是协程最简单的演示
def simple_coroutine():
	print('-> coroutine started')
	x = yield
	print('-> coroutine received:',x)
>> my_coro = simple_coroutine()
>> my_coro
<generator object simple_coroutine at 0xxxxxx>
>> next(my_coro)
-> coroutine started
>> my_coro.send(42)
-> coroutine received:42
Traceback (most recent call last)
.....
StopIteration

协程可以身处四个状态中的一个1.GEN_CREATED,等待开始执行；2.GEN_RUNNING，解释器正在运行；3.GEN_SUSPENDED,在yield表达式处暂停；4.GEN_CLOSED,执行结束
def simple_coro2(a):
	print('-> started a = ',a)
	b = yield a
	print('-> received: b=',b)
	c = yield a+b
	print('-> received: c=',c)
>> my_coro2 = simple_coro2(14)
>> from inspect import getgeneratorstate
>> getgeneratorstate(my_coro2)
'GEN_CREATED'
>> next(my_coro2)  #预激协程，即让协程向前执行到第一个yield表达式，准备好作为活跃的协程使用
-> started a = 14
>> getgeneratorstate(my_coro2)
'GEN_SUSPENDED'
>> my_coro2.send(28)
-> received:b=28
42
>> my_coro2.send(99)
-> received:c=99
Traceback (most recent call last)
.....
StopIteration
>> getgeneratorstate(my_coro2)
'GEN_CLOSED'

关键一点是