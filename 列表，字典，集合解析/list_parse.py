from random import randint

data = [randint(-10,10) for _ in range(10)]

new_list = [x for x in data if x >= 0]

print(new_list)
