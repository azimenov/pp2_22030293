import re
text = input()
pattern = re.compile(r'[A-Z]')

x = re.split(pattern, text)
res = x[0]
for i in x:
    res+=i
print(res)
