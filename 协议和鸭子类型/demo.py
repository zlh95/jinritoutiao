'''
引用大佬 Alex Martelli的话：
不要检查它是不是鸭子：检查它的叫声像不像鸭子，它走路的姿势像不像鸭子，等等。具体检查什么取决于你想使用的语言的哪些行为。
'''
#协议和鸭子类型，首先弄清楚一些基本概念：
1.在python中创建功能完善的序列类型无需继承，只需要实现符合序列协议的方法。
2.在面向对象编程中，协议是非正式的接口，只在文档中定义，在代码中不定义。例如，python的序列协议只需要__len__和
__getitem__两个方法，任何类只要使用了标准的签名和语义实现了这两个方法，就能用在任何期待序列的地方。

import collections

Card = collections.namedtuple('Card',['rank','suit'])

class FrenchDeck:
	ranks = [str(n) for n in range(2,11)] + list('JQKA')
	suits = 'spades diamonds clubs hearts'.split()

	def __init__(self):
		self.cards = [Card(rank,suit) for suit in suits for rank in ranks]

	def __len__(self):
		return len(self.cards)

	def __getitem__(self,index):
		return self.cards[index]

#上面这个例子一看就是序列，即便他是object的子类也没问题。我们说他是序列，因为他的行为像序列，这才是重点。
#这就是鸭子类型。
总结：
	协议是非正式的，没有强制力，因此你如果知道类的具体使用场景，通常只需要实现协议的一部分。