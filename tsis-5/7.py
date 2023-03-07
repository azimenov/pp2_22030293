import re
text = input()
x = re.split('_', text)

res = ''
for i in x:
    res += i.capitalize()
print(res)
