#使用标准库的双向队列deque
#退出程序时，使用pickle将队列存入文件，再次运行程序将其导入
#使用猜数字游戏实现

from collections import deque
from random import randint
import pickle

N = randint(0,100)
history = deque([],5)

def guess(k):
    if k == N:
        print('right')
        return True
    if k < N:
        print('{} is less-than N'.format(k))
    else:
        print('{} is greater-than N'.format(k))
    return False

while True:
    h = pickle.load(open('history.txt','rb'))
    line = input('please input a number:')
    if line.isdigit():
        k = int(line)
        history.append(k)
        if guess(k):
            with open('history.txt','wb') as f:
                pickle.dump(history,f)
            break
    elif line == 'history' or line == 'h?':
        print(list(history))
    elif line == 'old':
        print(list(h))
