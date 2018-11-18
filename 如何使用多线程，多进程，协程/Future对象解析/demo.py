1.标准库中有两个名为Future的类，concurrent.futures.Future和asyncio.Future。这两个类的作用相同：两个Future类的实例都可以
表示可能或者尚未完成的延迟计算。类似于Twisted引擎中的Deferred类，Tornado框架中的Future类。
2.concurrent.futures模块提供了一个用于异步执行callables的高级接口。
3.futures封装待完成的操作，可以放入队列，完成的状态可查询，得到结果（或抛出异常）后可以获取结果。
4.通常情况下，我们不应该自己创建future，而只能由并发框架（concurrent.futures或asyncio）实例化，原因很简单，因为future表示
终将发生的事情，而确定某件事情会发生的唯一方式是执行的时间已经排定.因此，只有排定把某件事交给concurrent.futures.Executor
子类处理时，才会创建concurrent.future.Future实例，例如Executor.submit()方法的参数是一个可调用对象，调用这个方法后会为传入
的可调用对象排期，并返回一个future。
5.客户端的代码不应该改变future的状态，并发框架在future表示的延迟计算结束后会改变future的状态，而我们无法控制计算何时结束。

 '''
 Future模式只是生产者-消费者模型的扩展。经典“生产者-消费者”模型中消息的生产者不关心消费者何时处理完该条消息，也不关心处理结
 果。Future模式则可以让消息的生产者等待直到消息处理结束，如果需要的话还可以取得处理结果.
 '''
#经典“生产者-消费者”模型代码
import multiprocessing
import os
from time import sleep
from random import randint


class Producer(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            self.queue.put('one product')
            print(multiprocessing.current_process().name + str(
                os.getpid()) + ' produced one product, the no of queue now is: %d' % self.queue.qsize())
            sleep(randint(1, 3))


class Consumer(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            d = self.queue.get(1)
            if d != None:
                print(multiprocessing.current_process().name + str(
                    os.getpid()) + ' consumed  %s, the no of queue now is: %d' % (d, self.queue.qsize()))
                sleep(randint(1, 4))
                continue
            else:
                break


# create queue
queue = multiprocessing.Queue(40)

if __name__ == "__main__":
    print('Excited!')
    # create processes
    processed = []
    for i in range(3):
        processed.append(Producer(queue))
    processed.append(Consumer(queue))

    # start processes
    for i in range(len(processed)):
        processed[i].start()

    # join processes
    for i in range(len(processed)):
        processed[i].join()

'''
这就是生产-消费者模型的一个简单的实现，我们利用一个 multiprocessing 中的 Queue 来作为通信渠道，我们的生产者负责往队列
中传入数据，消费者负责从队列中获取数据并处理。不过就如同上面所说的一样，在这种模式中，生产者并不关心消费者何时处理完数据，
也不关心处理的结果。而在 Future 中，我们可以让生产者等待消息处理完成，如果需要的话，我们还可以获取相关的计算结果。
'''
#来个例子感受一下concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import time

def return_message(message):
	time.sleep(2)
	return message

executor = ThreadPoolExecutor(max_workers=3) #支持上下文管理器
#实例化ProcessPollExecutor类，它继承自类Executor，这是具体异步执行程序的抽象基类。
future1 = executor.submit(return_message,'hello') #executor.sumbit，排定可调用对象的执行时间，返回一个future对象，表示一个待执行的操作
future2 = executor.submit(return_message,'world')
print(future1.done())
time.sleep(3)
print(future2.done())
print(future1.result(),future2.result())

#map方法
import concurrent.futures
import requests

task_url = [('http://www.baidu.com', 40), ('http://example.com/', 40), ('https://www.github.com/', 40)]


def load_url(params: tuple):
    return requests.get(params[0], timeout=params[1]).text


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for url, data in zip(task_url, executor.map(load_url, task_url)): 
            print('%r page is %d bytes' % (url, len(data)))
#map函数与内置的map函数相似，返回一个迭代器。在map函数内部fs = [self.submit(fn, *args) for args in zip(*iterables)]
#对每个函数都调用了submit方法，排定可调用对象的执行时间,返回一个future对象.