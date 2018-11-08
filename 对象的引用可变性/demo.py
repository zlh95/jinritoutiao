'''
1.重点，变量是标注，不是盒子。对象在赋值前就创建好了，创建对象之后才会把变量赋值给对象。
2.为了理解python中的赋值语句，应当始终先读右边。对象在右边创建或获取，在此之后左边的变量
才会绑定到对象上，这就像为对象贴上标注。
3.python变量类似于java的引用式变量，最好把他们理解为附加在对象上的标注。
4.标识：可以理解为对象在内存中的地址。
5.别名：charles = {'name':'Chaeles'} ,lewis = charles这时，lewis是charles的别名，id(charles) == id(lewis)
6.每个变量都有标识，类型和值。对象一旦创建，他的标识绝不会变，你可以把表示理解成为对象在内存中的地址。
is运算符比较两个对象的标识，id()函数返回对象标识的整数
7.==运算符比较两个对象的值（对象中保存的数据），is比较对象的标识
'''
charles = {'name':'Chaeles','born':'1832'}
lewis = charles #lewis是charles的别名
lewis is charles #返回True,因为id(charles) == id(lewis)
lewis['balance'] = 950 #向lewis中添加一个元素，相当于向charles中添加一个元素。

'''
1.元组的相对不可变性，元组与多数的python集合（列表，字典，集等等）一样，保存的是对象的引用，如果引用的元素
是可变的，即便元组本身不可变，元素依然可变，也就是说，元组的不可变性其实指的是tuple数据结构的物理内容（即
保存的引用）不可变，与引用的对象无关.这个也解释了有些元组是不可散列的原因。
'''
t1 = (1,2,[30,40])
t2 = (1,2,[30,40])
t1 = t2 #True
id(t1[-1]) #12345
t1[-1].append(99) #t1:(1,2,[30,40,99])
id(t1[-1]) #12345
t1 = t2 #False

'''
1.默认做浅复制：使用列表的内置构造方法list()或者[:]做的是浅复制（即复制了最外层容器，副本中的元素是源容器中
元素的引用）。如果所有元素都是不可变的，那么这样没问题，还能节省内存，但是如果有可变元素就得注意。
'''
l1 = [3,[66,55,44],(7,8,9)]
l2 = list(l1)
l1.append(100)
l1.remove(55)
print(l1)  #[3,[66,44],(7,8,9),100]
print(l2)  #[3,[66,44],(7,8,9)] 100不会追加过来，因为l2是l1的副本，在l1中添加添加一个对象不会反应到l2上
		   #把内部列表l1[1]中的55删除，对l2有影响，因为l2[1]绑定的列表与l1[1]是同一个	
l2[1] += [33,22]#对可变对象来说，如l2[1]引用的列表，+=运算符就地的修改列表（不会产生新的对象），这次修改在
			    #l1[1]中也有体现，因为它是l2[1]的别名。
l2[2] += (10,11)#对于元组来说，+=运算符创建一个新的元组，然后重新绑定给变量l2[2]，这等同于l2[2] = l2[2] + (10,11)
				#现在l1和l2中最后位置上的元组不是同一个对象。
print(l1) #[3,[66,44,33,22],100]
print(l2) #[3,[66,44,33,22],(7,8,9,10,11)]

'''
1.为任意对象做深复制和浅复制，深复制（即副本不共享内部对象的引用），copy模块提供deepcopy和copy
函数能为任意对象做深复制和浅赋值
'''
class Bus:
	def __init__(self,passengers=None):
		if passengers is None:
			self.passengers = []
		else:
			self.passengers = list(passengers)

	def pick(self,name):
		self.passengers.append(name)

	def drop(self,name):
		self.passengers.remove(name)

import copy
bus1 = Bus(['Alice','Bill','Claire','David'])
bus2 = copy.copy(bus1)
bus3 = copy.deepcopy(bus1)

print(id(bus1),id(bus2),id(bus3)) #123,456,789
bus1.drop('Bill')
bus2.passengers #['Alice','Claire','David']
print(id(bus1.passengers),id(bus2.passengers),id(bus3.passengers)) #321,321,987 
bus3.passengers #['Alice','Bill','Claire','David']

'''
1.函数的参数作为引用时：python唯一支持的参数传递模式是共享传参（指函数的各个形式参数获得实参中各个引用的副本），
也就是说，函数内部的行参是实参的别名。这种方案的结果是，函数可能会修改作为参数传入的可变对象，但是无法修改那些
对象的标识（即不能把一个对象替换成另一个对象)
'''
def f(a,b):
	a += b
	return a

x,y = 1,1
f(x,y) #3
x,y #(1,1) 不可变对象
a = [1,2]
b = [3,4]
f(a,b) #[1,2,3,4]
a,b #([1,2,3,4],[3,4]) #可变对象
a = (1,2)
b = (3,4)
f(a,b) #(1,2,3,4)
a,b #((1,2),(3,4)) #不可变对象

'''
注意：千万不要使用可变类型作为参数的默认值
'''
class HauntedBus:
	def __init__(self,passengers=[]):
		self.passengers = passengers

	def pick(self,name):
		self.passengers.append(name)

	def drop(self,name):
		self.passengers.remove(name)

bus1 = HauntedBus(['Alice','Bill'])
bus1.passengers  #['Alice','Bill']
bus1.pick('Claire')
bus1.drop('Alice')
bus1.passengers # ['Bill','Claire']
bus2 = HauntedBus()
bus2.pick('Carrie')
bus2.passengers #['Carrie']
bus3 = HauntedBus()

