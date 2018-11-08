from random import randint

data = {randint(0,20) for _ in range(10) }

new_set = {x for x in data if x % 3 == 0}
print(new_set)
