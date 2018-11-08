'''
装饰器是可调用对象，其参数是另一个函数（被装饰的函数），装饰器可能会处理被装饰的函数，然后把它返回，或者将其替换成另一个函数或可调用对象
'''
@decorate   #装饰器
def target():   #被装饰的函数
	print('running target()')

#上述代码的效果与下述写法一样
def target():
	print('running target()')

target = decorate(target)

'''
上述两个代码片段执行完之后target不一定是原来的target函数，而是decorate(target)返回的函数。
总的来说，装饰有两大特性，1.把被装饰的函数替换成其他函数。2.装饰器在加载模块时立即执行。（在正式运行代码之前，解释器就会对代码进行一次扫描，对涉及装饰器的部分进行替换）
'''
#装饰器何时运行？装饰器的一个关键特性是，他们在被装饰的函数定义之后立即运行，这通常是在导入时（即python加载模块时）。

#registration.py模块
registry = []

def register(func):
	print('running register(%s)'%func)
	registry.append(func)
	return func

@register
def f1():
	print('running f1()')

@register
def f2():
	print('running f2()')

def f3():
	print('running f3()')

def main():
	print('running main()')
	print('registry ->',registry)
	f1()
	f2()
	f3()
if __name__ == '__main__':
	main()


$python3 registration.py
>> running register(<function f1 at 0xxxxxx>)
>> running register(<function f2 at 0xxxxxx>)
>> running main()
>> register ->[<function f1 at 0xxxxxx> ,<function f2 at 0xxxxxx>]
>> running f1()
>> running f2()
>> running f3()

'''
上述例子充分的说明了，函数装饰器在导入模块时立即执行，而被装饰的函数只在明确调用时运行，这突出了导入时与运行时的区别。（这种装饰器原封不动的
返回被装饰的函数，很多python web框架用的这样的装饰器把函数注册到某种中央注册处，如flask的app.route()装饰器，把url模式映射到生成的HTTP响应
的函数上的注册处。这种装饰器可能会也可能不会修改被装饰的函数。）
'''

# 变量作用域的规则
b = 6
def f(a):
	print(a)
	print(b)
	b = 9   '''python在编译函数定义体的时候，由于有在函数定义体赋值的情况（即b = 9），所以它判断b是局部变量，运行到print(b)时
				python会尝试在本地环境中获取b，但是尝试获取局部变量b的值时，发现b没有绑定值。'''
>> f(3)
3
>> UnboundLocalError:local variable 'b' referenced before assignment

'''
python不要求声明变量，但是假定在函数定义体赋值的变量是局部变量。在函数中赋值时想让解释器将b当成全局变量，要使用global声明
'''


'''
闭包：其实闭包指延伸了作用域的函数，其中包含函数定义体中引用、但是不在定义体中定义的非全局变量。
函数是不是匿名的没有关系，关键是它能访问定义体之外定义的非全局变量。
'''

#计算移动平均值的类 average.py
class Average:
	def __init__(self):
		self.series = []

	def __call__(self,new_value):
		self.series.append(new_value)
		total = sum(self.series)
		return total/len(self.series)

>> avg = Average()
>> avg(10)
10
>> avg(11)
10.5

def make_averager(new_value):
    -------------------------------
	|series = []                  |
	|def averager(new_value):     |
	|	series.append(new_value)  | ----> 闭包，在averager函数中，series是自由变量（指未在本地作用域上绑定的变量）
	|	total = sum(series)       |
	|	return total/len(series)  |
	|-----------------------------|
	return averager

>> avg = make_averager()
>> avg(10)
10
>> avg(11)
10.5

'''
综上：闭包是一种函数，他会保留定义函数时存在的自由变量的绑定，这样调用函数时，虽然定义作用域不可用了，但是仍能使用那些绑定。
注意：只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量。
'''

# nonlocal声明
def make_averager():
	count = 0
	total = 0 

	def averager(new_value):
		count += 1           #前面说过，不可变对象+=运算符，相当于count = count +1 这样会创建一个新的count变量，
							 #这会把count变成局部变量（上面讲的在函数定义体中赋值），所以这个会报错。UnboundLocalError:local variable 'count' referenced before assignment
		total += new_value
		return total/count

'''
对于数字，字符串，元组等不可变类型来说，只能读取，不能更新，如果尝试重新绑定，例如count = count + 1，其实会隐式的创建局部变量count，这样的话，count就不是自由变量了。
'''

def make_averager():
	count = 0
	total = 0 

	def averager(new_value):
		nonlocal count ,total
		count += 1           
		total += new_value
		return total/count

# nonlocald的作用是把变量标记为自由变量，即便在函数中为变量赋予了新值，也会成为自由变量。