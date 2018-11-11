# 要求：将抓取的天气内容，使用‘用时访问’的策略显示在屏幕上，即把所有的气温封装在一个对象中，可以使用for循环迭代。
# coding:utf8

import requests

# def get_weather(city):
#	res = requests.get('http://wthrcdn.etouch.cn/weather_mini?city=' + city)
# print(res.json())
#	data = res.json()['data']['forecast'][0]
#	return '{}:{},{}'.format(city,data['low'],data['high'])

# print(get_weather('长沙'))


from collections import Iterable, Iterator

class Weather_iterator(Iterator):
    def __init__(self, cities):
        self.index = 0
        self.cities = cities

    def get_weather(self, city):
        res = requests.get(
            'http://wthrcdn.etouch.cn/weather_mini?city=' + city)
        # print(res.json())
        data = res.json()['data']['forecast'][0]
        return '{}:{},{}'.format(city, data['low'], data['high'])

    def __next__(self):
        try:
            city = self.cities[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return self.get_weather(city)

    def __iter__(self):
        return self


class Weather(Iterable):
    def __init__(self, cities):
        self.cities = cities

    def __iter__(self):
        return Weather_iterator(self.cities)


#w = Weather(['长沙', '上海', '深圳', '北京'])
#for i in w:
#    print(i)


#使用生成器版本
class Weather(Iterable):
    def __init__(self, cities):
        self.cities = cities

    def __iter__(self):
        for city in self.cities:
            res = requests.get(
            'http://wthrcdn.etouch.cn/weather_mini?city=' + city)
            # print(res.json())
            data = res.json()['data']['forecast'][0]
            yield '{}:{},{}'.format(city, data['low'], data['high'])



w = Weather(['长沙', '上海', '深圳', '北京'])
for i in w:
    print(i)



    #补充一个：深入分析iter函数
Docstring:
iter(iterable) -> iterator
iter(callable, sentinel) -> iterator

Get an iterator from an object.  In the first form, the argument must
supply its own iterator, or be a sequence.
In the second form, the callable is called until it returns the sentinel.

1.常用的方式就是在迭代对象x的时候会调用iter(x)
2.还有一种鲜为人知的方法：传入两个参数，使用常规的函数或任何可调用的对象创建迭代器。这样使用时，第一个参数
必须是可调用对象，用于不断调用(没有参数),产出的各个值；第二个参数是哨符，这是个标记值，当可调用的对象返回
这个值的时候，触发迭代器抛出StopIteration的异常而产生哨符。

def func():
    return randint(1,6)

>> f_iter = iter(func,1)
>> f_iter
<callable_iterator object at 0xxxxxx>
>> for roll in f_iter:
     print(roll)
4
3
6
2
#有个好用的方法，这段代码逐行的读取文件，直到遇到空行或到达文件末尾
with open('text.txt','r') as f:
    for line in iter(f.readline,'\n'):
        process_line(line)