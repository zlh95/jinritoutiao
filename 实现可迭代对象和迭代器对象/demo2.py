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