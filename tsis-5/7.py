import re
text = input()
x = re.split('_', text)

res = x[0]
for i in x:
    res += i.capitalize()
print(res)