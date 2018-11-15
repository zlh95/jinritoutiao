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
......
StopIteration
>> getgeneratorstate(my_coro2)
'GEN_CLOSED'

	关键一点是，协程在yield关键字所在的位置暂停执行。前面说过，在赋值语句中，=右边的代码在赋值之前执行。因此，对于
b = yield a这行代码来说，等到客户端代码再激活协程时才会设定b的值。这种行为要花点时间才能习惯，不过一定要理解，这样
才能弄懂异步编程中yield的作用。

#使用协程计算移动的平均值
def averager():
	total = 0.0
	count = 0 
	average = None
	while True:
		term = yield
		total += term
		count += 1
		average = total/count

#终止协程和异常处理
#协程中未处理的异常会向上冒泡，传给next函数或send方法的调用方（即触发协程的对象）
#终止协程的一种方式：发送某个哨符值，让协程推出。
#客户端代码可以在生成器上调用两个方法，显示的把异常发送给协程，这两个方法是：
#1.generator.throw(exc_type[,exc_value[,traceback]]),致使生成器在暂停的yield表达式处抛出异常。如果生成器处理
#了抛出的异常，代码会前进到下一个yield表达式，而产出的值会成为调用generaor.throw方法得到的返回值。如果生成器没有
#处理异常，异常会向上冒泡，传到调用方的上下文中。
#2.generator.close()，致使生成器在暂停的yield表达式处抛出GeneratorExit的异常。如果生成器没有处理这个异常，或者抛出
#了StopIteration异常（通常指运行到结尾），调用方不会报错，如果收到了GeneratorExit异常，生成器一定不能产出值，
#否则解释器会抛出RuntimenError错误。生成器抛出的其他异常会向上冒泡，传给调用方。

#coro_exc_demo.py学习在协程中处理异常的测试代码
class DemoException(Exception):
	'演示所定义的异常类型'

def demo_exc_handling():
	print('-> coroutine started')
	while True:
		try:
			x = yield
		except DemoException:
			print('DemoException handled.Continuing...')
		else:
			print('-> coroutine received :{!r}'.format(x))
	raise RuntimeError('This line should never run.')
#关闭demo_exc_handling，，欸有异常
>> exc_coro = demo_exc_handling()
>> next(exc_coro)
-> coroutine started
>> exc_coro.close()
>> from inspect import getgeneratorstate
>> getgeneratorstate(exc_coro)
'GEN_CLOSED'

#传入已经处理的异常不会导致协程终止
>> exc_coro = demo_exc_handling()
>> next(exc_coro)
-> coroutine started
>> exc_coro.throw(DemoException)
DemoException handled.Continuing...
>> getgeneratorstate(exc_coro)
'GEN_SUSPENDED'

#如果传入的异常没有处理，协程会停止，异常冒泡。
>> exc_coro = demo_exc_handling()
>> next(exc_coro)
-> coroutine started
>> exc_coro.throw(ZeroDivisionError)
Traceback (most recent call last)
......
ZeroDivisionError
>> getgeneratorstate(exc_coro)
'GEN_SUSPENDED'


#让协程返回值，为了说明如何返回值，每次激活协程时不会产出移动的平均值。这么做是为了强调某些协程不会产出值，
#而是在最后返回值（通常是某种累计值）
from collections import namedtuple

Result = namedtuple('Result',['count','average'])
def averager():
	total = 0.0
	count = 0 
	average = None
	while True:
		term = yield
		if term is None:
			break  #为了返回值协程必须正常终止。
		total += term
		count += 1
		average = total/count
	return Result(count,average)
>> coro_avg = averager()
>> next(coro_avg)
>> coro_avg.send(10)
>> coro_avg.send(20)
>> coro_avg.send(6.5)
>> coro_avg.send(None)
Traceback (most recent call last)
......
StopIteration:Result(count=3,average=15.5)
#发送None终止循环，导致循环结束，返回结果，一如既往生成器抛出StopIteration。异常对象的value属性保存着返回的值。
#注意，return表达式的值会偷偷的传给调用方，赋值给StopIteration异常的一个属性。

#捕获异常，获取averager的返回值
>> coro_avg = averager()
>> next(coro_avg)
>> coro_avg.send(10)
>> coro_avg.send(20)
>> coro_avg.send(6.5)
>> try:
	coro_avg.send(None)
   except StopIteration as exc:
   	result = exc.exc_value
>> result
Result(count=3,average=15.5)

'''
小总结：获取协程的返回值虽然要绕个圈子，当我们意识到这一点之后就说的通了：yield from的结构会在内部自动捕捉StopIteration
异常。这种处理的方式与for循环处理StopIteration异常的方式一样：循环机制使用用户易于理解的方式处理异常。对yield from结构来说
解释器不仅会捕获StopIteration异常，还会把value属性的值变成yield from表达式的值。
'''

#使用yield from
1.yield from的作用比yield的作用要多，在新版本的python中可以用await关键字代替它，这个名称好多了，因为它传达了至关重要的
一点：在生成器gen中使用yield from subgen()时，subgen()会获得控制权（联想一下for循环，for循环在内部处理了StopIteration
异常，因为yield from 也是一个生成器，每次调用时，使用next(gen)或者gen.send(x)去让生成器，也就是迭代器向前运行一步，就可以从调
用方把值通过yield from开辟一个管道，送到子生成器，而for循环是不支持iterator.send(x)方法的。），把产出的值传给gen的调用方，
即调用方可以直接控制sugen()。与此同时，gen会阻塞，等待suben终止。
2.yield form x表达式对x对象所做的第一件事就是，调用iter(x),从中获取迭代器，x可以是任何可迭代对象。
3.yield from 的主要功能是打开双向通道，把最外层的调用方与最内层的子生成器连接起来，这样二者可以直接发送和产出值，
还可以直接传入异常，而不用在位于中间的协程中添加大量异常处理的样板代码。有了这个结构，协程可以通过以前不可能的方式
委托职责。
4.理清三个术语，‘委派生成器’:包含yield from <iterable>表达式的生成器函数。‘子生成器’：从yield from 表达式中<iterable>
部分获取的生成器。‘调用方’：这个术语指调用委派生成器的客户端代码，我们统一使用客户端来表示。

#使用yield from计算平均值并输出统计报告

from collections import namedtuple

Result = namedtuple('Result',['count','average'])
def averager():
	total = 0.0
	count = 0 
	average = None
	while True:
		term = yield
		if term is None:
			break  #为了返回值协程必须正常终止。
		total += term
		count += 1
		average = total/count
	return Result(count,average)

#委派生成器
def grouper(results,key):
	results[key] = yield from averager()

#客户端代码，即真正的调用方
def main(data):
	results = {}
	for key,values in data.items():
		group = grouper(results,key)
		next(grouper)
		for value in values:
			grouper.send(value)
		grouper.send(None)

	report(results)

#输出报告
def report(results):
	for key,result in sorted(results.items()):
		group,unit = key.split(';')
		print('{:2} {:5} averaging {:.2f}{}'.format(result.count,group,result.average.unit))

data = {
	'girls;kg':
		[40.9,38.5,44.3,42.2,45.2,,41.7,44.5,38.0,40.6,44.5],
	'girls;m':
		[1.6,1.51,1.4,1.3,1.41,1.39,1.33,1.46,1.45,1.43],
	'girls;kg':
		[40.9,38.5,44.3,42.2,45.2,,41.7,44.5,38.0,40.6,44.5],
	'girls;m':
		[1.6,1.51,1.4,1.3,1.41,1.39,1.33,1.46,1.45,1.43],
}
if __name__ == '__main__':
	main(data)

#简化的伪代码，等效于委派生成器中的 RESULT = yield from EXPR，针对只处理StopIteration的异常。
_i = iter(EXPR)
try:
	_y = next(_i)
except StopIteration as _e:
	_r = _e.value
else:
	while 1:
		_s = yield _y
		try:
			_y = _i.send(_s)
		except StopIteration as _e:
			_r = _e.value
			break
RESULT = _r

_i 迭代器，_y 子生成器产出的值，_r 最终的结果（即子生成器运行结束之后yield from表达式的值。）
_s 调用方发给委派生成器的值，这个值会转发给子生成器 _e 异常对象

#下面利用协程实现一个出租车队运营仿真
from collections import namedtuple
from random import randint
from queue import PriorityQueue

Event = namedtuple('Event',['time','proc','action'])

def taxi_process(ident,trips,start_time=0):
    '''每次改变状态时创建事件，把控制权交给仿真器
		ident:车辆标识
		trips:出租车回家之前的行程总数
		start_time：出租车离开车库的时间
    '''
    time = yield Event(start_time,ident,'leave garage')
    for i in range(trips):
        time = yield Event(time,ident,'pike up passenger')
        time = yield Event(time,ident,'drop off passenger')
    yield Event(time,ident,'going home')
    #出租车进程结束

#建立一个字典，字典的键表示出租车的编号，值是taxi_process协程
taxi = {i : taxi_process(i , randint(3,8) , i * 2) for i in range(4)}

class Simulation:
	def __init__(self,proc_map):
		self.events = PriorityQueue()   #优先队列，按照时间正向顺序
		self.proc_map = dict(proc_map)

	def run(self,end_time):
		'''
		排定并显示事件，直到事件结束
		'''
		#排定各出租车的第一个事件
		for _ , proc in sorted(self.proc_map.items()):
			first_event = next(proc)
			self.events.put(first_event)

		#仿真的主循环
		sim_time = 0 
		while sim_time < end_time:
			if self.events.empty():
				print('*** end of simulation ***')
				break

			current_event = self.events.get()
			sim_time , proc_id , previous_action = current_event
			print('taxi :',proc_id,proc_id*'  ' ,current_event)
			active_proc = self.proc_map[proc_id]
			next_time = sim_time + randint(3,9)
			try:
				next_event = active_proc.send(next_time)
			except StopIteration:
				del self.proc_map[proc_id]

			else:
				self.events.put(next_event)
		else:
			msg = '*** end of simulation time : {} events pending '
			print(msg.format(self.events.qsize()))

s = Simulation(taxi)
s.run(10000)