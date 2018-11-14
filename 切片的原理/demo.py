#首先这里展示的切片，行为表现的和内置的一样。比如，内置的序列类型，切片得到的都是各自类型的新实例，而不是其他类型。
#前面我们按照协议自己写的序列，如FrenchDeck，它虽然能实现切片，但是我们想要的效果是和内置序列表现一样的行为。

1.切片的原理
首先看几个简单的切片实例：
lst = [1,2,3,4,5,6]
lst[:2]  # [1,2]
lst[2:]  # [3,4,5,6]

s = 'bicycle'
s[::3] #'bye'
s[::-1] #'elcycib'
s[::-2] # 'eccb'

s[a:b:c] a:start->表示切片的起始位置，省略的话默认为0
		 b:end->表示切片的结束位置（切片操作区间不包含最后一个元素），省略的话默认直到最后一个元素
		 c:step->表示步进值，默认为1
a:b:c这种用法只能作为索引或者下标用在[]中返回一个切片对象：slice(a,b,c)；
对seq[start:stop:step]进行求值是时，python会调用seq.__getitem__(slice(start,stop,step))

#了解__getitem__的切片行为
class Myseq:
	def __getitem__(self,index):
		return index

>> s = Myseq()
>> s[1]
1
>> s[1:4]
slice(1,4,None)
>> s[1:4:2]
slice(1,4,2)
>> s[1:4:2,9]
(slice(1,4,2),9)
>> s[1:4:2,7:9]  #如果[]中有逗号，那么__getitem__返回一个元组
(slice(1,4,2),slice(7,9,None))

#在使用dir()方法审查slice对象时，有一个特别重要的方法，indices()方法。
S.indices(len) -> (start,stop,stride)
	给定长度为len的序列，计算S(slice对象)表示的扩展的起始(start)和结尾(stop)索引，以及步幅(stride)。
超出边界的索引会被截掉，这与常规的切片方式的处理方式一样。
	换句话说，indices方法开放了内置序列的棘手逻辑，用于优雅的处理确实索引和负索引，以及长度超过目标序列的切片。

>> slice(None,10,2).indices(5) #序列长度只有5，所以stop超出了边界被截掉，start=None所以起始位置为0
(0,5,2)
>> slice(-3,None,None).indices(5) #起始位置-3,序列长度为5,所以计算出起始位置实际是2，stop=None所以结尾为len的值
(2,5,1)
>> 'ABCDE'[:10:2] 等同于 'ABCDE'[0:5:2]
>> 'ABCDE'[-3:]   等同于 'ABCDE'[2:5:1]


#实现一个能处理切片的__getitem__方法

class Vector:
	def __init__(self,components):
		self.components = list(components)
	
	def __len__(self):
		return len(self.components)

	def __getitem__(self,index):
		cls = type(self)
		if isinstance(index,slice):
			return cls(self.components[index])
		elif isinstance(index,numbers.Integral):
			return self.components[index]

		else:
			msg = '{cls.__name__} indices must be integers'
			raise TypeError(msg.format(cls=cls))
#这个类告诉我们，在内置序列中，传入的seq[]中的参数，首先会做类型检查（检查是slice对象，还是简单的索引整数），然后根据类型返回不同的结果。
#序列切片之所以能实现，最主要的原因的slice对象的indices方法的功劳。