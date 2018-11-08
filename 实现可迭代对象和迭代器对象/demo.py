'''
1.凡是可以返回迭代器对象的都可称之为可迭代对象，如果对象实现了能返回迭代器的__iter__方法，那么对象就是可迭代的。.序列都可以迭代，其实现了__getitem__方法。
2.如果一个对象是可迭代对象，它能通过内置的iter()，实际上就是调用了魔术方法__iter__()得到迭代器对象。
3.对象可迭代的原因，是因为满足了迭代协议，即某个对象实现了__iter__()方法，我们认为它是可迭代的，
如果没有实现__iter__()方法，但是有__getitem__()时，python会调用它，传入0开始的索引，尝试迭代
对象，这是后备机制，虽然没有实现__contains__(),但也是能使用‘in’运算符，和迭代
4.标准的迭代器接口有两个方法 （1):__next__方法，返回下一个可用的元素，如果没有元素了，抛出StopIteration异常
						    (2):__iter__方法，返回self(自身),以便在应该使用可迭代对象的地方使用迭代器，例如for循环中
'''

#手动实现可迭代对象的例子
import re 

RE_WORD = re.compile(r'\w+')

class Sentence:
	def __init__(self,text):
		self.text = text
		self.words = RE_WORD.findall(text)
		#print(self.words)re.findall()返回一个列表

	def __getitem__(self,index):
		return self.words[index]

	def __len__(self):
		return len(self.words)

s = Sentence('Winter is comming')
for word in s:
	print(word)

#使用__iter__方法完成上面的操作（即手动实现可迭代对象，由可迭代对象返回迭代器对象。）
RE_WORD = re.compile(r'\w+')

class Sentence:
	def __init__(self,text):
		self.text = text
		self.words = RE_WORD.findall(text)

	def __iter__(self):
		return SentenceIterator(self.words)

	def __len__(self):
		return len(self.words)

class SentenceIterator:
	def __init__(self,words):
		self.words = words
		self.index = 0

	def __iter__(self):
		return self

	def __next__(self):
		try:
			word = self.words[self.index]
		except IndexError:
			raise StopIteration()
		self.index += 1
		return word

s = Sentence('Winter is comming')
for word in s:
	print(word)			


#生成器版本，注：迭代器是生成器对象

RE_WORD = re.compile(r'\w+')

class Sentence:
	def __init__(self,text):
		self.text = text
		self.words = RE_WORD.findall(text)

	def __iter__(self):
		for i in self.words:
			yield i

	def __len__(self):
		return len(self.words)

s = Sentence('Winter is comming')
for word in s:
	print(word)

#生成器表达式版本

RE_WORD = re.compile(r'\w+')

class Sentence:
	def __init__(self,text):
		self.text = text

	def __iter__(self):
		return (match.group() for match in RE_WORD.finditer(self.text))
		#finditer函数构建一个迭代器，它的__next__方法返回MatchObject实例，使用MatchObject.group()方法返回正则表达式匹配的具体文本。	

	def __len__(self):
		return len(self.words)

s = Sentence('Winter is comming')
for word in s:
	print(word)