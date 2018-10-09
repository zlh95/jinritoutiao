'''
如果 string 至少有一个字符并且所有字符都是字母或数字则返回 True,否则返回 False
该迷你搜索引擎的原理：字典的运用，通过遍历字典的键，然后嵌套遍历键的值，然后判断
用户的输入是否存在。
'''

data = {1:{'name':'Alice','professor':'Search Enginer','age':'32'},2:{'name':'Tom','professor':'UI/UX Enginer','age':'28'},3:{'name':'Staurt','professor':'Web Desiginer','age':'23'}}

s = input()
if s.isalnum() == False:
    print('Please enter a vaild keyword!')
else:
    print('You search for :',s)
    s = s.lower()
    for i in data:
        #print(i)
        for j in data[i].values():
            #print(j)
            if s in j.lower():
                print(data[i])
