from collections import namedtuple

#namedtuple用来创建只有少数属性但是没有方法的对象，涉及类元编程

Student = namedtuple('Student','name age sex')
s = Student(name='jim',age=18,sex='male')
print(s.name,s.age,s.sex)
