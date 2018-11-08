from random import randint

data = {x : randint(60,100) for x in range(1,21)}

new_dict = {k : v for k , v in data.items() if v >= 80}
print(new_dict)
