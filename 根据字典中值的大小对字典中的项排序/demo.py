from random import randint 

data = {k:randint(60,100) for k in 'abcxy'}
print(sorted(zip(data.values(),data.keys())))
print(sorted(data.items(),key=lambda x : x[1])) #sorted函数取序列的每一项进行排序
